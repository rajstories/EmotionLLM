"""
EmotionLLM - Enhanced Mental Health Companion (Fixed Dynamic Theme)
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path

# ==================== IMPORT FROM UTILS ====================
from utils import (
    EmotionDetector,
    EmotionLogger,
    get_reframe,
    get_affirmation,
    play_emotion_sound,
    EMOTION_THEMES  # Import the themes dictionary
)

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="EmotionLLM - Mental Health Companion",
    page_icon="💙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== SESSION STATE ====================
if 'current_emotion' not in st.session_state:
    st.session_state.current_emotion = None
if 'theme_applied' not in st.session_state:
    st.session_state.theme_applied = False

# ==================== INITIALIZE CORE CLASSES ====================
detector = EmotionDetector()
logger = EmotionLogger()

# ==================== DYNAMIC THEME FUNCTION ====================
def apply_dynamic_theme(emotion=None):
    """Apply theme that changes based on emotion"""
    
    # Default dark theme
    if emotion is None or emotion not in EMOTION_THEMES:
        gradient = "linear-gradient(135deg, #0F172A 0%, #1E293B 100%)"
        primary = "#3B82F6"
        emoji = "🧠"
        message = "Share your feelings"
    else:
        theme = EMOTION_THEMES[emotion]
        gradient = theme['gradient']
        primary = theme['primary']
        emoji = theme['emoji']
        message = theme['message']
    
    css = f"""
    <style>
    /* Main Background - Changes with emotion */
    .stApp {{
        background: {gradient} !important;
        transition: background 1.5s ease-in-out;
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }}
    
    [data-testid="stSidebar"] * {{
        color: #E2E8F0 !important;
    }}
    
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Text colors for main content */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
        color: #E2E8F0 !important;
    }}
    
    /* Input boxes */
    .stTextArea textarea {{
        background-color: rgba(30, 41, 59, 0.8) !important;
        color: #E2E8F0 !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 16px !important;
        font-size: 1.05rem !important;
        backdrop-filter: blur(10px);
    }}
    
    .stTextArea textarea:focus {{
        border-color: {primary} !important;
        box-shadow: 0 0 0 1px {primary} !important;
    }}
    
    /* Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, {primary} 0%, #8B5CF6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
        width: 100%;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.4) !important;
    }}
    
    /* Progress bars */
    .stProgress > div > div {{
        background-color: {primary} !important;
    }}
    
    /* Metrics */
    [data-testid="stMetricValue"] {{
        color: {primary} !important;
    }}
    
    /* Info/Success boxes */
    .stAlert {{
        background-color: rgba(30, 41, 59, 0.6) !important;
        backdrop-filter: blur(10px) !important;
        border-left: 4px solid {primary} !important;
        color: #E2E8F0 !important;
    }}
    
    /* Emotion card */
    .emotion-display-card {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 24px;
        padding: 2.5rem;
        text-align: center;
        margin: 2rem auto;
        max-width: 600px;
        animation: fadeIn 0.6s ease;
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .emotion-emoji-large {{
        font-size: 5rem;
        animation: bounce 2s ease-in-out infinite;
        display: block;
        margin-bottom: 1rem;
    }}
    
    @keyframes bounce {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-15px); }}
    }}
    
    .emotion-title {{
        font-size: 2rem;
        font-weight: 700;
        color: #FFFFFF;
        margin: 1rem 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }}
    
    .emotion-subtitle {{
        font-size: 1.2rem;
        color: rgba(255,255,255,0.9);
        font-weight: 400;
    }}
    
    /* Expander */
    .streamlit-expanderHeader {{
        background-color: rgba(30, 41, 59, 0.6) !important;
        border-radius: 10px !important;
        color: #E2E8F0 !important;
    }}
    
    /* Radio buttons */
    .stRadio > label {{
        color: #E2E8F0 !important;
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab"] {{
        color: #94A3B8 !important;
    }}
    
    .stTabs [aria-selected="true"] {{
        color: {primary} !important;
    }}
    
    /* Scrollbar */
    ::-webkit-scrollbar {{
        width: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: #1E293B;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {primary};
        border-radius: 5px;
    }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

# Apply initial theme
apply_dynamic_theme(st.session_state.current_emotion)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("<h1 style='text-align:center; color: #E2E8F0;'>💙 EmotionLLM</h1>", unsafe_allow_html=True)
    st.caption("Your AI companion for emotional awareness 🌱")
    st.markdown("---")

    page = st.radio(
        "Navigate",
        ["🏠 Home", "📊 Analytics", "📝 Journal", "📚 Resources"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Today's stats
    try:
        df = pd.read_csv('data/emotion_journal.csv')
        if not df.empty:
            st.markdown("### 📈 Today's Stats")
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            today_df = df[df['timestamp'].dt.date == datetime.now().date()]
            st.metric("Check-ins", len(today_df))
            if not today_df.empty:
                st.metric("Dominant", today_df['emotion'].mode()[0].capitalize())
    except:
        st.info("No journal entries yet")

    st.markdown("---")
    
    # Settings
    sound_on = st.checkbox("🔊 Emotion Sounds", value=True)
    theme_on = st.checkbox("🎨 Adaptive Theme", value=True)
    
    st.markdown("---")
    st.caption("Built with ❤️ for emotional intelligence")

# ==================== HOME PAGE ====================
if page == "🏠 Home":
    st.markdown("<h1 style='text-align:center; color: #E2E8F0; font-size: 2.5rem;'>🧠 EmotionLLM</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color: #94A3B8; font-size: 1.1rem;'>Your AI-powered mirror for mental well-being</p>", unsafe_allow_html=True)
    st.markdown("---")

    user_input = st.text_area(
        "💬 How are you feeling today?",
        placeholder="Type what's on your mind... (e.g., 'I'm feeling overwhelmed with work and can't focus')",
        height=150,
        key="emotion_input"
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_btn = st.button("🔍 Understand My Emotion", use_container_width=True)

    if analyze_btn and user_input.strip():
        with st.spinner("🧠 Analyzing your emotions..."):
            # Get emotion prediction
            emotion, confidence, probs = detector.predict_emotion(user_input)
            
            # Update session state
            st.session_state.current_emotion = emotion
            
            # Apply theme dynamically
            if theme_on:
                apply_dynamic_theme(emotion)
            
            # Play sound
            if sound_on:
                play_emotion_sound(emotion)
            
            # Log emotion
            logger.log_emotion(emotion, confidence, user_input, probs)
            
            st.markdown("---")
            
            # Display emotion card with proper theme
            theme = EMOTION_THEMES.get(emotion, {
                'emoji': '😌',
                'message': 'Emotion detected',
                'primary': '#3B82F6'
            })
            
            st.markdown(f"""
            <div class="emotion-display-card">
                <span class="emotion-emoji-large">{theme['emoji']}</span>
                <div class="emotion-title">Detected: {emotion.capitalize()}</div>
                <div class="emotion-subtitle">{theme['message']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Confidence bar
            st.markdown(f"**Confidence Level:** {confidence:.1%}")
            st.progress(confidence)
            
            st.markdown("---")
            
            # Two column layout
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 💭 Cognitive Reframe")
                st.info(get_reframe(emotion))
                
                st.markdown("### ✨ Daily Affirmation")
                st.success(get_affirmation(emotion))
            
            with col2:
                # Emotion breakdown chart
                st.markdown("### 🎚️ Emotion Breakdown")
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=list(probs.keys()),
                        y=list(probs.values()),
                        text=[f"{v:.1%}" for v in probs.values()],
                        textposition="auto",
                        marker=dict(
                            color=list(probs.values()),
                            colorscale='Viridis',
                            showscale=False
                        )
                    )
                ])
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#E2E8F0'),
                    xaxis=dict(title="Emotions", gridcolor='rgba(255,255,255,0.1)'),
                    yaxis=dict(title="Probability", gridcolor='rgba(255,255,255,0.1)'),
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Breathing exercise for negative emotions
            if emotion.lower() in ['sad', 'sadness', 'fear', 'anger', 'angry']:
                st.markdown("---")
                st.warning(f"😰 Feeling {emotion}? Let's try a calming technique.")
                
                with st.expander("🫁 Box Breathing Exercise (4-4-4-4)"):
                    st.markdown("""
                    ### How to do Box Breathing:
                    
                    1. 🌊 **Breathe IN** for 4 seconds
                    2. ⏸️ **HOLD** for 4 seconds
                    3. 🍃 **Breathe OUT** for 4 seconds
                    4. ⏸️ **HOLD** for 4 seconds
                    
                    **Repeat 4-5 cycles. Focus only on your breath.**
                    
                    *This technique is used by Navy SEALs to manage stress.*
                    """)
                    
                    st.video("https://www.youtube.com/watch?v=Uxbdx-SeOOo")
            
            # Music recommendation
            st.markdown("---")
            st.markdown("### 🎵 Mood-Based Music Therapy")
            
            playlists = {
                "joy": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
                "happy": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
                "sad": "https://open.spotify.com/playlist/37i9dQZF1DWVrtsSlLKzro",
                "sadness": "https://open.spotify.com/playlist/37i9dQZF1DWVrtsSlLKzro",
                "anger": "https://open.spotify.com/playlist/37i9dQZF1DWYxwmBaMqxsl",
                "angry": "https://open.spotify.com/playlist/37i9dQZF1DWYxwmBaMqxsl",
                "fear": "https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0",
                "love": "https://open.spotify.com/playlist/37i9dQZF1DX50QitC6Oqtn",
                "surprise": "https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0",
                "neutral": "https://open.spotify.com/playlist/37i9dQZF1DWZUAeYvs88zc"
            }
            
            url = playlists.get(emotion.lower(), playlists["neutral"])
            st.markdown(f"🎧 [Listen to a **{emotion.capitalize()}** Playlist on Spotify]({url})")

# ==================== ANALYTICS PAGE ====================
elif page == "📊 Analytics":
    st.markdown("<h1 style='text-align:center; color: #E2E8F0;'>📊 Your Emotional Journey</h1>", unsafe_allow_html=True)

    if Path("data/emotion_journal.csv").exists():
        df = pd.read_csv("data/emotion_journal.csv")
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['date'] = df['timestamp'].dt.date

            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Logs", len(df))
            with col2:
                st.metric("Most Frequent", df['emotion'].mode()[0].capitalize())
            with col3:
                avg_conf = df['intensity'].mean() if 'intensity' in df.columns else 0
                st.metric("Avg Confidence", f"{avg_conf:.0%}")
            with col4:
                st.metric("Unique Emotions", df['emotion'].nunique())

            st.markdown("---")

            # Timeline
            st.markdown("### 📈 Emotion Timeline (Last 30 Days)")
            df_recent = df[df['timestamp'] >= datetime.now() - pd.Timedelta(days=30)]
            daily = df_recent.groupby(['date', 'emotion']).size().reset_index(name='count')

            fig = px.line(
                daily,
                x='date',
                y='count',
                color='emotion',
                title='Daily Emotion Trends',
                markers=True
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#E2E8F0'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig, use_container_width=True)

            # Distribution
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🥧 Emotion Distribution")
                counts = df['emotion'].value_counts()
                pie = px.pie(
                    names=counts.index,
                    values=counts.values,
                    hole=0.4
                )
                pie.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#E2E8F0')
                )
                st.plotly_chart(pie, use_container_width=True)
            
            with col2:
                st.markdown("### 📊 Intensity Over Time")
                if 'intensity' in df.columns:
                    intensity_trend = df_recent.groupby('date')['intensity'].mean().reset_index()
                    fig = px.line(intensity_trend, x='date', y='intensity', markers=True)
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#E2E8F0'),
                        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                    )
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📝 No emotion data yet. Start tracking on the Home page!")
    else:
        st.info("📝 No emotion logs found. Start your first check-in!")

# ==================== JOURNAL PAGE ====================
elif page == "📝 Journal":
    st.markdown("<h1 style='text-align:center; color: #E2E8F0;'>📝 Your Emotion Journal</h1>", unsafe_allow_html=True)

    if Path("data/emotion_journal.csv").exists():
        df = pd.read_csv("data/emotion_journal.csv")
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp', ascending=False)
            
            st.write(f"**Showing {min(20, len(df))} most recent entries**")
            
            for _, row in df.head(20).iterrows():
                emotion = row['emotion']
                theme = EMOTION_THEMES.get(emotion, {'emoji': '😌'})
                ts = row['timestamp'].strftime("%B %d, %Y • %I:%M %p")
                
                with st.expander(f"{theme['emoji']} **{emotion.capitalize()}** — {ts}"):
                    intensity = row.get('intensity', row.get('confidence', 0))
                    st.write(f"**Confidence:** {intensity:.1%}")
                    st.progress(intensity)
                    st.markdown("**What you wrote:**")
                    text = row.get('note', row.get('text', 'No text recorded'))
                    st.info(text)
        else:
            st.info("📔 Your journal is empty. Start logging on the Home page!")
    else:
        st.info("📔 No journal file found. Log emotions to create one.")

# ==================== RESOURCES PAGE ====================
elif page == "📚 Resources":
    st.markdown("<h1 style='text-align:center; color: #E2E8F0;'>📚 Mental Wellness Toolkit</h1>", unsafe_allow_html=True)
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["🫁 Breathing", "💭 CBT Techniques", "📞 Crisis Support"])

    with tab1:
        st.markdown("### 🫁 Box Breathing (4-4-4-4)")
        st.info("**IN 4s — HOLD 4s — OUT 4s — HOLD 4s** • Repeat 4-5 cycles")
        st.video("https://www.youtube.com/watch?v=Uxbdx-SeOOo")
        
        st.markdown("### 4-7-8 Breathing")
        st.success("**IN 4s — HOLD 7s — OUT 8s** • Great for sleep")

    with tab2:
        st.markdown("### 🧠 Cognitive Reframing")
        st.markdown("""
        **Transform negative thoughts into balanced ones:**
        
        ❌ "I always fail at everything"  
        ✅ "I struggled this time, but I've succeeded before and I will again"
        
        ❌ "Nobody cares about me"  
        ✅ "I'm feeling lonely right now, but I have people who care"
        
        ❌ "I can't handle this"  
        ✅ "This is difficult, but I can take it one step at a time"
        """)

    with tab3:
        st.error("### 🚨 If you're in crisis, please reach out immediately")
        st.markdown("""
        **24/7 Global Mental Health Helplines:**
        
        🇺🇸 **United States:** 988 (Suicide & Crisis Lifeline)  
        🇮🇳 **India:** 1860-2662-345 (Vandrevala Foundation)  
        🇬🇧 **United Kingdom:** 116 123 (Samaritans)  
        🇨🇦 **Canada:** 1-833-456-4566  
        🌐 **Crisis Text Line:** Text 'HELLO' to 741741  
        
        **Remember:** Seeking help is a sign of strength, not weakness. ❤️
        """)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#94A3B8; font-size:0.95rem; padding: 1.5rem 0;'>
Built with ❤️ by <b style='color: #3B82F6;'>EmotionLLM</b> • Empowering emotional intelligence through AI
</div>
""", unsafe_allow_html=True)