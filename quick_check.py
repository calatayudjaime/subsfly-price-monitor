#!/usr/bin/env python3
"""
SubsFly Quick Check - Verificación rápida de una plataforma
Uso: python quick_check.py "Netflix"
"""

import os
import sys
import anthropic

def main():
    if len(sys.argv) < 2:
        print("\nUso: python quick_check.py \"Nombre de plataforma\"")
        print("Ejemplo: python quick_check.py \"Netflix\"\n")
        sys.exit(0)
    
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ Configura ANTHROPIC_API_KEY")
        sys.exit(1)
    
    platform = " ".join(sys.argv[1:])
    print(f"\n🔍 Buscando precios de {platform} en España...\n")
    
    client = anthropic.Anthropic(api_key=api_key)
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": f"Busca los precios actuales de {platform} en España. Lista todos los planes con precios mensuales y anuales."}]
    )
    
    for block in response.content:
        if hasattr(block, 'text'):
            print(block.text)
    print()

if __name__ == "__main__":
    main()
