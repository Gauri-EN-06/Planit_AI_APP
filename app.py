import streamlit as st
import time

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Planit", page_icon="🪐", layout="centered")

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Imports ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Inter:wght@400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: radial-gradient(ellipse at 20% 10%, #1a1040 0%, #0B0D1A 45%, #080C18 100%);
    min-height: 100vh;
}

/* ── Stars background ── */
.stars-bg {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}
.star {
    position: absolute;
    background: white;
    border-radius: 50%;
    animation: twinkle var(--dur, 3s) ease-in-out infinite;
    animation-delay: var(--delay, 0s);
    opacity: 0;
}
@keyframes twinkle {
    0%, 100% { opacity: 0; }
    50% { opacity: var(--peak, 0.8); }
}

/* ── Header ── */
.planit-header {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    position: relative;
    z-index: 1;
}
.planit-logo {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3.2rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #C4BFFF 0%, #6C63FF 50%, #A78BFA 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 0.5rem;
}
.planit-tagline {
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    color: #8B87C0;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 500;
}

/* ── Section labels ── */
.section-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #6C63FF;
    margin-bottom: 0.3rem;
}

/* ── Inputs ── */
div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stRadio"] label {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #C4BFFF !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background: rgba(108, 99, 255, 0.08) !important;
    border: 1px solid rgba(108, 99, 255, 0.3) !important;
    border-radius: 10px !important;
    color: #F0EEFF !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.2s ease !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: #6C63FF !important;
    box-shadow: 0 0 0 3px rgba(108, 99, 255, 0.15) !important;
}
div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stTextArea"] textarea::placeholder {
    color: #4a4870 !important;
}

/* ── Radio ── */
div[data-testid="stRadio"] > div {
    gap: 0.75rem !important;
}
div[data-testid="stRadio"] > div > label {
    background: rgba(108, 99, 255, 0.08) !important;
    border: 1px solid rgba(108, 99, 255, 0.25) !important;
    border-radius: 8px !important;
    padding: 0.4rem 1rem !important;
    color: #C4BFFF !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    cursor: pointer;
}
div[data-testid="stRadio"] > div > label:has(input:checked) {
    background: rgba(108, 99, 255, 0.25) !important;
    border-color: #6C63FF !important;
    color: #F0EEFF !important;
}

/* ── Primary button (Generate) ── */
div[data-testid="stButton"] > button[kind="primary"],
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #6C63FF, #8B5CF6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.03em !important;
    padding: 0.6rem 2rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(108, 99, 255, 0.35) !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 28px rgba(108, 99, 255, 0.5) !important;
}

/* ── Secondary button (Clear) ── */
.clear-btn > button {
    background: transparent !important;
    color: #8B87C0 !important;
    border: 1px solid rgba(139, 135, 192, 0.3) !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
}
.clear-btn > button:hover {
    border-color: #8B87C0 !important;
    color: #C4BFFF !important;
    background: rgba(139, 135, 192, 0.08) !important;
}

/* ── Progress bar ── */
div[data-testid="stProgress"] > div > div > div {
    background: linear-gradient(90deg, #6C63FF, #A78BFA) !important;
    border-radius: 4px !important;
}
div[data-testid="stProgress"] > div > div {
    background: rgba(108, 99, 255, 0.15) !important;
    border-radius: 4px !important;
}

/* ── Output plan area ── */
.plan-output {
    background: rgba(240, 238, 255, 0.04);
    border: 1px solid rgba(108, 99, 255, 0.2);
    border-radius: 14px;
    padding: 1.5rem 1.75rem;
    margin-top: 1rem;
}
.plan-intro {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #F0EEFF;
    line-height: 1.4;
    margin-bottom: 1.2rem;
}
.plan-outro {
    font-style: italic;
    color: #8B87C0;
    font-size: 0.9rem;
    margin-top: 0.5rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(108, 99, 255, 0.15);
}
.day-divider {
    border: none;
    border-top: 1px solid rgba(108, 99, 255, 0.15);
    margin: 0.5rem 0;
}

/* ── Expanders ── */
div[data-testid="stExpander"] {
    background: rgba(108, 99, 255, 0.06) !important;
    border: 1px solid rgba(108, 99, 255, 0.18) !important;
    border-radius: 10px !important;
    margin-bottom: 0.5rem !important;
}
div[data-testid="stExpander"] summary {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #C4BFFF !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}
div[data-testid="stExpander"] summary:hover {
    color: #F0EEFF !important;
}
div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] {
    color: #C4BFFF !important;
    font-size: 0.9rem !important;
    line-height: 1.7 !important;
    padding-top: 0.25rem !important;
}

/* ── Divider ── */
hr[data-testid="stDivider"] {
    border-color: rgba(108, 99, 255, 0.2) !important;
    margin: 1.5rem 0 !important;
}

/* ── Warning ── */
div[data-testid="stAlert"] {
    background: rgba(108, 99, 255, 0.1) !important;
    border: 1px solid rgba(108, 99, 255, 0.3) !important;
    border-radius: 10px !important;
    color: #C4BFFF !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(108, 99, 255, 0.3); border-radius: 3px; }
</style>

<!-- Starfield -->
<div class="stars-bg" id="stars"></div>
<script>
(function() {
    const container = document.getElementById('stars');
    if (!container) return;
    for (let i = 0; i < 80; i++) {
        const s = document.createElement('div');
        s.className = 'star';
        const size = Math.random() * 2 + 0.5;
        s.style.cssText = [
            `width:${size}px`, `height:${size}px`,
            `left:${Math.random()*100}%`, `top:${Math.random()*100}%`,
            `--dur:${2 + Math.random()*4}s`,
            `--delay:${Math.random()*5}s`,
            `--peak:${0.4 + Math.random()*0.6}`
        ].join(';');
        container.appendChild(s);
    }
})();
</script>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="planit-header">
    <div class="planit-logo">🪐 Planit</div>
    <div class="planit-tagline">Turn your goals into a step-by-step plan</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Input section ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    goal = st.text_input("What is your goal? 💫", placeholder="e.g. Learn Python, Build a portfolio")
with col2:
    deadline = st.text_input("How much time do you have? ⏳", placeholder="e.g. 2 weeks, 1 month")

level = st.radio("Experience level 🚀", ["Beginner", "Intermediate", "Expert"], horizontal=True)

extra_details = st.text_area(
    "Any additional details? (Optional) ✍️",
    placeholder="e.g. I can study 1 hour a day, I have a gym membership, I prefer evenings",
    height=90
)

st.divider()

# ── Buttons ───────────────────────────────────────────────────────────────────
btn_left, btn_center, btn_right = st.columns([1, 2, 1])

with btn_center:
    generate = st.button("✨ Generate My Plan", use_container_width=True)

with btn_right:
    st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
    clear = st.button("✕ Clear", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

if clear:
    st.rerun()

# ── Plan generation ───────────────────────────────────────────────────────────
if generate:
    if not goal or not deadline:
        st.warning("Please fill in your goal and time available before launching! 🚀")
    else:
        # Progress bar simulation
        progress_text = st.empty()
        progress_bar = st.progress(0)

        stages = [
            ("Mapping your trajectory…", 20),
            ("Charting the course…", 45),
            ("Aligning the stars…", 70),
            ("Finalising your mission…", 90),
        ]
        for msg, val in stages:
            progress_text.markdown(f"<p style='color:#8B87C0;font-size:0.85rem;text-align:center'>{msg}</p>", unsafe_allow_html=True)
            progress_bar.progress(val)
            time.sleep(0.5)

        from planner import generate_plan
        plan = generate_plan(goal, deadline, level, extra_details)

        progress_bar.progress(100)
        time.sleep(0.3)
        progress_bar.empty()
        progress_text.empty()

        # Parse and display
        # Matches planner.py output: "Day 1: Title", bullet tasks, plain-text outro
        lines = plan.strip().split("\n")
        intro_lines = []
        days = {}        # { "Day 1: Title": "content" }
        outro_lines = []
        current_day = None
        current_day_content = []
        found_days = False

        for line in lines:
            stripped = line.strip()

            # Detect a day header — "Day 1:", "Day 2:", etc.
            is_day_header = (
                stripped.lower().startswith("day ")
                and len(stripped) > 4
                and stripped[4:].split(":")[0].strip().isdigit()
            )

            if is_day_header:
                # Save previous day if any
                if current_day:
                    days[current_day] = "\n".join(current_day_content).strip()
                current_day = stripped
                current_day_content = []
                found_days = True

            elif found_days and current_day:
                # We're inside a day — collect its content
                current_day_content.append(line)

            elif found_days and not current_day:
                # Past the last day — this is the outro
                if stripped:
                    outro_lines.append(stripped)

            else:
                # Before any day — this is the intro
                if stripped:
                    intro_lines.append(stripped)

        # Save the last day
        if current_day:
            days[current_day] = "\n".join(current_day_content).strip()

        intro = " ".join(intro_lines)
        outro = " ".join(outro_lines)

        # Render output
        st.markdown('<div class="plan-output">', unsafe_allow_html=True)

        if intro:
            st.markdown(f'<div class="plan-intro">{intro}</div>', unsafe_allow_html=True)

        for i, (day_title, day_content) in enumerate(days.items()):
            if i > 0:
                st.markdown('<hr class="day-divider">', unsafe_allow_html=True)
            with st.expander(f"📅 {day_title}", expanded=True):
                st.markdown(day_content)

        if outro:
            st.markdown(f'<div class="plan-outro">{outro}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)