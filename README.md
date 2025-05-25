# Testing

This repository contains a Streamlit application for recording both microphone
and system audio. It provides **Start** and **Stop** buttons to control
recording and shows playback controls once recording has completed.

## Running the app

1. Install the required packages:
    ```bash
    pip install streamlit sounddevice soundfile
    ```
2. Run the app:
    ```bash
    streamlit run streamlit_app.py
    ```

The system audio recording relies on WASAPI loopback and therefore works best
on Windows. On other platforms you may need additional configuration or virtual
audio devices for capturing system audio.
