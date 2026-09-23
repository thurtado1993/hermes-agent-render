# ⚡ Free 24/7 Autonomous AI Agent on Render & OpenRouter

[![Render](https://img.shields.io/badge/Render-Free%20Tier-46E3B7?logo=render&logoColor=white)](https://render.com)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-Free%20Models-6366F1?logo=openai&logoColor=white)](https://openrouter.ai)
[![Hermes Agent](https://img.shields.io/badge/NousResearch-Hermes%20Agent-38BDF8)](https://hermes-agent.nousresearch.com)
[![Design](https://img.shields.io/badge/Design-Swiss%20Modernist-00f0ff)](https://seunghyuk.com/?ref=siteinspire)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Deploy your personal, persistent, autonomous AI assistant in the cloud for $0/month, powered by Nous Research's Hermes Agent and OpenRouter's free-tier models (`:free`).**

---

## 🌐 Language Navigation / Navegación por Idioma
- [English Documentation](#-english-documentation)
- [Documentación en Español](#-documentación-en-español)

---

# 🇬🇧 English Documentation

## Overview

This repository contains everything needed to deploy and run **Hermes Agent** (by Nous Research) on **Render.com** (Free Plan) utilizing **OpenRouter**'s free-tier models (`:free`).

Say goodbye to recurring $20+/month subscriptions like ChatGPT Plus or Claude Pro. You can now operate your own private AI assistant 24/7 accessible from:
1. **Any Web Browser** (via the on-server console `chat.html` or standalone client `chat_web.html`).
2. **Telegram** (as a personal private bot on your smartphone or desktop).

---

## Key Features

- **Cost: $0.00 / Month Forever**: Runs on Render's 750 free monthly instance hours with OpenRouter `:free` models. No credit card required.
- **Persistent Memory & Tools**: Hermes Agent remembers conversations, builds skills, and executes multi-step workflows.
- **Swiss Modernist Interface**: Inspired by [seunghyuk.com](https://seunghyuk.com/?ref=siteinspire) with 32px structural grid, high-contrast dark palette, corner crosshairs (`+`), and `Space Grotesk` + `JetBrains Mono` + `Syne` precision typography.
- **On-Server Web Chat (`chat.html`)**: Built-in console hosted directly on your Render domain (`https://your-service.onrender.com`). Zero CORS issues, zero installation.
- **Standalone Web Client (`chat_web.html`)**: Lightweight single-file client to connect to your agent remotely from any browser with full configuration storage.
- **Interactive Presentation (`presentation.html`)**: 12-slide modernist visual manual with real-time `[EN / ES]` language switching, touch swipe gestures, and direct links.
- **Telegram Bot Support**: Send voice notes, files, and text messages directly to your agent from your phone.
- **High-Performance Free Models**: Access Meta Llama 3.3 70B, Google Gemini 2.0 Flash Lite, DeepSeek R1, and Qwen 2.5 Coder at zero cost.

---

## 📁 Repository Structure

```
manual-hermes-render/
├── README.md                      # Project documentation (English & Spanish)
├── LICENSE                        # MIT License
├── .gitignore                     # Git ignore rules
├── docs/
│   ├── MANUAL_HERMES_RENDER.md   # Step-by-step master manual (English & Spanish)
│   └── PRESENTATION_SLIDES.md    # Markdown slide deck for Marp / Slidev
├── web/
│   ├── chat.html                 # Hosted directly on Render (relative endpoints)
│   ├── chat_web.html             # Standalone client for any local browser
│   └── presentation.html         # Interactive slide presentation (Bilingual EN/ES)
├── deploy/
│   ├── Dockerfile                # Custom container bundling Hermes + on-server chat
│   ├── server.py                 # Lightweight reverse proxy & static file server
│   ├── start.sh                  # Process supervisor (Gateway + Web UI)
│   ├── docker-compose.yml        # Local or alternative container deployment
│   └── render.yaml               # Render Blueprint (Infrastructure as Code)
└── config/
    └── .env.example              # Environment variables template
```

---

## 🚀 Quickstart in 3 Steps

### Step 1: Obtain a Free OpenRouter API Key
1. Visit [openrouter.ai](https://openrouter.ai) and sign in.
2. Go to [openrouter.ai/keys](https://openrouter.ai/keys) and click **Create Key**.
3. Name it `Hermes Free`, leave credit limit empty, and copy your `sk-or-v1-...` key.

### Step 2: Deploy on Render.com
1. Register for free on [render.com](https://render.com).
2. Click **+ New** ➔ **Web Service**.
3. Connect your GitHub repository (or choose **Existing Image** with `docker.io/nousresearch/hermes-agent:latest`).
4. Select the **Free** instance type ($0/mo).
5. Add the following **Environment Variables**:
   - `OPENROUTER_API_KEY`: Your OpenRouter secret key.
   - `MODEL_NAME`: `meta-llama/llama-3.3-70b-instruct:free`
   - `PORT`: `10000`
   - `API_SERVER_KEY`: A secure password of your choice.
   - `TELEGRAM_BOT_TOKEN` *(optional)*: Bot token from Telegram `@BotFather`.
   - `TELEGRAM_ALLOWED_USERS` *(optional)*: Your numeric Telegram ID from `@userinfobot`.
6. Click **Create Web Service**. Wait 2–3 minutes until the status shows **Live**.

### Step 3: Start Chatting!
- **From Your Browser**: Open `https://your-service.onrender.com` in your browser. Enter your `API_SERVER_KEY` and start chatting immediately!
- **From Telegram**: Open Telegram, find your bot, tap **Start**, and send your first message.

---

## ⚡ 24/7 Keep-Alive Tip
Render's free tier spins down instances after 15 minutes of inactivity. To keep your agent responsive 24/7:
1. Copy your public Render URL (`https://your-app.onrender.com`).
2. Create a free account on [cron-job.org](https://cron-job.org) or [uptimerobot.com](https://uptimerobot.com).
3. Schedule an automated HTTP GET request to your URL every **10 minutes**.
4. Your server will stay permanently awake with near-zero latency.

---

# 🇪🇸 Documentación en Español

## Visión General

Este repositorio contiene todo lo necesario para desplegar y ejecutar **Hermes Agent** (de Nous Research) en **Render.com** (Plan Gratuito) utilizando los modelos gratuitos de **OpenRouter** (`:free`).

Despídete de pagar 20€/mes por suscripciones como ChatGPT Plus o Claude Pro. Ahora dispones de tu propio asistente de inteligencia artificial funcionando las 24 horas del día, accesible desde:
1. **Cualquier Navegador Web** (mediante la consola `chat.html` alojada en el propio servidor o el cliente autónomo `chat_web.html`).
2. **Telegram** (como bot privado en tu smartphone, tablet o PC).

---

## Características Principales

- **Coste: 0,00 € al mes de por vida**: Aprovecha las 750 horas mensuales gratuitas de Render con modelos `:free` de OpenRouter. Sin tarjeta de crédito.
- **Memoria Persistente y Habilidades**: Hermes Agent recuerda conversaciones pasadas, evoluciona sus destrezas y ejecuta flujos de tareas complejas.
- **Diseño Modernista Suizo**: Inspirado en [seunghyuk.com](https://seunghyuk.com/?ref=siteinspire) con retícula estructural de 32px, paleta oscura de alto contraste, cruces de calibración (`+`) y tipografía técnica `Space Grotesk` + `JetBrains Mono` + `Syne`.
- **Chat Web en el Servidor (`chat.html`)**: Interfaz web integrada servida directamente en tu dominio de Render (`https://tu-servicio.onrender.com`). Cero problemas de CORS y sin instalar nada.
- **Cliente Web Autónomo (`chat_web.html`)**: Archivo HTML único para conectarte remotamente a tu servidor desde cualquier máquina con almacenamiento persistente de credenciales.
- **Presentación Interactiva (`presentation.html`)**: Manual visual interactivo de 12 diapositivas con conmutador instantáneo de idioma `[EN / ES]`, navegación táctil por deslizamiento y enlaces directos.
- **Integración con Telegram**: Envía notas de voz, documentos y texto desde tu teléfono a tu agente.
- **Modelos de Primer Nivel Gratuitos**: Llama 3.3 70B, Gemini 2.0 Flash Lite, DeepSeek R1 y Qwen 2.5 Coder sin coste por token.

---

## 📁 Estructura del Repositorio

```
manual-hermes-render/
├── README.md                      # Documentación del proyecto (Inglés y Español)
├── LICENSE                        # Licencia MIT
├── .gitignore                     # Reglas de exclusión de Git
├── docs/
│   ├── MANUAL_HERMES_RENDER.md   # Manual maestro paso a paso (Inglés y Español)
│   └── PRESENTATION_SLIDES.md    # Diapositivas en Markdown para Marp / Slidev
├── web/
│   ├── chat.html                 # Alojado directamente en Render (rutas relativas)
│   ├── chat_web.html             # Cliente autónomo para cualquier navegador local
│   └── presentation.html         # Presentación de diapositivas interactiva (Bilingüe EN/ES)
├── deploy/
│   ├── Dockerfile                # Contenedor personalizado (Hermes + chat en servidor)
│   ├── server.py                 # Reverse proxy ligero y servidor de archivos estáticos
│   ├── start.sh                  # Supervisor de procesos (Gateway + Web UI)
│   ├── docker-compose.yml        # Despliegue en contenedor local o alternativo
│   └── render.yaml               # Render Blueprint (Infraestructura como Código)
└── config/
    └── .env.example              # Plantilla de variables de entorno
```

---

## 🚀 Inicio Rápido en 3 Pasos

### Paso 1: Obtén tu Clave Gratuita de OpenRouter
1. Entra en [openrouter.ai](https://openrouter.ai) e inicia sesión con Google o correo.
2. Ve a [openrouter.ai/keys](https://openrouter.ai/keys) y pulsa en **Create Key**.
3. Nómbrala `Hermes Gratis`, deja el límite monetario vacío y copia tu clave `sk-or-v1-...`.

### Paso 2: Despliega en Render.com
1. Crea tu cuenta gratuita en [render.com](https://render.com).
2. Pulsa en **+ New** ➔ **Web Service**.
3. Conecta este repositorio de GitHub (o selecciona **Existing Image** con `docker.io/nousresearch/hermes-agent:latest`).
4. Elige el plan **Free** ($0/mes).
5. Añade las siguientes **Variables de Entorno**:
   - `OPENROUTER_API_KEY`: Tu clave secreta de OpenRouter.
   - `MODEL_NAME`: `meta-llama/llama-3.3-70b-instruct:free`
   - `PORT`: `10000`
   - `API_SERVER_KEY`: Una contraseña secreta inventada por ti.
   - `TELEGRAM_BOT_TOKEN` *(opcional)*: Token de tu bot creado con `@BotFather` en Telegram.
   - `TELEGRAM_ALLOWED_USERS` *(opcional)*: Tu ID numérico de Telegram obtenido con `@userinfobot`.
6. Haz clic en **Create Web Service**. Espera 2–3 minutos hasta que el estado esté en verde (**Live**).

### Paso 3: ¡Empieza a Chatear!
- **Desde el Navegador**: Entra en `https://tu-servicio.onrender.com` desde tu móvil o PC. Introduce tu contraseña `API_SERVER_KEY` y chatea al instante.
- **Desde Telegram**: Abre Telegram, busca tu bot, pulsa en **Iniciar** y envíale cualquier pregunta.

---

## ⚡ Estrategia Keep-Alive 24/7
El plan gratuito de Render suspende los contenedores tras 15 minutos sin peticiones entrantes. Para mantener a tu asistente activo y receptivo 24/7 sin latencia de arranque:
1. Copia la URL pública de tu servicio en Render (`https://tu-app.onrender.com`).
2. Crea una cuenta gratuita en [cron-job.org](https://cron-job.org) o [uptimerobot.com](https://uptimerobot.com).
3. Configura un ping HTTP GET recurrente a tu URL cada **10 minutos**.
4. Tu agente permanecerá permanentemente despierto sin coste adicional.

---

## 📄 Licencia

Este proyecto está bajo la licencia [MIT](LICENSE). Eres libre de modificarlo, adaptarlo y compartirlo.
