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

echo "🧠 Setting up NLTK data..."
export NLTK_DATA="$(pwd)/nltk_data"
mkdir -p "$NLTK_DATA"
python -c "import nltk; nltk.data.path.append('$NLTK_DATA'); nltk.download('punkt')"

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

# Check for Vosk model
echo "🔎 Checking for Vosk model..."
if [ ! -d "vosk-model-small-en-us-0.15" ]; then
    echo "⚠️ Vosk model directory not found! Please download and place it inside the project folder."
else
    echo "✅ Vosk model found."
fi

echo "🎉 Installation complete! Run the program with: ./run.sh"
echo "To activate the virtual environment, run: source venv/bin/activate"
