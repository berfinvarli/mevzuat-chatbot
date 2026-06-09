import asyncio
import json
import logging
from typing import AsyncIterator

from openai import AsyncOpenAI

from app.persistence.conversation_repository import ConversationRepository, SessionId
from app.schemas.message import Message
from app.services.mcp_service import MCPService
from app.services.runtime_settings_service import RuntimeSettingsService

logger = logging.getLogger(__name__)


def _to_openai_tool(tool) -> dict:
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description or "",
            "parameters": tool.inputSchema or {"type": "object", "properties": {}},
        },
    }


class ChatService:
    def __init__(
        self,
        openai_client: AsyncOpenAI,
        mcp_service: MCPService,
        settings_service: RuntimeSettingsService,
        repo: ConversationRepository | None = None,
    ) -> None:
        self._openai = openai_client
        self._mcp = mcp_service
        self._settings = settings_service
        self._repo = repo

    @staticmethod
    def _sse(event: dict) -> str:
        return f"data: {json.dumps(event, ensure_ascii=False)}\n\n"

    async def get_history(self, session_id: SessionId) -> list[dict]:
        if not self._repo:
            return []
        return await self._repo.get_messages(session_id)

    async def stream(
        self,
        request_messages: list[Message],
        session_id: SessionId | None = None,
    ) -> AsyncIterator[str]:
        rs = await self._settings.get()

        try:
            raw_tools = await self._mcp.list_tools()
            openai_tools = [_to_openai_tool(t) for t in raw_tools]
        except Exception as exc:
            logger.exception("MCP sunucusuna bağlanılamadı")
            yield self._sse({"type": "error", "message": f"MCP sunucusuna bağlanılamadı: {exc}"})
            return

        history: list[dict] = [{"role": "system", "content": rs.system_prompt}]
        history += [{"role": m.role, "content": m.content} for m in request_messages]

        extra_params: dict = {"temperature": rs.temperature}
        if rs.max_tokens is not None:
            extra_params["max_tokens"] = rs.max_tokens

        for _ in range(rs.max_tool_iterations):
            try:
                response = await self._openai.chat.completions.create(
                    model=rs.openai_model,
                    messages=history,
                    tools=openai_tools,
                    tool_choice="auto",
                    **extra_params,
                )
            except Exception as exc:
                logger.exception("OpenAI API hatası")
                yield self._sse({"type": "error", "message": f"OpenAI hatası: {exc}"})
                return

            choice = response.choices[0]
            msg = choice.message

            if choice.finish_reason == "tool_calls" and msg.tool_calls:
                history.append({
                    "role": "assistant",
                    "content": msg.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                        }
                        for tc in msg.tool_calls
                    ],
                })
                for tc in msg.tool_calls:
                    yield self._sse({"type": "tool_call", "name": tc.function.name})
                    try:
                        args = json.loads(tc.function.arguments or "{}")
                        tool_result = await self._mcp.call_tool(tc.function.name, args)
                    except Exception as exc:
                        logger.exception("Araç çalıştırma hatası: %s", tc.function.name)
                        tool_result = f"Araç çalıştırma hatası: {exc}"
                    history.append({"role": "tool", "tool_call_id": tc.id, "content": tool_result})
            else:
                content = msg.content or ""

                if self._repo and session_id and request_messages:
                    await self._repo.append_messages(session_id, [
                        Message(role="user", content=request_messages[-1].content),
                        Message(role="assistant", content=content),
                    ])

                words = content.split(" ")
                for i, word in enumerate(words):
                    yield self._sse({"type": "token", "content": word if i == len(words) - 1 else word + " "})
                    await asyncio.sleep(rs.stream_token_delay)
                yield self._sse({"type": "done"})
                return

        logger.warning("max_tool_iterations (%d) aşıldı: session_id=%s", rs.max_tool_iterations, session_id)
        yield self._sse({"type": "done"})
