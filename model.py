
import torch
import torch.nn as nn


class PlacementPrepLM(nn.Module):
    def __init__(self, vocab_size, embedding_size, hidden_size):
        super().__init__()

        self.embedding = nn.Embedding(vocab_size, embedding_size)

        self.gru = nn.GRU(
            input_size=embedding_size,
            hidden_size=hidden_size,
            batch_first=True
        )

        self.output_layer = nn.Linear(hidden_size, vocab_size)

    def forward(self, x):
        x = self.embedding(x)
        output, hidden = self.gru(x)
        last_output = output[:, -1, :]
        logits = self.output_layer(last_output)
        return logits


# Run this test only when model.py is executed directly.
if __name__ == "__main__":
    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    model = PlacementPrepLM(
        vocab_size=308,
        embedding_size=32,
        hidden_size=64
    ).to(device)

    sample = torch.tensor(
        [[38, 5, 45, 160, 47, 99, 268, 7]],
        dtype=torch.long,
        device=device
    )

    with torch.no_grad():
        prediction_scores = model(sample)

    print("Model test successful!")
    print("Device:", device)
    print("Trainable parameters:", sum(
        p.numel() for p in model.parameters()
    ))
    print("Output shape:", prediction_scores.shape)
