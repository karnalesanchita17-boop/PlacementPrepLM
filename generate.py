
import re
import torch

from model import PlacementPrepLM


# 1. Select the device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# 2. Load the saved model and vocabulary
checkpoint_path = "model/placementpreplm.pt"

checkpoint = torch.load(
    checkpoint_path,
    map_location=device,
    weights_only=False
)

vocabulary = checkpoint["vocabulary"]

token_to_id = {
    token: index
    for index, token in enumerate(vocabulary)
}

id_to_token = {
    index: token
    for index, token in enumerate(vocabulary)
}

sequence_length = checkpoint["sequence_length"]


# 3. Recreate the same model architecture
model = PlacementPrepLM(
    vocab_size=len(vocabulary),
    embedding_size=checkpoint["embedding_size"],
    hidden_size=checkpoint["hidden_size"]
).to(device)

model.load_state_dict(checkpoint["model_state_dict"])
model.eval()

print("PlacementPrepLM loaded successfully!")
print("Device:", device)
print("Vocabulary size:", len(vocabulary))
print("Type a question or starting phrase.")
print("Type 'exit' to stop.")


# 4. Generate text from the trained model
while True:
    prompt = input("\nYou: ").strip()

    if prompt.lower() == "exit":
        print("Goodbye!")
        break

    if not prompt:
        print("Please enter a starting phrase.")
        continue

    # Use the same lowercase tokenization as training
    prompt_tokens = re.findall(
        r"\w+|[^\w\s]",
        prompt.lower()
    )

    unknown_tokens = [
        token
        for token in prompt_tokens
        if token not in token_to_id
    ]

    if unknown_tokens:
        print("Unknown tokens:", unknown_tokens)
        print("Try a phrase using words from the training dataset.")
        continue

    context = [
        token_to_id[token]
        for token in prompt_tokens
    ]

    generated_tokens = prompt_tokens.copy()

    with torch.no_grad():
        for _ in range(30):
            context_ids = context[-sequence_length:]

            input_tensor = torch.tensor(
                [context_ids],
                dtype=torch.long,
                device=device
            )

            logits = model(input_tensor)[0]

            # Select the token with the highest predicted score
            next_id = torch.argmax(logits).item()
            next_token = id_to_token[next_id]

            generated_tokens.append(next_token)
            context.append(next_id)

            # Stop when the next question begins
            if next_token == "question":
                break

    print("Model:", " ".join(generated_tokens))
