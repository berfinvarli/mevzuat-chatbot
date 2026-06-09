API_V1_PREFIX = "/api/v1"
MAX_TOOL_ITERATIONS = 8
RATE_LIMIT = "10/minute"
STREAM_TOKEN_DELAY = 0.008
CONVERSATIONS_COLLECTION = "conversations"

MONGODB_DB = "mevzuat_chatbot"
DEFAULT_OPENAI_MODEL = "gpt-5.4-mini"

DEFAULT_CMS: dict[str, str] = {
    "mevzuat.chatbot.title": "Mevzuat Chatbot",
    "mevzuat.chatbot.subtitle": "Türk Hukuku & Mevzuat Asistanı",
    "mevzuat.chatbot.welcome_message": (
        "Merhaba! Ben Türk mevzuatı konusunda uzman bir asistanım. "
        "Kanunlar, yönetmelikler, tebliğler ve diğer mevzuat hakkında "
        "sorularınızı yanıtlayabilirim."
    ),
    "mevzuat.chatbot.input_placeholder": "Mevzuat hakkında bir soru sorun… (Enter ile gönder)",
    "mevzuat.chatbot.input_hint": "Shift+Enter ile yeni satır ekleyin",
}
