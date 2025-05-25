# Testing

This repository now contains a Streamlit application that records both microphone and system audio.

## Running the app

1. Install the required packages:
   ```bash
   pip install streamlit sounddevice soundcard soundfile numpy
   ```
2. Run the app:
   ```bash
   streamlit run streamlit_app.py
   ```

When the page loads, click **Start** to begin recording from your microphone and system audio. Click **Stop** to finish and the recorded audio files will appear with playback controls.
