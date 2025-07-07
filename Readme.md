# OS dependencies (manual step)
sudo apt update && sudo apt install ffmpeg

# Python dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
