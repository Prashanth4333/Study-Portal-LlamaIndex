# 🎓 Smart Portal

An **AI-powered college knowledge portal** built with **Streamlit**, **LlamaIndex**, and **Gemini API** that allows students, teachers, and staff to quickly find answers from uploaded PDFs, text files, and documents.

The system **indexes** various academic and administrative documents and allows users to **ask natural language questions** and get instant answers sourced from the provided materials.

---

## 🚀 Features

- **AI Question Answering** from uploaded documents (PDF, TXT, etc.)
- **Multi-folder document categorization** (notes, syllabus, roadmaps, admissions, etc.)
- **Automatic document indexing** with LlamaIndex
- **Google Gemini LLM** for advanced reasoning & contextual answers
- **Chunk-based processing** for better accuracy on large documents
- **Automatic change detection** → Index rebuilds when files are updated
- **File size filtering** (skips files > 15 MB)
- **Persistent storage** for faster subsequent queries
- **Timeout handling** for large embeddings
- **Streamlit UI** for easy use

---

## 📂 Project Structure

smart-college-portal/
│
├── app.py # Main Streamlit app file
├── requirements.txt # Python dependencies
│
├── backend/
│ ├── init.py
│ ├── llama_index_setup.py # LlamaIndex loading & query logic
│ ├── config.py # API keys, constants
│ ├── utils.py # Helper functions (optional)
│
├── data/ # Main data folder
│ ├── roadmaps/ # PDF/Docs for career & skill roadmaps
│ ├── notes/ # Lecture notes, study material
│ ├── syllabus/ # Syllabus PDFs
│ ├── admissions/ # Admission process docs
│ ├── events/ # Event details (JSON/PDF)
│
├── storage/ # Vector index storage (auto-created by LlamaIndex)
│
└── assets/ # (Optional) Images, logo, icons for the website




<img width="541" height="409" alt="image" src="https://github.com/user-attachments/assets/5b90a8e1-0c28-4e10-9c3c-d78e84c6c9b9" />




---

## 🛠 Installation & Setup

### 1️⃣ Clone the repository
git clone https://github.com/Prashanth4333/Study-Portal-LlamaIndex.git
cd smart-college-portal

2️⃣ Create & activate a virtual environment

python -m venv venv
# On Windows

venv\Scripts\activate
# On Mac/Linux

source venv/bin/activate

3️⃣ Install dependencies

pip install -r requirements.txt

4️⃣ Set up environment variables

Create a .env file in the root directory:

GOOGLE_API_KEY=your_google_api_key_here

5️⃣ Prepare your data

Organize PDFs and other documents inside the data/ folder, following the subfolder structure.

6️⃣ Run the app

streamlit run app.py


##🧠 How It Works

File Monitoring – The app tracks changes in the data/ folder using a file snapshot.

Index Building – On first run or when files change, it:

Reads PDFs using PyMuPDFReader

Reads TXT/Markdown files directly

Splits large docs into smaller chunks

Creates embeddings via GeminiEmbedding

Saves index in storage/

Querying – When you ask a question, the index is searched, and relevant chunks are passed to the Gemini LLM for answer generation.

Results – Only the final, clean text is returned to the user.


##📦 Dependencies

Main libraries used:

streamlit – UI framework

python-dotenv – Environment variable management

llama-index – Document indexing & retrieval

google-generativeai – Gemini API client

PyMuPDF (fitz) – PDF text extraction



