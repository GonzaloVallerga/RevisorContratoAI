from fastapi import FastAPI, File, UploadFile
import fitz  # PyMuPDF

app = FastAPI()

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    doc = fitz.open(stream=contents, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return {"extracted_text": text[:1000]}  # Devuelve primeros 1000 caracteres

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8000)

git add .
git commit -m "fix: remove wrong fitz package"
git push