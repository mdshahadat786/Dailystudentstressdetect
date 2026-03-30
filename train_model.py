import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier

# Load dataset
data = pd.read_csv("stress.csv")

# Simulated Federated Split
client1 = data.sample(frac=0.33, random_state=1)
remaining = data.drop(client1.index)
client2 = remaining.sample(frac=0.5, random_state=2)
client3 = remaining.drop(client2.index)

# In a real federated setup, we aggregate. 
# Here, we simulate by training a global model on the full knowledge.
X = data.drop("Stress", axis=1)
y = data["Stress"]

global_model = RandomForestClassifier(n_estimators=100, random_state=42)
global_model.fit(X, y)

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(global_model, f)

print("Federated Global Model Created and Saved.")