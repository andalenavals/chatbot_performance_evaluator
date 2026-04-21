Adding a New Bot
================

Bots are abstractions that take text input and return text output.

Modern LLMs context window are large enough for most FAQ augmented files. Therefore the two predefined types `full_context` and `strict_semantic_match` are more than enough for most applications. Vanilla bots therefore will just change the ``configs/bots/`` folder including a configuration file that requires a model and a prompt.

In case the domain knowledge is too large a combination of the two types might be neeeded, i.e., a RAG bot. For implementing a RAG bot or another more sophisticated system consider the following.


All bots must implement the interface:

.. code-block:: python

    class BaseBot:
        def answer(self, question: str) -> BotResult:
            ...

Steps to add a new bot
----------------------

1. Create a new file in:

   ``src/chatbot_eval/bots/``

2. Implement the interface:

.. code-block:: python

    from chatbot_eval.bots.base import BaseBot

    class MyNewBot(BaseBot):
        def __init__(self, client, prompt_template):
            self.client = client
            self.prompt_template = prompt_template

        def answer(self, question: str):
            prompt = self.prompt_template.substitute(question=question)
            response = self.client.generate(prompt)
            return BotResult(answer=response.text, metadata=response.metadata)

3. Register it in:

``bot_factory.py``

4. Create a config file:

.. code-block:: json

    {
      "type": "my_new_bot",
      "model_config": "configs/models/deepseek-r1.json",
      "prompt_path": "configs/bots/prompts/full_context_prompt.txt"
    }
