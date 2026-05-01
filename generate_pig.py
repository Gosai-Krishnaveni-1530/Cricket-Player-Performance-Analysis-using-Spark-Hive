import pandas as pd

df = pd.read_csv("data/final_cricket_data.csv")

result = df.groupby("Player").agg({
    "Runs_x": "sum",
    "Wkts": "sum",
    "Catches": "sum"
}).reset_index()

result.columns = ["Player", "Runs", "Wickets", "Catches"]

result.to_csv("output/pig_output.csv", index=False)

print("Pig output generated successfully")