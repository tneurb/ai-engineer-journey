from datasets import load_dataset
from collections import Counter
import re
import html
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
import mlflow

mlflow.set_experiment("ag-news-classifier")

dataset = load_dataset("fancyzhx/ag_news")
print(dataset)
print(dataset["train"][0])



def tokenize(text):
    text = clean_text(text)
    text = text.lower()
    return re.findall(r"\b\w+\b", text)


def clean_text(text):
    text = text.replace("#39;", "'")   # fix the broken apostrophe entity
    text = text.replace("&lt;", "<").replace("&gt;", ">")  # fix other common broken entities
    text = html.unescape(text)          # catch any properly-formed HTML entities too
    return text

# Build vocabulary from the training set
counter = Counter()
for example in dataset["train"]:
    counter.update(tokenize(example["text"]))

print(f"Total unique words found: {len(counter)}")
print("Top 10 most common words:", counter.most_common(10))

# Keep only reasonably common words - very rare words add noise without much benefit
vocab_size = 10000
most_common_words = counter.most_common(vocab_size)

# Build word -> number lookup. Reserve 0 for "unknown word" and 1 for "padding"
word_to_idx = {"<UNK>": 0, "<PAD>": 1}
for word, count in most_common_words:
    word_to_idx[word] = len(word_to_idx)

print(f"Vocabulary size: {len(word_to_idx)}")
print("Index for 'the':", word_to_idx.get("the"))
print("Index for 'reuters':", word_to_idx.get("reuters"))

def text_to_indices(text, word_to_idx, max_len=30):
    tokens = tokenize(text)
    indices = [word_to_idx.get(token, word_to_idx["<UNK>"]) for token in tokens]
    
    # Truncate if too long, pad if too short
    if len(indices) > max_len:
        indices = indices[:max_len]
    else:
        indices = indices + [word_to_idx["<PAD>"]] * (max_len - len(indices))
    
    return indices

sample_text = dataset["train"][0]["text"]
print("Original:", sample_text)
print("As indices:", text_to_indices(sample_text, word_to_idx))



def prepare_dataset(hf_dataset, word_to_idx, max_len=30):
    all_indices = []
    all_labels = []
    for example in hf_dataset:
        indices = text_to_indices(example["text"], word_to_idx, max_len)
        all_indices.append(indices)
        all_labels.append(example["label"])
    return torch.tensor(all_indices), torch.tensor(all_labels)

train_X, train_y = prepare_dataset(dataset["train"], word_to_idx)
test_X, test_y = prepare_dataset(dataset["test"], word_to_idx)

print("Train X shape:", train_X.shape)
print("Train y shape:", train_y.shape)
print("Test X shape:", test_X.shape)



class TextClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim=64, num_classes=4):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.fc = nn.Linear(embed_dim, num_classes)

    def forward(self, x):
        embedded = self.embedding(x)          # (batch, seq_len, embed_dim)
        pooled = embedded.mean(dim=1)          # average across the sequence -> (batch, embed_dim)
        output = self.fc(pooled)               # (batch, num_classes)
        return output

# model = TextClassifier(vocab_size=len(word_to_idx))
model = TextClassifier(vocab_size=len(word_to_idx), embed_dim=128)
print(model)

# Quick sanity test: run one batch through the untrained network
sample_batch = train_X[:5]
output = model(sample_batch)
print("Output shape:", output.shape)
print("Sample output (untrained, random):", output[0])



# Split off a small validation set from training data, to watch for overfitting
val_size = 10000
train_X_split, val_X = train_X[:-val_size], train_X[-val_size:]
train_y_split, val_y = train_y[:-val_size], train_y[-val_size:]

train_dataset = TensorDataset(train_X_split, train_y_split)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

val_dataset = TensorDataset(val_X, val_y)
val_loader = DataLoader(val_dataset, batch_size=64)

loss_fn = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

epochs = 5
with mlflow.start_run():
    mlflow.log_param("embed_dim", 128)
    mlflow.log_param("learning_rate", 0.001)
    mlflow.log_param("epochs", epochs)
    mlflow.log_param("batch_size", 64)

    for epoch in range(epochs):
        model.train()
        total_train_loss = 0
        for X_batch, y_batch in train_loader:
            optimizer.zero_grad()
            pred = model(X_batch)
            loss = loss_fn(pred, y_batch)
            loss.backward()
            optimizer.step()
            total_train_loss += loss.item()

        model.eval()
        total_val_loss = 0
        with torch.no_grad():
            for X_batch, y_batch in val_loader:
                pred = model(X_batch)
                loss = loss_fn(pred, y_batch)
                total_val_loss += loss.item()

        # calculate averages HERE, inside the loop, right after gathering totals
        avg_train_loss = total_train_loss / len(train_loader)
        avg_val_loss = total_val_loss / len(val_loader)

        mlflow.log_metric("train_loss", avg_train_loss, step=epoch)
        mlflow.log_metric("val_loss", avg_val_loss, step=epoch)
        print(f"Epoch {epoch+1}: train_loss={avg_train_loss:.4f}, val_loss={avg_val_loss:.4f}")

    # accuracy check happens AFTER training finishes, still inside the mlflow run
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for X_batch, y_batch in val_loader:
            pred = model(X_batch)
            predicted_labels = pred.argmax(dim=1)
            correct += (predicted_labels == y_batch).sum().item()
            total += y_batch.size(0)

    val_accuracy = correct / total
    mlflow.log_metric("val_accuracy", val_accuracy)
    print(f"Validation accuracy: {val_accuracy * 100:.2f}%")
    