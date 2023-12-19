import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier, plot_tree
import matplotlib.pyplot as plt
# import graphviz

df = pd.read_csv('tables/dataset.csv')
df = df.dropna()

# Separate features and target variable
X = df.drop('death', axis=1)
y = df['death']

# Encode categorical variables using LabelEncoder
label_encoder = LabelEncoder()
X_encoded = X.apply(label_encoder.fit_transform)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# Initialize XGBoost classifier with scale_pos_weight
scale_pos_weight = len(y_train[y_train == 0]) / len(y_train[y_train == 1])
xgb_classifier = XGBClassifier(objective='binary:logistic', scale_pos_weight=scale_pos_weight, random_state=42)

# Train the classifier
xgb_classifier.fit(X_train, y_train)

# Make predictions on the test set
y_pred = xgb_classifier.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

# Display classification report
print('Classification Report:\n', classification_report(y_test, y_pred))

# plt.figure(figsize=(20, 10))
# plot_tree(xgb_classifier, num_trees=0, rankdir='LR')
# plt.show()
