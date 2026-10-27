
from pathlib import Path
import re

# Load our original training text
data_path = Path("data/interview_data.txt")
text = data_path.read_text(encoding="utf-8")

# Split text into words and punctuation marks
tokens = re.findall(r"\w+|[^\w\s]", text)

# Create a vocabulary of unique tokens
vocabulary = sorted(set(tokens))

print("Tokenization successful!")
print("Total tokens:", len(tokens))
print("Unique tokens:", len(vocabulary))

print("\nFirst 30 tokens:")
print(tokens[:30])

print("\nFirst 30 vocabulary items:")
print(vocabulary[:30])
