#!/bin/bash
uv pip install llama-index
uv pip install llama-index-llms-openai-like
uv pip install openai==1.61.0
uv pip install llama-index-embeddings-huggingface
uv pip install cryptography # needed to read PDFs
