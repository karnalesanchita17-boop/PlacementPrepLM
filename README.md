\# PlacementPrepLM



PlacementPrepLM is a learning-focused placement preparation assistant built with Python, PyTorch, Flask, and React.



The project combines a question-answer retrieval system with small language models trained from scratch. Its goal is to help students practise technical interview questions while exploring how tokenization, neural networks, model training, and text generation work.



\## Features



\- A React-based web interface for placement preparation.

\- A Flask backend that handles questions from the frontend.

\- A retrieval system that searches a reviewed question-answer dataset.

\- A GRU-based language model trained from scratch.

\- An experimental Transformer model trained from scratch.

\- Separate scripts for training and text generation.



\*\*Important:\*\* The current web assistant uses the retrieval system. The trained language models are separate experiments and are not currently connected to the web assistant.



\## Technologies Used



\- Python

\- PyTorch

\- Flask

\- React

\- Vite

\- JavaScript



\## Project Structure



```text

PlacementPrepLM/

├── app.py

├── retrieval.py

├── model.py

├── transformer\_model.py

├── train.py

├── train\_transformer.py

├── generate.py

├── generate\_transformer.py

├── prepare\_data.py

├── tokenize\_data.py

├── training\_data.py

├── check\_data.py

├── test\_gpu.py

├── data/

│   └── interview\_data.txt

├── model/

│   ├── placementpreplm.pt

│   └── placementpreplm\_transformer.pt

└── frontend/

&#x20;   ├── src/

&#x20;   ├── package.json

&#x20;   └── vite.config.js

```



\## Requirements



\- Python 3.10 or a compatible Python version supported by the installed dependencies.

\- Node.js and npm.

\- Python packages listed in `requirements.txt`.

\- A web browser.



A CUDA-compatible NVIDIA GPU is optional. Training can be slower on a CPU.



\## Run Locally



\### 1. Clone the repository



```bash

git clone YOUR\_GITHUB\_REPOSITORY\_URL

cd PlacementPrepLM

```



Replace `YOUR\_GITHUB\_REPOSITORY\_URL` with the repository URL after publishing the project.



\### 2. Install Python dependencies



Create and activate a virtual environment, then install the packages listed in `requirements.txt`.



\### 3. Start the Flask backend



```bash

python app.py

```



The backend runs locally at `http://127.0.0.1:5000`.



\### 4. Start the frontend



Open another terminal:



```bash

cd frontend

npm install

npm run dev

```



Open the local URL displayed by Vite in your browser.



\## Understanding the AI Experiments



The GRU and Transformer training scripts are intended for learning about language-model training, next-token prediction, and text generation.



The models are small experiments trained on a limited custom dataset. Their generated text may be repetitive or inaccurate and should not be treated as authoritative interview guidance.



The web assistant currently uses dataset retrieval rather than generating its answers with either trained model.



\## Limitations and Future Improvements



\- Expand and improve the reviewed interview dataset.

\- Evaluate retrieval accuracy with test questions.

\- Add topic-wise practice and progress tracking.

\- Measure language-model performance on held-out text.

\- Improve text generation and document the training process.

\- Explore integrating the trained model into the web application.

\- Add automated tests and clearer installation instructions.



\## Learning Goal



This project is being developed as a practical way to learn Python, web development, machine learning, and placement preparation through experimentation and incremental improvements.



