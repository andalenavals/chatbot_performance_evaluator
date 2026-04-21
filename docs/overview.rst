Overview
========

This project compares two chatbot strategies.

Full-context prompting
----------------------
The full-context bot injects the entire domain knowledge text into one prompt. This approach is simple and transparent. Its strength is that every answer can draw on the same knowledge source. Its weakness is that the prompt can become long and noisy.

Strict semantic match
---------------------
The strict semantic match bot does not generate a new answer. Instead it compares the user question against all FAQ questions and returns the expected answer from the most similar row.

Semantic similarity and cosine similarity
-----------------------------------------
The semantic match bot tokenizes each question and computes a simple binary vector over the combined vocabulary. Cosine similarity is then the dot product divided by the product of vector norms. The score is highest when the same important terms appear in both questions.

Metrics
-------
Exact match checks whether the generated answer matches the expected answer after normalization. Keyword recall computes the fraction of expected-answer tokens that also appear in the generated answer. Politeness is a lightweight communication heuristic that rewards helpful phrasing. Latency is measured around the full bot call in milliseconds.

LLM as judge
------------
Judge metrics build a structured prompt containing the question, expected answer, and generated answer. A judge model returns JSON with a score and a short reason. Safety and robustness focus on refusal quality for dangerous or policy-sensitive requests. Relevance and faithfulness focus on whether the answer addresses the question and stays aligned with the expected answer.
