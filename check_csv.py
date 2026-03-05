import pandas as pd

# Load CSVs
fake = pd.read_csv("Fake.csv")
true = pd.read_csv("True.csv")

# Show top 5 rows
print("=== Fake News Sample ===")
print(fake.head())

print("\n=== Real News Sample ===")
print(true.head())