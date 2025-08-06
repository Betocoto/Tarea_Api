# Tarea_Api




### README para API de Análisis de Sentimientos (`sentiment_api.py`)

```markdown
# API de Análisis de Sentimientos

API para análisis de sentimientos textuales y generación de visualizaciones.

## Características principales
- Análisis de polaridad de textos
- Generación de nubes de palabras
- Gráficos de distribución de sentimientos
- Manejo de múltiples idiomas (español/inglés)

## Endpoints disponibles

### `POST /analisis_sentimiento`
Analiza el sentimiento de un texto:
- Clasificación: positivo, negativo, neutral
- Valor numérico de polaridad

### `POST /wordcloud`
Genera una nube de palabras a partir de un texto:
- Eliminación de stopwords
- Procesamiento multilingüe
- Imagen PNG de alta calidad

### `POST /bar_plot`
Crea gráfico de barras con distribución de sentimientos:
- Conteo por categoría
- Etiquetas de valores
- Colores representativos

### `POST /pie_chart`
Genera gráfico circular con proporción de sentimientos:
- Porcentajes exactos
- Colores temáticos
- Visualización clara de proporciones

## Requerimientos
- Python 3.7+
- FastAPI
- TextBlob
- WordCloud
- Matplotlib
- NLTK

## Instalación y ejecución
```bash
pip install fastapi uvicorn textblob wordcloud matplotlib nltk
python -m textblob.download_corpora
uvicorn sentiment_api:app --reload



### README para Notebook de Pruebas (`Pruebas_API_Sentimientos.ipynb`)

```markdown
# Notebook de Pruebas para API de Sentimientos

Jupyter Notebook para probar los endpoints de la API de Análisis de Sentimientos.

## Requerimientos
- Jupyter Notebook
- Requests
- IPython
- API en ejecución

## Contenido del notebook
1. Configuración básica
2. Pruebas de análisis de sentimiento
3. Generación de nubes de palabras
4. Creación de gráficos de barras
5. Generación de gráficos circulares

## Instrucciones de uso
1. Ejecutar la API primero:
```bash
uvicorn sentiment_api:app --reload


