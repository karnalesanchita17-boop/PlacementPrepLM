
from retrieval import load_questions_answers, find_answer


def main():
    pairs = load_questions_answers()

    print("=" * 45)
    print("       PlacementPrepLM Assistant")
    print("=" * 45)
    print("Knowledge base questions:", len(pairs))
    print("Type 'exit' to quit.")

    while True:
        question = input(
            "\nAsk an interview question: "
        ).strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            print("Please enter a question.")
            continue

        matched_question, answer, score = find_answer(
            question, pairs
        )

        # Increased threshold to reduce unrelated answers
        if answer is not None and score >= 0.60:
            print("\nMode: Retrieved answer")
            print("Matched question:", matched_question)
            print("Answer:", answer)
            print(f"Similarity score: {score:.2f}")

        else:
            print("\nNo confident match was found.")
            print(
                "Try rephrasing the question or add a relevant"
                " Q&A to data/interview_data.txt."
            )
            print(
                "Transformer generation is available separately:"
            )
            print("python generate_transformer.py")


if __name__ == "__main__":
    main()
