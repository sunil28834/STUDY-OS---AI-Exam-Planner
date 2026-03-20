import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
from datetime import datetime
import random

st.set_page_config(page_title="StudyOS — AI Planner", layout="wide", page_icon="🧠")

# ─────────────────────────────────────────────
# GLOBAL CSS + ANIMATIONS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
    background: #080b14;
    color: #e8eaf0;
    font-family: 'DM Sans', sans-serif;
    min-height: 100vh;
}

/* Animated starfield background */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 20% 0%, rgba(99,102,241,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 100%, rgba(56,189,248,0.10) 0%, transparent 55%),
        radial-gradient(ellipse 40% 30% at 60% 50%, rgba(168,85,247,0.07) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

/* ── Particle Grid ── */
.grid-overlay {
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(99,102,241,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.04) 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none;
    z-index: 0;
}

/* ── Header ── */
.hero-section {
    position: relative;
    text-align: center;
    padding: 56px 20px 40px;
    z-index: 1;
}

.hero-badge {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.35);
    color: #a5b4fc;
    font-family: 'DM Sans', monospace;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 3px;
    text-transform: uppercase;
    padding: 6px 18px;
    border-radius: 100px;
    margin-bottom: 20px;
    animation: fadeSlideDown 0.6s ease both;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(40px, 6vw, 72px);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -2px;
    animation: fadeSlideDown 0.7s 0.1s ease both;
    margin-bottom: 14px;
}

.hero-title span.grad {
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 45%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-subtitle {
    font-size: 16px;
    color: #64748b;
    font-weight: 300;
    letter-spacing: 0.3px;
    animation: fadeSlideDown 0.7s 0.2s ease both;
    max-width: 480px;
    margin: 0 auto;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.3), transparent);
    margin: 0 auto 36px;
    max-width: 700px;
    animation: expandWidth 0.8s 0.4s ease both;
}

/* ── Glass Panel ── */
.panel {
    background: rgba(15,20,40,0.65);
    border: 1px solid rgba(255,255,255,0.07);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 22px;
    position: relative;
    overflow: hidden;
    animation: fadeSlideUp 0.6s ease both;
    z-index: 1;
}

.panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.5), rgba(56,189,248,0.5), transparent);
}

.panel-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 10px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #4f6080;
    margin-bottom: 18px;
    font-weight: 500;
}

/* ── Section Title ── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #e8eaf0;
    letter-spacing: -0.5px;
    margin-bottom: 6px;
    animation: fadeSlideUp 0.5s ease both;
    position: relative;
    z-index: 1;
}

/* ── Metric Cards ── */
.metrics-row {
    display: flex;
    gap: 16px;
    margin-bottom: 24px;
    flex-wrap: wrap;
    animation: fadeSlideUp 0.7s 0.1s ease both;
    position: relative;
    z-index: 1;
}

.metric-card {
    flex: 1;
    min-width: 160px;
    background: rgba(15,20,40,0.7);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 20px 22px;
    position: relative;
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.5);
}

.metric-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 0 0 16px 16px;
}

.metric-card.blue::after   { background: linear-gradient(90deg, #38bdf8, #0ea5e9); }
.metric-card.violet::after { background: linear-gradient(90deg, #818cf8, #6366f1); }
.metric-card.purple::after { background: linear-gradient(90deg, #c084fc, #a855f7); }
.metric-card.teal::after   { background: linear-gradient(90deg, #2dd4bf, #14b8a6); }

.metric-label {
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #4f6080;
    font-weight: 500;
    margin-bottom: 8px;
}

.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 32px;
    font-weight: 800;
    letter-spacing: -1px;
    line-height: 1;
}

.metric-value.blue   { color: #38bdf8; }
.metric-value.violet { color: #818cf8; }
.metric-value.purple { color: #c084fc; }
.metric-value.teal   { color: #2dd4bf; }

.metric-sub {
    font-size: 12px;
    color: #4f6080;
    margin-top: 4px;
}

/* ── Table Styling ── */
.stDataFrame {
    background: transparent !important;
}

/* ── Button ── */
.stButton > button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    letter-spacing: 0.3px !important;
    background: linear-gradient(135deg, #6366f1, #38bdf8) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 14px 36px !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    position: relative !important;
    overflow: hidden !important;
    text-transform: uppercase !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 40px rgba(99,102,241,0.5), 0 12px 30px rgba(0,0,0,0.4) !important;
}

.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── Inputs ── */
.stTextArea textarea,
.stDateInput input,
.stSlider [data-baseweb] {
    background: rgba(15,20,40,0.8) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    color: #e8eaf0 !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border-color 0.2s !important;
}

.stTextArea textarea:focus,
.stDateInput input:focus {
    border-color: rgba(99,102,241,0.5) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
}

label, .stSlider label {
    color: #8899bb !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0.3px !important;
}

/* ── Slider accent ── */
.stSlider [data-baseweb="slider"] [role="slider"] {
    background: #6366f1 !important;
    box-shadow: 0 0 12px rgba(99,102,241,0.6) !important;
}

/* ── Alerts ── */
.stWarning, .stError {
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 30px 0 50px;
    color: #2a3550;
    font-size: 12px;
    letter-spacing: 1px;
    position: relative;
    z-index: 1;
}

/* ── Animations ── */
@keyframes fadeSlideDown {
    from { opacity: 0; transform: translateY(-18px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes expandWidth {
    from { width: 0%; opacity: 0; }
    to   { width: 100%; opacity: 1; }
}

@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 20px rgba(99,102,241,0.3); }
    50%       { box-shadow: 0 0 40px rgba(99,102,241,0.6); }
}

@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position: 200% center; }
}

/* ── Progress bar ── */
.progress-wrap {
    background: rgba(255,255,255,0.05);
    border-radius: 100px;
    height: 6px;
    overflow: hidden;
    margin-top: 6px;
}

.progress-fill {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, #6366f1, #38bdf8);
    background-size: 200% 100%;
    animation: shimmer 2s infinite linear;
}

/* ── Subject pill tags ── */
.subject-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 12px;
    position: relative;
    z-index: 1;
    animation: fadeSlideUp 0.8s 0.2s ease both;
}

.pill {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 100px;
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.3px;
    animation: fadeSlideUp 0.5s ease both;
}

/* ── Column layout fix ── */
[data-testid="column"] {
    gap: 16px;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 1200px; }

</style>

<!-- Animated grid overlay -->
<div class="grid-overlay"></div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-section">
    <div class="hero-badge">✦ AI-Powered Learning OS</div>
    <div class="hero-title">
        <span class="grad">StudyOS</span><br>
        <span style="color:#e8eaf0;font-size:0.65em;letter-spacing:-1px;">Intelligent Exam Planner</span>
    </div>
    <div class="hero-subtitle">
        Plan smarter. Study deeper. Ace every exam with an adaptive schedule built around your goals.
    </div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# INPUT PANEL
# ─────────────────────────────────────────────
st.markdown("<div class='panel'>", unsafe_allow_html=True)
st.markdown("<div class='panel-label'>⬡ Configure Your Plan</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    subjects = st.text_area(
        "Subjects",
        placeholder="e.g. Mathematics, Physics, Chemistry, English",
        height=100,
        help="Separate multiple subjects with commas"
    )

with col2:
    hours_per_day = st.slider("Daily Study Hours", 1, 12, 4, help="How many hours can you study each day?")

with col3:
    exam_date = st.date_input("Exam Date", help="When is your exam?")

st.markdown("<br>", unsafe_allow_html=True)
generate = st.button("⚡ Generate My Study Plan", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PLAN GENERATION
# ─────────────────────────────────────────────
if generate:

    if not subjects.strip():
        st.warning("⚠️ Please enter at least one subject to continue.")
    else:
        subject_list = [s.strip() for s in subjects.split(",") if s.strip()]
        today = datetime.today().date()
        days_left = (exam_date - today).days

        if days_left <= 0:
            st.error("🗓 Please select a future exam date.")
        else:
            # ── Smart weights ──
            random.seed(42)
            weights = [random.uniform(0.8, 1.5) for _ in subject_list]
            total_weight = sum(weights)
            norm_weights = [w / total_weight for w in weights]

            plan = []
            for day in range(days_left):
                for i, subject in enumerate(subject_list):
                    hours = hours_per_day * norm_weights[i]
                    plan.append({
                        "Day": day + 1,
                        "Date": str(today + pd.Timedelta(days=day)),
                        "Subject": subject,
                        "Hours": round(hours, 2),
                        "Sessions": max(1, round(hours / 1.5))
                    })

            df = pd.DataFrame(plan)
            total_hours = round(df["Hours"].sum(), 1)
            avg_daily = round(df.groupby("Day")["Hours"].sum().mean(), 1)

            # ── Pill colors ──
            PILL_COLORS = [
                ("rgba(56,189,248,0.15)", "#38bdf8"),
                ("rgba(129,140,248,0.15)", "#818cf8"),
                ("rgba(192,132,252,0.15)", "#c084fc"),
                ("rgba(45,212,191,0.15)", "#2dd4bf"),
                ("rgba(251,191,36,0.15)", "#fbbf24"),
                ("rgba(251,113,133,0.15)", "#fb7185"),
            ]

            pill_html = ""
            for i, s in enumerate(subject_list):
                bg, col = PILL_COLORS[i % len(PILL_COLORS)]
                pill_html += f'<span class="pill" style="background:{bg};color:{col};border:1px solid {col}33;">{s}</span>'

            # ── Metric cards ──
            card_colors = ["blue", "violet", "purple", "teal"]
            card_data = [
                ("TOTAL HOURS", f"{total_hours}", "hrs planned", "blue"),
                ("DAYS LEFT", f"{days_left}", "until exam", "violet"),
                ("SUBJECTS", f"{len(subject_list)}", "topics covered", "purple"),
                ("DAILY AVG", f"{avg_daily}h", "per day", "teal"),
            ]

            metric_html = '<div class="metrics-row">'
            for label, value, sub, color in card_data:
                pct = min(100, int(float(value.replace('h','')) / max(1, total_hours) * 400))
                metric_html += f"""
                <div class="metric-card {color}">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value {color}">{value}</div>
                    <div class="metric-sub">{sub}</div>
                    <div class="progress-wrap"><div class="progress-fill" style="width:{pct}%"></div></div>
                </div>"""
            metric_html += "</div>"

            st.markdown(metric_html, unsafe_allow_html=True)
            st.markdown(f'<div class="subject-pills">{pill_html}</div><br>', unsafe_allow_html=True)

            # ── Dashboard ──
            col_table, col_charts = st.columns([3, 2])

            with col_table:
                st.markdown("<div class='panel'>", unsafe_allow_html=True)
                st.markdown("<div class='panel-label'>⬡ Full Schedule</div>", unsafe_allow_html=True)

                display_df = df[["Day", "Date", "Subject", "Hours", "Sessions"]].copy()
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    height=420,
                    hide_index=True,
                    column_config={
                        "Day": st.column_config.NumberColumn("Day", width="small"),
                        "Date": st.column_config.TextColumn("Date"),
                        "Subject": st.column_config.TextColumn("Subject"),
                        "Hours": st.column_config.ProgressColumn("Hours", min_value=0, max_value=hours_per_day),
                        "Sessions": st.column_config.NumberColumn("Sessions", width="small"),
                    }
                )
                st.markdown("</div>", unsafe_allow_html=True)

            with col_charts:

                # ── PIE CHART ──
                st.markdown("<div class='panel'>", unsafe_allow_html=True)
                st.markdown("<div class='panel-label'>⬡ Subject Distribution</div>", unsafe_allow_html=True)

                subject_totals = df.groupby("Subject")["Hours"].sum()
                pie_colors = ["#38bdf8","#818cf8","#c084fc","#2dd4bf","#fbbf24","#fb7185","#34d399"][:len(subject_list)]

                fig1, ax1 = plt.subplots(figsize=(5, 4))
                fig1.patch.set_facecolor('#0d1424')
                ax1.set_facecolor('#0d1424')

                wedges, texts, autotexts = ax1.pie(
                    subject_totals.values,
                    labels=subject_totals.index,
                    autopct='%1.0f%%',
                    startangle=140,
                    colors=pie_colors,
                    pctdistance=0.75,
                    wedgeprops=dict(width=0.55, edgecolor='#080b14', linewidth=2.5),
                    textprops=dict(color='#8899bb', fontsize=9)
                )
                for at in autotexts:
                    at.set_color('#e8eaf0')
                    at.set_fontsize(9)
                    at.set_fontweight('bold')

                ax1.set_title("Hours per Subject", color='#4f6080', fontsize=10, pad=12)
                plt.tight_layout()
                st.pyplot(fig1)
                plt.close(fig1)
                st.markdown("</div>", unsafe_allow_html=True)

                # ── WEEKLY BAR CHART ──
                st.markdown("<div class='panel'>", unsafe_allow_html=True)
                st.markdown("<div class='panel-label'>⬡ Weekly Load</div>", unsafe_allow_html=True)

                df["Week"] = ((df["Day"] - 1) // 7) + 1
                weekly = df.groupby("Week")["Hours"].sum().reset_index()
                weeks_to_show = weekly.head(6)

                fig2, ax2 = plt.subplots(figsize=(5, 3))
                fig2.patch.set_facecolor('#0d1424')
                ax2.set_facecolor('#0d1424')

                bar_colors = ["#6366f1" if i < len(weeks_to_show) - 1 else "#38bdf8"
                              for i in range(len(weeks_to_show))]

                bars = ax2.bar(
                    [f"W{int(w)}" for w in weeks_to_show["Week"]],
                    weeks_to_show["Hours"],
                    color=bar_colors,
                    width=0.55,
                    edgecolor='none',
                    zorder=3
                )

                ax2.set_facecolor('#0d1424')
                ax2.spines[:].set_visible(False)
                ax2.tick_params(colors='#4f6080', labelsize=9)
                ax2.yaxis.set_tick_params(labelleft=False, left=False)
                ax2.set_ylabel("")
                ax2.grid(axis='y', color=(1, 1, 1, 0.04), linewidth=0.8, zorder=0)

                for bar in bars:
                    h = bar.get_height()
                    ax2.text(
                        bar.get_x() + bar.get_width() / 2,
                        h + 0.5,
                        f"{int(h)}h",
                        ha='center', va='bottom',
                        color='#8899bb', fontsize=8
                    )

                plt.tight_layout()
                st.pyplot(fig2)
                plt.close(fig2)
                st.markdown("</div>", unsafe_allow_html=True)

            # ── TIPS PANEL ──
            TIPS = [
                ("🧠", "Spaced Repetition", "Review each subject at increasing intervals: Day 1 → Day 3 → Day 7 → Day 14."),
                ("🎯", "Pomodoro Sessions", "Study in 25-min focused bursts with 5-min breaks to maintain peak concentration."),
                ("📝", "Active Recall", "Test yourself after every session — retrieval practice beats passive re-reading."),
                ("🌙", "Sleep to Consolidate", "Memory consolidation happens during sleep. Don't sacrifice rest for extra hours."),
                ("📊", "Track Progress", "Check off completed sessions daily to build momentum and stay accountable."),
            ]

            st.markdown("<div class='section-title' style='margin-bottom:14px;'>✦ Study Science Tips</div>", unsafe_allow_html=True)

            tip_cols = st.columns(len(TIPS))
            for col, (icon, title, desc) in zip(tip_cols, TIPS):
                with col:
                    st.markdown(f"""
                    <div class="panel" style="padding:18px;text-align:center;min-height:140px;animation-delay:0.1s;">
                        <div style="font-size:22px;margin-bottom:8px;">{icon}</div>
                        <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;color:#818cf8;margin-bottom:6px;">{title}</div>
                        <div style="font-size:11.5px;color:#4f6080;line-height:1.5;">{desc}</div>
                    </div>
                    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# EMPTY STATE
# ─────────────────────────────────────────────
else:
    st.markdown("""
    <div style="text-align:center;padding:60px 20px;position:relative;z-index:1;">
        <div style="font-size:56px;margin-bottom:16px;opacity:0.4;">🎓</div>
        <div style="font-family:'Syne',sans-serif;font-size:18px;color:#2a3550;font-weight:700;">
            Fill in your subjects & exam date above<br>
            <span style="font-size:14px;font-weight:400;">and hit Generate to build your plan</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class='footer'>
    STUDYOS · AI EXAM PLANNER · BUILT WITH STREAMLIT
</div>
""", unsafe_allow_html=True)