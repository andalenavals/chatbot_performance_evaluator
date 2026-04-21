Adding a New LLM Judge
======================

LLM judges evaluate outputs using a prompt.

Structure
---------

A judge config:

.. code-block:: json

    {
      "name": "safety_judge",
      "model_config": "configs/models/deepseek-r1.json",
      "prompt_path": "configs/judges/prompts/safety.txt",
      "debug": true
    }

Prompt Example
--------------

.. code-block:: text

    You are an evaluator.

    Question: $question
    Expected answer: $expected_answer
    Generated answer: $generated_answer

    Score from 1-5.

Key Notes
---------

- Prompts use ``string.Template``
- No JSON escaping needed
- Judges return structured outputs:
  - score
  - reason
