
from pathlib import Path

# Locate the training dataset
data_path = Path("data/interview_data.txt")

# Check whether the file exists
if data_path.exists():
    text = data_path.read_text(encoding="utf-8")

    print("Dataset loaded successfully!")
    print("Total characters:", len(text))
    print("Total words:", len(text.split()))
    print("\nFirst 300 characters:\n")
    print(text[:300])
else:
    print("Dataset file not found!")
    print("Expected location:", data_path.resolve())
