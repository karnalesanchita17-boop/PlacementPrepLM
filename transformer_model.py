
import torch
import torch.nn as nn


class TransformerBlock(nn.Module):
    def __init__(self, embedding_size, num_heads, dropout=0.1):
        super().__init__()

        # Self-attention layer
        self.attention = nn.MultiheadAttention(
            embed_dim=embedding_size,
            num_heads=num_heads,
            dropout=dropout,
            batch_first=True
        )

        # Normalize attention and feed-forward outputs
        self.norm1 = nn.LayerNorm(embedding_size)
        self.norm2 = nn.LayerNorm(embedding_size)

        # Feed-forward neural network
        self.feed_forward = nn.Sequential(
            nn.Linear(embedding_size, embedding_size * 4),
            nn.GELU(),
            nn.Linear(embedding_size * 4, embedding_size),
            nn.Dropout(dropout)
        )

        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        sequence_length = x.size(1)

        # Prevent each token from seeing future tokens
        causal_mask = torch.triu(
            torch.ones(
                sequence_length,
                sequence_length,
                device=x.device,
                dtype=torch.bool
            ),
            diagonal=1
        )

        attention_output, _ = self.attention(
            x, x, x,
            attn_mask=causal_mask,
            need_weights=False
        )

        # Residual connection and normalization
        x = self.norm1(x + self.dropout(attention_output))

        # Feed-forward processing
        x = self.norm2(x + self.dropout(self.feed_forward(x)))

        return x


class PlacementPrepTransformer(nn.Module):
    def __init__(
        self,
        vocab_size,
        embedding_size=64,
        num_heads=4,
        num_layers=2,
        max_seq_len=64
    ):
        super().__init__()

        self.max_seq_len = max_seq_len

        # Convert token IDs into learnable vectors
        self.token_embedding = nn.Embedding(
            vocab_size, embedding_size
        )

        # Give tokens information about their positions
        self.position_embedding = nn.Embedding(
            max_seq_len, embedding_size
        )

        # Stack Transformer blocks
        self.blocks = nn.ModuleList([
            TransformerBlock(embedding_size, num_heads)
            for _ in range(num_layers)
        ])

        self.final_norm = nn.LayerNorm(embedding_size)

        # Predict scores for the next token at every position
        self.output_layer = nn.Linear(embedding_size, vocab_size)

    def forward(self, token_ids):
        batch_size, sequence_length = token_ids.shape

        if sequence_length > self.max_seq_len:
            raise ValueError("Input exceeds the maximum sequence length.")

        positions = torch.arange(
            sequence_length, device=token_ids.device
        )

        x = self.token_embedding(token_ids)
        x = x + self.position_embedding(positions)

        for block in self.blocks:
            x = block(x)

        x = self.final_norm(x)
        logits = self.output_layer(x)

        return logits


if __name__ == "__main__":
    import re
    from pathlib import Path

    # Get the vocabulary size from our current dataset
    text = Path("data/interview_data.txt").read_text(
        encoding="utf-8"
    )
    tokens = re.findall(r"\w+|[^\w\s]", text)
    vocabulary = sorted(set(tokens))
    token_to_id = {token: i for i, token in enumerate(vocabulary)}

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    model = PlacementPrepTransformer(
        vocab_size=len(vocabulary)
    ).to(device)

    # Test using the first eight tokens
    sample_ids = [token_to_id[token] for token in tokens[:8]]
    sample = torch.tensor(
        [sample_ids], dtype=torch.long, device=device
    )

    model.eval()
    with torch.no_grad():
        output = model(sample)

    parameter_count = sum(
        p.numel() for p in model.parameters() if p.requires_grad
    )

    print("Transformer model created successfully!")
    print("Device:", device)
    print("Vocabulary size:", len(vocabulary))
    print("Transformer layers:", len(model.blocks))
    print("Attention heads per layer:", 4)
    print("Trainable parameters:", parameter_count)
    print("Input shape:", sample.shape)
    print("Output shape:", output.shape)
