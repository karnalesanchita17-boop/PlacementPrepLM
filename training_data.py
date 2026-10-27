
from pathlib import Path
import re

# Load and tokenize the dataset
text = Path("data/interview_data.txt").read_text(encoding="utf-8")
tokens = re.findall(r"\w+|[^\w\s]", text)

# Build token mappings
vocabulary = sorted(set(tokens))
token_to_id = {token: i for i, token in enumerate(vocabulary)}

# Encode the text as numbers
encoded_data = [token_to_id[token] for token in tokens]

# Prepare next-token prediction examples
sequence_length = 8

inputs = []
targets = []

for i in range(len(encoded_data) - sequence_length):
    inputs.append(encoded_data[i:i + sequence_length])
    targets.append(encoded_data[i + sequence_length])

print("Training examples prepared!")
print("Sequence length:", sequence_length)
print("Number of training examples:", len(inputs))

print("\nFirst input tokens:")
print([tokens[j] for j in range(sequence_length)])

print("\nTarget token:")
print(tokens[sequence_length])

print("\nFirst input numbers:")
print(inputs[0])

print("\nTarget number:")
print(targets[0])
