import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
data = pd.read_csv("dataset/student_data.csv")

# Features and Target
X = data[['coding_skill','hours_spent','projects_completed','attendance']]
y = data['success']

# Split data
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train,y_train)

# Save model
joblib.dump(model,"model.pkl")
print("Model trained and saved as model.pkl")