from fastapi import FastAPI, File, UploadFile
import fitz  # PyMuPDF
import openai
import os
from dotenv import load_dotenv

app = FastAPI()

# Cargamos la API Key desde variables de entorno
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    doc = fitz.open(stream=contents, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    # Llamamos a la API de OpenAI para analizar el texto
    prompt = f"""
    Este es un contrato de alquiler redactado en Argentina. Quiero que lo analices y me digas:
    1. Si hay cláusulas abusivas.
    2. Qué puntos legales faltan según la ley argentina.
    3. Si está bien redactado y es justo para el inquilino.
    Texto del contrato:
    {text[:4000]}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Sos un abogado experto en contratos de alquiler en Argentina."},
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "extracted_text": text[:1000],
        "contract_analysis": response['choices'][0]['message']['content']
    }
