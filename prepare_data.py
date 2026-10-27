
from pathlib import Path
import re

# Read our training dataset
text = Path("data/interview_data.txt").read_text(encoding="utf-8")

# Split the text into tokens
tokens = re.findall(r"\w+|[^\w\s]", text)

# Assign a unique number to every token
vocabulary = sorted(set(tokens))
token_to_id = {token: i for i, token in enumerate(vocabulary)}
id_to_token = {i: token for token, i in token_to_id.items()}

# Convert the complete text into numbers
encoded_data = [token_to_id[token] for token in tokens]

print("Data preparation successful!")
print("Vocabulary size:", len(vocabulary))
print("Encoded token count:", len(encoded_data))

print("\nExample token-to-number mapping:")
for token in tokens[:10]:
    print(repr(token), "->", token_to_id[token])

print("\nFirst 20 encoded numbers:")
print(encoded_data[:20])

# Verify that numbers can be converted back into tokens
decoded_tokens = [id_to_token[i] for i in encoded_data[:10]]
print("\nDecoded tokens:")
print(decoded_tokens)
