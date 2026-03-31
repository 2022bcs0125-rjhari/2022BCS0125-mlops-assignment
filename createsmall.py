import pandas as pd

df = pd.read_csv("data/train.csv")
df.sample(2000, random_state=42).to_csv("data/train_small.csv", index=False)