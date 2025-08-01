# --- backend/main.py ---
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.whisper_utils import transcribe_audio
from app.ai_utils import generate_contract
from app.pdf_utils import save_contract_pdf
import shutil, os, logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Voice-to-Contract Generator")

# Allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure directories
os.makedirs("audio", exist_ok=True)
os.makedirs("contracts", exist_ok=True)

@app.post("/generate_contract/")
async def contract_from_audio(file: UploadFile = File(...)):
    logger.info(f"Received file: {file.filename}")
    file_path = f"audio/{file.filename}"

    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        logger.info(f"Saved file to {file_path}")
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        return {"error": "Failed to save uploaded file."}

    try:
        transcript = transcribe_audio(file_path)
        logger.info(f"Transcription successful: {transcript[:100]}...")
    except Exception as e:
        logger.error(f"Error in transcription: {e}")
        return {"error": "Transcription failed."}

    try:
        contract_text = generate_contract(transcript)
        logger.info(f"Generated contract: {contract_text[:100]}...")
    except Exception as e:
        logger.error(f"Error in contract generation: {e}")
        return {"error": "Contract generation failed."}

    try:
        pdf_path = save_contract_pdf(contract_text, filename="contract_from_audio.pdf")
        logger.info(f"PDF saved at {pdf_path}")
    except Exception as e:
        logger.error(f"Error saving PDF: {e}")
        return {"error": "Failed to save PDF."}

    return {
        "message": "Contract generated successfully.",
        "transcript": transcript,
        "contract_text": contract_text,
        "pdf_path": "contracts/contract_from_audio.pdf"
    }

app.mount("/contracts", StaticFiles(directory="contracts"), name="contracts")
