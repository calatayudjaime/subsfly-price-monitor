#!/usr/bin/env python3
"""
SubsFly Price Intelligence System
Monitorización automática de precios de suscripciones
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
import anthropic
import requests

CONFIG_FILE = Path(__file__).parent / "config.json"
HISTORY_FILE = Path(__file__).parent / "price_history.json"
CLAUDE_MODEL = "claude-sonnet-4-20250514"

@dataclass
class PriceChange:
    name: str
    category: str
    old_price: float
    new_price: float
    change_amount: float
    change_percent: float
    is_increase: bool

def load_config() -> dict:
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_history() -> dict:
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"checks": []}

def save_history(history: dict):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def send_telegram(token: str, chat_id: str, message: str) -> bool:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": chat_id, "text": message, "parse_mode": "HTML"}, timeout=30)
        return r.status_code == 200
    except:
        return False

def verify_category(client: anthropic.Anthropic, category_name: str, platforms: list) -> tuple:
    platforms_text = "\n".join([f"- {p['name']}: {p['monthly_price']}€/mes" for p in platforms if p.get('monthly_price')])
    
    prompt = f"""Verifica los precios ACTUALES en España de estas suscripciones de {category_name}.

PRECIOS REGISTRADOS:
{platforms_text}

Busca en las webs oficiales y responde SOLO en JSON:
{{"results": [{{"name": "...", "registered": 0.00, "current": 0.00, "changed": true/false}}], "new_plans": []}}"""

    try:
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=4096,
            tools=[{"type": "web_search_20250305", "name": "web_search"}],
            messages=[{"role": "user", "content": prompt}]
        )
        
        text = "".join([b.text for b in response.content if hasattr(b, 'text')])
        text = text.strip().replace("```json", "").replace("```", "").strip()
        
        data = json.loads(text)
        changes = []
        
        for item in data.get("results", []):
            if item.get("changed") and item.get("registered") and item.get("current"):
                old_p = float(item["registered"])
                new_p = float(item["current"])
                if old_p != new_p:
                    changes.append(PriceChange(
                        name=item["name"],
                        category=category_name,
                        old_price=old_p,
                        new_price=new_p,
                        change_amount=new_p - old_p,
                        change_percent=((new_p - old_p) / old_p) * 100,
                        is_increase=new_p > old_p
                    ))
        
        return changes, data.get("new_plans", [])
    except Exception as e:
        print(f"Error en {category_name}: {e}")
        return [], []

def format_report(changes: List[PriceChange], new_plans: list, cats: int, plats: int) -> str:
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    if not changes and not new_plans:
        return f"""🟢 <b>SubsFly Price Monitor</b>
━━━━━━━━━━━━━━━━━━━━━
📅 {now}

✅ <b>Sin cambios detectados</b>

📊 Categorías: {cats} | Plataformas: {plats}

Próxima verificación: en 7 días"""
    
    msg = f"""🔴 <b>SubsFly Price Monitor</b>
━━━━━━━━━━━━━━━━━━━━━
📅 {now}

⚠️ <b>CAMBIOS: {len(changes)}</b>

"""
    for c in changes:
        emoji = "📈" if c.is_increase else "📉"
        sign = "+" if c.is_increase else ""
        msg += f"""{emoji} <b>{c.name}</b>
   {c.old_price}€ → {c.new_price}€
   {sign}{c.change_amount:.2f}€ ({sign}{c.change_percent:.1f}%)

"""
    
    if new_plans:
        msg += "🆕 <b>Nuevos planes:</b>\n"
        for p in new_plans:
            msg += f"• {p.get('name', 'N/A')}: {p.get('price', 'N/A')}€\n"
    
    msg += f"\n━━━━━━━━━━━━━━━━━━━━━\n⚡ Actualiza CloudKit"
    return msg

def main():
    print("\n" + "="*50)
    print("  SUBSFLY PRICE INTELLIGENCE")
    print("="*50 + "\n")
    
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    tg_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    tg_chat = os.environ.get("TELEGRAM_CHAT_ID", "")
    
    if not all([api_key, tg_token, tg_chat]):
        print("❌ Faltan credenciales")
        sys.exit(1)
    
    config = load_config()
    client = anthropic.Anthropic(api_key=api_key)
    
    all_changes = []
    all_new_plans = []
    total_platforms = 0
    
    for cat_id, cat_data in config.get("categories", {}).items():
        name = cat_data.get("name", cat_id)
        platforms = cat_data.get("platforms", [])
        icon = cat_data.get("icon", "📦")
        
        print(f"{icon} Verificando {name}... ({len(platforms)} plataformas)")
        total_platforms += len(platforms)
        
        changes, new_plans = verify_category(client, name, platforms)
        all_changes.extend(changes)
        all_new_plans.extend(new_plans)
        
        if changes:
            for c in changes:
                print(f"   ⚠️ {c.name}: {c.old_price}€ → {c.new_price}€")
        else:
            print(f"   ✓ Sin cambios")
        
        time.sleep(1)
    
    print("\n" + "="*50)
    print(f"  RESUMEN: {len(all_changes)} cambios detectados")
    print("="*50 + "\n")
    
    report = format_report(all_changes, all_new_plans, len(config.get("categories", {})), total_platforms)
    
    print("📤 Enviando a Telegram...")
    if send_telegram(tg_token, tg_chat, report):
        print("✅ Enviado correctamente")
    else:
        print("❌ Error enviando")
    
    history = load_history()
    history["checks"].append({
        "timestamp": datetime.now().isoformat(),
        "changes": len(all_changes),
        "platforms": total_platforms
    })
    save_history(history)
    
    print("\n✅ Verificación completada\n")

if __name__ == "__main__":
    main()
