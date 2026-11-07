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

## 🧪 Automated MCP & Dense RAG Benchmarks

SlothVault includes a zero-cloud verification suite (`test_suite`) to benchmark Model Context Protocol (MCP) tool execution, vector retrieval accuracy (`all-MiniLM-L6-v2`), and dynamic memory ingestion.

### Test Execution Output

```text
 EXECUTING SLOTHVAULT TEST CASES (MCP + DENSE RAG)

▶ Running [TC-01]: Local Network Credentials
  Query: "What is my home lab wifi password?"
  • [MCP Tool] Top Chunk (Similarity: 0.794): "WiFi Password for Home Lab is 'lazy_sloth_42'. Do not share externally."
  ✔ PASS: Grounded correctly on 'lazy_sloth_42'

▶ Running [TC-02]: Financial Invoice & Due Date
  Query: "When is the cloud hosting bill due and how much is it?"
  • [MCP Tool] Top Chunk (Similarity: 0.745): "Invoice #8841 from Cloud hosting was $45.20, due on November 5th."
  ✔ PASS: Grounded correctly on '45.20'

▶ Running [TC-03]: Emergency Contact Lookup
  Query: "Who is the emergency contact for my landlord?"
  • [MCP Tool] Top Chunk (Similarity: 0.699): "Emergency contact for landlord: Ramesh Uncle at +91-98200-11223."
  ✔ PASS: Grounded correctly on '98200-11223'

▶ Running [TC-04]: Project Roadmap Milestone
  Query: "What is required for roadmap milestone 2?"
  • [MCP Tool] Top Chunk (Similarity: 0.646): "Project roadmap milestone 2 requires TabPFN model benchmarking by next Tuesday."
  ✔ PASS: Grounded correctly on 'TabPFN'

----------------------------------------------------------------------
▶ Running [TC-05]: Dynamic Ingestion & Instant Retrieval (mcp_add_to_vault)
  • [MCP Tool] Ingest status: Ingested new note into vault! Total items: 8
  • [MCP Tool] Dynamic Chunk (Similarity: 0.780): "The spare key to the storage room is kept under the green pot."
  ✔ PASS: Dynamic note successfully encoded, indexed, and retrieved.

 ALL 5 TEST CASES PASSED SUCCESSFULLY (Zero Cloud Dependencies)

```

### Benchmark Summary

| Test Case ID | Evaluation Target | MCP Function | Cosine Score | Status |
| --- | --- | --- | --- | --- |
| **TC-01** | Local Credentials | `mcp_retrieve_from_vault` | **0.794** | PASSED |
| **TC-02** | Financial Invoice Data | `mcp_retrieve_from_vault` | **0.745** | PASSED |
| **TC-03** | Emergency Contact Lookup | `mcp_retrieve_from_vault` | **0.699** | PASSED |
| **TC-04** | Technical Milestone Data | `mcp_retrieve_from_vault` | **0.646** | PASSED |
| **TC-05** | Dynamic Vector Ingestion | `mcp_add_to_vault` | **0.780** | PASSED |

---

## Tech Stack

* **Language:** Python 3.10+ (`SlothVault-SlowAndSteady.py`)
* **Models:** `all-MiniLM-L6-v2` (Embeddings) & `Qwen/Qwen2.5-1.5B-Instruct` (LLM)
* **Frameworks:** PyTorch, Hugging Face `transformers`, `sentence-transformers`, `scikit-learn`
* **Frontend/UI:** Gradio (`gr.Blocks`)

---

## License

This project is open-source under the MIT License. Built with for the Hacktoberfest Open-Source AI Challenge.
