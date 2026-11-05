# SlothVault: Zero-Effort Local MCP + RAG Agent

**SlothVault** is an open-source, local-first retrieval-augmented agent built for the **Hacktoberfest Week 3: Slow and Steady** challenge.

It allows users to dump unorganized notes, Wi-Fi keys, invoices, or `.txt` clutter into a local vector store without manual folder structures. Utilizing a Model Context Protocol (MCP) design, it uses `all-MiniLM-L6-v2` embeddings for vector search and `Qwen/Qwen2.5-1.5B-Instruct` to generate direct, factual answers offline.

---

## Demo & Output
# SlothVault: Zero-Effort Local MCP + RAG Agent

**SlothVault** is an open-source, local-first retrieval-augmented agent built for the **Hacktoberfest Week 3: Slow and Steady** challenge.

It allows users to dump unorganized notes, Wi-Fi keys, invoices, or `.txt` clutter into a local vector store without manual folder structures. Utilizing a Model Context Protocol (MCP) design, it uses `all-MiniLM-L6-v2` embeddings for vector search and `Qwen/Qwen2.5-1.5B-Instruct` to generate direct, factual answers offline.

---

## Demo & Output

### Agent Query & MCP Trace
![SlothVault Agent Query](SlothVault%20Zero-Effort%20Local%20MCP%20%2B%20RAG%20Agent_Sloth_Agent.png)

### Unstructured Note Ingestion
![SlothVault Note Ingestion](SlothVault%20Zero-Effort%20Local%20MCP%20%2B%20RAG%20Agent__Dump_More_Clutter.png)

---

## Key Features
- **Local MCP Architecture:** Standardized Model Context Protocol tool execution (`retrieve_from_vault`, `add_to_vault`).
- **Zero-Effort Ingestion:** Add raw notes or upload `.txt` exports directly into an in-memory vector database without sorting.
- **Semantic RAG Search:** Local vector matching powered by `sentence-transformers` and cosine similarity.
- **Privacy-First & Open Weights:** Runs completely offline using `Qwen/Qwen2.5-1.5B-Instruct` with zero external API calls.
- **Interactive Dashboard:** Gradio web interface featuring sample presets and live MCP execution traces.

---

## Tech Stack
- **Language:** Python 3.10+ (`SlothVault-SlowAndSteady.py`)
- **Models:** `all-MiniLM-L6-v2` (Embeddings) & `Qwen/Qwen2.5-1.5B-Instruct` (LLM)
- **Frameworks:** PyTorch, Hugging Face `transformers`, `sentence-transformers`, `scikit-learn`
- **Frontend/UI:** Gradio (`gr.Blocks`)

---

## License
This project is open-source under the MIT License. Built for the Hacktoberfest Open-Source AI Challenge.

---

## Key Features
- **Local MCP Architecture:** Standardized Model Context Protocol tool execution (`retrieve_from_vault`, `add_to_vault`).
- **Zero-Effort Ingestion:** Add raw notes or upload `.txt` exports directly into an in-memory vector database without sorting.
- **Semantic RAG Search:** Local vector matching powered by `sentence-transformers` and cosine similarity.
- **Privacy-First & Open Weights:** Runs completely offline using `Qwen/Qwen2.5-1.5B-Instruct` with zero external API calls.
- **Interactive Dashboard:** Gradio web interface featuring sample presets and live MCP execution traces.

---

## Tech Stack
- **Language:** Python 3.10+ (`SlothVault-SlowAndSteady.py`)
- **Models:** `all-MiniLM-L6-v2` (Embeddings) & `Qwen/Qwen2.5-1.5B-Instruct` (LLM)
- **Frameworks:** PyTorch, Hugging Face `transformers`, `sentence-transformers`, `scikit-learn`
- **Frontend/UI:** Gradio (`gr.Blocks`)

---

## License
This project is open-source under the MIT License. Built with ❤️ for the Hacktoberfest Open-Source AI Challenge.
