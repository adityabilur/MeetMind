# 🧠 MeetMind — AI Audio & Video Intelligence Assistant

MeetMind is a RAG-based AI assistant that converts meeting recordings and YouTube videos into searchable, intelligent insights.

Users can upload an audio/video file or provide a YouTube URL. MeetMind transcribes the content using Whisper, analyzes it using Gemini, stores transcript chunks as embeddings in ChromaDB, and uses Retrieval-Augmented Generation (RAG) to answer questions based on the recorded content.

## ✨ Features

- 🎥 Upload MP4, MP3, and WAV files
- 🔗 Process YouTube videos using a YouTube URL
- 🎙️ Automatic speech-to-text transcription using Whisper
- ⏱️ Timestamped transcripts
- 🤖 AI-powered meeting/content analysis using Gemini
- 📝 Automatic summaries and key discussion points
- 🎯 Action items and decisions extraction
- 🔎 Semantic search using embeddings
- 🗄️ ChromaDB vector database
- 💬 Conversational RAG-based question answering
- 📄 PDF report generation
- 🖥️ Interactive Streamlit web interface

## 🧩 How MeetMind Works

```text
YouTube URL / Audio / Video
            ↓
      Audio Processing
            ↓
          Whisper
            ↓
   Timestamped Transcript
            ↓
         Chunking
            ↓
       Embeddings
            ↓
        ChromaDB
            ↓
      Similarity Search
            ↓
       Relevant Chunks
            ↓
          Gemini
            ↓
       AI Response