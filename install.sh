#!/bin/bash

echo "Checking for Python 3.10 installation..."
if ! command -v python3.10 &>/dev/null; then
    echo "❌ Python 3.10 not found! Please install Python 3.10.16 first."
    exit 1
fi

# Check if venv already exists
if [ ! -d "venv" ]; then
    echo "📂 Creating a virtual environment..."
    python3.10 -m venv venv
else
    echo "✅ Virtual environment already exists. Skipping creation."
fi

source venv/bin/activate

echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Download the Vosk model
echo "Fetching vosk model..."
cd /Users/jacktoth-egeto/Downloads && { 
  curl -L -o vosk-model-small-en-us-0.15_c_.zip https://huggingface.co/ambind/vosk-model-small-en-us-0.15/resolve/main/vosk-model-small-en-us-0.15_c_.zip 
  if [ $? -eq 0 ]; then
    echo "Download successful."
    unzip vosk-model-small-en-us-0.15_c_.zip
    rm vosk-model-small-en-us-0.15_c_.zip
  else
    echo "Download failed."
  fi
}

# Download NLTK
echo "📥 Checking for existing NLTK data..."
if [ ! -d "$NLTK_DATA" ]; then
    echo "📥 Downloading NLTK data..."
    python -c "import nltk; nltk.download('punkt', download_dir='$NLTK_DATA')"
else
    echo "✅ NLTK data already exists. Skipping download."
fi

# Install meloTTS
MELO_REPO="https://github.com/myshell-ai/meloTTS.git"
MELO_DIR="MeloTTS"

if [ ! -d "$MELO_DIR" ]; then
    echo "🌍 Cloning meloTTS repository..."
    git clone "$MELO_REPO"
else
    echo "🔄 Updating meloTTS repository..."
    git -C "$MELO_DIR" pull origin main
fi

echo "📦 Installing meloTTS dependencies..."
pip install -r "$MELO_DIR/requirements.txt"
if [ $? -ne 0 ]; then
    echo "❌ Failed to install meloTTS dependencies. Please check the error messages above."
    exit 1
fi

echo "🔧 Installing meloTTS..."
pip install -e "$MELO_DIR"
if [ $? -ne 0 ]; then
    echo "❌ Failed to install meloTTS. Please check the error messages above."
    exit 1
fi

# Download unidic
echo "📥 Downloading unidic..."
python -m unidic download
if [ $? -ne 0 ]; then
    echo "❌ Failed to download unidic. Please check the error messages above."
    exit 1
fi

echo "🎉 Installation complete! Run the program with: ./run.sh"
echo "To activate the virtual environment, run: source venv/bin/activate"
