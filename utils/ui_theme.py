"""
Dynamic UI themes that adapt to detected emotions
"""
import streamlit as st

# Emotion theme configurations
EMOTION_THEMES = {
    "happy": {
        "gradient": "linear-gradient(135deg, #f6d365 0%, #fda085 100%)",
        "primary_color": "#FFD700",
        "text_color": "#2C3E50",
        "card_bg": "rgba(255, 255, 255, 0.9)",
        "emoji": "😊",
        "message": "You're radiating positive energy!",
        "animation": "bounce",
        "description": "Bright and energizing"
    },
    "sad": {
        "gradient": "linear-gradient(135deg, #89CFF0 0%, #B0E0E6 100%)",
        "primary_color": "#5DADE2",
        "text_color": "#34495E",
        "card_bg": "rgba(255, 255, 255, 0.85)",
        "emoji": "🫂",
        "message": "It's okay to feel this way. I'm here with you.",
        "animation": "fade",
        "description": "Soft and supportive"
    },
    "anxious": {
        "gradient": "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)",
        "primary_color": "#85C1E9",
        "text_color": "#2C3E50",
        "card_bg": "rgba(255, 255, 255, 0.9)",
        "emoji": "🫁",
        "message": "Let's ground ourselves together.",
        "animation": "breathe",
        "description": "Calming and grounding"
    },
    "angry": {
        "gradient": "linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%)",
        "primary_color": "#AE8FBF",
        "text_color": "#2C3E50",
        "card_bg": "rgba(255, 255, 255, 0.9)",
        "emoji": "🧘",
        "message": "Take a moment. This feeling will pass.",
        "animation": "pulse-slow",
        "description": "Cooling and spacious"
    },
    "neutral": {
        "gradient": "linear-gradient(135deg, #e0e0e0 0%, #c9d6df 100%)",
        "primary_color": "#95A5A6",
        "text_color": "#2C3E50",
        "card_bg": "rgba(255, 255, 255, 0.95)",
        "emoji": "😌",
        "message": "You're in a balanced state.",
        "animation": "none",
        "description": "Clean and balanced"
    }
}

def apply_emotion_theme(emotion):
    """Apply dynamic CSS theme based on detected emotion"""
    theme = EMOTION_THEMES.get(emotion.lower(), EMOTION_THEMES["neutral"])
    
    css = f"""
    <style>
    /* Main app background with smooth transition */
    .stApp {{
        background: {theme['gradient']} !important;
        transition: background 2s ease-in-out;
    }}
    
    /* Emotion display card */
    .emotion-card {{
        background: {theme['card_bg']};
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin: 20px auto;
        max-width: 600px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        backdrop-filter: blur(10px);
        animation: {theme['animation']} 2s ease-in-out;
    }}
    
    .emotion-emoji {{
        font-size: 80px;
        animation: {theme['animation']} 2s ease-in-out infinite;
        display: block;
        margin: 0 auto 20px;
    }}
    
    .emotion-message {{
        color: {theme['text_color']};
        font-size: 24px;
        font-weight: 600;
        margin: 20px 0;
    }}
    
    .emotion-description {{
        color: {theme['text_color']};
        font-size: 14px;
        opacity: 0.8;
    }}
    
    /* Button styling */
    .stButton>button {{
        background: {theme['primary_color']} !important;
        color: white !important;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }}
    
    /* Progress bar */
    .stProgress > div > div {{
        background-color: {theme['primary_color']} !important;
    }}
    
    /* Animations */
    @keyframes bounce {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-10px); }}
    }}
    
    @keyframes fade {{
        0%, 100% {{ opacity: 0.8; }}
        50% {{ opacity: 1; }}
    }}
    
    @keyframes breathe {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
    }}
    
    @keyframes pulse-slow {{
        0%, 100% {{ transform: scale(1); opacity: 0.9; }}
        50% {{ transform: scale(1.02); opacity: 1; }}
    }}
    
    /* Smooth transitions for all elements */
    .element-container {{
        transition: all 0.5s ease;
    }}
    
    /* Info boxes */
    .stAlert {{
        background-color: {theme['card_bg']};
        border-left: 4px solid {theme['primary_color']};
        border-radius: 10px;
    }}
    
    /* Metrics */
    [data-testid="stMetricValue"] {{
        color: {theme['primary_color']} !important;
    }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)
    
    # Display emotion card
    st.markdown(f"""
    <div class="emotion-card">
        <span class="emotion-emoji">{theme['emoji']}</span>
        <div class="emotion-message">{theme['message']}</div>
        <div class="emotion-description">{theme['description']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    return theme