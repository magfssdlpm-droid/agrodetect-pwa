"""
AgroDetect — Clasificador Agrícola con InceptionV3
Grupo 9 | Curso: Computación Blanda / Visión por Computador

Ejecutar: streamlit run app_agrodetect.py
"""

import streamlit as st
import numpy as np
import json
import os
from PIL import Image
import io
import time

# ── Configuración de página ───────────────────────────────────────────────
st.set_page_config(
    page_title="AgroDetect",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Estilos CSS personalizados ────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&family=Inter:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.main-header {
    background: linear-gradient(135deg, #1a5c2a 0%, #2d8a47 50%, #3dba5f 100%);
    padding: 2rem;
    border-radius: 16px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(45, 138, 71, 0.3);
}

.main-header h1 {
    font-family: 'Montserrat', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    color: white;
    margin: 0;
    letter-spacing: -1px;
}

.main-header p {
    color: rgba(255,255,255,0.85);
    font-size: 1rem;
    margin: 0.5rem 0 0 0;
}

.prediction-card {
    background: linear-gradient(135deg, #f0fff4, #e6f4ea);
    border-left: 5px solid #2d8a47;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
}

.disease-card {
    background: linear-gradient(135deg, #fff5f5, #ffe8e8);
    border-left: 5px solid #e53e3e;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
}

.metric-box {
    background: white;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    border: 1px solid #e2e8f0;
}

.info-badge {
    display: inline-block;
    background: #2d8a47;
    color: white;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    margin: 3px;
}

.stProgress > div > div > div > div {
    background-color: #2d8a47;
}

footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ── Carga del modelo (cacheado) ───────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model_and_classes():
    """Carga modelo y clases. Se ejecuta solo una vez."""
    try:
        import tensorflow as tf
        from tensorflow.keras.models import load_model

        model_path = 'agrodetect_inceptionv3.keras'
        classes_path = 'class_names.json'

        if not os.path.exists(model_path):
            return None, None, "❌ Modelo no encontrado. Ejecuta primero el notebook de entrenamiento."

        if not os.path.exists(classes_path):
            return None, None, "❌ class_names.json no encontrado."

        model = load_model(model_path)
        with open(classes_path) as f:
            class_names = json.load(f)

        return model, class_names, None

    except ImportError:
        return None, None, "❌ TensorFlow no instalado. Ejecuta: pip install tensorflow"
    except Exception as e:
        return None, None, f"❌ Error cargando modelo: {str(e)}"


def preprocess_image(img: Image.Image, img_size=(224, 224)) -> np.ndarray:
    """Preprocesa imagen para InceptionV3."""
    img = img.convert('RGB').resize(img_size)
    arr = np.array(img, dtype=np.float32)
    arr = (arr / 127.5) - 1.0   # Escala [-1, 1] como InceptionV3
    return np.expand_dims(arr, 0)


def get_class_info(class_name: str) -> dict:
    """Retorna información y recomendaciones por clase.
    Tolerante a variaciones en mayúsculas y guiones bajos."""

    # Normalizar: minúsculas, colapsar múltiples guiones a uno
    def normalize(s):
        import re
        return re.sub(r'_+', '_', s.lower().strip())

    INFO_RAW = {
        "pepper_bell_bacterial_spot": {
            "emoji": "🫑🔴",
            "nombre": "Mancha Bacteriana del Pimiento",
            "estado": "enfermedad",
            "descripcion": "Infección bacteriana causada por Xanthomonas campestris. Produce lesiones oscuras en hojas y frutos.",
            "recomendaciones": [
                "Aplicar cobre bactericida cada 7-10 días",
                "Eliminar hojas infectadas y destruirlas",
                "Evitar riego excesivo en el follaje",
                "Rotar cultivos la próxima temporada",
                "Usar semillas certificadas libres de bacteria"
            ],
            "urgencia": "Alta",
            "color": "#e53e3e"
        },
        "pepper_bell_healthy": {
            "emoji": "🫑✅",
            "nombre": "Pimiento Saludable",
            "estado": "saludable",
            "descripcion": "La planta presenta condiciones óptimas. Continúa con el manejo agronómico actual.",
            "recomendaciones": [
                "Mantener riego regular (2-3 veces/semana)",
                "Aplicar fertilizante N-P-K cada 3 semanas",
                "Monitorear plagas preventivamente",
                "Asegurar buena ventilación entre plantas"
            ],
            "urgencia": "Ninguna",
            "color": "#2d8a47"
        },
        "potato_early_blight": {
            "emoji": "🥔🟡",
            "nombre": "Tizón Temprano de la Papa",
            "estado": "enfermedad",
            "descripcion": "Causado por Alternaria solani. Manchas oscuras con anillos concéntricos en hojas bajas.",
            "recomendaciones": [
                "Aplicar fungicida con Clorotalonil o Mancozeb",
                "Eliminar el material vegetal afectado",
                "Aumentar el espacio entre plantas",
                "Evitar fertilización excesiva con nitrógeno",
                "Monitorear con mayor frecuencia"
            ],
            "urgencia": "Media",
            "color": "#d69e2e"
        },
        "potato_late_blight": {
            "emoji": "🥔🔴",
            "nombre": "Tizón Tardío de la Papa",
            "estado": "enfermedad",
            "descripcion": "Phytophthora infestans — el patógeno más devastador de la papa. Requiere acción INMEDIATA.",
            "recomendaciones": [
                "⚠️ URGENTE: Aplicar fungicida sistémico (Metalaxyl)",
                "Destruir plantas severamente afectadas",
                "No regar por aspersión, usar goteo",
                "Alertar a agricultores vecinos",
                "Consultar con agrónomo inmediatamente"
            ],
            "urgencia": "Crítica",
            "color": "#c53030"
        },
        "potato_healthy": {
            "emoji": "🥔✅",
            "nombre": "Papa Saludable",
            "estado": "saludable",
            "descripcion": "La planta de papa se encuentra en excelentes condiciones fitosanitarias.",
            "recomendaciones": [
                "Continuar monitoreo cada 5-7 días",
                "Mantener humedad del suelo al 70%",
                "Aporcar cuando las plantas alcancen 20 cm",
                "Prevenir escarabajo de la papa (Leptinotarsa)"
            ],
            "urgencia": "Ninguna",
            "color": "#2d8a47"
        }
    }

    # Buscar por clave normalizada
    key = normalize(class_name)
    result = INFO_RAW.get(key)

    # Si no encontró con clave exacta normalizada, buscar por palabras clave
    if result is None:
        for k, v in INFO_RAW.items():
            if all(word in key for word in k.split('_') if len(word) > 3):
                result = v
                break

    if result is None:
        result = {
            "emoji": "🌿",
            "nombre": class_name.replace('__', ' ').replace('_', ' ').title(),
            "estado": "desconocido",
            "descripcion": "Clase detectada por el modelo.",
            "recomendaciones": ["Consulta con un agrónomo experto."],
            "urgencia": "Consultar",
            "color": "#718096"
        }

    return result


# ═══════════════════════════════════════════════════════════════════════════
# INTERFAZ PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════

# ── Header ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🌿 AgroDetect</h1>
    <p>Inteligencia Artificial para una Agricultura Saludable | InceptionV3 · Transfer Learning</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo si existe
    if os.path.exists('logo.png'):
        st.image('logo.png', use_container_width=True)
    else:
        st.markdown("## 🌿 AgroDetect")

    st.markdown("---")
    st.markdown("### 📋 Información del Modelo")
    st.markdown("""
    **Arquitectura:** InceptionV3  
    **Dataset:** PlantVillage  
    **Clases:** 5 enfermedades/estados  
    **Estrategia:** Transfer Learning + Fine-tuning  
    """)

    # Cargar métricas si existen
    if os.path.exists('model_metrics.json'):
        with open('model_metrics.json') as f:
            metrics = json.load(f)
        st.markdown("### 📊 Rendimiento")
        acc_pct = metrics.get('val_accuracy', 0) * 100
        st.metric("Val. Accuracy", f"{acc_pct:.1f}%")
        st.metric("Val. Loss", f"{metrics.get('val_loss', 0):.4f}")
        st.metric("Parámetros", f"{metrics.get('total_params', 0):,}")

    st.markdown("---")
    st.markdown("### 🌱 Cultivos soportados")
    st.markdown("""
    - 🫑 **Pimiento Bell** (2 estados)
    - 🥔 **Papa** (3 estados)
    """)

    st.markdown("---")
    st.markdown("### 👥 Grupo 9")
    st.markdown("*Computación Blanda · 2026*")

# ── Carga del modelo ──────────────────────────────────────────────────────
with st.spinner("🔄 Cargando modelo InceptionV3..."):
    model, class_names, error_msg = load_model_and_classes()

if error_msg:
    st.error(error_msg)
    st.info("""
    **Para usar AgroDetect:**
    1. Ejecuta el notebook `AgroDetect_InceptionV3_Train.ipynb`
    2. Asegúrate de que `agrodetect_inceptionv3.keras` y `class_names.json` estén en la misma carpeta
    3. Reinicia la app con `streamlit run app_agrodetect.py`
    """)
    st.stop()

st.success(f"✅ Modelo cargado — {len(class_names)} clases detectables")

# ── Tabs principales ──────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🔍 Diagnóstico", "📊 Información del Modelo", "📖 Guía de Uso"])

# ─────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown("## 🔍 Diagnóstico de Planta")
    st.markdown("Sube una imagen de hoja de **pimiento** o **papa** para detectar posibles enfermedades.")

    col_upload, col_result = st.columns([1, 1], gap="large")

    with col_upload:
        uploaded_file = st.file_uploader(
            "📸 Cargar imagen",
            type=["jpg", "jpeg", "png", "bmp", "webp"],
            help="Formatos: JPG, PNG, BMP, WEBP"
        )

        # Galería de ejemplos rápidos (desde validation set)
        st.markdown("---")
        st.markdown("**🗂️ O selecciona una imagen de prueba:**")

        test_images = []
        for clase in (class_names or []):
            val_dir = os.path.join('dataset', 'validation', clase)
            if os.path.isdir(val_dir):
                imgs = [f for f in os.listdir(val_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                if imgs:
                    test_images.append((clase, os.path.join(val_dir, imgs[0])))

        if test_images:
            cols_test = st.columns(min(len(test_images), 3))
            for i, (clase, img_path) in enumerate(test_images[:3]):
                with cols_test[i % 3]:
                    info = get_class_info(clase)
                    thumb = Image.open(img_path).resize((100, 100))
                    if st.button(info['emoji'], key=f"test_{i}", help=info['nombre']):
                        st.session_state['test_img_path'] = img_path
                    st.caption(info['nombre'][:20] + "...")

        if uploaded_file:
            img = Image.open(uploaded_file)
            st.image(img, caption="Imagen cargada", use_container_width=True)
        elif st.session_state.get('test_img_path'):
            img = Image.open(st.session_state['test_img_path'])
            st.image(img, caption="Imagen de prueba", use_container_width=True)
        else:
            img = None

    with col_result:
        if img is not None:
            with st.spinner("🧠 Analizando con InceptionV3..."):
                t0 = time.time()
                arr = preprocess_image(img)
                preds = model.predict(arr, verbose=0)[0]
                elapsed = (time.time() - t0) * 1000

            idx      = np.argmax(preds)
            clase    = class_names[idx]
            conf     = float(preds[idx]) * 100
            info     = get_class_info(clase)

            # ── Resultado principal ──────────────────────────────────────
            if info['estado'] == 'saludable':
                card_class = "prediction-card"
                estado_emoji = "✅"
                estado_texto = "SALUDABLE"
            else:
                card_class = "disease-card"
                estado_emoji = "⚠️"
                estado_texto = "ENFERMEDAD DETECTADA"

            st.markdown(f"""
            <div class="{card_class}">
                <h3>{info['emoji']} {info['nombre']}</h3>
                <p><strong>{estado_emoji} {estado_texto}</strong></p>
                <p>{info['descripcion']}</p>
            </div>
            """, unsafe_allow_html=True)

            # ── Métricas ──────────────────────────────────────────────────
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Confianza", f"{conf:.1f}%")
            with m2:
                st.metric("Urgencia", info['urgencia'])
            with m3:
                st.metric("Inferencia", f"{elapsed:.0f} ms")

            # ── Barra de confianza ────────────────────────────────────────
            st.markdown(f"**Confianza del diagnóstico:** {conf:.1f}%")
            st.progress(float(conf / 100))

            # ── Top 3 predicciones ────────────────────────────────────────
            st.markdown("**Top predicciones:**")
            top3_idx = np.argsort(preds)[::-1][:3]
            for rank, i in enumerate(top3_idx):
                c     = class_names[i]
                p     = float(preds[i]) * 100
                inf   = get_class_info(c)
                emoji = "🥇" if rank == 0 else ("🥈" if rank == 1 else "🥉")
                st.markdown(f"{emoji} **{inf['nombre']}** — {p:.1f}%")
                st.progress(float(p / 100))

            # ── Recomendaciones ───────────────────────────────────────────
            st.markdown("---")
            st.markdown("### 💡 Recomendaciones")
            for rec in info['recomendaciones']:
                st.markdown(f"- {rec}")

        else:
            st.markdown("""
            <div style="text-align:center; padding:3rem; background:#f7fafc; border-radius:12px; border:2px dashed #cbd5e0;">
                <h3>📸</h3>
                <p style="color:#718096;">Sube una imagen para comenzar el diagnóstico</p>
                <p style="color:#a0aec0; font-size:0.85rem;">Soporta hojas de pimiento y papa</p>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("## 📊 InceptionV3 — Arquitectura e Información")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 🏗️ Arquitectura")
        st.markdown("""
        | Característica | Valor |
        |---|---|
        | Desarrollado por | Google Brain |
        | Año | 2015 (publicado 2016) |
        | Parámetros totales | ~23.9 millones |
        | Profundidad | 159 capas |
        | Accuracy ImageNet Top-1 | 78.8% |
        | Accuracy ImageNet Top-5 | 94.4% |
        | Input mínimo | 75 × 75 px |
        | Input típico | 299 × 299 px |
        | Tamaño del modelo | ~92 MB |
        """)

    with col_b:
        st.markdown("### 🔬 Innovaciones clave")
        st.markdown("""
        **Módulo Inception:**
        Aplica simultáneamente convoluciones de 1×1, 3×3, 5×5 y max-pooling
        en paralelo, capturando características a múltiples escalas.

        **Factorización de convoluciones:**
        Descompone 5×5 en dos 3×3, reduciendo operaciones un 28%.
        Descompone n×n en 1×n y n×1 (convoluciones asimétricas).

        **Regularización con Label Smoothing:**
        Técnica de regularización que mejora la generalización del modelo.

        **Batch Normalization:**
        Aplicado extensivamente para acelerar el entrenamiento.
        """)

    st.markdown("### ⚖️ Comparación con otras CNNs")
    st.markdown("""
    | Modelo | Parámetros | Top-1 Acc | Tamaño | Vel. (ms) |
    |---|---|---|---|---|
    | **InceptionV3** | 23.9M | 78.8% | 92 MB | 55 |
    | VGG19 | 143.7M | 71.3% | 549 MB | 140 |
    | ResNet50 | 25.6M | 75.3% | 98 MB | 35 |
    | MobileNetV2 | 3.4M | 71.3% | 14 MB | 14 |
    | EfficientNetB0 | 5.3M | 77.1% | 29 MB | 46 |
    | DenseNet121 | 8.1M | 75.0% | 33 MB | 49 |
    """)

    # Gráficas si existen los archivos
    if os.path.exists('training_curves.png'):
        st.markdown("### 📈 Curvas de Entrenamiento")
        st.image('training_curves.png', use_container_width=True)

    if os.path.exists('confusion_matrix.png'):
        st.markdown("### 🟩 Matriz de Confusión")
        st.image('confusion_matrix.png', use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown("## 📖 Guía de Uso de AgroDetect")

    st.markdown("""
    ### 🚀 Inicio rápido

    1. **Instala dependencias:**
    ```bash
    pip install tensorflow streamlit pillow
    ```

    2. **Entrena el modelo** (o usa uno preentrenado):
    ```bash
    # En Jupyter / VS Code:
    jupyter notebook AgroDetect_InceptionV3_Train.ipynb

    # En Google Colab:
    # Sube el .ipynb y ejecútalo en Runtime > Run All
    ```

    3. **Lanza la aplicación:**
    ```bash
    streamlit run app_agrodetect.py
    ```

    ---

    ### 🌿 Clases detectadas
    """)

    for cn in (class_names or []):
        info = get_class_info(cn)
        urgencia_color = {
            "Ninguna": "🟢",
            "Media": "🟡",
            "Alta": "🔴",
            "Crítica": "🚨"
        }.get(info['urgencia'], "⚪")

        with st.expander(f"{info['emoji']} {info['nombre']} {urgencia_color}"):
            st.markdown(f"**Urgencia:** {info['urgencia']}")
            st.markdown(f"**Descripción:** {info['descripcion']}")
            st.markdown("**Recomendaciones:**")
            for r in info['recomendaciones']:
                st.markdown(f"  - {r}")

    st.markdown("""
    ---
    ### 📁 Estructura de archivos necesaria

    ```
    AgroDetect/
    ├── app_agrodetect.py              ← Esta app
    ├── AgroDetect_InceptionV3_Train.ipynb
    ├── agrodetect_inceptionv3.keras   ← Generado al entrenar
    ├── class_names.json               ← Generado al entrenar
    ├── model_metrics.json             ← Generado al entrenar
    ├── logo.png                       ← Logo de AgroDetect
    └── dataset/
        ├── train/
        │   ├── Pepper__bell__Bacterial_spot/
        │   ├── Pepper__bell__healthy/
        │   ├── Potato__Early_blight/
        │   ├── Potato__Late_blight/
        │   └── Potato__healthy/
        └── validation/
            └── (mismas carpetas)
    ```
    """)

# ── Footer ─────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#718096; font-size:0.85rem;'>"
    "🌿 AgroDetect · Grupo 9 · InceptionV3 · Computación Blanda 2026 · "
    "Inteligencia Artificial para una Agricultura Saludable"
    "</p>",
    unsafe_allow_html=True
)
