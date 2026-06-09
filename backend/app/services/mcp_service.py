from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


class MCPService:
    def __init__(self, url: str) -> None:
        self._url = url.rstrip("/")

    async def list_tools(self) -> list:
        async with streamable_http_client(self._url) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.list_tools()
                return result.tools

    async def call_tool(self, name: str, arguments: dict) -> str:
        async with streamable_http_client(self._url) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(name, arguments)
        parts = [
            item.text if hasattr(item, "text") else str(item)
            for item in result.content
        ]
        return "\n".join(parts) if parts else "Sonuç bulunamadı."
