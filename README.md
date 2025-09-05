# AI Interview Bot

A voice-enabled AI interview bot built with FastAPI backend and Streamlit frontend.

## Issue Fixed

The application was failing with `APIRemovedInV1` error because it was using the old OpenAI API (`openai.ChatCompletion.create`). This has been updated to use the new OpenAI API v1.0+ with the `client.chat.completions.create` method.

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

4. Run the backend server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your OpenAI API key (same as backend):
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

4. Run the frontend:
   ```bash
   streamlit run app.py
   ```

## Changes Made

1. **Updated OpenAI API usage**: Replaced `openai.ChatCompletion.create` with `client.chat.completions.create`
2. **Fixed circular imports**: Separated FastAPI app code from interview logic
3. **Updated TTS API**: Changed from `openai.audio.speech.with_streaming_response.create` to `client.audio.speech.create`
4. **Added proper error handling**: Wrapped OpenAI API calls in try-catch blocks
5. **Created requirements.txt files**: Added proper dependency management for both frontend and backend

## API Endpoints

- `POST /start`: Start a new interview session
- `POST /answer`: Submit an answer and get feedback

## Features

- Voice recording and transcription using OpenAI Whisper
- AI-generated interview questions based on role, difficulty, topic, and tone
- Real-time feedback on answers
- Text-to-speech feedback using OpenAI TTS
- WebRTC-based audio recording
