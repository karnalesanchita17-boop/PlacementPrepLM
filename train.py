
from pathlib import Path
import re

import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

from model import PlacementPrepLM


# 1. Make training repeatable
torch.manual_seed(42)

if torch.cuda.is_available():
    torch.cuda.manual_seed_all(42)

# 2. Select the available device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Training device:", device)


# 3. Load our own placement interview dataset
data_path = Path("data/interview_data.txt")

if not data_path.exists():
    raise FileNotFoundError(f"Dataset not found: {data_path}")

text = data_path.read_text(encoding="utf-8").lower()

# Tokenize text consistently using lowercase
tokens = re.findall(r"\w+|[^\w\s]", text)

if len(tokens) <= 8:
    raise ValueError("Dataset is too small for training.")

# 4. Create the vocabulary and token mappings
vocabulary = sorted(set(tokens))

token_to_id = {
    token: index
    for index, token in enumerate(vocabulary)
}

encoded_data = [token_to_id[token] for token in tokens]

print("Total tokens:", len(tokens))
print("Vocabulary size:", len(vocabulary))


# 5. Create input sequences and next-token targets
sequence_length = 8

inputs = []
targets = []

for i in range(len(encoded_data) - sequence_length):
    inputs.append(encoded_data[i:i + sequence_length])
    targets.append(encoded_data[i + sequence_length])

X = torch.tensor(inputs, dtype=torch.long)
y = torch.tensor(targets, dtype=torch.long)

dataset = TensorDataset(X, y)

loader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=True
)

print("Training examples:", len(dataset))


# 6. Create a new model with randomly initialized weights
model = PlacementPrepLM(
    vocab_size=len(vocabulary),
    embedding_size=32,
    hidden_size=64
).to(device)

print(
    "Trainable parameters:",
    sum(parameter.numel() for parameter in model.parameters())
)


# 7. Configure the loss function and optimizer
loss_function = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.003
)


# 8. Train the model
epochs = 30

for epoch in range(epochs):
    model.train()
    total_loss = 0.0

    for batch_X, batch_y in loader:
        batch_X = batch_X.to(device)
        batch_y = batch_y.to(device)

        optimizer.zero_grad()

        predictions = model(batch_X)

        loss = loss_function(predictions, batch_y)

        loss.backward()
        optimizer.step()

        total_loss += loss.item() * batch_X.size(0)

    average_loss = total_loss / len(dataset)

    if (epoch + 1) % 5 == 0 or epoch == 0:
        print(
            f"Epoch {epoch + 1:2d}/{epochs}, "
            f"Loss: {average_loss:.4f}"
        )


# 9. Save the trained model and vocabulary
model_dir = Path("model")
model_dir.mkdir(exist_ok=True)

checkpoint = {
    "model_state_dict": model.state_dict(),
    "vocabulary": vocabulary,
    "sequence_length": sequence_length,
    "embedding_size": 32,
    "hidden_size": 64
}

torch.save(
    checkpoint,
    model_dir / "placementpreplm.pt"
)

print("\nTraining complete!")
print("Saved model to model/placementpreplm.pt")
