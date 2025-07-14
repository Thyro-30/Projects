import xgboost as xgb
import joblib
import pandas as pd
import numpy as np

TRACK_CONFIG = {} 


compound_lifespans = {
    "SOFT": 25,
    "MEDIUM": 35,
    "HARD": 45
}

compound_failure_thresholds = {
    "SOFT": 30,
    "MEDIUM": 40,
    "HARD": 55
}

def tyre_failure_probability(lap, compound):
    limit = compound_failure_thresholds[compound]
    if lap <= limit:
        return 0
    else:
        return min(0.03 * (lap - limit), 0.5) 

def get_degradation(compound, lap_in_stint):
    base_deg = {
        "SOFT": 0.02,
        "MEDIUM": 0.015,
        "HARD": 0.01
    }
    multipliers = {
        "SOFT": 1.2,
        "MEDIUM": 1.0,
        "HARD": 0.8
    }

    degradation = base_deg[compound] * (lap_in_stint ** 1.1) * multipliers[compound]

    safe_limit = compound_lifespans[compound]
    if lap_in_stint > safe_limit:
        over_wear = lap_in_stint - safe_limit
        penalty = 0.05 * (over_wear ** 1.5)
        degradation += penalty

    return degradation

def simulate_race(strategy, track="Silverstone"):
    model_path = f"models/lap_time_model_{track.lower()}.json"
    encoder_path = f"models/compound_encoder_{track.lower()}.pkl"

    encoder = joblib.load(encoder_path)
    model = xgb.Booster()
    model.load_model(model_path)

    total_time = 0
    lap_counter = 0
    laps_required = 52 
    pit_penalty = 20  

    for compound, stint_len, used_laps in strategy:
        compound = compound.upper()
        tyre_life = np.arange(used_laps + 1, used_laps + stint_len + 1)
        laps = lap_counter + tyre_life
        compound_list = [compound] * stint_len

        for lap_num in tyre_life:
            failure_chance = tyre_failure_probability(lap_num, compound)
            if np.random.rand() < failure_chance:
                return 99999, lap_counter 

        base_df = pd.DataFrame({
            "TyreLife": tyre_life,
            "Compound": compound_list,
            "LapNumber": laps
        })

        compound_encoded = encoder.transform(base_df[["Compound"]])
        compound_df = pd.DataFrame(compound_encoded, columns=encoder.get_feature_names_out(["Compound"]))

        X_final = pd.concat([
            base_df.drop(columns=["Compound"]).reset_index(drop=True),
            compound_df.reset_index(drop=True)
        ], axis=1)

        dmatrix = xgb.DMatrix(X_final)
        lap_times = model.predict(dmatrix)

        degradation = np.array([get_degradation(compound, lap) for lap in tyre_life])
        noise = np.random.normal(0, 0.4, size=stint_len)

        total_time += np.sum(lap_times + degradation + noise)
        total_time += pit_penalty
        lap_counter += stint_len

    return total_time, lap_counter
