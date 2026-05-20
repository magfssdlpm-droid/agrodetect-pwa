# 🚀 GUÍA DE DEPLOY: AgroDetect en Streamlit Cloud

## 📋 PASO 4: Preparar GitHub (30 minutos)

### 4.1 Crear cuenta en GitHub (si no tienes)

1. Ve a https://github.com
2. Click en "Sign up"
3. Sigue los pasos de registro
4. Verifica tu email

### 4.2 Instalar Git (si no lo tienes)

**Windows:**
- Descargar desde: https://git-scm.com/download/win
- Instalar con opciones por defecto

**Mac:**
```bash
# Abrir Terminal y ejecutar:
xcode-select --install
```

**Linux:**
```bash
sudo apt-get install git
```

### 4.3 Configurar Git (primera vez)

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"
```

### 4.4 Subir tu proyecto a GitHub

```bash
# 1. Abrir terminal/cmd en la carpeta de tu proyecto
cd ruta/a/InceptionV3_AgroDetect

# 2. Inicializar repositorio Git
git init

# 3. Agregar todos los archivos
git add .

# 4. Hacer primer commit
git commit -m "AgroDetect PWA - Primera versión"

# 5. Crear repositorio en GitHub:
# - Ve a https://github.com/new
# - Nombre: agrodetect-pwa
# - Descripción: App móvil de detección de enfermedades agrícolas
# - Público o Privado (tu elección)
# - NO marcar "Initialize with README"
# - Click "Create repository"

# 6. Conectar con GitHub (reemplaza TU-USUARIO con tu usuario)
git branch -M main
git remote add origin https://github.com/TU-USUARIO/agrodetect-pwa.git
git push -u origin main
```

**IMPORTANTE:** Si el modelo `.keras` es muy grande (>100MB), GitHub lo rechazará.

**Solución:** Usar Git LFS o subir el modelo a otro servicio.

```bash
# Opción 1: Git LFS (Large File Storage)
git lfs install
git lfs track "*.keras"
git add .gitattributes
git add agrodetect_inceptionv3.keras
git commit -m "Agregar modelo con LFS"
git push

# Opción 2: No subir el modelo a GitHub
# En .gitignore agregar:
# *.keras
# Luego subirlo manualmente a Streamlit Cloud
```

---

## 📋 PASO 5: Deploy en Streamlit Cloud (15 minutos)

### 5.1 Crear cuenta en Streamlit Cloud

1. Ve a https://streamlit.io/cloud
2. Click en "Sign up"
3. **Selecciona "Continue with GitHub"** (más fácil)
4. Autoriza Streamlit a acceder a tus repositorios

### 5.2 Crear nueva app

1. Click en **"New app"**
2. Configurar:
   - **Repository**: Selecciona `tu-usuario/agrodetect-pwa`
   - **Branch**: `main`
   - **Main file path**: `app_agrodetect.py`
   - **App URL** (opcional): Personaliza la URL si quieres

3. Click en **"Advanced settings"** (opcional):
   - Python version: 3.11 (recomendado)
   - Si tu modelo es muy grande, puedes necesitar más recursos

4. Click en **"Deploy!"**

### 5.3 Esperar el deploy (5-10 minutos)

Verás logs en tiempo real:
```
[YYYY-MM-DD HH:MM:SS] 📦 Clonando repositorio...
[YYYY-MM-DD HH:MM:SS] 🐍 Instalando dependencias...
[YYYY-MM-DD HH:MM:SS] 🚀 Iniciando app...
[YYYY-MM-DD HH:MM:SS] ✅ App deployed!
```

### 5.4 Tu app estará en:

```
https://tu-usuario-agrodetect-pwa.streamlit.app
```

O la URL personalizada que elegiste.

---

## 📋 PASO 6: Probar en celulares (20 minutos)

### 6.1 Probar en Android

1. Abre Chrome en tu Android
2. Visita tu URL de Streamlit
3. Espera que cargue completamente
4. Toca menú (⋮) → "Instalar aplicación"
5. Confirma instalación
6. ✅ Abre desde pantalla de inicio

**Verificar:**
- ✅ Se ve bien en pantalla pequeña
- ✅ Botones son fáciles de tocar
- ✅ Upload de imagen funciona
- ✅ Predicciones se hacen correctamente

### 6.2 Probar en iOS

1. Abre Safari en iPhone
2. Visita tu URL de Streamlit
3. Toca botón compartir (□↑)
4. "Agregar a pantalla de inicio"
5. ✅ Abre desde pantalla de inicio

**Verificar lo mismo que en Android**

---

## 📋 PASO 7: Solucionar Problemas Comunes

### Problema 1: "ModuleNotFoundError"

**Causa:** Falta una dependencia en `requirements.txt`

**Solución:**
```bash
# Agregar la dependencia faltante a requirements.txt
echo "nombre-del-modulo==version" >> requirements.txt

# Hacer commit y push
git add requirements.txt
git commit -m "Agregar dependencia faltante"
git push
```

Streamlit Cloud se actualizará automáticamente.

### Problema 2: "File not found: agrodetect_inceptionv3.keras"

**Causa:** El modelo no se subió a GitHub

**Soluciones:**

**A) Usar Git LFS:**
```bash
git lfs install
git lfs track "*.keras"
git add .gitattributes agrodetect_inceptionv3.keras
git commit -m "Agregar modelo con LFS"
git push
```

**B) Subir manualmente en Streamlit Cloud:**
1. En Streamlit Cloud, ve a tu app
2. Click en "⋮" → "Settings"
3. Upload el archivo `.keras` manualmente

**C) Hospedar modelo externamente:**
```python
# En app_agrodetect.py
import gdown

# Descargar desde Google Drive
@st.cache_resource
def load_model_from_drive():
    url = 'https://drive.google.com/uc?id=TU_ID_DEL_ARCHIVO'
    output = 'agrodetect_inceptionv3.keras'
    
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)
    
    return load_model(output)
```

### Problema 3: App muy lenta

**Causas:**
- Modelo muy grande (176 MB)
- Demasiadas peticiones

**Soluciones:**
1. Optimizar modelo con cuantización
2. Usar `@st.cache_resource` (ya lo tienen)
3. Reducir tamaño de imágenes antes de procesar

### Problema 4: No se ve el botón de instalación

**Causas:**
- PWA requiere HTTPS (Streamlit Cloud lo tiene)
- Navegador no soporta PWA
- Ya está instalada

**Verificar:**
- Chrome/Safari versión actualizada
- Abrir en modo incógnito para probar
- Revisar consola del navegador (F12)

### Problema 5: Límites de Streamlit Cloud (gratis)

**Límites:**
- 1 GB de recursos
- Tiempo de ejecución limitado
- Duerme después de 7 días sin uso

**Alternativas si lo superan:**
- Streamlit Cloud (plan de pago): $20/mes
- Render.com (gratis con límites similares)
- Hugging Face Spaces (gratis, ilimitado)
- Railway.app (gratis $5 crédito)

---

## 📋 PASO 8: Actualizar la app (cuando hagan cambios)

```bash
# 1. Hacer cambios en tu código
# 2. Guardar archivos

# 3. Hacer commit
git add .
git commit -m "Descripción de los cambios"

# 4. Push a GitHub
git push

# 5. Streamlit Cloud se actualiza AUTOMÁTICAMENTE en 1-2 minutos
```

---

## 📋 PASO 9: Compartir con profesores y compañeros

### Para la presentación:

**1. Link directo:**
```
https://tu-usuario-agrodetect-pwa.streamlit.app
```

**2. QR Code:**
- Generar en: https://www.qr-code-generator.com/
- Pegar tu URL
- Descargar QR
- Incluir en presentación

**3. Screenshots:**
- Captura de la app en celular
- Captura del proceso de instalación
- Captura de una predicción

**4. Video demo (1-2 min):**
- Abrir app en celular
- Instalar desde navegador
- Tomar foto de planta
- Mostrar resultado
- Enfatizar que funciona como app nativa

---

## ✅ CHECKLIST FINAL

Antes de la entrega, verificar:

### Funcionalidad:
- [ ] App carga en navegador móvil
- [ ] Se puede instalar en Android
- [ ] Se puede instalar en iOS  
- [ ] Upload de imágenes funciona
- [ ] Modelo hace predicciones correctas
- [ ] Resultados se muestran bien
- [ ] No hay errores en consola (F12)

### PWA:
- [ ] manifest.json está accesible
- [ ] service-worker.js está registrado
- [ ] Iconos se cargan correctamente
- [ ] Funciona offline (básico)
- [ ] Botón de instalación aparece

### Documentación:
- [ ] README con instrucciones
- [ ] Screenshots de la app
- [ ] Link de la app funcionando
- [ ] Video demo (opcional pero recomendado)

### Presentación:
- [ ] Slides explicando PWA
- [ ] Demo en vivo desde celular
- [ ] Comparativa de modelos
- [ ] Métricas de rendimiento

---

## 🎯 PARA LA PRESENTACIÓN

### Argumentos para defender PWA:

**"¿Por qué no app nativa?"**

> "Implementamos una Progressive Web App, tecnología usada por Twitter, Starbucks y Uber. Las ventajas son:
> 
> 1. **Instalable**: Se instala como app nativa en iOS y Android
> 2. **Sin tiendas**: No requiere aprobación de App Store/Play Store
> 3. **Actualizaciones instantáneas**: Sin esperar aprobaciones
> 4. **Moderna**: Es el estándar actual para apps web
> 5. **Funciona offline**: Con service workers
> 6. **Multiplataforma**: Un código para todas las plataformas
> 
> Esto nos permitió enfocarnos en la implementación de la CNN con InceptionV3, que es la parte más compleja del proyecto."

### Comparativa técnica:

| Característica | App Nativa | PWA (AgroDetect) |
|----------------|------------|------------------|
| Instalable | ✅ | ✅ |
| Funciona offline | ✅ | ✅ |
| Acceso a cámara | ✅ | ✅ |
| Tiempo desarrollo | 4-6 semanas | 2-3 días |
| Publicación | Aprobación requerida | Instantáneo |
| Actualizaciones | Manual | Automático |
| Costo | $124/año | $0 |

---

## 📞 SOPORTE

Si tienen problemas durante el deploy:

1. **Revisar logs de Streamlit Cloud:**
   - En tu app → "Manage app" → "Logs"
   - Buscar errores en rojo

2. **GitHub Issues:**
   - Verificar que todos los archivos se subieron

3. **Probar localmente primero:**
   ```bash
   streamlit run app_agrodetect.py
   ```

4. **Consola del navegador:**
   - F12 → Console
   - Buscar errores de PWA

---

## 🎉 ¡ÉXITO!

Si completaste todos los pasos, ahora tienes:

✅ App móvil funcionando en iOS y Android
✅ Instalable como app nativa
✅ Deploy automático en la nube
✅ Link para compartir
✅ Proyecto completo para entregar

**¡Tu proyecto está listo para el 30 de Mayo!** 🚀

---

**Grupo 9 - AgroDetect**  
**Computación Blanda 2026**
