from fastapi import FastAPI, File, UploadFile
import fitz  # PyMuPDF
import openai
import os

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configurar CORS (permite hacer requests desde Hoppscotch o Postman sin errores de CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar OpenRouter como proveedor de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    # Leer el archivo PDF
    contents = await file.read()
    doc = fitz.open(stream=contents, filetype="pdf")

    # Extraer el texto
    text = ""
    for page in doc:
        text += page.get_text()

    # Limitar a 4000 tokens aprox (~16,000 caracteres)
    extracted_text = text[:16000]

    # Llamar al modelo de OpenRouter
    prompt = f"""
Sos un abogado especializado en contratos inmobiliarios en Argentina.
Tu tarea es revisar el siguiente contrato de alquiler y señalar si hay cláusulas poco claras, abusivas, ilegales, o si falta alguna cláusula importante.

Texto del contrato:
\"\"\"
{extracted_text}
\"\"\"

Devuelve un resumen claro, ordenado y fácil de entender.
"""

    response = openai.ChatCompletion.create(
        model="mistralai/mixtral-8x7b-instruct",
        messages=[
            {"role": "system", "content": "Sos un experto en contratos de alquiler en Argentina."},
            {"role": "user", "content": prompt}
        ]
    )

    ai_response = response.choices[0].message.content
    return {"result": ai_response}
