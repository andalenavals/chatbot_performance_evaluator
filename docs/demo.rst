Demo
====

Hosted demo
-----------

The Streamlit demo is prepared for Hugging Face Spaces:

`Open the live demo <https://andalenavals-chatbot-performance-evaluator.hf.space>`_

The Space runs the same app as the local command below, but starts Ollama inside
the Docker container and prepares the bundled local models:
``deepseek-r1:latest`` and ``qwen3:8b``.

On the free Hugging Face CPU tier, the first request can be slow while the Space
wakes up and Ollama loads a model. Short questions and one Ollama-backed bot at
a time give the smoothest demo experience.

Local demo
----------

Run the CLI benchmark against the default FAQ file:

.. code-block:: bash

   python examples/run_benchmark.py

Run the same benchmark against the adversarial FAQ set:

.. code-block:: bash

   python examples/run_benchmark.py --faq-csv data/faq_adversarial.csv

Start the Streamlit inspection app:

.. code-block:: bash

   streamlit run app/main.py
