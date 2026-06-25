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

/* ── Stars — pure CSS, no JS needed ── */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 0;
    background-image:
        radial-gradient(1px 1px at 10% 15%, rgba(255,255,255,0.7) 0%, transparent 100%),
        radial-gradient(1px 1px at 25% 60%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 40% 30%, rgba(255,255,255,0.8) 0%, transparent 100%),
        radial-gradient(1px 1px at 55% 80%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 70% 20%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 80% 55%, rgba(255,255,255,0.7) 0%, transparent 100%),
        radial-gradient(1px 1px at 90% 40%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 15% 85%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(2px 2px at 35% 10%, rgba(196,191,255,0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 60% 50%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 75% 90%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 5% 45%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 48% 70%, rgba(196,191,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 88% 10%, rgba(255,255,255,0.7) 0%, transparent 100%),
        radial-gradient(2px 2px at 20% 35%, rgba(255,255,255,0.3) 0%, transparent 100%),
        radial-gradient(1px 1px at 65% 5%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 92% 75%, rgba(196,191,255,0.4) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 30% 95%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 50% 25%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 8% 65%, rgba(255,255,255,0.6) 0%, transparent 100%);
    animation: twinkle-field 6s ease-in-out infinite alternate;
}
@keyframes twinkle-field {
    0%   { opacity: 0.6; }
    50%  { opacity: 1;   }
    100% { opacity: 0.7; }
}

/* ── Header ── */
.planit-header {
    text-align: center;
    padding: 3rem 1rem 2rem;
    position: relative;
    z-index: 1;
}
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
    color: #9B97D4;
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

/* ── Disable browser autocomplete dropdown ── */
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus {
    -webkit-box-shadow: 0 0 0px 1000px #12112a inset !important;
    -webkit-text-fill-color: #F0EEFF !important;
}
</style>

""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="planit-header">
    <span class="planit-planet">🪐</span>
    <div class="planit-logo">Planit</div>
    <div class="planit-tagline">Turn your goals into a <span>step-by-step plan</span></div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Clear flag: reset values BEFORE widgets render ────────────────────────────
if st.session_state.get("_do_clear"):
    st.session_state["goal"] = ""
    st.session_state["deadline"] = ""
    st.session_state["extra_details"] = ""
    st.session_state["level"] = "Beginner"
    st.session_state["_do_clear"] = False

# ── Input section ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    goal = st.text_input("What is your goal? 💫", placeholder="e.g. Learn Python, Build a portfolio", key="goal", autocomplete="off")
with col2:
    deadline = st.text_input("How much time do you have? ⏳", placeholder="e.g. 2 weeks, 1 month", key="deadline", autocomplete="off")

level = st.radio("Experience level 🚀", ["Beginner", "Intermediate", "Expert"], horizontal=True, key="level")

extra_details = st.text_area(
    "Any additional details? (Optional) ✍️",
    placeholder="e.g. I can study 1 hour a day, I have a gym membership, I prefer evenings",
    height=90,
    key="extra_details"
)

st.divider()

# ── Buttons ───────────────────────────────────────────────────────────────────
plan_generated = st.session_state.get("plan_generated", False)

if plan_generated:
    btn_left, btn_center, btn_right = st.columns([1, 3, 1])
    with btn_center:
        generate = st.button("✨ Generate My Plan", use_container_width=True)
    with btn_right:
        st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
        clear = st.button("✕ Clear", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    btn_left, btn_center, btn_right = st.columns([1, 2, 1])
    with btn_center:
        generate = st.button("✨ Generate My Plan", use_container_width=True)
    clear = False

if clear:
    st.session_state["_do_clear"] = True
    st.session_state["plan_generated"] = False
    st.session_state["plan_output"] = None
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
        st.session_state["plan_generated"] = True
        st.session_state["plan_output"] = plan

        progress_bar.progress(100)
        time.sleep(0.3)
        progress_bar.empty()
        progress_text.empty()
        st.rerun()

# ── Display stored plan ───────────────────────────────────────────────────────
if st.session_state.get("plan_output"):
    plan = st.session_state["plan_output"]
    lines = plan.strip().split("\n")
    intro_lines = []
    days = []
    outro_lines = []
    current_day = None
    current_day_content = []
    found_days = False
    in_bonus = False

    for line in lines:
        stripped = line.strip()
        is_bonus_marker = "bonus days" in stripped.lower() and "---" in stripped
        is_day_header = (
            stripped.lower().startswith("day ")
            and len(stripped) > 4
            and stripped[4:].split(":")[0].strip().isdigit()
        )
        if is_bonus_marker:
            if current_day:
                days.append((current_day, "\n".join(current_day_content).strip(), False))
                current_day = None
                current_day_content = []
            in_bonus = True
        elif is_day_header:
            if current_day:
                days.append((current_day, "\n".join(current_day_content).strip(), in_bonus))
            current_day = stripped
            current_day_content = []
            found_days = True
        elif found_days and current_day:
            current_day_content.append(line)
        elif found_days and not current_day:
            if stripped:
                outro_lines.append(stripped)
        else:
            if stripped:
                intro_lines.append(stripped)

    if current_day:
        days.append((current_day, "\n".join(current_day_content).strip(), in_bonus))

    intro = " ".join(intro_lines)
    outro = " ".join(outro_lines)

    if intro:
        st.markdown(f'<div class="plan-intro">{intro}</div>', unsafe_allow_html=True)

    bonus_banner_shown = False
    for i, (day_title, day_content, is_bonus) in enumerate(days):
        if is_bonus and not bonus_banner_shown:
            st.markdown("""
                <div style="
                    margin: 1.2rem 0 0.8rem;
                    padding: 0.75rem 1rem;
                    background: linear-gradient(135deg, rgba(108,99,255,0.15), rgba(167,139,250,0.1));
                    border: 1px solid rgba(108,99,255,0.35);
                    border-radius: 10px;
                    text-align: center;
                ">
                    <span style="font-family:'Space Grotesk',sans-serif; font-size:0.7rem; font-weight:600; letter-spacing:0.12em; text-transform:uppercase; color:#6C63FF;">
                        ✦ Bonus Days
                    </span>
                    <p style="margin:0.3rem 0 0; color:#8B87C0; font-size:0.8rem;">
                        Optional — but highly recommended if you want to go further.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            bonus_banner_shown = True
        elif i > 0:
            st.markdown('<hr class="day-divider">', unsafe_allow_html=True)

        with st.expander(f"{"⭐" if is_bonus else "📅"} {day_title}", expanded=True):
            st.markdown(day_content)

    if outro:
        st.markdown(f'<div class="plan-outro">{outro}</div>', unsafe_allow_html=True)