import streamlit as st
from simulation.race_simulator import simulate_race
import numpy as np

def run_monte_carlo(strategies, runs=500, track = "Silverstone"):
    results = []
    total_tasks = len(strategies) * runs
    progress = st.progress(0)
    task_count = 0

    for strat in strategies:
        times = []
        for _ in range(runs):
            total_time, laps = simulate_race(strat, track=track)
            if laps == 52:
                times.append(total_time)

            task_count += 1
            progress.progress(task_count / total_tasks)

        avg_time = np.mean(times)
        std_time = np.std(times)
        results.append({
            "strategy": strat,
            "average_time": avg_time,
            "std_dev": std_time
        })

    progress.empty()
    return results
