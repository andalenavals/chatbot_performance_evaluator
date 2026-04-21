Overview
========

[Github repo](https://github.com/andalenavals/chatbot_performance_evaluator/)

Why this project exists
-----------------------

Organizations increasingly expose chatbots to customers, employees, and partners. Those systems are expected to answer consistently, remain relevant, refuse unsafe requests appropriately, and do so with acceptable latency. The business problem is not merely building a chatbot. The harder operational problem is **verifying** that the chatbot continues to behave well as prompts, FAQs, safety policies, and domain knowledge evolve.

This package provides a practical framework to **automatically check and validate chatbots** against FAQ-style datasets. It turns evaluation into a repeatable engineering process rather than an ad hoc manual review. That matters for product teams that want to reduce support risk, for operations teams that want regression checks before release, and for leadership teams that need evidence that an assistant is improving over time.

What the framework provides
---------------------------

The framework supports two complementary bot strategies:

* **Full-context prompting** injects a domain-knowledge file into a reusable prompt and asks a chat model to answer from that context.
* **Strict semantic match** treats the FAQ as a controlled answer bank and returns the answer attached to the most similar question.

Both strategies implement the same text-in/text-out contract, so they can be evaluated and compared with the same metric pipeline. The package then:

* loads FAQ datasets from CSV files,
* runs one or more bots over the same questions,
* computes deterministic metrics and LLM-as-a-judge metrics,
* stores row-level results for every question-answer pair,
* produces aggregate summaries, and
* exposes an inspection workflow through a Streamlit app.

Why FAQ evaluation matters
--------------------------

FAQ-style evaluation is especially useful for teams that care about **high-frequency, business-critical interactions**. A customer-support assistant, an HR help bot, or an internal policy assistant often succeeds or fails on narrow, repetitive queries. The FAQ format gives teams a compact benchmark that is easy to expand and govern.

The framework is intentionally designed so the FAQ can grow over time. As a program matures, teams can add:

* newly discovered user intents,
* ambiguous rephrasings,
* edge cases,
* multilingual variations, and
* adversarial or safety-sensitive prompts.

That incremental process turns the FAQ from a static artifact into a living regression suite.

Business value
--------------

This project helps teams answer practical questions such as:

* Is the new model more accurate than the previous one?
* Does a prompt update improve communication quality without hurting safety?
* Are refusal behaviors still robust on dangerous or adversarial inputs?
* Which bot strategy is more appropriate for a tightly governed support workflow?

Because the outputs are saved at row level, the framework supports both executive summaries and deep investigation. Product owners can look at trend summaries, while engineers and evaluators can inspect exactly which questions failed and why.

Evaluation philosophy
---------------------

The package treats chatbot evaluation as a combination of:

* **deterministic measurement**, where simple mathematical rules capture exactness, recall, or latency, and
* **model-based judgment**, where an LLM evaluates more qualitative properties such as relevance, faithfulness, safety, and robustness.

That hybrid strategy is practical. Deterministic metrics are cheap, stable, and transparent. LLM-as-a-judge metrics can capture richer semantic properties that are difficult to encode with a single closed-form formula. Together they create a stronger validation loop than either family alone.

For the mathematical details behind similarity scoring and the metric definitions, see :doc:`metrics`.
