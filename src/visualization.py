"""
Módulo de visualización de datos.
Contiene funciones para generar gráficos estadísticos.
"""
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
import io
from src.config import VISUALIZATION_CONFIG


def apply_theme(theme):
    """
    Aplica un tema de visualización.
    
    Args:
        theme (str): Nombre del tema
    """
    theme_config = VISUALIZATION_CONFIG['themes'].get(theme, VISUALIZATION_CONFIG['themes']['default'])
    
    if theme_config.get('background'):
        plt.style.use("dark_background")
    else:
        plt.style.use("default")
    
    if theme_config['palette']:
        sns.set_theme(style=theme_config['style'], palette=theme_config['palette'])
    else:
        sns.set_theme(style=theme_config['style'])


def generate_histogram(data, variable_type, column_name):
    """
    Genera un histograma con Matplotlib.
    
    Args:
        data (pd.Series): Datos a graficar
        variable_type (str): Tipo de variable
        column_name (str): Nombre de la columna
        
    Returns:
        matplotlib.figure.Figure: Figura del histograma
    """
    if variable_type in ["Cuantitativa Continua", "Cuantitativa Discreta con Intervalos"]:
        fig, ax = plt.subplots(figsize=VISUALIZATION_CONFIG['figure_size'])
        sns.histplot(data, kde=True, bins='auto', ax=ax, color='steelblue')
        plt.title(f'Histograma de Frecuencias - {column_name}', fontsize=15)
        plt.xlabel('Intervalos', fontsize=12)
        plt.ylabel('Frecuencia Absoluta', fontsize=12)
        plt.grid(axis='y', alpha=0.3)
        return fig
    return None


def generate_interactive_histogram(data, variable_type, column_name):
    """
    Genera un histograma interactivo con Plotly.
    
    Args:
        data (pd.Series): Datos a graficar
        variable_type (str): Tipo de variable
        column_name (str): Nombre de la columna
        
    Returns:
        plotly.graph_objects.Figure: Figura interactiva
    """
    if variable_type in ["Cuantitativa Continua", "Cuantitativa Discreta con Intervalos"]:
        fig = px.histogram(
            data, 
            x=column_name,
            title=f'Histograma Interactivo - {column_name}',
            labels={'x': 'Valores', 'y': 'Frecuencia'},
            opacity=0.8,
            color_discrete_sequence=['steelblue'],
            marginal='box'
        )
        fig.update_layout(
            bargap=0.1,
            xaxis_title='Valores',
            yaxis_title='Frecuencia',
            template='plotly_white'
        )
        return fig
    return None


def generate_pie_chart(data, variable_type, column_name):
    """
    Genera un gráfico de pastel.
    
    Args:
        data (pd.Series): Datos a graficar
        variable_type (str): Tipo de variable
        column_name (str): Nombre de la columna
        
    Returns:
        matplotlib.figure.Figure: Figura del gráfico de pastel
    """
    if variable_type in ["Cualitativa", "Cuantitativa Discreta"]:
        fig, ax = plt.subplots(figsize=(10, 10))
        value_counts = data.value_counts()
        
        max_categories = VISUALIZATION_CONFIG['max_categories_pie']
        if len(value_counts) > max_categories:
            other_sum = value_counts.iloc[max_categories:].sum()
            value_counts = value_counts.iloc[:max_categories]
            if other_sum > 0:
                value_counts['Otros'] = other_sum
        
        wedges, texts, autotexts = ax.pie(
            value_counts, 
            autopct='%1.1f%%', 
            textprops={'color': "w", 'fontsize': 12},
            shadow=False, 
            startangle=90,
            explode=[0.05] * len(value_counts)
        )
        
        plt.title(f'Distribución de {column_name}', fontsize=16)
        ax.legend(
            wedges, 
            value_counts.index, 
            title="Categorías",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1)
        )
        plt.tight_layout()
        return fig
    return None


def generate_bar_chart(data, variable_type, column_name):
    """
    Genera un gráfico de barras.
    
    Args:
        data (pd.Series): Datos a graficar
        variable_type (str): Tipo de variable
        column_name (str): Nombre de la columna
        
    Returns:
        matplotlib.figure.Figure: Figura del gráfico de barras
    """
    if variable_type in ["Cualitativa", "Cuantitativa Discreta"]:
        fig, ax = plt.subplots(figsize=(12, 8))
        value_counts = data.value_counts().sort_values(ascending=False)
        
        max_categories = VISUALIZATION_CONFIG['max_categories_bar']
        if len(value_counts) > max_categories:
            value_counts = value_counts.iloc[:max_categories]
        
        sns.barplot(x=value_counts.index, y=value_counts.values, ax=ax, hue=value_counts.index, palette='viridis', legend=False)
        plt.title(f'Gráfico de Barras - {column_name}', fontsize=15)
        plt.xlabel('Categorías', fontsize=12)
        plt.ylabel('Frecuencia', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        return fig
    return None


def generate_horizontal_bar_chart(data, variable_type, column_name):
    """
    Genera un gráfico de barras horizontales.
    
    Args:
        data (pd.Series): Datos a graficar
        variable_type (str): Tipo de variable
        column_name (str): Nombre de la columna
        
    Returns:
        matplotlib.figure.Figure: Figura del gráfico
    """
    if variable_type in ["Cualitativa", "Cuantitativa Discreta"]:
        fig, ax = plt.subplots(figsize=(12, max(6, min(20, len(data.value_counts())//2))))
        value_counts = data.value_counts().sort_values()
        
        if len(value_counts) > 20:
            value_counts = value_counts.tail(20)
        
        sns.barplot(y=value_counts.index, x=value_counts.values, ax=ax, hue=value_counts.index, palette='viridis', orient='h', legend=False)
        plt.title(f'Gráfico de Barras Horizontales - {column_name}', fontsize=15)
        plt.ylabel('Categorías', fontsize=12)
        plt.xlabel('Frecuencia', fontsize=12)
        plt.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        return fig
    return None


def generate_boxplot(data, variable_type, column_name):
    """
    Genera un diagrama de caja (boxplot).
    
    Args:
        data (pd.Series): Datos a graficar
        variable_type (str): Tipo de variable
        column_name (str): Nombre de la columna
        
    Returns:
        matplotlib.figure.Figure: Figura del boxplot
    """
    if variable_type in ["Cuantitativa Continua", "Cuantitativa Discreta", "Cuantitativa Discreta con Intervalos"]:
        fig, ax = plt.subplots(figsize=VISUALIZATION_CONFIG['figure_size'])
        sns.boxplot(x=data, ax=ax, color='steelblue')
        plt.title(f'Diagrama de Caja - {column_name}', fontsize=15)
        plt.grid(axis='x', alpha=0.3)
        return fig
    return None


def generate_violinplot(data, variable_type, column_name):
    """
    Genera un diagrama de violín.
    
    Args:
        data (pd.Series): Datos a graficar
        variable_type (str): Tipo de variable
        column_name (str): Nombre de la columna
        
    Returns:
        matplotlib.figure.Figure: Figura del violin plot
    """
    if variable_type in ["Cuantitativa Continua", "Cuantitativa Discreta", "Cuantitativa Discreta con Intervalos"]:
        fig, ax = plt.subplots(figsize=VISUALIZATION_CONFIG['figure_size'])
        sns.violinplot(x=data, ax=ax, color='steelblue', inner='quartile')
        plt.title(f'Diagrama de Violín - {column_name}', fontsize=15)
        plt.grid(axis='x', alpha=0.3)
        return fig
    return None


def save_plot_for_pdf(fig, filename):
    """
    Guarda un gráfico en formato adecuado para PDF.
    
    Args:
        fig (matplotlib.figure.Figure): Figura a guardar
        filename (str): Nombre del archivo
        
    Returns:
        io.BytesIO: Buffer con la imagen
    """
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=VISUALIZATION_CONFIG['dpi'], bbox_inches='tight')
    buf.seek(0)
    return buf


# ============= NUEVAS VISUALIZACIONES =============

def generate_correlation_heatmap(corr_matrix):
    """
    Genera un mapa de calor de correlaciones.
    
    Args:
        corr_matrix (pd.DataFrame): Matriz de correlación
        
    Returns:
        matplotlib.figure.Figure: Figura del heatmap
    """
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(
        corr_matrix, 
        annot=True, 
        fmt='.2f', 
        cmap='coolwarm', 
        center=0,
        square=True,
        linewidths=1,
        cbar_kws={"shrink": 0.8},
        ax=ax
    )
    plt.title('Matriz de Correlación', fontsize=16, pad=20)
    plt.tight_layout()
    return fig


def generate_interactive_correlation_heatmap(corr_matrix):
    """
    Genera un mapa de calor interactivo con Plotly.
    
    Args:
        corr_matrix (pd.DataFrame): Matriz de correlación
        
    Returns:
        plotly.graph_objects.Figure: Figura interactiva
    """
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr_matrix.values,
        texttemplate='%{text:.2f}',
        textfont={"size": 10},
        colorbar=dict(title="Correlación")
    ))
    
    fig.update_layout(
        title='Matriz de Correlación Interactiva',
        xaxis_title='Variables',
        yaxis_title='Variables',
        template='plotly_white',
        height=600,
        width=800
    )
    
    return fig


def generate_scatter_plot(df, x_col, y_col):
    """
    Genera un gráfico de dispersión.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        x_col (str): Columna para eje X
        y_col (str): Columna para eje Y
        
    Returns:
        matplotlib.figure.Figure: Figura del scatter plot
    """
    fig, ax = plt.subplots(figsize=VISUALIZATION_CONFIG['figure_size'])
    
    ax.scatter(df[x_col], df[y_col], alpha=0.6, s=50, color='steelblue')
    
    # Agregar línea de tendencia
    z = np.polyfit(df[x_col].dropna(), df[y_col].dropna(), 1)
    p = np.poly1d(z)
    ax.plot(df[x_col], p(df[x_col]), "r--", alpha=0.8, linewidth=2, label='Tendencia')
    
    plt.xlabel(x_col, fontsize=12)
    plt.ylabel(y_col, fontsize=12)
    plt.title(f'Dispersión: {x_col} vs {y_col}', fontsize=15)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    return fig


def generate_interactive_scatter(df, x_col, y_col):
    """
    Genera un gráfico de dispersión interactivo.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        x_col (str): Columna para eje X
        y_col (str): Columna para eje Y
        
    Returns:
        plotly.graph_objects.Figure: Figura interactiva
    """
    fig = px.scatter(
        df, 
        x=x_col, 
        y=y_col,
        trendline="ols",
        title=f'Dispersión Interactiva: {x_col} vs {y_col}',
        labels={x_col: x_col, y_col: y_col},
        opacity=0.7
    )
    
    fig.update_traces(marker=dict(size=8, color='steelblue'))
    fig.update_layout(template='plotly_white')
    
    return fig


def generate_qq_plot(data, column_name):
    """
    Genera un gráfico Q-Q para verificar normalidad.
    
    Args:
        data (pd.Series): Datos a graficar
        column_name (str): Nombre de la columna
        
    Returns:
        matplotlib.figure.Figure: Figura del Q-Q plot
    """
    from scipy import stats
    
    fig, ax = plt.subplots(figsize=VISUALIZATION_CONFIG['figure_size'])
    stats.probplot(data.dropna(), dist="norm", plot=ax)
    plt.title(f'Gráfico Q-Q - {column_name}', fontsize=15)
    plt.xlabel('Cuantiles Teóricos', fontsize=12)
    plt.ylabel('Cuantiles Muestrales', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    return fig


def generate_outliers_plot(data, outliers_info, column_name):
    """
    Genera un gráfico mostrando los outliers detectados.
    
    Args:
        data (pd.Series): Datos originales
        outliers_info (dict): Información de outliers
        column_name (str): Nombre de la columna
        
    Returns:
        matplotlib.figure.Figure: Figura con outliers resaltados
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Boxplot con outliers
    ax1.boxplot(data.dropna(), vert=True)
    ax1.axhline(y=outliers_info['Límite Superior'], color='r', linestyle='--', label='Límite Superior')
    ax1.axhline(y=outliers_info['Límite Inferior'], color='r', linestyle='--', label='Límite Inferior')
    ax1.set_ylabel('Valores', fontsize=12)
    ax1.set_title(f'Boxplot con Límites - {column_name}', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Scatter plot de índices vs valores
    indices = range(len(data))
    colors = ['red' if x in outliers_info['Valores Atípicos'] else 'blue' for x in data]
    ax2.scatter(indices, data, c=colors, alpha=0.6, s=30)
    ax2.axhline(y=outliers_info['Límite Superior'], color='r', linestyle='--', label='Límite Superior')
    ax2.axhline(y=outliers_info['Límite Inferior'], color='r', linestyle='--', label='Límite Inferior')
    ax2.set_xlabel('Índice', fontsize=12)
    ax2.set_ylabel('Valores', fontsize=12)
    ax2.set_title(f'Valores Atípicos - {column_name}', fontsize=14)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def generate_distribution_comparison(data, column_name):
    """
    Genera una comparación de la distribución con la normal.
    
    Args:
        data (pd.Series): Datos a comparar
        column_name (str): Nombre de la columna
        
    Returns:
        matplotlib.figure.Figure: Figura comparativa
    """
    fig, ax = plt.subplots(figsize=VISUALIZATION_CONFIG['figure_size'])
    
    # Histograma de datos
    ax.hist(data.dropna(), bins='auto', density=True, alpha=0.7, color='steelblue', label='Datos')
    
    # Curva normal teórica
    mu, sigma = data.mean(), data.std()
    x = np.linspace(data.min(), data.max(), 100)
    ax.plot(x, (1/(sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5*((x - mu)/sigma)**2), 
            'r-', linewidth=2, label='Distribución Normal')
    
    plt.xlabel('Valores', fontsize=12)
    plt.ylabel('Densidad', fontsize=12)
    plt.title(f'Comparación con Distribución Normal - {column_name}', fontsize=15)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    return fig
