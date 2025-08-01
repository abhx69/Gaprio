import whisper

model = whisper.load_model("base")  # or "small" for faster processing

def transcribe_audio(file_path: str) -> str:
    result = model.transcribe(file_path)
    return result.get("text", "")
