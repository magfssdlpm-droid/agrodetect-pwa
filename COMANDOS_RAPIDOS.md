# ⚡ COMANDOS RÁPIDOS - AgroDetect PWA

## 🚀 DEPLOY RÁPIDO (Copiar y pegar)

### 1. Configurar Git (solo primera vez)
```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@example.com"
```

### 2. Subir a GitHub
```bash
cd ruta/a/InceptionV3_AgroDetect
git init
git add .
git commit -m "AgroDetect PWA - Primera versión"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/agrodetect-pwa.git
git push -u origin main
```

### 3. Actualizar cambios
```bash
git add .
git commit -m "Actualización PWA"
git push
```

---

## 🧪 PROBAR LOCALMENTE

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar app
streamlit run app_agrodetect.py

# Ver en navegador
# http://localhost:8501
```

---

## 📱 INSTALAR EN CELULAR

### Android (Chrome):
1. Abrir Chrome
2. Ir a: https://tu-app.streamlit.app
3. Menú (⋮) → "Instalar aplicación"

### iOS (Safari):
1. Abrir Safari
2. Ir a: https://tu-app.streamlit.app
3. Compartir (□↑) → "Agregar a pantalla de inicio"

---

## 🔧 SOLUCIÓN RÁPIDA DE PROBLEMAS

### Error: ModuleNotFoundError
```bash
# Agregar dependencia faltante
echo "nombre-modulo==version" >> requirements.txt
git add requirements.txt
git commit -m "Fix dependencias"
git push
```

### Error: Modelo no encontrado
```bash
# Verificar que el archivo existe
ls -lh agrodetect_inceptionv3.keras

# Si es muy grande (>100MB), usar Git LFS
git lfs install
git lfs track "*.keras"
git add .gitattributes agrodetect_inceptionv3.keras
git commit -m "Agregar modelo con LFS"
git push
```

### App muy lenta
```bash
# Reducir tamaño del modelo
python optimize_model.py  # (crear este script si es necesario)
```

---

## 📊 VERIFICAR TODO FUNCIONA

```bash
# 1. Probar localmente
streamlit run app_agrodetect.py

# 2. Verificar archivos PWA
ls -la manifest.json service-worker.js icons/

# 3. Verificar Git
git status
git log --oneline

# 4. Ver URL de deploy
# https://share.streamlit.io/tu-usuario/agrodetect-pwa/main/app_agrodetect.py
```

---

## 🎯 CHECKLIST PRE-ENTREGA

```bash
# Verificar estructura
tree -L 2

# Debe mostrar:
# .
# ├── app_agrodetect.py ✅
# ├── agrodetect_inceptionv3.keras ✅
# ├── class_names.json ✅
# ├── manifest.json ✅
# ├── service-worker.js ✅
# ├── requirements.txt ✅
# ├── icons/ ✅
# └── ...
```

---

## 📞 LINKS ÚTILES

- **GitHub**: https://github.com
- **Streamlit Cloud**: https://streamlit.io/cloud
- **Git LFS**: https://git-lfs.github.com
- **QR Generator**: https://www.qr-code-generator.com

---

## 🆘 COMANDO DE EMERGENCIA

Si algo sale mal, resetear:

```bash
# Hacer backup
cp -r InceptionV3_AgroDetect InceptionV3_AgroDetect_BACKUP

# Limpiar Git (cuidado!)
rm -rf .git
git init
git add .
git commit -m "Reset - nueva versión"
```

**⚠️ Solo usar en caso de emergencia total**

---

**Grupo 9 - AgroDetect - 2026**
