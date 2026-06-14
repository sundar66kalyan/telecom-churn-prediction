import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier

print("🔧 Creating telecom churn model files...")

feature_list = ['account_length', 'international_plan', 'vmail_plan', 'vmail_message', 
                'day_mins', 'day_calls', 'eve_mins', 'eve_calls', 'night_mins', 
                'night_calls', 'intl_mins', 'intl_calls', 'custserv_calls']

X_sample = np.random.rand(1000, len(feature_list))
y_sample = np.random.randint(0, 2, 1000)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_sample, y_sample)

with open('telecom_churn_model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('feature_list.pkl', 'wb') as f:
    pickle.dump(feature_list, f)

print("✅ Model files created successfully!")
print(f"   - Features: {len(feature_list)}")
