# Mevzuat Chatbot

Türk mevzuatı hakkındaki soruları, [mevzuat-mcp](https://github.com/saidsurucu/mevzuat-mcp) MCP sunucusu üzerinden yanıtlayan bir chatbot.

```
React (frontend) → FastAPI (backend) → MCP Server → mevzuat.gov.tr
```

- **Frontend** — React + Vite, cevaplar SSE ile streaming gösterilir
- **Backend** — FastAPI + OpenAI function calling; MCP tool'larını çağırarak yanıt üretir
- **MCP Server** — Azure Container Apps'te deploy, mevzuat.gov.tr'den canlı veri


## Çalıştırma

Backend ve frontend lokal çalışır. Ön koşullar: [uv](https://docs.astral.sh/uv/), Node.js ve erişilebilir bir **MongoDB** + **PostgreSQL** (bağlantıları `.env`'de verilir).

```bash
# Backend
cd backend
uv sync
cp .env.example .env          
uv run uvicorn main:app --port 8001

# Frontend
cd frontend
npm install
npm run dev                   # http://localhost:3000
```

Zorunlu env değişkenleri: `OPENAI_API_KEY`, `MCP_SERVER_URL`, `MONGODB_URL`, `POSTGRES_URL`, `ADMIN_TOKEN`, `CLIENT_URL`. Eksik olan varsa uygulama açılışta hata verir.

## API

| Endpoint | Method | Açıklama |
|---|---|---|
| `/api/v1/chat` | POST | SSE streaming chat |
| `/api/v1/history` | GET | Oturuma ait konuşma geçmişi |
| `/api/v1/cms` | GET | UI metinleri (hepsi) |
| `/api/v1/cms/{key}` | GET | UI metni (key bazlı) |
| `/api/v1/admin/settings` | GET/PUT | Runtime model ayarları (token gerekli) |
| `/api/v1/health` | GET | Sistem durumu |

## Spec dışında eklenenler

- **Konuşma geçmişi (MongoDB)** — oturum cookie'si bazında mesajlar saklanır; `/history` ile geri yüklenir.
- **Runtime model ayarları (PostgreSQL)** — `system_prompt`, `openai_model`, `temperature`, `max_tokens`, `max_tool_iterations`, `stream_token_delay` alanları `app_settings` tablosunda tutulur ve `/admin/settings` ile **redeploy gerekmeden** değiştirilebilir. DB boşsa env/kod default'larına düşülür.
- **CMS (PostgreSQL)** — UI metinleri (başlık, karşılama mesajı, placeholder vb.) `cms` tablosundan gelir; frontend bunları `/cms/{key}` ile çeker. İlk açılışta varsayılan metinlerle seed edilir.
- **Admin auth** — `/admin/*` endpoint'leri `X-Admin-Token` header'ı ile korunur.
- **Rate limiting** — `/chat` üzerinde istek sınırı (slowapi).
- **Health endpoint** — aktif model ve MCP URL'ini döner.

**Neden iki veritabanı?** Konuşma geçmişi şemasız, sürekli eklenen (append) ve oturuma göre büyüyen bir akış olduğu için doküman tabanlı **MongoDB**'ye uygun. Ayarlar ve CMS ise az sayıda, yapısal ve `key` üzerinde benzersizlik/transaction isteyen kayıtlar olduğundan ilişkisel **PostgreSQL**'de tutuluyor.

Runtime ayarlarını güncelleme örneği:

```bash
curl -X PUT http://localhost:8001/api/v1/admin/settings \
  -H "X-Admin-Token: <token>" -H "Content-Type: application/json" \
  -d '{"openai_model": "gpt-5.4", "temperature": 0.3}'
```

## MCP Server Deployment (Azure Container Apps)

Kaynak kod [saidsurucu/mevzuat-mcp](https://github.com/saidsurucu/mevzuat-mcp), [mcp-server/Dockerfile](mcp-server/Dockerfile) ile dockerize edilip Azure Container Apps'e deploy edildi. Image Playwright/Chromium içerdiğinden container ortamı gerektirir.

```bash
RG=case-study-berfin-varli
LOC=westeurope
ACR=mevzuatcasestudy
ENV=mevzuat-env
APP=mevzuat-mcp-server

az login

# Registry + ortam
az acr create -g $RG -n $ACR --sku Basic --admin-enabled true
az containerapp env create -n $ENV -g $RG -l $LOC

# Build & push
az acr build -r $ACR -g $RG --image mevzuat-mcp:latest --file mcp-server/Dockerfile mcp-server/

# Public endpoint olarak çalıştır
az containerapp create -n $APP -g $RG --environment $ENV \
  --image $ACR.azurecr.io/mevzuat-mcp:latest --registry-server $ACR.azurecr.io \
  --target-port 8000 --ingress external --min-replicas 1 --cpu 1.0 --memory 2.0Gi

# URL'i al → backend/.env içindeki MCP_SERVER_URL'e "https://$FQDN/mcp" yaz
az containerapp show -n $APP -g $RG --query properties.configuration.ingress.fqdn -o tsv
```

Redeploy:

```bash
az acr build -r $ACR -g $RG --image mevzuat-mcp:latest --file mcp-server/Dockerfile mcp-server/
az containerapp update -n $APP -g $RG --image $ACR.azurecr.io/mevzuat-mcp:latest
```
