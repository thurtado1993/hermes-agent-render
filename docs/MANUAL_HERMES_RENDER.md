# Master Manual: 24/7 Free Sovereign AI Server with Hermes Agent, Render & OpenRouter

> **Goal:** Run your personal, persistent Artificial Intelligence server in the cloud 24 hours a day **100% free of charge**, eliminating reliance on paid monthly subscriptions (ChatGPT Plus, Claude Pro, Gemini Advanced).
>
> **Stack:**
> 1. **OpenRouter**: Access state-of-the-art AI models at $0.00 cost (`:free` tier).
> 2. **Render.com**: Host your private containerized server 24/7 on the Free Web Service tier.
> 3. **Hermes Agent** (Nous Research): Persistent memory, self-evolving skills, and OpenAI-compatible API gateway.
> 4. **On-Server Web Chat (`chat.html`)**: Instant browser access directly on your domain without installing anything.
> 5. **Telegram Bot** (optional): Chat with your agent on mobile or desktop via standard chat messaging.

---

## 🌐 Language Index / Índice de Idiomas
1. [🇬🇧 English Manual](#-english-manual)
2. [🇪🇸 Manual en Español](#-manual-en-español)

---

# 🇬🇧 English Manual

## Table of Contents
1. [Architecture Overview](#1-architecture-overview)
2. [Prerequisites](#2-prerequisites)
3. [Step 1: Get Your Free OpenRouter Key](#step-1-get-your-free-openrouter-key)
4. [Step 2: Set Up Telegram Bot (Optional)](#step-2-set-up-telegram-bot-optional)
5. [Step 3: Deploy the Server on Render.com](#step-3-deploy-the-server-on-rendercom)
6. [Step 4: Using the On-Server Web Chat (`chat.html`)](#step-4-using-the-on-server-web-chat-chathtml)
7. [Step 5: Alternative Web Clients (`chat_web.html` & NextChat)](#step-5-alternative-web-clients-chat_webhtml--nextchat)
8. [Free Models Catalog (`:free`)](#free-models-catalog-free)
9. [Keeping Your Free Server Awake 24/7](#keeping-your-free-server-awake-247)
10. [Troubleshooting & FAQ](#troubleshooting--faq)

---

### 1. Architecture Overview

```
+------------------------------------+
|   Your Client Device               |
|   (Browser / Phone / Telegram)     |
+-----------------+------------------+
                  |  HTTPS Requests (chat.html / Telegram API)
                  v
+-----------------+------------------+
|   Render.com (Free Web Service)    |
|   - Reverse Proxy (:10000)         |
|     --> Serves chat.html at '/'    |
|     --> Proxies '/v1/*' to Gateway |
|   - Hermes Agent Gateway (:8642)   |
+-----------------+------------------+
                  |  Inference API Calls
                  v
+-----------------+------------------+
|   OpenRouter.ai (:free models)     |
|   - Llama 3.3 70B, Gemini Flash    |
+------------------------------------+
```

---

### 2. Prerequisites
- A web browser (Chrome, Edge, Safari, Firefox).
- A free email account or Google account.
- No coding or server administration skills required.

---

### Step 1: Get Your Free OpenRouter Key
1. Go to **[https://openrouter.ai/](https://openrouter.ai/)**.
2. Click **Sign In** and authenticate using Google or email.
3. Open the API Keys panel: **[https://openrouter.ai/keys](https://openrouter.ai/keys)**.
4. Click **Create Key**:
   - **Key Name**: `Hermes Free`
   - **Credit Limit**: Leave blank (unlimited for free models).
5. Click **Create** and copy your secret key starting with `sk-or-v1-...`.
> *Note: Your account balance will remain $0.00. Free models ending with `:free` do not consume credits or require a credit card.*

---

### Step 2: Set Up Telegram Bot (Optional)
If you want to chat from your mobile phone:
1. Open Telegram and search for **`@BotFather`** (verified badge).
2. Send `/newbot`.
3. Provide a display name (e.g. `My Hermes Assistant`) and a unique username ending in `bot` (e.g. `my_hermes_2026_bot`).
4. Save the **HTTP API Token** provided by BotFather.
5. In Telegram search for **`@userinfobot`**, click Start, and note your numeric **Id**. This prevents anyone else from accessing your bot.

---

### Step 3: Deploy the Server on Render.com

#### Option A: Deploy via GitHub (Recommended for On-Server `chat.html`)
1. Push or fork this repository to your GitHub account.
2. Sign in to **[https://render.com/](https://render.com/)**.
3. In the Dashboard, click **+ New** ➔ **Web Service**.
4. Select your repository.
5. Configure the service:
   - **Name**: `hermes-agent-free`
   - **Region**: Select Frankfurt (EU) or Oregon/Ohio (US).
   - **Environment**: Docker (Render will detect `deploy/Dockerfile`).
   - **Instance Type**: **Free ($0/month)**.

#### Option B: Deploy Pre-built Image (Quick No-Code Setup)
1. In Render, select **"Existing Image"**.
2. Enter: `docker.io/nousresearch/hermes-agent:latest`.
3. Select the **Free** instance type.

#### Environment Variables (Both options)
Add the following keys under the **Environment Variables** section:

| Variable | Recommended Value | Explanation |
| :--- | :--- | :--- |
| `OPENROUTER_API_KEY` | *(Your `sk-or-v1-...` key)* | Connects agent to OpenRouter |
| `MODEL_NAME` | `meta-llama/llama-3.3-70b-instruct:free` | Default high-capability free model |
| `PORT` | `10000` | Port expected by Render router |
| `API_SERVER_ENABLED` | `true` | Enables OpenAI-compatible API |
| `API_SERVER_PORT` | `10000` (or `8642` with Dockerfile) | Gateway server port |
| `API_SERVER_KEY` | *(Your secret password)* | Protects access to the API |
| `TELEGRAM_BOT_TOKEN` | *(From @BotFather)* | Enables mobile Telegram bot |
| `TELEGRAM_ALLOWED_USERS`| *(Your numeric Telegram ID)* | Restricts bot to your account only |

Click **Create Web Service**. After 2–3 minutes, the status badge will turn green (**Live**).

---

### Step 4: Using the On-Server Web Chat (`chat.html`)
If deployed using our repository's `deploy/Dockerfile`:
1. Open your web browser on any device (laptop, smartphone, iPad).
2. Navigate directly to your Render public URL:
   ```text
   https://hermes-agent-free.onrender.com
   ```
3. The on-server web chat interface will load instantly.
4. Enter your `API_SERVER_KEY` once when prompted.
5. You can now chat directly with your Hermes Agent with **zero configuration, zero CORS issues, and no external dependencies**!

---

### Step 5: Alternative Web Clients (`chat_web.html` & NextChat)

#### 1. Standalone File (`web/chat_web.html`)
- Double click `web/chat_web.html` on your computer.
- In the sidebar, set your Render URL (`https://your-service.onrender.com`) and your `API_SERVER_KEY`.
- Click **Save Settings** and start chatting.

#### 2. NextChat Web
- Visit **[https://app.nextchat.dev/](https://app.nextchat.dev/)**.
- Go to Settings ➔ Provider: **Custom / OpenAI**.
- Endpoint: `https://your-service.onrender.com/v1`.
- API Key: Your `API_SERVER_KEY`.

---

### Free Models Catalog (`:free`)

| Model Identifier | Primary Focus | Best Use Case |
| :--- | :--- | :--- |
| `meta-llama/llama-3.3-70b-instruct:free` | **All-Rounder** | 70B parameters, exceptional Spanish and English reasoning, creative writing. |
| `google/gemini-2.0-flash-lite:free` | **Speed & Context** | Near-zero latency, large context window for big documents. |
| `deepseek/deepseek-r1:free` | **Deep Reasoning** | Chain-of-thought logic, math, riddles, and scientific deduction. |
| `qwen/qwen-2.5-coder-32b-instruct:free` | **Coding Specialist** | Python, JavaScript, bug diagnosis, architecture design. |
| `openrouter/free` | **Smart Router** | Automatically routes prompts to whichever free model is currently healthiest. |

---

### Keeping Your Free Server Awake 24/7
Render's free tier idles after 15 minutes of inactivity. To eliminate cold starts:
1. Copy your Render URL (`https://your-service.onrender.com`).
2. Go to **[https://cron-job.org/](https://cron-job.org/)** (free).
3. Create a cronjob making a simple HTTP GET request to your URL every **10 minutes**.
4. Your server will stay active 24 hours a day with zero delays.

---

### Troubleshooting & FAQ
- **Why did my first message take 40 seconds?** The free server was asleep. Subsequent messages respond in 1–2 seconds. Use the keep-alive tip above.
- **Telegram bot does not answer?** Verify that `TELEGRAM_ALLOWED_USERS` matches your exact ID from `@userinfobot`.
- **Can anyone else access my server?** No. Web endpoints require your `API_SERVER_KEY`, and Telegram strictly enforces your user ID.

---
---

# 🇪🇸 Manual en Español

## Índice de Contenidos
1. [Visión General de la Arquitectura](#1-visión-general-de-la-arquitectura)
2. [Requisitos Previos](#2-requisitos-previos-1)
3. [Paso 1: Obtener tu Clave Gratuita de OpenRouter](#paso-1-obtener-tu-clave-gratuita-de-openrouter-1)
4. [Paso 2: Configurar el Bot de Telegram (Opcional)](#paso-2-configurar-el-bot-de-telegram-opcional)
5. [Paso 3: Desplegar el Servidor en Render.com](#paso-3-desplegar-el-servidor-en-rendercom)
6. [Paso 4: Usar el Chat Web en el Servidor (`chat.html`)](#paso-4-usar-el-chat-web-en-el-servidor-chathtml)
7. [Paso 5: Clientes Web Alternativos (`chat_web.html` y NextChat)](#paso-5-clientes-web-alternativos-chat_webhtml-y-nextchat)
8. [Catálogo de Modelos Gratuitos (`:free`)](#catálogo-de-modelos-gratuitos-free)
9. [Mantener el Servidor Despierto 24/7](#mantener-el-servidor-despierto-247)
10. [Preguntas Frecuentes y Resolución de Problemas](#preguntas-frecuentes-y-resolución-de-problemas)

---

### 1. Visión General de la Arquitectura

* **Hermes Agent**: Cerebro autónomo con memoria persistente desarrollado por Nous Research.
* **OpenRouter**: Acceso a modelos potentes con coste cero (`:free`).
* **Render.com**: Servidor en la nube gratuito 24/7 sin tarjeta bancaria.
* **chat.html**: Interfaz web integrada en tu propio dominio de Render.
* **Telegram**: Acceso desde el móvil estés donde estés.

---

### 2. Requisitos Previos
* Un navegador web moderno (Chrome, Edge, Firefox, Safari).
* Una cuenta de correo o Google.
* Cero conocimientos de programación o servidores.

---

### Paso 1: Obtener tu Clave Gratuita de OpenRouter
1. Entra en **[https://openrouter.ai/](https://openrouter.ai/)** y pulsa **Sign In**.
2. Ve a la sección de claves: **[https://openrouter.ai/keys](https://openrouter.ai/keys)**.
3. Haz clic en **Create Key**:
   * **Nombre**: `Hermes Gratis`
   * **Límite de crédito**: Déjalo en blanco.
4. Pulsa **Create** y copia la clave que empieza por `sk-or-v1-...`.

---

### Paso 2: Configurar el Bot de Telegram (Opcional)
1. En Telegram, busca **`@BotFather`** y envía `/newbot`.
2. Dale un nombre visible y un nombre de usuario que termine en `bot`.
3. Guarda el **HTTP API Token** proporcionado.
4. Busca **`@userinfobot`**, pulsa Iniciar y copia tu número de **Id** para proteger el acceso.

---

### Paso 3: Desplegar el Servidor en Render.com
1. Regístrate gratis en **[https://render.com/](https://render.com/)**.
2. Pulsa en **+ New** ➔ **Web Service**.
3. Si conectas tu repositorio de GitHub, Render usará automáticamente `deploy/Dockerfile`.
   *(O si prefieres despliegue directo sin GitHub, elige **Existing Image** con `docker.io/nousresearch/hermes-agent:latest`)*.
4. Selecciona el plan **Free ($0/month)**.
5. En **Environment Variables**, añade:
   * `OPENROUTER_API_KEY`: Tu clave `sk-or-v1-...`.
   * `MODEL_NAME`: `meta-llama/llama-3.3-70b-instruct:free`.
   * `PORT`: `10000`.
   * `API_SERVER_KEY`: Tu contraseña secreta para el servidor.
   * `TELEGRAM_BOT_TOKEN` *(opcional)*: El token de @BotFather.
   * `TELEGRAM_ALLOWED_USERS` *(opcional)*: Tu ID numérico de Telegram.
6. Haz clic en **Create Web Service**. Espera 2–3 minutos hasta ver la etiqueta verde **Live**.

---

### Paso 4: Usar el Chat Web en el Servidor (`chat.html`)
Si has desplegado el proyecto con el `deploy/Dockerfile` incluido:
1. Abre tu navegador en cualquier dispositivo (ordenador, móvil o tablet).
2. Entra directamente a la URL de tu Render:
   ```text
   https://tu-servicio.onrender.com
   ```
3. La interfaz web cargará al instante directamente desde tu servidor.
4. Introduce tu contraseña `API_SERVER_KEY` una sola vez.
5. ¡Empieza a chatear sin instalar nada, con conexión directa y sin bloqueos de CORS!

---

### Paso 5: Clientes Web Alternativos (`chat_web.html` y NextChat)

#### 1. Archivo local (`web/chat_web.html`)
Haz doble clic sobre `web/chat_web.html` en tu ordenador, introduce la URL de Render y tu clave API, y disfruta de un chat privado en local.

#### 2. NextChat Web
Entra en **[https://app.nextchat.dev/](https://app.nextchat.dev/)**, ve a Ajustes ➔ Custom OpenAI, y pon tu URL de Render (`https://tu-servicio.onrender.com/v1`) con tu contraseña.

---

### Catálogo de Modelos Gratuitos (`:free`)

| Modelo | Especialidad | Ventajas |
| :--- | :--- | :--- |
| `meta-llama/llama-3.3-70b-instruct:free` | **Todoterreno** | 70B parámetros, redacción y razonamiento de primer nivel. |
| `google/gemini-2.0-flash-lite:free` | **Velocidad** | Respuestas inmediatas y gran ventana de contexto. |
| `deepseek/deepseek-r1:free` | **Lógica** | Razonamiento reflexivo paso a paso para matemáticas y ciencia. |
| `qwen/qwen-2.5-coder-32b-instruct:free` | **Programación** | Análisis y generación de código de alta precisión. |
| `openrouter/free` | **Auto Router** | Enrutador automático al modelo libre más rápido disponible. |

---

### Mantener el Servidor Despierto 24/7
Copia tu URL de Render y crea una tarea gratuita en **[cron-job.org](https://cron-job.org)** que haga una petición HTTP simple cada **10 minutos**. ¡Tu servidor responderá al instante las 24 horas del día!
