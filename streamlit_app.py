import streamlit as st
import sounddevice as sd
import soundfile as sf
import soundcard as sc
import numpy as np
import threading
from pathlib import Path

MIC_FILE = "microphone.wav"
SYS_FILE = "system.wav"
SAMPLE_RATE = 44100
CHUNK_SIZE = 1024


def record_microphone(stop_event, frames):
    mic = sc.default_microphone()
    with mic.recorder(samplerate=SAMPLE_RATE) as recorder:
        while not stop_event.is_set():
            frames.append(recorder.record(numframes=CHUNK_SIZE))
    audio = np.concatenate(frames, axis=0)
    sf.write(MIC_FILE, audio, SAMPLE_RATE)


def record_system(stop_event, frames):
    speaker = sc.default_speaker()
    with speaker.recorder(samplerate=SAMPLE_RATE) as recorder:
        while not stop_event.is_set():
            frames.append(recorder.record(numframes=CHUNK_SIZE))
    audio = np.concatenate(frames, axis=0)
    sf.write(SYS_FILE, audio, SAMPLE_RATE)


st.title("Audio Recorder")

if "recording" not in st.session_state:
    st.session_state.recording = False
    st.session_state.mic_frames = []
    st.session_state.sys_frames = []
    st.session_state.stop_event = threading.Event()

col1, col2 = st.columns(2)

with col1:
    if st.button("Start") and not st.session_state.recording:
        st.session_state.stop_event.clear()
        st.session_state.mic_frames = []
        st.session_state.sys_frames = []
        mic_thread = threading.Thread(target=record_microphone, args=(st.session_state.stop_event, st.session_state.mic_frames))
        sys_thread = threading.Thread(target=record_system, args=(st.session_state.stop_event, st.session_state.sys_frames))
        mic_thread.start()
        sys_thread.start()
        st.session_state.threads = [mic_thread, sys_thread]
        st.session_state.recording = True

with col2:
    if st.button("Stop") and st.session_state.recording:
        st.session_state.stop_event.set()
        for t in st.session_state.threads:
            t.join()
        st.session_state.recording = False

if st.session_state.recording:
    st.success("Recording...")

if Path(MIC_FILE).exists():
    st.subheader("Microphone Recording")
    st.audio(MIC_FILE)
if Path(SYS_FILE).exists():
    st.subheader("System Audio Recording")
    st.audio(SYS_FILE)
