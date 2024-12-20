import pandas as pd

df = pd.read_parquet("hf://datasets/Prazzwal07/soil_data/data/train-00000-of-00001.parquet")
# save df to csv
df.to_csv("soil_data.csv", index=False)