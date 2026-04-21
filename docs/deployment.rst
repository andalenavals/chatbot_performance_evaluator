Deployment
==========

Hugging Face Spaces demo
------------------------

This repository includes a Docker-based Hugging Face Space configuration for the
interactive Streamlit app:

`Open the demo Space <https://andalenavals-chatbot-performance-evaluator.hf.space>`_

The Space metadata lives at the top of ``README.md`` and points Hugging Face to
the root ``Dockerfile``. The container installs the package, starts Ollama, pulls
the models required by the bundled Ollama configs, and then serves Streamlit on
port ``7860``.

Prepared Ollama models:

* ``deepseek-r1:latest``
* ``qwen3:8b``

The startup script is ``deploy/huggingface/start.sh``. In the Hugging Face Space
settings, you can override the models pulled at boot with the
``SPACE_OLLAMA_MODELS`` environment variable, for example:

.. code-block:: bash

   SPACE_OLLAMA_MODELS="deepseek-r1:latest"

On Hugging Face's free CPU tier, expect cold starts and slow inference. The
configuration is intended as a convenient public demo, not as a production
serving setup.

GitHub Pages documentation
--------------------------

The repository includes a GitHub Actions workflow at ``.github/workflows/docs.yml`` that builds the Sphinx documentation and deploys it to GitHub Pages.

The docs build is driven from source files in ``docs/``. The generated ``docs/_build`` directory should remain out of version control.
