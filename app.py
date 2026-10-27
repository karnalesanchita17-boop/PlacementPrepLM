
from pathlib import Path

from flask import Flask, jsonify, request
import retrieval

app = Flask(__name__)

# Locate the dataset relative to this file, not the terminal folder.
retrieval.DATA_PATH = (
    Path(__file__).resolve().parent
    / "data"
    / "interview_data.txt"
)

# Load the reviewed Q&A dataset once when the app starts.
try:
    PAIRS = retrieval.load_questions_answers()
    DATASET_ERROR = None
except (OSError, UnicodeError) as error:
    PAIRS = []
    DATASET_ERROR = str(error)

# Stricter matching threshold for website answers.
SIMILARITY_THRESHOLD = 0.60


@app.route("/")
def home():
    return jsonify({
        "app": "PlacementPrepLM",
        "message": "Placement preparation backend is running!"
    })


@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy" if DATASET_ERROR is None else "degraded",
        "app": "PlacementPrepLM",
        "questions_loaded": len(PAIRS),
        "dataset_available": DATASET_ERROR is None
    }), 200 if DATASET_ERROR is None else 503


@app.route("/api/ask", methods=["POST"])
def ask():
    if DATASET_ERROR is not None:
        return jsonify({
            "error": "The question dataset could not be loaded."
        }), 503

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Send a JSON object containing a question."
        }), 400

    question_text = data.get("question")

    if not isinstance(question_text, str) or not question_text.strip():
        return jsonify({
            "error": "Please enter a question."
        }), 400

    question_text = question_text.strip()

    if len(question_text) > 500:
        return jsonify({
            "error": "Your question must be 500 characters or fewer."
        }), 400

    matched_question, answer, score = retrieval.find_answer(
        question_text, PAIRS
    )

    if answer is None or score < SIMILARITY_THRESHOLD:
        return jsonify({
            "found": False,
            "message": (
                "I couldn't find a sufficiently reliable match "
                "in the reviewed question dataset yet."
            )
        }), 200

    return jsonify({
        "found": True,
        "matched_question": matched_question,
        "answer": answer,
        "similarity": round(score, 2),
        "source": "Reviewed placement Q&A dataset"
    })


if __name__ == "__main__":
    app.run(debug=True)
