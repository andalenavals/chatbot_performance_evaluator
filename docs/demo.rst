Demo
====

Run the CLI benchmark against the default FAQ file:

.. code-block:: bash

   python examples/run_benchmark.py

Run the same benchmark against the adversarial FAQ set:

.. code-block:: bash

   python examples/run_benchmark.py --faq-csv data/faq_adversarial.csv

Start the Streamlit inspection app:

.. code-block:: bash

   streamlit run app/main.py
