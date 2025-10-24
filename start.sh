#!/bin/bash

# Script de inicio rápido para Análisis Estadístico v2.0
# Autor: JOSE CAMARENA MEZA

echo "🚀 Iniciando Análisis Estadístico v2.0..."
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    exit 1
fi

echo "✅ Python detectado: $(python3 --version)"

# Verificar Streamlit
if ! command -v streamlit &> /dev/null; then
    echo "⚠️  Streamlit no está instalado"
    echo "📦 Instalando dependencias..."
    pip install -r requirements.txt
fi

echo "✅ Streamlit detectado: $(streamlit version)"
echo ""

# Ejecutar aplicación
echo "🌐 Abriendo aplicación en http://localhost:8501"
echo "💡 Presiona Ctrl+C para detener"
echo ""

streamlit run app.py
