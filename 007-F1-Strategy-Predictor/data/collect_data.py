import fastf1
import pandas as pd
import os

def load_race_data_by_track(track_name, years=[2023, 2024]):
    all_data = []
    for year in years:
        session = fastf1.get_session(year, track_name, "R")
        session.load()
        laps = session.laps
        laps = laps.loc[laps['PitOutTime'].notnull() | laps['PitInTime'].notnull()]
        tyre_data = laps[['Driver', 'LapNumber', 'Compound', 'FreshTyre', 'TyreLife', 'LapTime', 'TrackStatus']]
        tyre_data["Year"] = year
        tyre_data["Track"] = track_name
        all_data.append(tyre_data)

    df = pd.concat(all_data)
    out_path = f"data/tyre_data_{track_name.lower()}.csv"
    df.to_csv(out_path, index=False)
    print(f"Tyre data for {track_name} saved to {out_path}")
    return out_path

if __name__ == "__main__":
    import sys
    track = sys.argv[1] if len(sys.argv) > 1 else "Silverstone"
    load_race_data_by_track(track)