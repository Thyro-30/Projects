import streamlit as st
import subprocess
import pandas as pd
import json
from simulation.generate_strategies import generate_legal_strategies
from simulation.monte_carlo import run_monte_carlo

st.set_page_config(page_title="F1 Strategy Predictor", layout="centered")
st.title("F1 Strategy Predictor")

track_options = [
    "Albert Park", "Jeddah", "Bahrain", "Imola", "Monaco", "Barcelona", "Silverstone",
    "Hungaroring", "Spa-Francorchamps", "Zandvoort", "Monza", "Singapore", "Suzuka",
    "Austin", "Mexico City", "Interlagos", "Las Vegas", "Yas Marina"
]

track = st.selectbox("Select a Grand Prix track:", sorted(track_options))


st.markdown("### Available Tyres (including used tyres from qualifying)")
tyre_input = st.text_area(
    "Enter tyres as a list of dictionaries:",
    value='''[
  {"compound": "SOFT", "used_laps": 0},
  {"compound": "SOFT", "used_laps": 10},
  {"compound": "MEDIUM", "used_laps": 0},
  {"compound": "HARD", "used_laps": 0}
]''')

try:
    available_tyres = json.loads(tyre_input)
except:
    st.error("Invalid tyre input format. Must be a valid list of dictionaries.")
    st.stop()

runs = st.slider("Monte Carlo runs per strategy", 100, 1000, 300, step=100)

if st.button("Run Full Strategy Prediction"):
    with st.spinner("Collecting data and training model for selected track..."):
        subprocess.run(["python", "data/collect_data.py", track])
        subprocess.run(["python", "models/train_lap_time_model.py", track])

    st.write("Generating legal strategies...")
    strategies = generate_legal_strategies(available_tyres)
    st.write(f"Generated {len(strategies)} legal strategies.")

    st.write("Running Monte Carlo simulations...")
    results = run_monte_carlo(strategies, runs=runs, track=track)
    results = [r for r in results if r['average_time'] < 99999]
    results.sort(key=lambda x: x['average_time'])

    st.markdown("### Top 3 Strategies")
    for i, r in enumerate(results[:3]):
        st.markdown(f"**{i+1}.** {r['strategy']} → {r['average_time']:.2f}s ± {r['std_dev']:.2f}")

    import matplotlib.pyplot as plt
    labels = [str(r['strategy']) for r in results[:10]]
    times = [r['average_time'] for r in results[:10]]
    fig, ax = plt.subplots()
    ax.barh(labels, times)
    ax.set_xlabel("Average Race Time (s)")
    ax.set_title("Top Strategies")
    st.pyplot(fig)
