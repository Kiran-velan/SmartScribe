from summarizer import transcribe_file, transcribe_youtube
# run this file alone to test the transcription functionality inside venv and backend/app/

# Test YouTube
text = transcribe_youtube("https://www.youtube.com/watch?v=XYOZ4RzrHW0&list=PLGwmAEmjn4fkLREr7BTGHvmL1eJeQPn0O")
print("Transcript:", text[:500])

# Test file
with open("Monologue.ogg", "rb") as f:
    content = f.read()
    text = transcribe_file(content, "Monologue.ogg")
    print("Transcript:", text[:500])

# Download a audio or video file then place it in backend/app/ which is same as this file
# and run this script to test the transcription.
# For Youtube, you can use any public video URL.