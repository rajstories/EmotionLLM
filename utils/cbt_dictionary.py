"""
CBT (Cognitive Behavioral Therapy) reframes and affirmations
"""
import random

# CBT Reframing Dictionary
REFRAMES = {
    "anxious": [
        "🧠 Reframe: Anxiety is your brain trying to protect you. Thank it, then ask: am I in actual danger right now?",
        "💡 Perspective: This alertness shows you care. Channel this energy into preparation.",
        "🌱 Growth: You've felt anxious before and handled it. You have the strength to do it again.",
        "🎯 Action: What's one small thing you can control in this moment?"
    ],
    "sad": [
        "🫂 Validation: Sadness is data. What is it telling you that you need right now?",
        "⏳ Perspective: Feelings are like weather—temporary and always changing.",
        "💙 Self-compassion: You'd comfort a friend feeling this way. Can you offer yourself that kindness?",
        "🌈 Hope: This heaviness won't last forever, even when it feels like it will."
    ],
    "angry": [
        "🎯 Reframe: Anger shows something matters to you. What boundary was crossed?",
        "🧘 Pause: Before reacting, take 10 deep breaths. Anger isn't wrong, but how we express it matters.",
        "🔍 Curiosity: What's beneath this anger? Often it's protecting hurt or fear.",
        "💪 Power: You can feel angry AND choose how to respond. That's strength."
    ],
    "happy": [
        "📸 Savor: Notice what made this moment good. Your brain learns from joy.",
        "🔄 Multiply: Happiness grows when shared. Who can you tell about this?",
        "🌟 Gratitude: What are you grateful for in this moment?",
        "💛 Deserve: You deserve this happiness. Don't minimize it."
    ],
    "neutral": [
        "⚖️ Balance: Neutral isn't boring—it's peaceful. That's valuable.",
        "🧘 Grounded: You're present and stable. That's a gift.",
        "🌊 Flow: Not every moment needs to be intense. This calm is okay."
    ]
}

# Affirmations Dictionary
AFFIRMATIONS = {
    "anxious": [
        "I am safe in this moment.",
        "I can handle uncertainty.",
        "My anxiety doesn't define me.",
        "I breathe in calm, I breathe out tension.",
        "One step at a time is enough."
    ],
    "sad": [
        "This too shall pass.",
        "I deserve kindness—especially from myself.",
        "It's okay to not be okay right now.",
        "My feelings are valid and temporary.",
        "I am allowed to rest and heal."
    ],
    "angry": [
        "I can feel angry without losing control.",
        "I choose how to respond to this feeling.",
        "My anger is information, not a command.",
        "I have the power to pause.",
        "I am stronger than this moment."
    ],
    "happy": [
        "I deserve this joy.",
        "I'm grateful for this moment.",
        "Happiness is my natural state.",
        "I celebrate my wins, big and small.",
        "I choose to be present in this joy."
    ],
    "neutral": [
        "I am present and grounded.",
        "Balance is a strength.",
        "I'm exactly where I need to be.",
        "Calm is my superpower."
    ]
}

def get_reframe(emotion):
    """Get a random CBT reframe for the emotion"""
    emotion = emotion.lower()
    return random.choice(REFRAMES.get(emotion, REFRAMES["neutral"]))

def get_affirmation(emotion):
    """Get a random affirmation for the emotion"""
    emotion = emotion.lower()
    return random.choice(AFFIRMATIONS.get(emotion, AFFIRMATIONS["neutral"]))

def get_multiple_affirmations(emotion, count=3):
    """Get multiple affirmations"""
    emotion = emotion.lower()
    affirmations = AFFIRMATIONS.get(emotion, AFFIRMATIONS["neutral"])
    return random.sample(affirmations, min(count, len(affirmations)))