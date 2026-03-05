import pandas as pd

# Load Kaggle CSVs safely
fake = pd.read_csv("Fake.csv", on_bad_lines='skip')
true = pd.read_csv("True.csv", on_bad_lines='skip')

# Add labels
fake["label"] = 0
true["label"] = 1

# Combine datasets
data = pd.concat([fake, true], ignore_index=True)

# Shuffle rows
data = data.sample(frac=1, random_state=42).reset_index(drop=True)

# Save as new CSV
data.to_csv("combined_fake_news_dataset.csv", index=False)
print("Combined dataset created ✅")