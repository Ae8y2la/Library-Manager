import streamlit as st
import random
import time
from datetime import datetime
import pandas as pd
import plotly.express as px

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="LIBRARY MANAGER",
    page_icon="💾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== AUTHENTIC Y2K CSS ==========
def load_css():
    st.markdown(r"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');
    
    /* Base Styles - CRT Monitor Effect */
    html, body, [class*="css"] {
        font-family: 'VT323', monospace;
        color: #00ff00 !important;
        background-color: #000000 !important;
        background-image: radial-gradient(rgba(0, 255, 0, 0.1) 1px, transparent 1px);
        background-size: 20px 20px;
        animation: scanlines 1s infinite linear;
    }
    
    /* CRT Scanlines Animation */
    @keyframes scanlines {
        0% { background-position: 0 0; }
        100% { background-position: 0 20px; }
    }
    
    /* Glow Effect for Text */
    @keyframes textglow {
        0% { text-shadow: 0 0 5px #00ff00; }
        50% { text-shadow: 0 0 20px #00ff00, 0 0 30px #00ffff; }
        100% { text-shadow: 0 0 5px #00ff00; }
    }
    
    /* Loading Animation */
    @keyframes loading {
        0% { content: "LOADING"; }
        25% { content: "LOADING."; }
        50% { content: "LOADING.."; }
        75% { content: "LOADING..."; }
        100% { content: "LOADING"; }
    }
    
    /* Main Container - Floppy Disk Inspired */
    .y2k-container {
        background: #000000 !important;
        border: 3px solid #00ff00 !important;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.5), 
                    inset 0 0 15px rgba(0, 255, 0, 0.3);
        padding: 20px;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }
    
    .y2k-container::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(
            rgba(0, 255, 0, 0.1) 0%, 
            transparent 5%, 
            transparent 95%, 
            rgba(0, 255, 0, 0.1) 100%
        );
        pointer-events: none;
    }
    
    /* Titles with Matrix-like Effect */
    .y2k-title {
        font-family: 'Press Start 2P', cursive !important;
        color: #00ff00 !important;
        font-size: 2.2rem !important;
        margin-bottom: 0.5rem !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        animation: textglow 2s infinite;
        position: relative;
    }
    
    .y2k-title::after {
        content: "";
        position: absolute;
        bottom: -5px;
        left: 0;
        width: 100%;
        height: 2px;
        background: #00ff00;
        animation: titleunderline 3s infinite;
    }
    
    @keyframes titleunderline {
        0% { width: 0%; left: 0; }
        50% { width: 100%; left: 0; }
        100% { width: 0%; left: 100%; }
    }
    
    /* Cards - Inspired by Windows 98 */
    .y2k-card {
        background: #000000 !important;
        border: 2px solid #00ff00 !important;
        border-radius: 0 !important;
        padding: 15px !important;
        margin-bottom: 15px !important;
        box-shadow: 4px 4px 0px rgba(0, 255, 0, 0.5) !important;
        transition: all 0.3s ease !important;
    }
    
    .y2k-card:hover {
        transform: translate(-2px, -2px) !important;
        box-shadow: 6px 6px 0px rgba(0, 255, 0, 0.8) !important;
    }
    
    /* Buttons - Retro Clickable */
    button {
        background: #000000 !important;
        color: #00ff00 !important;
        border: 2px solid #00ff00 !important;
        border-radius: 0 !important;
        font-family: 'VT323', monospace !important;
        font-size: 1.3rem !important;
        padding: 8px 20px !important;
        margin: 5px 0 !important;
        transition: all 0.3s !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        position: relative;
        overflow: hidden;
    }
    
    button:hover {
        background: rgba(0, 255, 0, 0.1) !important;
        box-shadow: 0 0 10px rgba(0, 255, 0, 0.5) !important;
    }
    
    button:active {
        transform: translate(2px, 2px) !important;
        box-shadow: none !important;
    }
    
    button::after {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            to bottom right,
            transparent 45%,
            rgba(0, 255, 0, 0.3) 50%,
            transparent 55%
        );
        transform: rotate(30deg);
        animation: buttonshine 3s infinite;
    }
    
    @keyframes buttonshine {
        0% { transform: translateX(-100%) rotate(30deg); }
        100% { transform: translateX(100%) rotate(30deg); }
    }
    
    /* Inputs - Retro Terminal Style */
    .stTextInput input, .stSelectbox select, .stTextArea textarea {
        background: #000000 !important;
        color: #00ff00 !important;
        border: 2px solid #00ff00 !important;
        border-radius: 0 !important;
        font-family: 'VT323', monospace !important;
        font-size: 1.2rem !important;
        padding: 8px !important;
    }
    
    .stTextInput input:focus, .stSelectbox select:focus, .stTextArea textarea:focus {
        outline: none !important;
        box-shadow: 0 0 10px rgba(0, 255, 0, 0.5) !important;
    }
    
    /* Special Elements */
    .y2k-highlight {
        background: rgba(0, 255, 0, 0.2) !important;
        padding: 2px 5px !important;
        border-left: 3px solid #00ff00 !important;
    }
    
    .y2k-badge {
        display: inline-block !important;
        background: #000000 !important;
        color: #00ff00 !important;
        padding: 3px 8px !important;
        margin: 2px !important;
        font-size: 0.9rem !important;
        border: 1px solid #00ff00 !important;
        box-shadow: 2px 2px 0px rgba(0, 255, 0, 0.5) !important;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px !important;
    }
    
    ::-webkit-scrollbar-track {
        background: #000000 !important;
        border-left: 1px solid #00ff00 !important;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #00ff00 !important;
        border: 1px solid #000000 !important;
    }
    
    /* Loading Screen */
    .loading-screen {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: #000000;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    }
    
    .loading-text {
        color: #00ff00;
        font-family: 'VT323', monospace;
        font-size: 2rem;
        margin-top: 20px;
        animation: textglow 2s infinite;
    }
    
    .loading-text::after {
        content: "LOADING";
        animation: loading 1.5s infinite;
    }
    
    /* Pixel Art Elements */
    .pixel-divider {
        height: 10px;
        background: repeating-linear-gradient(
            to right,
            #000000,
            #000000 5px,
            #00ff00 5px,
            #00ff00 10px
        );
        margin: 15px 0;
    }
    
    /* Animation for deletion */
    @keyframes disappear {
        0% { opacity: 1; transform: scale(1); }
        100% { opacity: 0; transform: scale(0); }
    }

    /* Copyright notice style */
    .copyright-notice {
        text-align: center;
        margin-top: 50px;
        color: #00ff00;
        font-family: 'VT323', monospace;
        font-size: 1rem;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# ========== Y2K LIBRARY CLASS ==========
class Y2KLibrary:
    def __init__(self):
        if "books" not in st.session_state:
            st.session_state.books = {}
            st.session_state.achievements = set()
            st.session_state.loading = True
            self._initialize_easter_eggs()
    
    def _initialize_easter_eggs(self):
        self.easter_eggs = {
            "The Matrix": "💾 SYSTEM OVERRIDE: Welcome to the Bookrix!",
            "2001: A Space Odyssey": "🛸 AI RECOGNIZED: HAL 9000 approved",
            "Neuromancer": "💿 CYBERPUNK CLASSIC: Gibson would be proud",
            "Snow Crash": "🗡️ PIZZA DELIVERY: 30 minutes or less guaranteed",
            "Hackers": "🖥️ HACK THE PLANET: This is our world now",
            "Fight Club": "🧼 FIRST RULE: Don't talk about this book",
            "The Hitchhiker's Guide": "🌌 DON'T PANIC: The answer is 42"
        }
        
        self.secret_codes = {
            "1337": self._activate_hacker_mode,
            "8008": self._show_tech_easter_egg,
            "1984": self._big_brother_warning,
            "2020": self._bug_effect
        }
    
    def _activate_hacker_mode(self):
        st.session_state.hacker_mode = not st.session_state.get("hacker_mode", False)
        msg = "HACKER MODE ACTIVATED" if st.session_state.hacker_mode else "HACKER MODE DEACTIVATED"
        st.toast(f'💻 {msg}!', icon="👨‍💻")
    
    def _show_tech_easter_egg(self):
        st.toast('📞 8008: LEGACY SYSTEM DIALTONE', icon="📠")
    
    def _big_brother_warning(self):
        st.toast('👁️ BIG BROTHER IS WATCHING YOU', icon="⚠️")
    
    def _bug_effect(self):
        st.session_state.y2k_effect = True
        st.toast('⚠️ SYSTEM BUG DETECTED!', icon="🐛")
        time.sleep(1)
        st.balloons()
        st.session_state.y2k_effect = False
    
    def _check_achievements(self, title):
        achievements = {
            "5_books": ("📼 VHS Collector", len(st.session_state.books) >= 5),
            "10_books": ("💾 Data Hoarder", len(st.session_state.books) >= 10),
            "scifi_fan": ("👽 Cyber Explorer", sum(1 for b in st.session_state.books.values() if b["genre"] == "Sci-Fi") >= 3),
            "midnight": ("🌃 Midnight Hacker", datetime.now().hour in [0, 23]),
            "y2k_bug": ("🐛 Y2K Survivor", any(b["title"] in ["The Matrix", "2001: A Space Odyssey"] for b in st.session_state.books.values())),
            "leet": ("1337 H4X0R", st.session_state.get("hacker_mode", False))
        }
        
        for code, (name, condition) in achievements.items():
            if condition and code not in st.session_state.achievements:
                st.session_state.achievements.add(code)
                with st.empty():
                    st.success(f'✨ {name} unlocked!')
                    time.sleep(2)
                st.toast(f'✨ {name} unlocked!', icon="🎉")
    
    def add_book(self, title, author, genre):
        # Check for secret codes
        if title in self.secret_codes:
            self.secret_codes[title]()
            return "🔒 SECRET CODE ACCEPTED"
        
        book_id = f"BK-{int(time.time())}-{random.randint(1000,9999)}"
        
        secret_message = self.easter_eggs.get(title, "")
        if secret_message:
            st.balloons()
            time.sleep(0.5)
        
        st.session_state.books[book_id] = {
            "title": title,
            "author": author,
            "genre": genre,
            "added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mood": None,
            "secret_note": "",
            "easter_egg": secret_message,
            "status": "📶 ONLINE"
        }
        
        self._check_achievements(title)
        return f"💾 '{title.upper()}' SAVED TO DATABASE! {secret_message}"

    def get_mood_analytics(self):
        moods = [b.get("mood") for b in st.session_state.books.values() if b.get("mood")]
        if moods:
            mood_data = pd.DataFrame({"mood": moods})
            fig = px.pie(mood_data, names="mood", 
                        title="EMOTION MATRIX ANALYSIS",
                        color_discrete_sequence=['#00ff00', '#00ffff', '#00cc00', '#009900'],
                        hole=0.4)
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0.8)',
                plot_bgcolor='rgba(0,0,0,0.8)',
                font=dict(family='VT323', size=20, color='#00ff00'),
                legend=dict(font=dict(size=16)))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📡 SCANNING FOR EMOTIONAL DATA... NONE DETECTED")

# ========== LOADING SCREEN ==========
def show_loading_screen():
    with st.empty():
        st.markdown("""
        <div class="loading-screen">
            <div style="width: 100px; height: 100px; border: 5px solid #00ff00; 
                       border-radius: 50%; border-top-color: transparent;
                       animation: spin 1s linear infinite;"></div>
            <div class="loading-text"></div>
        </div>
        <style>
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
        """, unsafe_allow_html=True)
        time.sleep(2)
        st.session_state.loading = False
        st.rerun()

# ========== MAIN APP ==========
def main():
    # Show loading screen if needed
    if st.session_state.get("loading", True):
        show_loading_screen()
        return
    
    # Initialize library
    if "lib" not in st.session_state:
        st.session_state.lib = Y2KLibrary()
    
    # Header with animated matrix effect
    with st.container():
        st.markdown("""
        <div class="y2k-container">
            <h1 class="y2k-title">LIBRARY MANAGER</h1>
            <div class="pixel-divider"></div>
            <p style="font-size: 1.3rem; color: #00ff00;">v1.0 • ©Aeyla Naseer.</p>
            <p style="font-size: 1rem; color: #00aa00;">SYSTEM TIME: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main columns
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Add Books Section
        with st.container():
            st.markdown("""
            <div class="y2k-container">
                <h2>📥 ENTER NEW BOOK DATA</h2>
                <div class="pixel-divider"></div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("add_books", clear_on_submit=True):
                title = st.text_input("TITLE*", key="title", help="Try entering '1337' for a secret!")
                author = st.text_input("AUTHOR*", key="author")
                genre = st.selectbox("GENRE*", ["", "Sci-Fi", "Fantasy", "Mystery", "Tech", "Romance", "Horror"])
                
                mood = st.select_slider("EMOTION MATRIX", 
                                      options=["😴 BORED", "🫤 MEH", "😊 PLEASED", "🤩 SYSTEM OVERLOAD"],
                                      value="😊 PLEASED")
                
                submitted = st.form_submit_button("💾 SAVE TO DATABASE")
                if submitted:
                    if title in st.session_state.lib.secret_codes:
                        st.session_state.lib.secret_codes[title]()
                    elif title and author and genre:
                        result = st.session_state.lib.add_book(title, author, genre)
                        st.session_state.books[list(st.session_state.books.keys())[-1]]["mood"] = mood
                        
                        # Special effect for certain books
                        if title.lower() == "the matrix":
                            with st.empty():
                                st.markdown("""
                                <style>
                                @keyframes matrix {
                                    0% { color: #00ff00; }
                                    50% { color: #00ffff; }
                                    100% { color: #00ff00; }
                                }
                                .matrix-effect {
                                    animation: matrix 0.5s infinite;
                                }
                                </style>
                                <p class="matrix-effect">WAKE UP, NEO...</p>
                                """, unsafe_allow_html=True)
                                time.sleep(2)
                        
                        st.success(result)
                    else:
                        st.error("ERROR: MISSING REQUIRED FIELDS")
        
        # Book List
        if st.session_state.books:
            with st.container():
                st.markdown("""
                <div class="y2k-container">
                    <h2>📁 DATABASE RECORDS</h2>
                    <div class="pixel-divider"></div>
                </div>
                """, unsafe_allow_html=True)
                
                for book_id, book in st.session_state.books.items():
                    with st.expander(f"{book['title'].upper()} : {book['status']}", expanded=False):
                        cols = st.columns([4,1])
                        with cols[0]:
                            st.markdown(f"""
                            <div class="y2k-card">
                                <p><span class="y2k-highlight">AUTHOR:</span> {book['author'].upper()}</p>
                                <p><span class="y2k-highlight">GENRE:</span> {book['genre'].upper()}</p>
                                <p><span class="y2k-highlight">DATE STORED:</span> {book['added']}</p>
                                {f"<p><span class='y2k-highlight'>MOOD:</span> {book['mood']}</p>" if book['mood'] else ""}
                                {f"<p style='color: #00ffff;'>{book['easter_egg']}</p>" if book['easter_egg'] else ""}
                            </div>
                            """, unsafe_allow_html=True)
                        with cols[1]:
                            if st.button("❌ DELETE", key=f"del_{book_id}"):
                                # Add deletion effect
                                with st.empty():
                                    st.markdown(f"""
                                    <style>
                                    @keyframes disappear {{
                                        0% {{ opacity: 1; transform: scale(1); }}
                                        100% {{ opacity: 0; transform: scale(0); }}
                                    }}
                                    .deleting {{
                                        animation: disappear 0.5s forwards;
                                    }}
                                    </style>
                                    <div class="deleting">
                                        DELETING {book['title'].upper()}...
                                    </div>
                                    """, unsafe_allow_html=True)
                                    time.sleep(0.5)
                                del st.session_state.books[book_id]
                                st.rerun()
    
    with col2:
        # Book Wizard
        with st.expander("💻 BOOK.EXE", expanded=True):
            st.markdown("""
            <div class="y2k-container">
                <h3>📀 BOOK RECOMMENDATION ENGINE v1.0</h3>
                <div class="pixel-divider"></div>
                <p>CLICK TO SUMMON RETRO-FUTURISTIC READS:</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("⌨️ RUN PROGRAM", key="spell_button"):
                with st.spinner("INITIALIZING CD-ROM..."):
                    time.sleep(1.5)
                    spells = {
                        "Sci-Fi": ("NEUROMANCER", "WILLIAM GIBSON", "CLASSIC CYBERPUNK"),
                        "Fantasy": ("SNOW CRASH", "NEAL STEPHENSON", "PIZZA DELIVERY INCLUDED"),
                        "Mystery": ("THE CRYING OF LOT 49", "THOMAS PYNCHON", "PARANOIA MODE ACTIVATED"),
                        "Tech": ("HACKERS", "STEVEN LEVY", "ACCESS GRANTED"),
                        "Horror": ("HOUSE OF LEAVES", "MARK Z. DANIELEWSKI", "MIND-BENDING TERROR")
                    }
                    genre = random.choice(list(spells.keys()))
                    title, author, desc = spells[genre]
                    
                    st.markdown(f"""
                    <div class="y2k-card">
                        <h3>{title}</h3>
                        <p><span class="y2k-highlight">AUTHOR:</span> {author}</p>
                        <p><span class="y2k-highlight">DESCRIPTION:</span> {desc}</p>
                        <p style="color: #00ff00; font-weight: bold;">GENRE: {genre} • ★★★★☆</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Mood Analytics
        st.session_state.lib.get_mood_analytics()
        
        # Achievements
        if st.session_state.get("achievements"):
            with st.container():
                st.markdown("""
                <div class="y2k-container">
                    <h2>🏆 ACHIEVEMENTS UNLOCKED</h2>
                    <div class="pixel-divider"></div>
                </div>
                """, unsafe_allow_html=True)
                
                for code in st.session_state.achievements:
                    st.markdown(f'<div class="y2k-badge">{code.replace("_", " ").upper()}</div>', unsafe_allow_html=True)
        
        # System Status
        with st.container():
            st.markdown("""
            <div class="y2k-container">
                <h2>🖥️ SYSTEM STATUS</h2>
                <div class="pixel-divider"></div>
                <div style="display: flex; justify-content: space-between;">
                    <span>MEMORY:</span>
                    <span>""" + f"{random.randint(30, 90)}% USED" + """</span>
                </div>
                <div style="height: 10px; background: #000000; border: 1px solid #00ff00; margin: 5px 0;">
                    <div style="height: 100%; width: """ + f"{random.randint(30, 90)}" + """%; background: #00ff00;"></div>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>DISK SPACE:</span>
                    <span>""" + f"{random.randint(10, 80)}% FREE" + """</span>
                </div>
                <div style="height: 10px; background: #000000; border: 1px solid #00ff00; margin: 5px 0;">
                    <div style="height: 100%; width: """ + f"{100 - random.randint(10, 80)}" + """%; background: #00ff00;"></div>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>VIRUS SCAN:</span>
                    <span>CLEAN</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                    <span>Y2K COMPLIANCE:</span>
                    <span>""" + random.choice(["PASSED", "FAILED", "UNKNOWN"]) + """</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Copyright Notice (placed at the bottom of the app)
    st.markdown("""
    <div class="copyright-notice">
        © 2025 Aeyla Naseer. All rights reserved.
    </div>
    """, unsafe_allow_html=True)

# Print statement (for terminal/logging)
print("© 2025 Aeyla Naseer. All rights reserved.")

# ----------------------------------------------------THE-END----------------------------------------------------------------
if __name__ == "__main__":
    main()