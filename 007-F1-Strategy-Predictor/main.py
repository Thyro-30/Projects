from simulation.monte_carlo import run_monte_carlo

strategies = [
    [("SOFT", 12), ("MEDIUM", 20), ("HARD", 20)],
    [("MEDIUM", 26), ("HARD", 26)],
    [("SOFT", 15), ("SOFT", 15), ("MEDIUM", 22)],
    [("HARD", 52)],
    [("MEDIUM", 17), ("MEDIUM", 17), ("HARD", 18)]
]

if __name__ == "__main__":
    print("Running Monte Carlo Strategy Comparison (GPU)...")
    results = run_monte_carlo(strategies, runs=500)

    results.sort(key=lambda x: x["average_time"])

    for r in results:
        print(f"\nStrategy: {r['strategy']}")
        print(f"Avg Time: {r['average_time']:.2f}s ± {r['std_dev']:.2f}")

    best = results[0]
    print("\nBest Strategy:")
    print(f"{best['strategy']} with avg time {best['average_time']:.2f} seconds")
