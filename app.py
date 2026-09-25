#!/usr/bin/env python3
"""
Portfolio JL Backend - Genera briefing automático cada lunes 22:45
Lee Google Sheet → Obtiene precios → Genera HTML → Sube a GitHub
"""

import os
import json
import subprocess
from datetime import datetime
import requests
from io import StringIO
import csv

# ==================== CONFIGURACIÓN ====================

GITHUB_USER = "jlguillen-creator"
GITHUB_REPO = "portfolio-jl"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # GitHub Actions lo proporciona
GOOGLE_SHEET_ID = "14BgUCgmwHbeOt1AOc3HZ_z7Ia9MstQifbGuknweKyM0"

# API para precios (AlphaVantage - free tier)
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")

# ==================== FUNCIONES ====================

def get_google_sheet_data():
    """Lee cartera del Google Sheet usando CSV export"""
    try:
        # URL de exportación CSV del Google Sheet
        csv_url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv"
        
        response = requests.get(csv_url, timeout=10)
        response.raise_for_status()
        
        # Parsear CSV
        csv_reader = csv.reader(StringIO(response.text))
        rows = list(csv_reader)
        
        cartera = {}
        for row in rows[1:]:  # Skip header
            if len(row) >= 3 and row[0].strip():
                try:
                    ticker = row[0].strip()
                    acciones = float(row[1].strip())
                    coste_medio = float(row[2].strip())
                    cartera[ticker] = {"acciones": acciones, "coste_medio": coste_medio}
                except ValueError:
                    continue
        
        print(f"✅ Cartera leída: {len(cartera)} posiciones")
        return cartera
    except Exception as e:
        print(f"❌ Error leyendo Google Sheet: {e}")
        return None

def get_prices(tickers):
    """Obtiene precios actuales de AlphaVantage (o fallback local)"""
    import time
    precios = {}
    
    print(f"  Using API Key: {ALPHA_VANTAGE_API_KEY[:10]}..." if ALPHA_VANTAGE_API_KEY else "  NO API KEY!")
    
    for ticker in tickers:
        try:
            # AlphaVantage API
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={ALPHA_VANTAGE_API_KEY}"
            response = requests.get(url, timeout=10)  # Aumentado a 10 segundos
            response.raise_for_status()
            data = response.json()
            
            # Debug: imprimir respuesta
            if "Error Message" in data:
                print(f"  {ticker}: API Error - {data['Error Message']}")
                precios[ticker] = None
            elif "Note" in data:
                print(f"  {ticker}: Rate limit - {data['Note']}")
                precios[ticker] = None
            elif "Global Quote" in data and "05. price" in data["Global Quote"]:
                precio_str = data["Global Quote"]["05. price"]
                if precio_str and precio_str != "0":
                    precio = float(precio_str)
                    precios[ticker] = precio
                    print(f"  {ticker}: €{precio:.2f}")
                else:
                    print(f"  {ticker}: Precio vacío o cero")
                    precios[ticker] = None
            else:
                print(f"  {ticker}: Respuesta incompleta - {data}")
                precios[ticker] = None
                
        except requests.exceptions.Timeout:
            print(f"  {ticker}: Timeout (>10s)")
            precios[ticker] = None
        except Exception as e:
            print(f"  {ticker}: ERROR ({type(e).__name__}: {e})")
            precios[ticker] = None
        
        # Pequeño delay para evitar rate limit
        time.sleep(0.2)
    
    return precios

def calculate_portfolio(cartera, precios):
    """Calcula valor total, P&L, etc."""
    total_valor = 0
    total_invertido = 0
    posiciones = []
    
    for ticker, data in cartera.items():
        acciones = data["acciones"]
        coste_medio = data["coste_medio"]
        precio_actual = precios.get(ticker)
        
        if precio_actual is None:
            print(f"  ⚠️ {ticker}: sin precio, skipping")
            continue
        
        coste_total = acciones * coste_medio
        valor_actual = acciones * precio_actual
        pyl = valor_actual - coste_total
        pyl_pct = (pyl / coste_total * 100) if coste_total > 0 else 0
        
        total_valor += valor_actual
        total_invertido += coste_total
        
        posiciones.append({
            "ticker": ticker,
            "acciones": acciones,
            "coste_medio": coste_medio,
            "precio_actual": precio_actual,
            "valor_actual": valor_actual,
            "pyl": pyl,
            "pyl_pct": pyl_pct
        })
    
    total_pyl = total_valor - total_invertido
    total_pyl_pct = (total_pyl / total_invertido * 100) if total_invertido > 0 else 0
    
    return {
        "total_valor": total_valor,
        "total_invertido": total_invertido,
        "total_pyl": total_pyl,
        "total_pyl_pct": total_pyl_pct,
        "posiciones": posiciones,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

def generate_html(portfolio_data):
    """Genera HTML briefing con tema oscuro"""
    pos = portfolio_data
    
    # Construir rows de posiciones
    pos_rows = ""
    for p in pos["posiciones"]:
        pyl_class = "pos" if p["pyl"] >= 0 else "neg"
        pos_rows += f"""
        <div class="c">
            <div class="top">
                <span class="nm">{p['ticker']}</span>
                <span class="sig buy">Comprar</span>
            </div>
            <div class="nums">
                <span class="pr">€{p['precio_actual']:.2f}</span>
                <div class="pnl-wrap">
                    <div class="pnl {pyl_class}">+€{p['pyl']:.2f} ({p['pyl_pct']:+.1f}%)</div>
                </div>
            </div>
        </div>
        """
    
    # Calidad KPI
    total_class = "pos" if pos["total_pyl"] >= 0 else "neg"
    
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Portfolio JL</title>
<style>
:root {{
  --bg-primary: #0F172A;
  --bg-secondary: #1E293B;
  --text-primary: #F1F5F9;
  --text-secondary: #CBD5E1;
  --text-tertiary: #94A3B8;
  --border-light: #334155;
  --green-light: #6EE7B7;
  --red-light: #FCA5A5;
}}

* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 100%; height: 100%; }}
body {{
  background: var(--bg-primary);
  color: var(--text-primary);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  padding: 12px;
}}
.container {{ max-width: 640px; margin: 0 auto; }}

.hdr {{ background: linear-gradient(135deg, #0F172A, #1E293B); padding: 18px 0; margin-bottom: 16px; border-bottom: 2px solid var(--border-light); }}
.hdr h1 {{ font-size: 18px; font-weight: 700; }}
.hdr .date {{ font-size: 11px; color: var(--text-tertiary); }}

.flash {{ background: linear-gradient(135deg, #064E3B, #047857); border: 1px solid var(--green-light); border-radius: 12px; padding: 14px; margin-bottom: 16px; font-size: 13px; color: var(--green-light); }}

.kpis {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 16px; }}
.kpi {{ background: var(--bg-secondary); border: 1px solid var(--border-light); border-radius: 10px; padding: 14px; text-align: center; }}
.kpi .lbl {{ font-size: 11px; color: var(--text-tertiary); margin-bottom: 6px; }}
.kpi .val {{ font-size: 18px; font-weight: 700; }}
.kpi .val.pos {{ color: var(--green-light); }}
.kpi .val.neg {{ color: var(--red-light); }}

.sect {{ font-size: 15px; font-weight: 700; margin: 20px 0 10px; padding-bottom: 8px; border-bottom: 2px solid var(--border-light); }}

.c {{ background: var(--bg-secondary); border: 1px solid var(--border-light); border-radius: 12px; margin-bottom: 12px; padding: 14px; }}
.c .top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
.nm {{ font-size: 15px; font-weight: 700; }}
.sig {{ font-size: 10px; font-weight: 700; padding: 4px 12px; border-radius: 8px; background: #064E3B; color: var(--green-light); }}
.c .nums {{ display: flex; justify-content: space-between; align-items: baseline; }}
.pr {{ font-size: 20px; font-weight: 700; }}
.pnl {{ font-size: 12px; font-weight: 700; }}
.pnl.pos {{ color: var(--green-light); }}
.pnl.neg {{ color: var(--red-light); }}

.disc {{ font-size: 10px; color: var(--text-tertiary); text-align: center; margin-top: 20px; padding-top: 12px; border-top: 1px solid var(--border-light); }}
</style>
</head>
<body>
<div class="container">
  <div class="hdr">
    <h1>📊 Portfolio JL</h1>
    <div class="date">{pos['fecha']}</div>
  </div>

  <div class="flash">⚡ Precios actualizados — {len(pos['posiciones'])} posiciones activas</div>

  <div class="kpis">
    <div class="kpi">
      <div class="lbl">Valor Cartera</div>
      <div class="val pos">€{pos['total_valor']:,.2f}</div>
    </div>
    <div class="kpi">
      <div class="lbl">Invertido</div>
      <div class="val">€{pos['total_invertido']:,.2f}</div>
    </div>
    <div class="kpi">
      <div class="lbl">P&L Total</div>
      <div class="val {total_class}">€{pos['total_pyl']:+,.2f}</div>
    </div>
    <div class="kpi">
      <div class="lbl">Rentabilidad</div>
      <div class="val {total_class}">{pos['total_pyl_pct']:+.2f}%</div>
    </div>
  </div>

  <div class="sect">Posiciones</div>
  {pos_rows}

  <div class="disc">Portfolio JL · Backend automático — Actualizado {pos['fecha']}</div>
</div>
</body>
</html>"""
    
    return html

def upload_to_github(html_content):
    """Sube index.html a GitHub"""
    if not GITHUB_TOKEN:
        print("❌ GITHUB_TOKEN no configurado")
        return False
    
    try:
        # API GitHub para actualizar archivo
        url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/index.html"
        
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Obtener el SHA actual del archivo (para reemplazarlo)
        response = requests.get(url, headers=headers)
        sha = response.json().get("sha") if response.status_code == 200 else None
        
        # Preparar contenido (en base64)
        import base64
        content_b64 = base64.b64encode(html_content.encode()).decode()
        
        data = {
            "message": f"🤖 Actualizar briefing - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "content": content_b64,
            "sha": sha
        }
        
        response = requests.put(url, json=data, headers=headers)
        
        if response.status_code in [200, 201]:
            print("✅ index.html subido a GitHub")
            return True
        else:
            print(f"❌ Error subiendo a GitHub: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Error GitHub API: {e}")
        return False

# ==================== MAIN ====================

def main():
    print("🤖 Portfolio JL Backend - Ejecutando...")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. Leer cartera
    cartera = get_google_sheet_data()
    if not cartera:
        print("❌ No se pudo leer cartera. Abortando.")
        return False
    
    # 2. Obtener precios
    print("📊 Obteniendo precios...")
    tickers = list(cartera.keys())
    precios = get_prices(tickers)
    
    # 3. Calcular P&L
    print("💰 Calculando P&L...")
    portfolio = calculate_portfolio(cartera, precios)
    print(f"  Valor total: €{portfolio['total_valor']:.2f}")
    print(f"  P&L: €{portfolio['total_pyl']:.2f} ({portfolio['total_pyl_pct']:+.2f}%)")
    
    # 4. Generar HTML
    print("🎨 Generando HTML...")
    html = generate_html(portfolio)
    
    # 5. Subir a GitHub
    print("📤 Subiendo a GitHub...")
    if upload_to_github(html):
        print("\n✅ ¡Briefing generado y publicado!")
        return True
    else:
        print("\n❌ Error publicando. Guardando localmente...")
        with open("index.html", "w") as f:
            f.write(html)
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
