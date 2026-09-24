# 🚀 PUBLICAR PORTFOLIO JL EN GITHUB — PASO A PASO

## 📋 FICHEROS QUE NECESITAS

Estos 7 archivos (ya los tienes descargados):

1. ✅ `index.html` (renombra `index-pwa.html` a esto)
2. ✅ `manifest.json`
3. ✅ `service-worker.js`
4. ✅ `icon-192.png` (icono)
5. ✅ `icon-512.png` (icono)
6. ✅ `icon-maskable-192.png` (icono)
7. ✅ `icon-maskable-512.png` (icono)

---

## 🛠️ OPCIÓN A: Hacerlo desde GitHub Web (MÁS FÁCIL — SIN TERMINAL)

### **Paso 1: Crear nuevo repo en GitHub**

1. Ve a https://github.com/new
2. **Repository name:** `portfolio-jl` (exacto, minúsculas)
3. **Description:** "App Portfolio JL - Análisis diario de cartera"
4. **Public** ✅ (para que GitHub Pages funcione gratis)
5. **Initialize with:** NO marques nada
6. Click **"Create repository"**

### **Paso 2: Subir archivos a GitHub**

Una vez creado el repo, verás una pantalla vacía.

**Opción A.1: Upload por web (MÁS SENCILLO)**

1. Click en **"uploading an existing file"** (botón azul)
2. Arrastra y suelta estos 7 archivos:
   - `index.html`
   - `manifest.json`
   - `service-worker.js`
   - `icon-192.png`
   - `icon-512.png`
   - `icon-maskable-192.png`
   - `icon-maskable-512.png`

3. Click **"Commit changes"**
4. Espera 30 segundos

**Opción A.2: Crear archivo por archivo (si el upload falla)**

1. Click **"Add file"** → **"Create new file"**
2. Nombre: `index.html`
3. Pega el contenido de `index-pwa.html`
4. **"Commit new file"**
5. Repite con: `manifest.json`, `service-worker.js`
6. Para los PNGs: **"Add file"** → **"Upload files"** (sí acepta PNGs)

### **Paso 3: Activar GitHub Pages**

1. En tu repo, ve a **Settings** (engranaje arriba a la derecha)
2. Baja hasta **"Pages"** (lado izquierdo)
3. **Source:** Selecciona **"Deploy from a branch"**
4. **Branch:** `main` | **Folder:** `/root`
5. Click **"Save"**
6. Espera 1-2 minutos (ves un aviso azul → verde)

### **Paso 4: Ver tu PWA**

Tu app estará en: **`https://tunombre-github.github.io/portfolio-jl/`**

Copia el enlace en tu navegador (Chrome en móvil) y verás:
- El banner de Chrome: **"Instalar aplicación"**
- O el menú ⋮ → "Instalar"

---

## 🖥️ OPCIÓN B: Desde terminal (MÁS RÁPIDO SI TIENES GIT)

Si prefieres usar Git en tu máquina:

### **Paso 1: Clonar repo**

```bash
# En tu carpeta de descargas
git clone https://github.com/tunombre-github/portfolio-jl.git
cd portfolio-jl
```

### **Paso 2: Copiar archivos**

```bash
# Copiar aquí los 7 archivos descargados
cp ~/Descargas/index-pwa.html index.html
cp ~/Descargas/manifest.json .
cp ~/Descargas/service-worker.js .
cp ~/Descargas/icon-*.png .

# Verificar que están todos
ls -la
```

Deberías ver:
```
index.html
manifest.json
service-worker.js
icon-192.png
icon-512.png
icon-maskable-192.png
icon-maskable-512.png
```

### **Paso 3: Subir a GitHub**

```bash
git add .
git commit -m "Initial PWA setup - Portfolio JL"
git push origin main
```

### **Paso 4: Activar GitHub Pages**

```bash
# Mismo que Opción A, Paso 3
# Settings → Pages → Deploy from branch → main /root → Save
```

En 1-2 minutos: **https://tunombre-github.github.io/portfolio-jl/**

---

## 📱 INSTALAR EN ANDROID

### **Desde Chrome (recomendado):**

1. **Abre Chrome en tu teléfono**
2. **Entra en:** `https://tunombre-github.github.io/portfolio-jl/`
3. **Espera 2-3 segundos** (Chrome descarga el manifest)
4. **Deberías ver:**
   - Menú ⋮ (arriba a la derecha)
   - O un banner diciendo **"Instalar Portfolio JL"**
5. **Toca "Instalar"** o **Menú ⋮ → "Instalar aplicación"**
6. **Confirma** → ¡Listo!

La app aparecerá en tu pantalla de inicio como cualquier app.

---

## ✅ VERIFICAR QUE FUNCIONA

### **Desktop (Chrome/Firefox):**

1. Abre DevTools: `F12`
2. Pestaña **Console** (esquina izquierda)
3. Si ves: `✅ Service Worker registrado` → Todo bien
4. Si ves errores: 
   - Comprueba que `manifest.json` existe en la raíz
   - Comprueba que `service-worker.js` existe
   - F5 (refrescar)

### **Móvil (Chrome):**

1. Abre DevTools remoto: PC Chrome → `chrome://inspect`
2. Conecta móvil por USB
3. Aceptar "Debug" en el móvil
4. Verás la pestaña del móvil en PC
5. Click → ver console

---

## 🔄 ACTUALIZAR LA APP

**Si cambias algo (ej: actualizas `index.html`):**

### **Opción A: Por web GitHub**
1. Ve a tu repo
2. Haz click en el archivo (ej: `index.html`)
3. Icono del lápiz (Edit) arriba a la derecha
4. Edita
5. **Commit changes**
6. En tu móvil: Cierra y abre la app (se actualiza automático)

### **Opción B: Con Git**
```bash
# Editas los archivos en tu PC
# Luego:
git add .
git commit -m "Actualizar contenido"
git push origin main
```

La app se actualiza automático en 30-60 segundos.

---

## 🎯 PRÓXIMO PASO: AUTOMATIZAR CON BACKEND

Una vez tengas la PWA funcionando, el siguiente paso es:

1. **Crear un backend** en Render.com (gratis)
2. **Backend llama a MI API** cada lunes 22:45
3. **Genera HTML completo** con análisis macro
4. **Sube a GitHub** automático
5. **Tu app lo carga** sin que hagas nada

Eso lo configuramos después. Por ahora: **¡Que funcione la PWA!**

---

## ⚠️ TROUBLESHOOTING

### **"No veo el botón de instalar en Chrome móvil"**

Causas comunes:
- [ ] El `manifest.json` **no está en la raíz** del repo
- [ ] El `manifest.json` **tiene errores de JSON** (faltan comas)
- [ ] Los **iconos no existen** (falta `icon-192.png` o `icon-512.png`)
- [ ] GitHub Pages **aún no ha publicado** (espera 2-3 min)

**Solución:**
1. Ve a tu repo
2. Verifica que ves en la raíz:
   - ✅ `index.html`
   - ✅ `manifest.json`
   - ✅ `service-worker.js`
   - ✅ `icon-192.png` (¡debe estar! no en carpeta)
3. Entra en `manifest.json` y verifica que tiene `]` al final
4. F5 en el móvil (refrescar)

### **"Instalé pero la app está vacía"**

Es normal. Aparece porque en `index.html` ahora tiene un placeholder.

**Próximo lunes:** Cuando tu backend genere el briefing completo, se actualizará automático.

Mientras tanto, la app funciona y muestra datos de ejemplo.

---

## 🚀 RESUMEN RÁPIDO

| Paso | Acción | Tiempo |
|------|--------|--------|
| 1 | Crear repo `portfolio-jl` en GitHub | 1 min |
| 2 | Subir 7 archivos | 2 min |
| 3 | Activar GitHub Pages | 1 min |
| 4 | Instalar en Android | 1 min |
| **TOTAL** | | **~5 min** |

---

**¿Ya tienes GitHub? ¿Cuál opción prefieres: A (web) o B (terminal)?** 🚀

Cuando me digas, te digo exactamente tu URL final. 📱
