"""
Configuración centralizada de la aplicación.
"""

# Configuración de la aplicación
APP_CONFIG = {
    "title": "Análisis Estadístico Descriptivo",
    "icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Configuración de archivos
FILE_CONFIG = {
    "allowed_extensions": ["csv", "xlsx", "txt"],
    "max_file_size_mb": 200,
    "default_encoding": "utf-8",
    "encodings": ["utf-8", "latin-1", "ISO-8859-1"],
    "separators": [",", ";", "\t", "|", " "],
    "decimals": [".", ","],
}

# Configuración de visualización
VISUALIZATION_CONFIG = {
    "themes": {
        "default": {"style": "whitegrid", "palette": None},
        "dark": {"style": "darkgrid", "palette": None, "background": True},
        "blue": {"style": "whitegrid", "palette": "Blues_d"},
        "green": {"style": "whitegrid", "palette": "Greens_d"},
        "purple": {"style": "whitegrid", "palette": "Purples_d"},
    },
    "figure_size": (10, 6),
    "dpi": 300,
    "max_categories_pie": 10,
    "max_categories_bar": 15,
}

# Configuración de análisis estadístico
ANALYSIS_CONFIG = {
    "min_data_points": 4,
    "max_intervals": 20,
    "confidence_level": 0.95,
}

# Estilos CSS personalizados
CUSTOM_CSS = """
<style>
    .main {
        padding: 2rem;
    }
    .title {
        font-size: 3rem !important;
        color: #1E6091;
        text-align: center;
        margin-bottom: 2rem;
    }
    .subtitle {
        font-size: 1.5rem !important;
        font-weight: 600;
        color: #2C3E50;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #6c757d;
        font-size: 0.8rem;
    }
    .stButton button {
        background-color: #1E6091;
        color: white;
        font-weight: 600;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        width: 100%;
    }
    .stDownloadButton button {
        background-color: #28a745;
        color: white;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
"""
