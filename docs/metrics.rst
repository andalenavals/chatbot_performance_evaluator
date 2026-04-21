Metrics and Mathematical Foundations
====================================

This section describes the mathematical logic behind the framework's core scoring methods.

Semantic search in the strict semantic-match bot
------------------------------------------------

The strict semantic-match bot uses a lightweight lexical proxy for semantic retrieval. For each question, the system constructs a token set after lower-casing and stripping light punctuation.

Let

.. math::

   T(q) = 	\text{token set of question } q

For an input question :math:`q` and a candidate FAQ question :math:`q_i`, the system builds binary vectors over the union vocabulary

.. math::

   V = T(q) \cup T(q_i)

and then assigns

.. math::

   x_j = \begin{cases}
   1 & \text{if token } v_j \in T(q) \\
   0 & \text{otherwise}
   \end{cases}
   \qquad
   y_j = \begin{cases}
   1 & \text{if token } v_j \in T(q_i) \\
   0 & \text{otherwise}
   \end{cases}

The similarity score is cosine similarity:

.. math::

   \cos(\theta) = \frac{x \cdot y}{\lVert x \rVert_2 \lVert y \rVert_2}

where :math:`x \cdot y` is the dot product and :math:`\lVert x \rVert_2` is the Euclidean norm. The bot selects the FAQ row with the maximum cosine similarity and returns its stored answer.

This method is computationally simple and highly interpretable. It does **not** learn a semantic embedding space, but it approximates semantic relatedness when paraphrases share important vocabulary.

Full-context prompting
----------------------

The full-context bot does not retrieve a single FAQ row. Instead it concatenates the entire domain-knowledge document into one prompt template and asks a generative model to answer.

Formally, the model receives a prompt

.. math::

   p = f(k, q)

where :math:`k` is the domain-knowledge text, :math:`q` is the user question, and :math:`f` is the prompt template function. The model then samples or decodes an answer

.. math::

   a = M(p)

where :math:`M` is the configured LLM backend. This approach trades retrieval precision for contextual completeness.

Deterministic metrics
---------------------

Exact match
^^^^^^^^^^^

Exact match is a binary indicator after normalization. If :math:`\hat{a}` is the generated answer and :math:`a^*` is the expected answer, then

.. math::

   \operatorname{EM}(\hat{a}, a^*) =
   \begin{cases}
   1 & \text{if } N(\hat{a}) = N(a^*) \\
   0 & \text{otherwise}
   \end{cases}

where :math:`N(\cdot)` lower-cases text, trims leading and trailing spaces, and collapses repeated whitespace.

Keyword recall
^^^^^^^^^^^^^^

The framework computes a token-set recall over the expected answer. Let :math:`E` be the token set of the expected answer and :math:`G` be the token set of the generated answer. Then

.. math::

   \operatorname{Recall}(G, E) = \frac{|G \cap E|}{|E|}

when :math:`|E| > 0`, and :math:`0` otherwise.

This score rewards answers that preserve expected factual content, even when the wording is not identical.

Answer length
^^^^^^^^^^^^^

Answer length is reported as a simple scalar

.. math::

   L(\hat{a}) = \text{number of characters in } \hat{a}

This metric is not a quality score by itself. Instead it acts as a communication descriptor that can reveal truncation, verbosity, or excessively terse answers.

Politeness heuristic
^^^^^^^^^^^^^^^^^^^^

The politeness metric is a lightweight communication heuristic. Let :math:`m_1, \dots, m_k` be a small set of politeness markers such as “please” or “happy to help”. The metric counts how many markers appear in the answer, then scales and clips the result:

.. math::

   P(\hat{a}) = \min\left(\frac{1}{2} \sum_{i=1}^{k} \mathbf{1}[m_i \subseteq \hat{a}], 1\right)

This metric is intentionally simple. It provides a rough communication-quality signal, not a linguistic model of tone.

Latency
^^^^^^^

The evaluator records end-to-end latency for one bot call:

.. math::

   T = t_{\text{end}} - t_{\text{start}}

The result is reported in milliseconds. This is an operational-performance metric rather than a semantic-quality metric.

LLM-as-a-judge metrics
----------------------

Some evaluation properties are difficult to encode as a deterministic formula. Relevance, faithfulness, safety, and robustness often require holistic judgment over the relation between:

* the input question,
* the expected answer, and
* the generated answer.

For those cases, the framework constructs a judge prompt:

.. math::

   j = g(q, a^*, \hat{a})

and asks a judge model to return structured JSON containing a score and a rationale. If the judge returns

.. code-block:: json

   {"score": s, "reason": r}

then the metric score is simply :math:`s`, while :math:`r` is stored as supporting detail.

This turns qualitative review into a repeatable programmatic step. The output is still model-based and therefore not purely objective, but it is auditable because the framework can persist the judge output and, when available, the judge reasoning trace.

Interpreting metric families together
-------------------------------------

No single metric is sufficient. A business-facing evaluation should inspect several axes at once:

* **Correctness:** exact match and keyword recall.
* **Communication:** answer length and politeness.
* **Operations:** latency.
* **Semantic review:** judge scores for relevance, faithfulness, safety, and robustness.

The framework therefore saves each metric at row level so that teams can diagnose disagreements between metric families. For example, a response may score low on exact match but high on judge-based relevance if it uses a paraphrase that preserves meaning.
