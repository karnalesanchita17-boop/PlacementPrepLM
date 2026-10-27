
from pathlib import Path
import re
import torch

from transformer_model import PlacementPrepTransformer

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

checkpoint = torch.load(
    "model/placementpreplm_transformer.pt",
    map_location=device,
    weights_only=False
)

vocabulary = checkpoint["vocabulary"]

token_to_id = {
    token: i for i, token in enumerate(vocabulary)
}

id_to_token = {
    i: token for i, token in enumerate(vocabulary)
}

sequence_length = checkpoint["sequence_length"]

model = PlacementPrepTransformer(
    vocab_size=len(vocabulary),
    embedding_size=checkpoint["embedding_size"],
    num_heads=checkpoint["num_heads"],
    num_layers=checkpoint["num_layers"],
    max_seq_len=checkpoint["max_seq_len"]
).to(device)

model.load_state_dict(checkpoint["model_state_dict"])
model.eval()

print("PlacementPrepLM Transformer loaded!")
print("Device:", device)
print("Type 'exit' to quit.")

while True:
    prompt = input("\nEnter a prompt: ").strip()

    if prompt.lower() == "exit":
        break

    tokens = re.findall(r"\w+|[^\w\s]", prompt)

    unknown = [
        token for token in tokens
        if token not in token_to_id
    ]

    if unknown:
        print("Unknown words will be skipped:", unknown)

    tokens = [
        token for token in tokens
        if token in token_to_id
    ]

    if not tokens:
        print("No recognized words. Try another prompt.")
        continue

    input_ids = [
        token_to_id[token] for token in tokens
    ]

    generated = input_ids[:]

    with torch.no_grad():
        for _ in range(40):
            context = generated[-sequence_length:]

            x = torch.tensor(
                [context],
                dtype=torch.long,
                device=device
            )

            logits = model(x)
            next_token_logits = logits[0, -1, :]

            next_id = torch.argmax(
                next_token_logits
            ).item()

            generated.append(next_id)

            if id_to_token[next_id] in {".", "?", "!"}:
                break

    print(
        "Generated:",
        " ".join(id_to_token[i] for i in generated)
    )
