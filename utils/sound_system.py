"""
Emotion Sound System
"""
import streamlit as st
from pathlib import Path


def play_emotion_sound(emotion):
    """
    Play emotion-specific sound (if available)
    For production, you'd load actual audio files from assets/sounds/
    """
    sound_map = {
        "happy": "assets/sounds/happy.mp3",
        "sad": "assets/sounds/sad.mp3",
        "anger": "assets/sounds/anger.mp3",
        "fear": "assets/sounds/fear.mp3",
        "love": "assets/sounds/love.mp3",
        "neutral": "assets/sounds/neutral.mp3"
    }
    
    sound_file = Path(sound_map.get(emotion, ""))
    
    if sound_file.exists():
        try:
            st.audio(str(sound_file), format='audio/mp3', autoplay=True)
        except Exception as e:
            pass  # Silently fail if sound doesn't work
    else:
        # No sound file found - that's okay, feature is optional
        pass