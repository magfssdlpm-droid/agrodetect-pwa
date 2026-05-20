# 🌿 AgroDetect — Instrucciones de Uso

**Clasificador Agrícola con InceptionV3 | Grupo 9 | Computación Blanda 2026**

---

## 📁 Estructura necesaria

```
TuCarpeta/
├── AgroDetect_InceptionV3_Train.ipynb   ← Notebook entrenamiento
├── app_agrodetect.py                    ← App Streamlit
├── Informe_Tecnico_AgroDetect.md        ← Informe técnico
├── logo.png                             ← (opcional) Logo AgroDetect
└── dataset/
    ├── train/
    │   ├── Pepper__bell__Bacterial_spot/
    │   ├── Pepper__bell__healthy/
    │   ├── Potato__Early_blight/
    │   ├── Potato__Late_blight/
    │   └── Potato__healthy/
    └── validation/
        ├── Pepper__bell__Bacterial_spot/
        ├── Pepper__bell__healthy/
        ├── Potato__Early_blight/
        ├── Potato__Late_blight/
        └── Potato__healthy/
```

---

## 🚀 Paso 1: Entrenar el modelo

### En Google Colab (RECOMENDADO — más rápido con GPU gratuita)

1. Ve a [colab.research.google.com](https://colab.research.google.com)
2. Sube `AgroDetect_InceptionV3_Train.ipynb`
3. Cambia a GPU: `Entorno de ejecución > Cambiar tipo de entorno > GPU T4`
4. Sube tu dataset a Google Drive en la carpeta `dataset/`
5. Ejecuta todas las celdas (`Entorno de ejecución > Ejecutar todo`)
6. El modelo se guardará en Drive como `agrodetect_inceptionv3.keras`

**Tiempo estimado en Colab T4:** ~10-20 minutos

### En Visual Studio Code / Jupyter Local

1. Instala dependencias:
```bash
pip install tensorflow streamlit pillow scikit-learn matplotlib seaborn
```

2. Asegúrate de que la carpeta `dataset/` esté al mismo nivel que el notebook

3. Abre el notebook:
```bash
jupyter notebook AgroDetect_InceptionV3_Train.ipynb
# o en VS Code: abre el archivo .ipynb directamente
```

4. Ejecuta todas las celdas (`Run All`)

**Tiempo estimado (CPU):** ~60-120 minutos  
**Tiempo estimado (GPU local):** ~15-30 minutos

---

## 🌐 Paso 2: Lanzar la aplicación web

Una vez que tengas `agrodetect_inceptionv3.keras` y `class_names.json`:

```bash
streamlit run app_agrodetect.py
```

La app se abrirá automáticamente en: **http://localhost:8501**

---

## 📂 Archivos generados por el entrenamiento

| Archivo | Descripción |
|---|---|
| `agrodetect_inceptionv3.keras` | Modelo entrenado (**REQUERIDO** por la app) |
| `class_names.json` | Lista de clases (**REQUERIDO** por la app) |
| `model_metrics.json` | Accuracy, loss y configuración |
| `training_curves.png` | Gráficas de entrenamiento |
| `confusion_matrix.png` | Matriz de confusión |
| `dataset_sample.png` | Muestra visual del dataset |

---

## ❓ Preguntas frecuentes

**¿Por qué no aparece el modelo?**  
Ejecuta primero el notebook de entrenamiento. El modelo debe estar en la misma carpeta que `app_agrodetect.py`.

**¿Qué hago si el entrenamiento es muy lento en local?**  
Usa Google Colab con GPU gratuita — es la opción más rápida y fácil.

**¿Puedo agregar más clases?**  
Sí: agrega carpetas con imágenes en `train/` y `validation/`, vuelve a entrenar, y agrega la información de la nueva clase en la función `get_class_info()` de la app.

**¿El modelo funciona con otras plantas?**  
Solo para las 5 clases entrenadas (pimiento/papa). Para más cultivos necesitas reentrenar con nuevas imágenes.

---

*Grupo 9 — AgroDetect · Computación Blanda · 2026*
