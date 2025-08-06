from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, Response
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
import re
import nltk
from nltk.corpus import stopwords
from collections import Counter
from pydantic import BaseModel

# Descargar stopwords si no están disponibles
nltk.download('stopwords', quiet=True)

app = FastAPI(
    title="API de Análisis de Sentimientos",
    description="API para análisis de sentimientos y visualización de datos textuales",
    version="1.0.0"
)


# Modelos de solicitud
class TextRequest(BaseModel):
    texto: str


class TextsRequest(BaseModel):
    textos: list[str]


# Función para análisis de sentimiento
def analizar_sentimiento(texto: str) -> str:
    analisis = TextBlob(texto)
    polaridad = analisis.sentiment.polarity

    if polaridad > 0.1:
        return "positivo"
    elif polaridad < -0.1:
        return "negativo"
    else:
        return "neutral"


# Función para limpiar texto
def limpiar_texto(texto: str) -> str:
    texto = re.sub(r"http\S+|www\S+|https\S+", "", texto, flags=re.MULTILINE)
    texto = re.sub(r"\@\w+|\#", "", texto)
    texto = re.sub(r"[^\w\s]", "", texto)
    texto = texto.lower()

    # Detectar idioma para stopwords
    try:
        lang = 'spanish' if TextBlob(texto).detect_language() == 'es' else 'english'
    except:
        lang = 'english'  # Default si no puede detectar

    stop_words = set(stopwords.words(lang))
    palabras = texto.split()
    palabras = [palabra for palabra in palabras if palabra not in stop_words and len(palabra) > 2]
    return " ".join(palabras)


# Función para generar imágenes
def generar_imagen():
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return Response(content=buf.read(), media_type="image/png")


@app.post("/analisis_sentimiento")
async def analisis_sentimiento_endpoint(request: TextRequest):
    try:
        texto = request.texto
        if not texto.strip():
            raise HTTPException(status_code=400, detail="Texto no proporcionado")

        sentimiento = analizar_sentimiento(texto)
        polaridad = TextBlob(texto).sentiment.polarity

        return JSONResponse(content={
            "texto": texto,
            "sentimiento": sentimiento,
            "polaridad": polaridad
        })
    except Exception as e:
        return JSONResponse(
            content={"error": f"Error al analizar sentimiento: {str(e)}"},
            status_code=500
        )


@app.post("/wordcloud")
async def generar_wordcloud(request: TextRequest):
    try:
        texto = request.texto
        if not texto.strip():
            raise HTTPException(status_code=400, detail="Texto no proporcionado")

        texto_limpio = limpiar_texto(texto)
        wordcloud = WordCloud(
            width=1200,
            height=600,
            background_color='white',
            max_words=200,
            colormap='viridis'
        ).generate(texto_limpio)

        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)

        return generar_imagen()
    except Exception as e:
        plt.close('all')
        return JSONResponse(
            content={"error": f"Error al generar wordcloud: {str(e)}"},
            status_code=500
        )


@app.post("/bar_plot")
async def generar_bar_plot(request: TextsRequest):
    try:
        textos = request.textos
        if not textos:
            raise HTTPException(status_code=400, detail="Lista de textos vacía")

        sentimientos = [analizar_sentimiento(texto) for texto in textos]
        conteo = Counter(sentimientos)

        # Ordenar categorías consistentemente
        categorias = ["positivo", "negativo", "neutral"]
        valores = [conteo.get(cat, 0) for cat in categorias]
        colores = ['#4CAF50', '#F44336', '#2196F3']  # Verde, Rojo, Azul

        plt.figure(figsize=(10, 6))
        bars = plt.bar(categorias, valores, color=colores)
        plt.title('Distribución de Sentimientos', fontsize=14)
        plt.xlabel('Sentimientos')
        plt.ylabel('Cantidad')

        # Añadir valores encima de las barras
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height,
                     f'{height}', ha='center', va='bottom')

        return generar_imagen()
    except Exception as e:
        plt.close('all')
        return JSONResponse(
            content={"error": f"Error al generar gráfico de barras: {str(e)}"},
            status_code=500
        )


@app.post("/pie_chart")
async def generar_pie_chart(request: TextsRequest):
    try:
        textos = request.textos
        if not textos:
            raise HTTPException(status_code=400, detail="Lista de textos vacía")

        sentimientos = [analizar_sentimiento(texto) for texto in textos]
        conteo = Counter(sentimientos)

        etiquetas = list(conteo.keys())
        valores = list(conteo.values())
        colores = ['#4CAF50', '#F44336', '#2196F3']  # Verde, Rojo, Azul

        plt.figure(figsize=(8, 8))
        plt.pie(valores, labels=etiquetas, colors=colores,
                autopct='%1.1f%%', startangle=90,
                textprops={'fontsize': 12})
        plt.axis('equal')
        plt.title('Proporción de Sentimientos', fontsize=14)

        return generar_imagen()
    except Exception as e:
        plt.close('all')
        return JSONResponse(
            content={"error": f"Error al generar gráfico circular: {str(e)}"},
            status_code=500
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)