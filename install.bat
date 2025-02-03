@echo off

echo Checking for Python 3.10 installation...
where python3.10 >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python 3.10 is not installed. Please install Python 3.10.16 first.
    exit /b
)

:: Check for Git installation
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Git is not installed. Please install Git first.
    exit /b
)

:: Check if virtual environment exists
if exist venv (
    echo ✅ Virtual environment already exists. Skipping creation.
) else (
    echo 📂 Creating a virtual environment...
    python3.10 -m venv venv
)

call venv\Scripts\activate

echo 📦 Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo 🧠 Setting up NLTK data...
set NLTK_DATA=%cd%\nltk_data
if not exist "%NLTK_DATA%" mkdir "%NLTK_DATA%"
python -c "import nltk; nltk.data.path.append(r'%NLTK_DATA%'); nltk.download('punkt')"

:: Install meloTTS
set MELO_REPO=https://github.com/myshell-ai/meloTTS.git
set MELO_DIR=MeloTTS

if exist %MELO_DIR% (
    echo 🔄 Updating meloTTS repository...
    git -C %MELO_DIR% pull origin main
) else (
    echo 🌍 Cloning meloTTS repository...
    git clone %MELO_REPO%
)

echo 📦 Installing meloTTS dependencies...
pip install -r %MELO_DIR%\requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install meloTTS dependencies. Please check the error messages above.
    exit /b
)

echo 🔧 Installing meloTTS...
pip install -e %MELO_DIR%
if %errorlevel% neq 0 (
    echo ❌ Failed to install meloTTS. Please check the error messages above.
    exit /b
)

:: Download unidic
echo 📥 Downloading unidic...
python -m unidic download
if %errorlevel% neq 0 (
    echo ❌ Failed to download unidic. Please check the error messages above.
    exit /b
)

echo 🎉 Installation complete! Run the program with: run.bat
