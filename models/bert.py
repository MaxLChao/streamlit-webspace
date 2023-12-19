# Import necessary libraries
import pandas as pd
import torch
from tqdm import tqdm
from transformers import BertTokenizer, BertForSequenceClassification, AdamW, Trainer, TrainingArguments
from datasets import load_dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

df = pd.read_csv('tables/dataset.csv')
df = df.dropna(ignore_index=True)

text = []

for i in tqdm(df.index):
    gender, race, _, age, value, status, condition, discharge = df.loc[i, :].values.flatten().tolist()
    t = f"There is a {age} years old {gender.lower()} {race.lower()} patient has {condition}, and the condition source value is {value} and the condition status is {status.lower()}, the patient is {discharge.lower()}"
    text.append(t)

df['text'] = text

# Split the data into training and testing sets
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Load ClinicalBERT model and tokenizer
model_name = "emilyalsentzer/Bio_ClinicalBERT"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)  # Assuming binary classification

# Tokenize the input data
train_encodings = tokenizer(train_df['text'].tolist(), truncation=True, padding=True, return_tensors='pt')
test_encodings = tokenizer(test_df['text'].tolist(), truncation=True, padding=True, return_tensors='pt')

# Prepare PyTorch datasets
class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = CustomDataset(train_encodings, train_df['death'].tolist())
test_dataset = CustomDataset(test_encodings, test_df['death'].tolist())

# Define training arguments
training_args = TrainingArguments(
    output_dir="./clinicalbert_binary_classification",
    evaluation_strategy="epoch",
    per_device_train_batch_size=128,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
)

# Instantiate Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

# Train the model
trainer.train()

# Evaluate the model
results = trainer.evaluate()
print(results)

# Make predictions on the test set
predictions = trainer.predict(test_dataset)
y_pred = predictions.predictions.argmax(axis=1)

# Evaluate the model
accuracy = accuracy_score(test_df['death'].tolist(), y_pred)
print(f'Accuracy: {accuracy:.2f}')

# Display classification report
print('Classification Report:\n', classification_report(test_df['death'].tolist(), y_pred))

def get_bert_embeddings(sentence):
    inputs = tokenizer(sentence, return_tensors="pt").to('cuda')
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.hidden_states.mean(dim=1).squeeze().numpy()
    return embeddings

embeddings = [get_bert_embeddings(sentence) for sentence in test_df['text']]

tsne = TSNE(n_components=2, random_state=42)
embeddings_2d = tsne.fit_transform(embeddings)

# Visualize the embeddings with color-coded labels
plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], c=test_df['death'], cmap='viridis')
for i, sentence in enumerate(sentences):
    plt.annotate(sentence, (embeddings_2d[i, 0], embeddings_2d[i, 1]))

plt.title("t-SNE Visualization of BERT Sentence Embeddings with Labels")
plt.colorbar(label='Labels')
plt.savefig('t-SNE.pdf')

