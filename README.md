# 🚀 SubsFly Price Intelligence System

Sistema automatizado de monitorización de precios de suscripciones para SubsFly.

## ✨ Características

- 🔍 Verifica **82 plataformas** automáticamente
- 📱 Notificaciones por **Telegram**
- ⏰ Ejecución **semanal** automática
- 💰 Coste: **~2-5€/mes**

## 📦 Plataformas Monitorizadas

| Categoría | Servicios |
|-----------|-----------|
| 🎬 Entretenimiento | Netflix, Max, Disney+, Prime, SkyShowtime, Filmin... |
| 🎵 Música | Spotify, Apple Music, YouTube Music, Deezer, Tidal |
| ⚽ Deportes | DAZN (Fútbol, Premium, Motor, Baloncesto) |
| 🎮 Videojuegos | Xbox Game Pass, PlayStation Plus, Nintendo, EA Play |
| 💼 Productividad | Microsoft 365, Google One, iCloud+, Dropbox, Notion |
| 🤖 IA | ChatGPT, Claude, Gemini, Midjourney, Copilot |

## 🚀 Configuración

### 1. Crear Bot de Telegram
1. Busca **@BotFather** en Telegram
2. Envía `/newbot` y sigue las instrucciones
3. Guarda el **token**

### 2. Obtener Chat ID
1. Busca **@userinfobot** en Telegram
2. Envía `/start`
3. Copia tu **Id**

### 3. Configurar Anthropic API
1. Ve a [console.anthropic.com](https://console.anthropic.com)
2. Crea una API Key
3. Añade $10-20 de créditos

### 4. Configurar GitHub
1. Sube estos archivos a un repositorio
2. Ve a Settings → Secrets → Actions
3. Añade:
   - `ANTHROPIC_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`

### 5. Ejecutar
- **Automático:** Cada domingo a las 10:00
- **Manual:** Actions → Run workflow

## 📱 Ejemplo de Notificación

```
🔴 SubsFly Price Monitor
━━━━━━━━━━━━━━━━━━━━━
📅 19/12/2025 10:00

⚠️ CAMBIOS: 2

📈 Netflix Estándar
   13.99€ → 14.99€
   +1.00€ (+7.1%)

📉 Spotify Premium
   11.99€ → 10.99€
   -1.00€ (-8.3%)

━━━━━━━━━━━━━━━━━━━━━
⚡ Actualiza CloudKit
```

## 📄 Licencia

© 2025 Jaime Calatayud - SubsFly
