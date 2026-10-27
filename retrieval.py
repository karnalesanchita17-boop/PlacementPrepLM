
from pathlib import Path
import re
from difflib import SequenceMatcher

DATA_PATH = Path("data/interview_data.txt")


def load_questions_answers():
    text = DATA_PATH.read_text(encoding="utf-8")

    # Find Question: ... Answer: ... pairs
    pattern = re.compile(
        r"Question:\s*(.*?)\s*Answer:\s*(.*?)(?=\n\s*Question:|\Z)",
        re.IGNORECASE | re.DOTALL
    )

    pairs = []

    for match in pattern.finditer(text):
        question = " ".join(match.group(1).split())
        answer = " ".join(match.group(2).split())

        if question and answer:
            pairs.append((question, answer))

    return pairs


def normalize(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def similarity(user_question, stored_question):
    user_words = set(normalize(user_question))
    stored_words = set(normalize(stored_question))

    if not user_words or not stored_words:
        return 0.0

    # Compare shared words and overall wording
    overlap = len(user_words & stored_words) / len(
        user_words | stored_words
    )

    wording = SequenceMatcher(
        None,
        " ".join(normalize(user_question)),
        " ".join(normalize(stored_question))
    ).ratio()

    return 0.65 * overlap + 0.35 * wording


def find_answer(user_question, pairs):
    ranked = sorted(
        (
            (similarity(user_question, question), question, answer)
            for question, answer in pairs
        ),
        reverse=True,
        key=lambda item: item[0]
    )

    if not ranked or ranked[0][0] < 0.25:
        return None, None, 0.0

    score, question, answer = ranked[0]
    return question, answer, score


if __name__ == "__main__":
    pairs = load_questions_answers()

    print("PlacementPrepLM Retrieval System")
    print("Questions loaded:", len(pairs))
    print("Type 'exit' to quit.")

    while True:
        user_question = input("\nEnter your question: ").strip()

        if user_question.lower() == "exit":
            break

        question, answer, score = find_answer(
            user_question, pairs
        )

        if answer is None:
            print("No sufficiently similar question found.")
            print("Try rephrasing or adding this topic to the dataset.")
        else:
            print("Matched question:", question)
            print("Answer:", answer)
            print(f"Similarity score: {score:.2f}")
