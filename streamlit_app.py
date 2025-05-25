import queue
import numpy as np
import sounddevice as sd
import soundfile as sf
import streamlit as st


st.title("Audio Recorder")

# Initialize session state
if "recording" not in st.session_state:
    st.session_state.recording = False
if "mic_queue" not in st.session_state:
    st.session_state.mic_queue = queue.Queue()
if "sys_queue" not in st.session_state:
    st.session_state.sys_queue = queue.Queue()
if "mic_stream" not in st.session_state:
    st.session_state.mic_stream = None
if "sys_stream" not in st.session_state:
    st.session_state.sys_stream = None

SAMPLE_RATE = 44100
CHANNELS = 2


def _mic_callback(indata, frames, time, status):
    """Collect microphone frames."""
    st.session_state.mic_queue.put(indata.copy())


def _sys_callback(indata, frames, time, status):
    """Collect system audio frames."""
    st.session_state.sys_queue.put(indata.copy())


def start_recording():
    """Start microphone and system audio streams."""
    st.session_state.mic_queue = queue.Queue()
    st.session_state.sys_queue = queue.Queue()

    st.session_state.mic_stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        callback=_mic_callback,
    )

    output_dev = sd.query_devices(kind="output")
    st.session_state.sys_stream = sd.InputStream(
        device=output_dev["index"],
        samplerate=int(output_dev["default_samplerate"]),
        channels=CHANNELS,
        callback=_sys_callback,
        extra_settings=sd.WasapiSettings(loopback=True),
    )

    st.session_state.mic_stream.start()
    st.session_state.sys_stream.start()
    st.session_state.recording = True


def stop_recording():
    """Stop streams and save recordings to WAV files."""
    st.session_state.mic_stream.stop()
    st.session_state.sys_stream.stop()
    st.session_state.recording = False

    mic_frames = list(st.session_state.mic_queue.queue)
    sys_frames = list(st.session_state.sys_queue.queue)

    mic_audio = np.concatenate(mic_frames) if mic_frames else np.empty((0, CHANNELS))
    sys_audio = np.concatenate(sys_frames) if sys_frames else np.empty((0, CHANNELS))

    mic_file = "microphone.wav"
    sys_file = "system.wav"

    if mic_audio.size:
        sf.write(mic_file, mic_audio, SAMPLE_RATE)
    if sys_audio.size:
        sf.write(sys_file, sys_audio, SAMPLE_RATE)

    return mic_file, sys_file


col1, col2 = st.columns(2)

with col1:
    if not st.session_state.recording:
        if st.button("Start"):
            start_recording()
    else:
        if st.button("Stop"):
            mic_path, sys_path = stop_recording()
            if mic_path:
                st.audio(mic_path)
            if sys_path:
                st.audio(sys_path)

