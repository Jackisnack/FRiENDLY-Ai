# FRiENDLY-Ai

Welcome to FRiENDLY-Ai! A general-purpose chatbot.

## Table of Contents:

1. MacOS/Linux Installation
2. Windows Installation
3. Usage
4. Credits
5. License

## MacOS/Linux Install:

1. Open a terminal.
2. Run the following commands:
   chmod +x install.sh run.sh  # Make them executable
   ./install.sh  # Install dependencies
   ./run.sh  # Run the app

## Windows Install:

IMPORTANT: Due to compatability issues with MeloTTS, I
recommend, in case of install failure, to run MeloTTS
via Docker.

1. Open Command Prompt or PowerShell.
2. Run the following commands:
   ```bash
   chmod +x install.bat run.bat # Make them executable (if necessary)
   ./install.bat # Install dependencies
   ./run.bat # Run the app
   ```

## Usage:

This chatbot can be used like any LLM (Large Language 
Model), however, since it runs completely locally 
(meaning you don't need an internet connection), it can 
be slow, depending on your system specifications.

The program itself has the following features:

1. Choose a username and an AI-name
2. TTS - The program will read outloud the AI's response
3. Remembering and storing conversations. This is done
   by storing each conversation in a json file called
   chat_history.json.
4. Voice Recognition - The program will listen to your
   voice and respond accordingly.

## Credits:

This application was made by Jack W. Tóth-Égetö. Pay
credit where credit is due:

- [Vosk](https://alphacephei.com/vosk/)
- [LangChain](https://python.langchain.com/)
- [melotts](https://github.com/myshell-ai/MeloTTS)
- [nltk](https://www.nltk.org/)

## License:

This project is open-source and is under the MIT-
license (see "LICENSE").