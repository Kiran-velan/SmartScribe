import whisper
import tempfile
import yt_dlp
import os

# Load Whisper model once at startup
model = whisper.load_model("base")  # You can use "tiny", "medium", "large" as needed


def transcribe_file(file_bytes: bytes, filename: str) -> str:
    """
    Save uploaded file temporarily and transcribe using Whisper.
    """
    ext = os.path.splitext(filename)[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        result = model.transcribe(tmp_path)
        return result["text"]
    finally:
        os.remove(tmp_path)


def transcribe_youtube(youtube_url: str) -> str:
    """
    Download best audio from YouTube and transcribe using Whisper.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "audio.%(ext)s")
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": output_path,
            "quiet": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            # FFmpeg postprocessor converts to .mp3
            downloaded_audio_path = os.path.join(tmpdir, "audio.mp3")

            if not os.path.exists(downloaded_audio_path):
                raise FileNotFoundError("Audio download failed or file missing")

        result = model.transcribe(downloaded_audio_path)
        return result["text"]
