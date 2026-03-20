🧠 StudyOS — AI Exam Planner

An intelligent, adaptive study planner built with Streamlit. Generate personalized study schedules, visualize your workload, and get AI-powered insights — all from a sleek, animated dashboard.

✨ Features

Smart Study Plan Generator — Enter your subjects, daily study hours, and exam date to instantly generate a full day-by-day schedule
Adaptive Difficulty Weights — Hours are distributed intelligently across subjects using a weighted normalization system
Interactive Dashboard — Live metrics, donut charts, weekly load bar charts, and a scrollable schedule table
Subject Pill Tags — Color-coded subject badges for quick visual identification
Study Science Tips — Built-in evidence-based study strategies (spaced repetition, Pomodoro, active recall, and more)
Pro UI with Animations — Glass-morphism cards, CSS keyframe animations, gradient accents, and a fully dark-themed interface


📸 Preview
Input PanelDashboardConfigure subjects, hours & exam dateMetrics, charts & full schedule

🚀 Getting Started
Prerequisites

Python 3.8 or higher
pip

Installation

Clone the repository

bashgit clone https://github.com/your-username/studyos-ai-planner.git
cd studyos-ai-planner

Create a virtual environment (recommended)

bashpython -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

Install dependencies

bashpip install -r requirements.txt

Run the app

bashstreamlit run app.py

Open your browser at http://localhost:8501


📦 Requirements
streamlit>=1.28.0
pandas
matplotlib
numpy
Or install directly:
bashpip install streamlit pandas matplotlib numpy

🗂️ Project Structure
studyos-ai-planner/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── .gitignore              # Git ignore file

🧩 How It Works

Enter your subjects — comma-separated (e.g. Mathematics, Physics, Chemistry)
Set your daily study hours — using the slider (1–12 hours)
Pick your exam date — the app calculates days remaining automatically
Hit Generate — the planner builds a full schedule, distributes hours across subjects using weighted normalization, and renders the dashboard

Weighted Hour Distribution
Each subject is assigned a random weight between 0.8 and 1.5, then normalized so the total daily hours always equals your target — no matter how many subjects you have.
pythonnorm_weights = [w / total_weight for w in weights]
hours = hours_per_day * norm_weights[i]

📊 Dashboard Sections
SectionDescriptionMetric CardsTotal hours, days left, subject count, daily averageFull Schedule TableDay-by-day breakdown with progress bars per subjectSubject DistributionDonut chart showing proportion of hours per subjectWeekly LoadBar chart showing total study hours per weekStudy Tips5 evidence-based study strategy cards

🛠️ Built With

Streamlit — App framework
Pandas — Data manipulation
Matplotlib — Charts and visualizations
NumPy — Numerical operations
Google Fonts — Syne & DM Sans typography
