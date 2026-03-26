# Telegram GenAI Bot using Local LLM (Qwen3-1.7B GGUF + llama.cpp)

## Overview

This project implements a Telegram chatbot powered by a fully local Generative AI Large Language Model using Retrieval Augmented Generation (RAG).

The system integrates:

• Local LLM inference using Qwen3-1.7B GGUF via llama.cpp  
• Retrieval Augmented Generation using FAISS and SentenceTransformers  
• Image captioning using BLIP model  
• Telegram bot interface  
• Local chat memory using SQLite database  

The complete pipeline runs locally after downloading the required models.

---

## Project Structure

telegram-genai-bot/

app.py  
Main Telegram bot logic  

rag.py  
Retrieval Augmented Generation pipeline using FAISS + LLM  

vision.py  
Image captioning using BLIP model  

docs.txt  
Knowledge base used for retrieval  

chat.db  
SQLite database automatically created to store chat history  

embeddings.pkl  
Vector embeddings generated automatically  

README.md  

.gitignore  

---

## System Requirements

Operating System:
Windows 10 or Windows 11

Software:
Python 3.10 or higher
Git
Visual Studio Build Tools (C++)

Hardware:
Minimum 8GB RAM recommended

---

# Step 1 — Install Visual Studio C++ Build Tools (Windows)

llama.cpp requires a C++ compiler to build dependencies.

Download Visual Studio Build Tools:
https://visualstudio.microsoft.com/visual-cpp-build-tools/

Run installer and select:

Workload:
Desktop development with C++

Required components:

MSVC v143 VS 2022 C++ x64/x86 build tools  
Windows 10 SDK or Windows 11 SDK  
C++ CMake tools for Windows  

After installation restart the system.

---

# Step 2 — Install llama.cpp Python binding

Install llama-cpp-python:

pip install llama-cpp-python

Optional GPU acceleration:

pip install llama-cpp-python --config-settings=cmake.args="-DLLAMA_CUBLAS=on"

Official llama.cpp documentation:
https://qwen.readthedocs.io/en/latest/run_locally/llama.cpp.html

---

# Step 3 — Download Qwen3 GGUF model

Model repository:
https://huggingface.co/Qwen/Qwen3-1.7B-GGUF

Download recommended file:

Qwen3-1.7b.Q4_K_M.gguf

Create folder:

D:\Gen-AI\qwen\

Place model file:

D:\Gen-AI\qwen\qwen3-1.7b.Q4_K_M.gguf

Update model path inside rag.py if needed:

llm = Llama(
    model_path=r"D:\Gen-AI\qwen\qwen3-1.7b.Q4_K_M.gguf",
    n_ctx=2048,
    n_threads=6
)

---

# Step 4 — Install Python dependencies

Install dependencies:

pip install -r requirements.txt

---

# Step 5 — Create Telegram Bot using BotFather

Open Telegram application

Search for:
BotFather

Start BotFather:

/start

Create a new bot:

/newbot

Provide:

Bot name:
ExampleGenAIBot

Bot username:
example_genai_bot

BotFather will generate a token similar to:

123456789:ABCDEF...

Copy token and paste inside app.py:

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

---

# Step 6 — Add knowledge documents

Create file:

docs.txt

Example content:

Artificial Intelligence is the simulation of human intelligence processes by machines.

Machine Learning is a subset of AI focused on learning patterns from data.

Each line acts as one knowledge document.

---

# Step 7 — Run the bot

Start the bot:

python app.py

Expected output:

LLM loaded successfully
Loading embedding model...
Bot is running...

---

# Telegram Commands

/start

Initialize bot

/ask your question

Example:

/ask What is artificial intelligence?

/image

Upload image to receive caption and tags

/help

Show available commands

---

# Retrieval Augmented Generation Details

Embedding model:
all-MiniLM-L6-v2

Vector search:
FAISS IndexFlatIP

Language model:
Qwen3-1.7B GGUF

Inference backend:
llama.cpp via llama-cpp-python

---

# Database

Chat history stored locally in:

chat.db

Table structure:

id
user_id
user_message
bot_response
timestamp

---

# Notes

First run automatically creates:

embeddings.pkl
chat.db

These files are reused in future runs.

---

# Security Notes

Do not upload:

Telegram bot token
Local GGUF model files
Private datasets

Use .gitignore to exclude large files.

---

# Future Improvements

Streaming token generation
GPU acceleration optimization
Larger document retrieval dataset
Web interface deployment
Docker containerization
Multi-user session memory

---

# References

Qwen GGUF model:
https://huggingface.co/Qwen/Qwen3-1.7B-GGUF

llama.cpp usage guide:
https://qwen.readthedocs.io/en/latest/run_locally/llama.cpp.html

---

# License

For research and educational use.