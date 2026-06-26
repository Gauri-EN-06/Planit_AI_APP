"""
app.py — Planit 🪐
==================
Streamlit frontend for Planit, an AI-powered planning app that turns any
goal into a personalized day-by-day action plan.

Structure:
    1. Imports & page config
    2. Custom CSS (theme, animations, component styles)
    3. Session state initialisation
    4. Header
    5. Input section
    6. Generate / Clear buttons
    7. Plan generation logic
    8. Plan display (parser + renderer)

Dependencies:
    pip install streamlit groq python-dotenv
"""

import streamlit as st
import time

# ─────────────────────────────────────────────────────────────────────────────
# 1. PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Planit", page_icon="🪐", layout="centered")

# ─────────────────────────────────────────────────────────────────────────────
# 2. CUSTOM CSS
#    All styling is injected via st.markdown() since Streamlit doesn't support
#    external .css files. Organised into logical sections below.
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Inter:wght@400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Deep space background gradient */
.stApp {
    background: radial-gradient(ellipse at 20% 10%, #1a1040 0%, #0B0D1A 45%, #080C18 100%);
    min-height: 100vh;
}

/* ── Starfield bg
    Uses radial-gradient dots scattered across the viewport via a
   pseudo-element so they sit behind all content. Opacity animates
   to create a subtle twinkling effect. ── */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 0;
    background-image:
        radial-gradient(1px 1px at 10% 15%, rgba(255,255,255,1) 0%, transparent 100%),
        radial-gradient(1px 1px at 25% 60%, rgba(255,255,255,0.9) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 40% 30%, rgba(255,255,255,1) 0%, transparent 100%),
        radial-gradient(1px 1px at 55% 80%, rgba(255,255,255,0.85) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 70% 20%, rgba(255,255,255,1) 0%, transparent 100%),
        radial-gradient(2px 2px at 80% 55%, rgba(255,255,255,0.95) 0%, transparent 100%),
        radial-gradient(1px 1px at 90% 40%, rgba(255,255,255,0.9) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 15% 85%, rgba(255,255,255,1) 0%, transparent 100%),
        radial-gradient(2.5px 2.5px at 35% 10%, rgba(196,191,255,1) 0%, transparent 100%),
        radial-gradient(1px 1px at 60% 50%, rgba(255,255,255,0.85) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 75% 90%, rgba(255,255,255,0.95) 0%, transparent 100%),
        radial-gradient(2px 2px at 5% 45%, rgba(255,255,255,1) 0%, transparent 100%),
        radial-gradient(1px 1px at 48% 70%, rgba(196,191,255,0.9) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 88% 10%, rgba(255,255,255,1) 0%, transparent 100%),
        radial-gradient(2px 2px at 20% 35%, rgba(255,255,255,0.85) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 65% 5%, rgba(255,255,255,1) 0%, transparent 100%),
        radial-gradient(1px 1px at 92% 75%, rgba(196,191,255,0.9) 0%, transparent 100%),
        radial-gradient(2px 2px at 30% 95%, rgba(255,255,255,0.95) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 50% 25%, rgba(255,255,255,1) 0%, transparent 100%),
        radial-gradient(1px 1px at 8% 65%, rgba(255,255,255,0.9) 0%, transparent 100%);
    animation: twinkle-field 6s ease-in-out infinite alternate;
}
@keyframes twinkle-field {
    0%   { opacity: 0.65; }
    50%  { opacity: 1;   }
    100% { opacity: 0.75; }
}

/* ── Header ── */
.planit-header {
    text-align: center;
    padding: 3rem 1rem 2rem;
    position: relative;
    z-index: 1;
}

/* Planet emoji floats up and down with a purple glow */
.planit-planet {
    font-size: 3.5rem;
    display: block;
    line-height: 1;
    margin-bottom: 0.5rem;
    filter: drop-shadow(0 0 18px rgba(108,99,255,0.6));
    animation: float 4s ease-in-out infinite;
}
@keyframes float {
    0%, 100% { transform: translateY(0);    }
    50%       { transform: translateY(-6px); }
}

/* Brand logotype with white-to-purple gradient */
.planit-logo {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3.4rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #ffffff 0%, #C4BFFF 40%, #6C63FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 0.6rem;
}

.planit-tagline {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    color: #6B6899;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    font-weight: 500;
}
.planit-tagline span {
    color: #9B97D4; /* accent on "step-by-step plan" */
}

/* ── Input labels ── */
div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stRadio"] label {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #C4BFFF !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
}

/* ── Text inputs & textarea ── */
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

/* Suppress browser autofill yellow highlight */
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus {
    -webkit-box-shadow: 0 0 0px 1000px #12112a inset !important;
    -webkit-text-fill-color: #F0EEFF !important;
}

/* ── Experience level radio buttons — styled as pill toggles ── */
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

/* ── Generate button — purple gradient with lift-on-hover ── */
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

/* ── Progress bar — purple gradient fill ── */
div[data-testid="stProgress"] > div > div > div {
    background: linear-gradient(90deg, #6C63FF, #A78BFA) !important;
    border-radius: 4px !important;
}
div[data-testid="stProgress"] > div > div {
    background: rgba(108, 99, 255, 0.15) !important;
    border-radius: 4px !important;
}

/* ── Plan output ── */
.plan-intro {
    /* Bold intro sentence displayed above the day expanders */
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #F0EEFF;
    line-height: 1.4;
    margin-bottom: 1.2rem;
}
.plan-outro {
    /* Italic closing message displayed below all day expanders */
    font-style: italic;
    color: #8B87C0;
    font-size: 1rem;
    margin-top: 0.5rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(108, 99, 255, 0.15);
}
.day-divider {
    /* Thin separator line between day expanders */
    border: none;
    border-top: 1px solid rgba(108, 99, 255, 0.15);
    margin: 0.5rem 0;
}

/* ── Day expanders ── */
div[data-testid="stExpander"] {
    background: rgba(108, 99, 255, 0.06) !important;
    border: 1px solid rgba(108, 99, 255, 0.18) !important;
    border-radius: 10px !important;
    margin-bottom: 0.25rem !important;
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

/* ── Divider lines ── */
hr[data-testid="stDivider"] {
    border-color: rgba(108, 99, 255, 0.2) !important;
    margin: 1.5rem 0 !important;
}

/* ── Warning / error alerts ── */
div[data-testid="stAlert"] {
    background: rgba(108, 99, 255, 0.1) !important;
    border: 1px solid rgba(108, 99, 255, 0.3) !important;
    border-radius: 10px !important;
    color: #C4BFFF !important;
}
            
/* ── Clear button — fixed top-right corner ── */
div[data-testid="stMainBlockContainer"] > div > div > div > div:has(button[data-testid="baseButton-secondary"]) {
    position: fixed;
    top: 0.75rem;
    right: 1rem;
    z-index: 99999;
    width: auto;
}
button[data-testid="baseButton-secondary"] {
    background: transparent !important;
    border: 1px solid rgba(139,135,192,0.4) !important;
    border-radius: 50% !important;
    width: 34px !important;
    height: 34px !important;
    padding: 0 !important;
    color: #8B87C0 !important;
    font-size: 0.9rem !important;
    min-height: unset !important;
    box-shadow: none !important;
    line-height: 1 !important;
}
button[data-testid="baseButton-secondary"]:hover {
    background: rgba(108,99,255,0.2) !important;
    border-color: #6C63FF !important;
    color: #F0EEFF !important;
    transform: none !important;
}
 
/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(108, 99, 255, 0.3); border-radius: 3px; }

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 3. SESSION STATE INITIALISATION
#    Streamlit reruns the entire script on every interaction, so persistent
#    values are stored in st.session_state between reruns.
# ─────────────────────────────────────────────────────────────────────────────

# Rate limiting: tracks timestamp of the last API call
if "last_request_time" not in st.session_state:
    st.session_state.last_request_time = 0

# Stores the raw plan text returned by the AI
if "plan_output" not in st.session_state:
    st.session_state.plan_output = None

# Tracks whether a plan has been generated in this session
if "plan_generated" not in st.session_state:
    st.session_state.plan_generated = False

# Clear flag: set to True by the Clear button, consumed before widgets render
# This pattern is needed because Streamlit doesn't allow modifying a widget's
# session state key after the widget has already been rendered on the page.
if st.session_state.get("_do_clear"):
    st.session_state["goal"]         = ""
    st.session_state["deadline"]     = ""
    st.session_state["extra_details"] = ""
    st.session_state["level"]        = "Beginner"
    st.session_state["_do_clear"]    = False


# ─────────────────────────────────────────────────────────────────────────────
# 4. HEADER
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="planit-header">
    <span class="planit-planet">🪐</span>
    <div class="planit-logo">Planit</div>
    <div class="planit-tagline">Turn your goals into a <span>step-by-step plan</span></div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# 5. INPUT SECTION
#    Goal and deadline side by side; level as pill radio; extra details as
#    a resizable textarea. All inputs use explicit keys so session state
#    can reset them cleanly via the Clear button.
# ─────────────────────────────────────────────────────────────────────────────

col1, col2 = st.columns(2)
with col1:
    goal = st.text_input("What is your goal? 💫", placeholder="e.g. Learn Python, Build a portfolio", key="goal", autocomplete="off")
with col2:
    deadline = st.text_input("How much time do you have? ⏳", placeholder="e.g. 2 weeks, 5 days", key="deadline", autocomplete="off")

level = st.radio("Experience level 🚀", ["Beginner", "Intermediate", "Expert"], horizontal=True, key="level")

extra_details = st.text_area(
    "Any additional details? (Optional) ✍️",
    placeholder="e.g. I can study 1 hour a day, I have a gym membership, I prefer evenings",
    height=90,
    key="extra_details"
)

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# 6. BUTTONS
#    Generate is always centered and never moves.
#    Clear is a fixed HTML button pinned to the top-right corner — it only
#    appears after a plan has been generated. Using a pure HTML button (not
#    a Streamlit widget) avoids layout interference with Generate.
#    Clear works by appending ?clear=1 to the URL, which Streamlit reads via
#    st.query_params on the next rerun.
# ─────────────────────────────────────────────────────────────────────────────

# Generate button — always centered in a 1:2:1 column layout
_, btn_center, _ = st.columns([1, 2, 1])
with btn_center:
    generate = st.button("✨ Generate My Plan", use_container_width=True)

# Clear button — rendered as a Streamlit secondary button
# Only shown after a plan has been generated.
if st.session_state.plan_generated:
    clear = st.button("✕", type="secondary", key="clear_btn")
    if clear:
        st.session_state["_do_clear"]      = True
        st.session_state["plan_generated"] = False
        st.session_state["plan_output"]    = None
        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# 7. PLAN GENERATION
#    Validates inputs, enforces a 10-second rate limit between requests,
#    shows a themed progress bar, calls the AI, and stores the result in
#    session state before triggering a rerun so the display block can render.
# ─────────────────────────────────────────────────────────────────────────────
if generate:
    if not goal or not deadline:
        st.warning("Please fill in your goal and time available before launching! 🚀")
    else:
        # Rate limiting — prevent rapid repeated API calls
        time_since_last = time.time() - st.session_state.last_request_time
        if time_since_last < 10:
            st.warning(f"Please wait {int(10 - time_since_last)} seconds before generating again! ⏳")
        else:
            st.session_state.last_request_time = time.time()

            # Progress bar simulation
            progress_text = st.empty()
            progress_bar = st.progress(0)

            stages = [
                ("🚀 Mapping your trajectory…", 20),
                ("🛰️ Charting the course…", 45),
                ("🌌 Aligning the stars…", 70),
                ("💫 Finalising your mission…", 90),
            ]
            for msg, val in stages:
                progress_text.markdown(f"<p style='color:#8B87C0;font-size:0.85rem;text-align:center'>{msg}</p>", unsafe_allow_html=True)
                progress_bar.progress(val)
                time.sleep(0.5)

            # Call the AI planner
            from planner import generate_plan
            try:
                plan = generate_plan(goal, deadline, level, extra_details)
            except Exception as e:
                st.error("Something went wrong connecting to the AI. Please try again in a moment!")
                st.stop()

            # Store result and trigger rerun so the display block renders    
            st.session_state["plan_generated"] = True
            st.session_state["plan_output"] = plan

            progress_bar.progress(100)
            time.sleep(0.3)
            progress_bar.empty()
            progress_text.empty()
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# 8. PLAN DISPLAY
#    Reads the stored plan from session state and parses it into three parts:
#      - intro  : bold opening sentence(s) before the first day
#      - days   : list of (title, content, is_bonus) tuples
#      - outro  : italic closing sentence(s) after the last day
#
#    Parsing rules:
#      - "Day N: Title" lines start a new day block
#      - "--- Bonus Days ---" marks the start of optional bonus days
#      - Trailing non-task lines at the end of the last day are moved to outro
#      - "optional ... highly recommended" lines are filtered out everywhere
#        (the planner sometimes appends this as a stray line)
# ─────────────────────────────────────────────────────────────────────────────

if st.session_state.get("plan_output"):
    plan  = st.session_state["plan_output"]
    lines = plan.strip().split("\n")

    intro_lines       = []
    days              = []   # list of (title, content, is_bonus)
    outro_lines       = []
    current_day       = None
    current_day_content = []
    found_days        = False
    in_bonus          = False

    for line in lines:
        stripped = line.strip()

        # Detect the bonus days separator line
        is_bonus_marker = "bonus days" in stripped.lower() and "---" in stripped

        # Detect a day header e.g. "Day 1: Introduction to Python"
        is_day_header = (
            stripped.lower().startswith("day ")
            and len(stripped) > 4
            and stripped[4:].split(":")[0].strip().isdigit()
        )

        if is_bonus_marker:
            # Save the current day and switch to bonus mode
            if current_day:
                days.append((current_day, "\n".join(current_day_content).strip(), False))
                current_day = None
                current_day_content = []
            in_bonus = True

        elif is_day_header:
            # Save the previous day before starting a new one
            if current_day:
                days.append((current_day, "\n".join(current_day_content).strip(), in_bonus))
            current_day = stripped
            current_day_content = []
            found_days = True

        elif found_days and current_day:
            # Inside a day — skip stray "optional/highly recommended" lines
            if not ("optional" in stripped.lower() and "highly recommended" in stripped.lower()):
                current_day_content.append(line)

        elif found_days and not current_day:
            # After the last day — collect outro, skipping stray lines
            skip = (
                ("optional" in stripped.lower() and "highly recommended" in stripped.lower()) or
                "--- bonus days" in stripped.lower() or
                stripped.lower().startswith("--- bonus")
            )
            if stripped and not skip:
                outro_lines.append(stripped)

        else:
            # Before any day — collect intro
            if stripped:
                intro_lines.append(stripped)

    # Save the last day, stripping any trailing outro text that the planner
    # may have appended inside the final day block
    if current_day:
        content_lines = current_day_content
        cutoff = len(content_lines)
        for j in range(len(content_lines) - 1, -1, -1):
            l = content_lines[j].strip()
            if l.startswith("-") or l.startswith("•") or l == "" or l.lower().startswith("resource"):
                break
            cutoff = j
        if cutoff < len(content_lines):
            # Move the trailing text to the front of outro_lines
            outro_lines = [l.strip() for l in content_lines[cutoff:] if l.strip()] + outro_lines
            content_lines = content_lines[:cutoff]
        days.append((current_day, "\n".join(content_lines).strip(), in_bonus))

    intro = " ".join(intro_lines)

    # Final outro cleanup — filter stray bonus lines regardless of position
    outro_lines = [
        l for l in outro_lines
        if not ("optional" in l.lower() and "highly recommended" in l.lower())
        and "--- bonus days" not in l.lower()
        and not l.lower().startswith("--- bonus")
    ]
    outro = " ".join(outro_lines)

    # ── Render intro ──
    if intro:
        st.markdown(f'<div class="plan-intro">{intro}</div>', unsafe_allow_html=True)

    # ── Render day expanders ──
    bonus_banner_shown = False
    for i, (day_title, day_content, is_bonus) in enumerate(days):

        if is_bonus and not bonus_banner_shown:
            # Show bonus section banner before the first bonus day
            st.markdown("""
                <div style="
                    margin: 1.2rem 0 0.8rem;
                    padding: 0.75rem 1rem;
                    background: linear-gradient(135deg, rgba(108,99,255,0.15), rgba(167,139,250,0.1));
                    border: 1px solid rgba(108,99,255,0.35);
                    border-radius: 10px;
                    text-align: center;
                ">
                    <span style="font-family:'Space Grotesk',sans-serif; font-size:0.7rem;
                                 font-weight:600; letter-spacing:0.12em; text-transform:uppercase; color:#6C63FF;">
                        ✦ Bonus Days
                    </span>
                    <p style="margin:0.3rem 0 0; color:#8B87C0; font-size:0.8rem;">
                        Optional — but highly recommended if you want to go further.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            bonus_banner_shown = True

        elif i > 0:
            # Thin divider between regular days
            st.markdown('<hr class="day-divider">', unsafe_allow_html=True)

        icon = "⭐" if is_bonus else "📅"
        with st.expander(f"{icon} {day_title}", expanded=True):
            st.markdown(day_content)

    # ── Render outro ──
    if outro:
        st.markdown(f'<div class="plan-outro">{outro}</div>', unsafe_allow_html=True)