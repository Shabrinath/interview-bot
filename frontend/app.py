import streamlit as st
import requests
import openai
import tempfile
import os
import soundfile as sf
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode

API_URL = "http://localhost:8000"

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🎤 AI Interview Bot (Voice Enabled)")

# Sidebar configs
role = st.sidebar.selectbox("Role", ["DevOps Engineer", "Cloud Engineer", "SRE", "AI Engineer", "Senior Engineer"])
difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
topic = st.sidebar.text_input("Topic (e.g., Kubernetes, Terraform, AI)", "Kubernetes")
tone = st.sidebar.selectbox("Interviewer Tone", ["Serious", "Friendly", "Neutral"])

# Session vars
if "question" not in st.session_state:
    st.session_state["question"] = None

# Start Interview
if st.button("Start Interview"):
    res = requests.post(f"{API_URL}/start", json={
        "role": role,
        "difficulty": difficulty,
        "topic": topic,
        "tone": tone
    })
    st.session_state["question"] = res.json()["question"]
    st.write(f"**Interviewer:** {st.session_state['question']}")

# Mic recording
class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.recorded_frames = []

    def recv_audio_frame(self, frame):
        self.recorded_frames.append(frame.to_ndarray().flatten())
        return frame

webrtc_ctx = webrtc_streamer(
    key="speech",
    mode=WebRtcMode.SENDONLY,
    audio_receiver_size=256,
    media_stream_constraints={"audio": True, "video": False},
    async_processing=True,
    audio_processor_factory=AudioProcessor,
)

if st.session_state.get("question") and webrtc_ctx.state.playing:
    if st.button("Submit Voice Answer"):
        # Save recorded audio to temp WAV file
        audio_frames = webrtc_ctx.audio_receiver.get_frames()
        if not audio_frames:
            st.warning("No audio captured yet.")
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
                audio_data = b"".join([f.to_ndarray().tobytes() for f in audio_frames])
                tmpfile.write(audio_data)
                tmpfile_path = tmpfile.name

            # Transcribe with OpenAI Whisper
            with open(tmpfile_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            user_answer = transcript.text
            st.write(f"**You said:** {user_answer}")

            # Send answer to backend
            res = requests.post(f"{API_URL}/answer", json={
                "question": st.session_state["question"],
                "answer": user_answer,
                "role": role,
                "difficulty": difficulty,
                "topic": topic,
                "tone": tone
            })
            feedback = res.json()["feedback"]
            st.write(f"**Feedback:** {feedback}")

            # Convert feedback to speech (OpenAI TTS)
            speech_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            response = client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=feedback
            )
            response.stream_to_file(speech_file.name)

            st.audio(speech_file.name, format="audio/mp3")
