import json
import gradio as gr
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline

# 1. LOAD LOCAL OPEN-WEIGHT MODELS (Zero External API Keys Required)
print("Loading local open-weight embedding model...")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading local Qwen 2.5 1.5B reasoning model...")
device = "cuda" if torch.cuda.is_available() else "cpu"
llm_pipeline = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-1.5B-Instruct",
    torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
    device_map="auto" if torch.cuda.is_available() else None,
)
print("Local models loaded successfully!")

# 2. IN-MEMORY VECTOR STORE & SEED KNOWLEDGE
INITIAL_DOCS = [
    "WiFi Password for Home Lab is 'lazy_sloth_42'. Do not share externally.",
    "Invoice #8841 from Cloud hosting was $45.20, due on November 5th.",
    "Doctor appointment rescheduled to Friday at 4:30 PM with Dr. Sharma.",
    (
        "Project roadmap milestone 2 requires TabPFN model benchmarking by next"
        " Tuesday."
    ),
    "Emergency contact for landlord: Ramesh Uncle at +91-98200-11223.",
    "Gym membership renewal is on pause until January 1st to conserve energy.",
]

vault_docs = list(INITIAL_DOCS)
vault_embeddings = embed_model.encode(vault_docs)

# 3. STANDARDIZED MODEL CONTEXT PROTOCOL (MCP) INTERFACE
MCP_SPEC = {
    "tools": [
        {
            "name": "retrieve_from_vault",
            "description": (
                "Performs semantic vector search across personal notes, receipts,"
                " and files."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query.",
                    }
                },
                "required": ["query"],
            },
        },
        {
            "name": "add_to_vault",
            "description": (
                "Appends a new raw note or document into the vector knowledge"
                " base."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Raw unorganized note text.",
                    }
                },
                "required": ["text"],
            },
        },
    ]
}


def mcp_retrieve_from_vault(query: str, top_k: int = 2):
    """MCP Tool: Semantic Vector Search"""
    global vault_docs, vault_embeddings
    if len(vault_docs) == 0:
        return []

    q_vec = embed_model.encode([query])
    scores = cosine_similarity(q_vec, vault_embeddings)[0]
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []
    for idx in top_indices:
        results.append({
            "text": vault_docs[idx],
            "similarity_score": round(float(scores[idx]), 3),
        })
    return results


def mcp_add_to_vault(new_text: str):
    """MCP Tool: Dynamic Ingestion"""
    global vault_docs, vault_embeddings
    cleaned = new_text.strip()
    if not cleaned:
        return "Empty note provided."

    vault_docs.append(cleaned)
    new_embedding = embed_model.encode([cleaned])
    vault_embeddings = np.vstack([vault_embeddings, new_embedding])
    return f"Ingested new note into vault! Total items: {len(vault_docs)}"


# 4. SLOTH AGENT REASONING CORE
SYSTEM_PROMPT = """You are SlothVault, a local MCP-powered knowledge retrieval agent built for Hacktoberfest Week 3 ("Slow and Steady").
The user is completely exhausted and refuses to manually search through messy folders, emails, or notes.
You have executed the MCP tool 'retrieve_from_vault' and retrieved the most relevant records.
Your job: Provide the direct answer to the user's question in exactly 1 or 2 clear, factual sentences.
End with a lighthearted sloth remark reminding them to conserve energy (e.g., 'Now go back to resting.').
Do not mention technical RAG jargon in the final answer."""


def sloth_agent_pipeline(query: str):
    if not query.strip():
        return "Ask something you're too lazy to search for!"

    # 1. MCP Tool Invocation
    retrieved_items = mcp_retrieve_from_vault(query, top_k=2)
    if not retrieved_items:
        return "The vault is currently empty."

    context_str = "\n".join([
        f"- {item['text']} (Cosine Match: {item['similarity_score']})"
        for item in retrieved_items
    ])

    # 2. Open-Weight Model Synthesis
    prompt_messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"User Query: {query}\n\nRetrieved Vault"
                f" Records:\n{context_str}\n\nAnswer directly:"
            ),
        },
    ]

    output = llm_pipeline(prompt_messages, max_new_tokens=150, temperature=0.2)
    answer = output[0]["generated_text"][-1]["content"].strip()

    # Format showing live MCP execution trace + clean UI card
    mcp_trace = (
        f"```json\n"
        f"// MCP Tool Execution Trace\n"
        f"{{\n"
        f'  "tool": "retrieve_from_vault",\n'
        f'  "parameters": {{"query": "{query}"}},\n'
        f'  "top_k_retrieved": {len(retrieved_items)}\n'
        f"}}\n"
        f"```\n\n"
        f"**Retrieved Semantic Chunks:**\n{context_str}\n\n"
        f"---\n"
        f"### Sloth Answer\n"
        f"{answer}"
    )
    return mcp_trace


def handle_file_or_text_upload(file_obj, raw_text):
    """Allows dropping custom .txt files or pasting raw notes."""
    added_count = 0
    if file_obj is not None:
        try:
            with open(
                file_obj.name, "r", encoding="utf-8", errors="ignore"
            ) as f:
                for line in f.readlines():
                    if line.strip():
                        mcp_add_to_vault(line.strip())
                        added_count += 1
        except Exception as e:
            return f"Error reading file: {e}"

    if raw_text and raw_text.strip():
        mcp_add_to_vault(raw_text.strip())
        added_count += 1

    return (
        f"Successfully added {added_count} new note(s) to the local vector"
        f" vault! Total items: {len(vault_docs)}"
    )


# 5. GRADIO DASHBOARD
with gr.Blocks(theme=gr.themes.Soft(), title="SlothVault") as demo:
    gr.Markdown("# SlothVault: Zero-Effort Local MCP + RAG Agent")
    gr.Markdown(
        "*Built for **Hacktoberfest Week 3: Slow and Steady** (International"
        " Sloth Day).*  \nToo lazy to organize receipts, Wi-Fi passwords,"
        " bills, or notes? Toss your clutter in here and let an open-weight"
        " local model fetch the answers for you."
    )

    with gr.Tab("Ask the Sloth Agent"):
        with gr.Row():
            with gr.Column(scale=1):
                query_input = gr.Textbox(
                    label="Ask anything you're too tired to search for:",
                    value=(
                        "What is my home lab wifi password and when is the"
                        " cloud bill due?"
                    ),
                    lines=3,
                )

                gr.Markdown("**Quick Presets (Click to autofill):**")
                with gr.Row():
                    p1 = gr.Button("Wi-Fi Password", size="sm")
                    p2 = gr.Button("Cloud Bill Due Date", size="sm")
                    p3 = gr.Button("Doctor Appointment", size="sm")

                search_btn = gr.Button("Find It For Me", variant="primary")

            with gr.Column(scale=1):
                output_display = gr.Markdown(label="Agent Response")

        p1.click(
            lambda: "What is the Wi-Fi password for the home lab?",
            outputs=query_input,
        )
        p2.click(
            lambda: (
                "How much was the cloud hosting invoice and when is it due?"
            ),
            outputs=query_input,
        )
        p3.click(
            lambda: "When is my rescheduled appointment with Dr. Sharma?",
            outputs=query_input,
        )

        search_btn.click(
            fn=sloth_agent_pipeline,
            inputs=query_input,
            outputs=output_display,
        )

    with gr.Tab("Dump More Clutter (Add Notes)"):
        gr.Markdown(
            "Dump your unorganized thoughts, snippets, or upload a `.txt` file"
            " without organizing it."
        )
        with gr.Row():
            note_input = gr.Textbox(
                label="Paste raw note or paste a receipt snippet:",
                placeholder="e.g., Gate code is 8842",
                lines=3,
            )
            file_input = gr.File(
                label="Or upload a .txt notes export", file_types=[".txt"]
            )

        add_btn = gr.Button(
            "Ingest Without Organizing", variant="secondary"
        )
        ingest_status = gr.Markdown()

        add_btn.click(
            fn=handle_file_or_text_upload,
            inputs=[file_input, note_input],
            outputs=ingest_status,
        )

if __name__ == "__main__":
    demo.launch(share=True)