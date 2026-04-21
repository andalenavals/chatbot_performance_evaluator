Installation
============

Create an isolated environment and install the package in editable mode.

.. code-block:: bash

   python -m venv .venv
   source .venv/bin/activate
   pip install -e .[dev]

For OpenAI-backed bots or judges:

.. code-block:: bash
   pip install -e .[dev,openai]
   export OPENAI_API_KEY=your_key_here


To build the documentation as well:

.. code-block:: bash

   pip install -e .[docs]
   sphinx-build -b html docs docs/_build/html


