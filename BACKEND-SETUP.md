# 🤖 SETUP BACKEND AUTOMÁTICO — Portfolio JL

## ✅ Lo que tienes listo

3 archivos Python listos para usar:

1. ✅ `app.py` — Backend que genera briefing
2. ✅ `requirements.txt` — Dependencias
3. ✅ `.github/workflows/portfolio-jl.yml` — Automatización

---

## 📋 PASO 1: Obtener API Key de AlphaVantage (GRATIS)

AlphaVantage proporciona precios de acciones de forma gratuita.

1. Ve a: https://www.alphavantage.co/api/
2. Introduce tu **email**
3. Haz click **"GET FREE API KEY"**
4. Te llegará por email: `ABC123XYZ` (algo así)
5. **Copia esta key** (la necesitas en el siguiente paso)

> **Límites gratis:** 5 llamadas/minuto, 500/día. Suficiente para tu cartera (8 tickers).

---

## 📤 PASO 2: Subir archivos a GitHub

### **Opción A: Por web GitHub (MÁS FÁCIL)**

1. Ve a tu repo: https://github.com/jlguillen-creator/portfolio-jl
2. Click **"Add file"** → **"Upload files"**
3. **Arrastra estos 3 archivos:**
   - `app.py`
   - `requirements.txt`
   - (La carpeta `.github/workflows/portfolio-jl.yml` se sube con ella)

4. **Commit changes**

Verifica que están en la raíz:
```
portfolio-jl/
├── index.html
├── manifest.json
├── service-worker.js
├── icon-*.png
├── app.py                          ← NUEVO
├── requirements.txt                ← NUEVO
└── .github/
    └── workflows/
        └── portfolio-jl.yml        ← NUEVO
```

### **Opción B: Con Git (si tienes terminal)**

```bash
cd portfolio-jl
# Copiar archivos descargados aquí
cp ~/Descargas/app.py .
cp ~/Descargas/requirements.txt .
cp -r ~/Descargas/.github .

git add .
git commit -m "🤖 Agregar backend automático"
git push origin main
```

---

## 🔐 PASO 3: Añadir API Key a GitHub Secrets

GitHub Actions necesita tu API key de AlphaVantage de forma segura.

1. Ve a tu repo: https://github.com/jlguillen-creator/portfolio-jl
2. **Settings** (engranaje, arriba a la derecha)
3. **Secrets and variables** → **Actions** (lado izquierdo)
4. Click **"New repository secret"**
5. **Name:** `ALPHA_VANTAGE_API_KEY`
6. **Secret:** Pega tu API key (la que copiaste en Paso 1)
7. **Add secret**

✅ Listo. GitHub Actions ahora tiene acceso a tu key.

---

## ⚙️ PASO 4: Verificar GitHub Actions

1. Ve a tu repo
2. Click en pestaña **"Actions"** (arriba del repo)
3. Deberías ver: **"Portfolio JL - Actualizar Briefing"**

**Para probar AHORA (no esperar al lunes 22:45):**

1. Click en el workflow **"Portfolio JL - Actualizar Briefing"**
2. Click en **"Run workflow"** (botón azul)
3. **Run workflow** de nuevo
4. Espera 30-60 segundos
5. Verifica que pasó ✅ o falló ❌

Si falla, click en el job para ver el error (probablemente API key).

---

## 🔄 CÓMO FUNCIONA

### **Automático cada lunes 22:45 CET:**

```
Lunes 22:45 → GitHub Actions se ejecuta automático
         ↓
Ejecuta app.py
         ↓
1. Lee tu Google Sheet (Ticker, Acciones, CostoMedio)
2. Obtiene precios de AlphaVantage
3. Calcula P&L (Valor, Ganancia/Pérdida)
4. Genera HTML briefing con datos actualizados
5. Sube index.html a tu repo automático
         ↓
Tu PWA se actualiza automático
(cuando la abres, muestra el briefing nuevo)
         ↓
En tu teléfono: Cierra y abre la app
(o recarga si está abierta)
         ↓
¡Ves el briefing del lunes!
```

### **Martes-Domingo:**

El briefing queda estático (no se actualiza). Es solo el lunes cuando GitHub Actions genera uno nuevo.

---

## 📊 ¿QUÉ VERÁS EN LA APP?

El briefing que genera tiene:

✅ **Valor total de cartera**  
✅ **Total invertido**  
✅ **P&L total** (euros y %)  
✅ **Cada posición:** precio actual, P&L, rentabilidad  
✅ **Fecha y hora** de actualización  

**NO tiene (aún):**
- ❌ Análisis macro (Fed, Brent, noticias)
- ❌ Gráficos de 30 días

Eso lo añadimos cuando lo necesites (es rápido).

---

## 🆘 TROUBLESHOOTING

### **"El workflow falla"**

Causas comunes:
- [ ] ALPHA_VANTAGE_API_KEY no configurada → Ve a Paso 3
- [ ] API key incorrecta → Verifica en AlphaVantage
- [ ] Google Sheet no accesible → Comprueba que está compartido (público)

**Para ver el error exacto:**
1. Ve a **Actions** en tu repo
2. Click en el workflow fallido
3. Click en el job
4. Scroll hasta ver el error en rojo

### **"No se actualiza en la app"**

1. Cierra completamente la app (desliza hacia arriba)
2. Abre de nuevo
3. Espera 2 segundos (se actualiza desde cache)
4. Si aún no: F5 (refrescar) en el navegador

### **"Precios aparecen null o 0"**

Probablemente AlphaVantage tiene rate limit (5 llamadas/min).
- Espera 1 minuto
- El próximo lunes funcionará

---

## 📅 PROGRAMACIÓN

El workflow se ejecuta:
- **Lunes 21:45 UTC** = 22:45 CET (ajustado por horario de verano)
- También puedes ejecutar manualmente (botón "Run workflow")

**¿Quieres cambiar el horario?**

Edita `.github/workflows/portfolio-jl.yml` línea 7:
```yaml
- cron: '45 21 * * 1'  # Minuto Hora * * Día (1=lunes)
```

Ejemplos:
- `'30 22 * * 1'` = Lunes 22:30 UTC (23:30 CET)
- `'0 23 * * 0'` = Domingo 23:00 UTC (lunes 00:00 CET)

---

## 🎯 PRÓXIMOS PASOS (OPCIONALES)

### **Si quieres análisis macro semanal (Fed, Brent, noticias):**

Me lo pides cada lunes y genero un briefing "premium" que incluye:
- Análisis de noticias macro
- Contexto económico
- Recomendaciones

Es rápido (~3-4K tokens) y lo subes a GitHub.

---

## ✅ RESUMEN

| Paso | Acción | Status |
|------|--------|--------|
| 1 | API Key AlphaVantage | ✅ Gratis |
| 2 | Subir archivos a GitHub | ✅ 2 min |
| 3 | Configurar GitHub Secrets | ✅ 1 min |
| 4 | Probar workflow | ✅ Manual |
| **TOTAL** | | **~5 min** |

**Luego:** Cada lunes 22:45, tu briefing se actualiza automático sin que hagas nada. 🤖

---

**¿Necesitas ayuda en algún paso?** Pregunta y te lo resuelvo. 🚀
