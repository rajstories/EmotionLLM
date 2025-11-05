"""
Utils package for Mental Health Companion
"""
from .emotion_helpers import EmotionDetector, EmotionLogger
from .cbt_dictionary import get_reframe, get_affirmation
from .ui_theme import apply_emotion_theme, EMOTION_THEMES
from .sound_system import play_emotion_sound

__all__ = [
    'EmotionDetector',
    'EmotionLogger',
    'get_reframe',
    'get_affirmation',
    'apply_emotion_theme',
    'EMOTION_THEMES',
    'play_emotion_sound'
]