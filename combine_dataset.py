import pandas as pd

# ISOT Dataset
fake = pd.read_csv("Fake.csv", on_bad_lines='skip')
true = pd.read_csv("True.csv", on_bad_lines='skip')

fake["label"] = 0
true["label"] = 1

isot_data = pd.concat([fake, true], ignore_index=True)
isot_data = isot_data[['title', 'text', 'label']]

# WELFake Dataset - label flip pannurom!
welfake = pd.read_csv("WELFake_Dataset.csv", on_bad_lines='skip')
welfake = welfake[['title', 'text', 'label']]

# 1=Fake → 0, 0=Real → 1 (flip pannurom)
welfake['label'] = welfake['label'].map({1: 0, 0: 1})

# Null values handle
welfake['title'] = welfake['title'].fillna('')
welfake['text'] = welfake['text'].fillna('')

# Combine all
data = pd.concat([isot_data, welfake], ignore_index=True)
data = data.sample(frac=1, random_state=42).reset_index(drop=True)
data.to_csv("combined_fake_news_dataset.csv", index=False)

print(f"Total dataset size: {len(data)}")
print(f"Fake: {(data['label']==0).sum()}")
print(f"Real: {(data['label']==1).sum()}")
print("Combined dataset created ✅")
