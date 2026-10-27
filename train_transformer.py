
from pathlib import Path
import re
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from transformer_model import PlacementPrepTransformer

torch.manual_seed(42)

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

# Configuration
sequence_length = 32
batch_size = 16
epochs = 100
learning_rate = 0.001

# Load the dataset
text = Path("data/interview_data.txt").read_text(
    encoding="utf-8"
)

tokens = re.findall(r"\w+|[^\w\s]", text)
vocabulary = sorted(set(tokens))

token_to_id = {
    token: i for i, token in enumerate(vocabulary)
}

encoded = torch.tensor(
    [token_to_id[token] for token in tokens],
    dtype=torch.long
)

# Create overlapping sequences.
# Input: tokens 0 through 31
# Target: tokens 1 through 32
class LanguageDataset(Dataset):
    def __init__(self, encoded, seq_len):
        self.encoded = encoded
        self.seq_len = seq_len

    def __len__(self):
        return len(self.encoded) - self.seq_len

    def __getitem__(self, index):
        chunk = self.encoded[
            index:index + self.seq_len + 1
        ]

        inputs = chunk[:-1]
        targets = chunk[1:]

        return inputs, targets


dataset = LanguageDataset(encoded, sequence_length)

loader = DataLoader(
    dataset,
    batch_size=batch_size,
    shuffle=True
)

# Create a fresh Transformer
model = PlacementPrepTransformer(
    vocab_size=len(vocabulary),
    embedding_size=64,
    num_heads=4,
    num_layers=2,
    max_seq_len=sequence_length
).to(device)

loss_function = nn.CrossEntropyLoss()
optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=learning_rate
)

print("Transformer training started!")
print("Device:", device)
print("Vocabulary size:", len(vocabulary))
print("Training sequences:", len(dataset))
print("Sequence length:", sequence_length)
print("Trainable parameters:", sum(
    p.numel() for p in model.parameters()
))

# Train the model
for epoch in range(epochs):
    model.train()
    total_loss = 0.0
    total_tokens = 0

    for inputs, targets in loader:
        inputs = inputs.to(device)
        targets = targets.to(device)

        optimizer.zero_grad()

        logits = model(inputs)

        loss = loss_function(
            logits.reshape(-1, len(vocabulary)),
            targets.reshape(-1)
        )

        loss.backward()

        # Avoid excessively large gradient updates
        torch.nn.utils.clip_grad_norm_(
            model.parameters(), max_norm=1.0
        )

        optimizer.step()

        token_count = targets.numel()
        total_loss += loss.item() * token_count
        total_tokens += token_count

    average_loss = total_loss / total_tokens

    if (epoch + 1) % 10 == 0 or epoch == 0:
        print(
            f"Epoch {epoch + 1:3d}/{epochs}, "
            f"Loss: {average_loss:.4f}"
        )

# Save the trained Transformer separately from the GRU
Path("model").mkdir(exist_ok=True)

torch.save({
    "model_state_dict": model.state_dict(),
    "vocabulary": vocabulary,
    "sequence_length": sequence_length,
    "embedding_size": 64,
    "num_heads": 4,
    "num_layers": 2,
    "max_seq_len": sequence_length
}, "model/placementpreplm_transformer.pt")

print("\nTransformer training complete!")
print(
    "Saved to model/placementpreplm_transformer.pt"
)
