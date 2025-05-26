import pandas as pd

dataset = pd.read_csv("data/questions.csv")

print(dataset.isnull().sum())
dataset.fillna("null", inplace=True)
dataset.to_csv("data/questions.csv", index=False)

# print(dataset["answer"].isnull().sum())
# dataset["answer"] = dataset["answer"].fillna("null").astype(str)