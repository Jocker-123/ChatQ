# 🧠 Local LLM-Powered RAG System with FastAPI
## 📦 Overview

<table>
  <tr>
    <td width="40%">
      <img src="images/logo2.png" alt="App Preview" width="100%">
    </td>
    <td>
      <p><strong>RAG-powered search assistant</strong></p>
      <ul>
        <li>Accepts user questions via API</li>
        <li>Searches internal docs (Vector DB + Elastic)</li>
        <li>Optionally pulls live web content</li>
        <li>Feeds everything into a local LLM (e.g., Mistral)</li>
        <li>Returns high-quality answers</li>
      </ul>
    </td>
  </tr>
</table>


This project is a minimal Retrieval-Augmented Generation (RAG) app that:

- Accepts user queries via FastAPI
- Searches documents semantically (Vector DB) and by keyword (Elasticsearch)
- Uses a local or remote LLM to generate responses from the retrieved context

## 🤖 Architecture Design
![architecture_design.png](images%2Farchitecture_design.png)
<table>
  <tr>
    <td>
      <p><strong>FastAPI-powered RAG architecture</strong> with hybrid local and live search capabilities.</p>
      <ul>
        <li>📄 Users upload docs → stored in Vector DB and Elasticsearch</li>
        <li>🔍 User queries processed via API and routed to multiple search services</li>
        <li>🧠 Results passed to a local/remote LLM (like Mistral or GPT-4o)</li>
        <li>💬 Context-rich response returned to the user</li>
      </ul>
    </td>
  </tr>
</table>

---
## UI:
![UI.png](images%2FUI.png)

### Upload Success
![upload_success.png](images%2Fupload_success.png)

### Query Response:
![query_success.png](images%2Fquery_success.png)
---

## 🔧 System Components Explained

### 🧑‍💻 User Input
- **Upload Docs**: Users can upload PDF/TXT files through a simple UI or API.
  - 📥 Documents are parsed, embedded, and stored for retrieval.
- **Query**: Users submit a question.
  - 🧠 This query goes through vector search, keyword search, and optionally web search to gather relevant context.

---

### 🧠 Vector Search (FAISS or Pinecone)
- Stores document **embeddings** as dense vectors.
- Allows **semantic search** — returns results that are *meaningfully similar*, even if the words don't match.
- Powered by models like `all-MiniLM-L6-v2`.

---

### 🔍 ElasticSearch (Keyword Indexing)
- Indexes raw document text for **exact keyword** and metadata-based lookup.
- Very fast for filtering, name-based lookups, or date/tag filtering.
- Complements vector search for **hybrid retrieval**.

---

### 🌐 Web Search Module
- Executes **live online search** (e.g., DuckDuckGo or SerpAPI).
- Pulls recent or missing information not found in local storage.
- Extracts clean page content via tools like `trafilatura`.

---

### 🧩 Prompt Update Engine
- Gathers results from vector DB, Elastic, and web search.
- Merges them into a single structured **context window** for the LLM.
- Ensures relevance, diversity, and context completeness.

---

### 🤖 LLM Service (Mistral, GPT-4o, etc.)
- Processes the final prompt with embedded context.
- Can be:
  - **Local** using [Ollama](https://ollama.com) with models like `mistral`, `phi`, or `tinyllama`
  - **Remote** via OpenAI's `gpt-4o` or `gpt-3.5-turbo`
- Returns concise or multi-step answers based on query complexity.

---

## 🔁 Full Query Flow
1. User uploads docs (PDF/TXT) → stored in FAISS + Elastic.
2. User asks a question → hits API.
3. API runs:
   - Vector similarity search
   - Elastic keyword search
   - Optional web search for recent info
4. All results merged → sent as context to LLM.
5. 🧠 LLM generates final output → returned to user.

---

## 🚀 System Overview

| Component         | Role                                                  |
|------------------|--------------------------------------------------------|
| FastAPI           | Web server to handle uploads & queries                |
| FAISS (Vector DB) | Stores document embeddings for semantic search        |
| Elasticsearch     | Indexes raw documents for keyword search              |
| LLM               | Generates answer from retrieved context               |
| LangChain         | Orchestrates RAG pipeline                             |

---

## 🔍 Why Use Both Vector DB and Elasticsearch?

| Feature             | FAISS (Vector DB)                        | Elasticsearch                        |
|--------------------|------------------------------------------|--------------------------------------|
| Search Type         | Semantic (meaning-based)                 | Lexical (keyword-based)              |
| Useful For          | Fuzzy queries, paraphrased questions     | Specific keywords, filters           |
| Example Match       | "boil water" ≈ "heat liquid"             | Only matches "boil" and "water"      |
| Index Size          | Small (dense vectors)                    | Larger (inverted index)              |
| Typical Use in RAG  | Find most relevant context chunks        | Boost recall or targeted retrieval   |

✅ **Hybrid RAG** uses both for best results.

---

## 🏃 Running Lightweight LLMs Locally (CPU-friendly)

**System Assumptions:**

- 32 GB RAM (use ~16 GB safely)
- 8 GB VRAM (unused for now)
- Goal: CPU-only text generation with ~50 token responses

You can use quantized models like `Mistral`, `Phi`, or `TinyLlama`.

### ✅ Recommended Setup: `ollama`

**Install once:**

```bash
# Mac/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Start the server
ollama run mistral
```

# windows
Download Ollama for Windows from their official site: 👉 https://ollama.com/download

Run the installer and launch the Ollama terminal.

Pull and run a model (e.g. mistral):
```
ollama run mistral
```
or 
```bash
"C:\Users\{user_name}\AppData\Local\Programs\Ollama\ollama.exe" run mistral
```

### Other Models
```bash
ollama run mistral         # 7B, solid quality
ollama run phi             # 2.7B, fast reasoning
ollama run tinyllama       # 1.1B, ultra lightweight
```
### Docker LLama
docker run -d -p 11434:11434 --name ollama ollama/ollama


### Calling these models 
```
curl http://localhost:11434/api/generate -d '{
  "model": "mistral",
  "prompt": "What's the capital of France?",
  "stream": false
}'
```


## ⚙️ Add to LangChain (Python)

```bash
from langchain_community.llms import Ollama

llm = Ollama(model="mistral", temperature=0.2, max_tokens=50)

```
## 🧪 Model Capability Comparison (For Local Use)

| Model        | Size    | RAM (Quantized) | Context Limit | Good At                        |
|--------------|---------|------------------|----------------|-------------------------------|
| **TinyLlama**    | 1.1B    | ~2 GB             | ~2K tokens     | Super fast, basic answers     |
| **Phi-2**        | 2.7B    | ~4 GB             | ~2K tokens     | Reasoning, logic, code        |
| **Mistral**      | 7B      | ~8 GB             | 4K–8K tokens   | Strong general-purpose        |
| **LLaMA 2 (7B)** | 7B      | ~10 GB            | 4K tokens      | Open-source GPT-alternative   |
| **Gemma**        | 2B      | ~5 GB             | 2K–4K tokens   | Efficient + clean output      |

⚙️ For short responses (~50 tokens), any of these models should run well on CPU in your 32GB system.




🧠 Example Query: "What’s the population of Germany?"
If you feed this into context:

- “According to 2022 stats, Germany had a population of 83.2 million people.”

Then ask:
- User Query: “What’s the capital of Germany?"

Add More context with Elasticsearch, VectorDB match to the query and fed to the LLM model.

LLM Output:

-  "The capital of Germany is Berlin. Germany, located entirely in Europe, is one of the continent's most powerful economies and has a high standard of living for its population. Its history dates back to 1871 when it was established, with significant periods of industrialization, imperial expansion, and international influence. However, the early 20th century saw Germany involved in both World Wars and the atrocities committed under the Nazi regime. After WWII, Germany lost territories and resources due to the fallout from the wars, and it was divided into East Germany (German Democratic Republic) and West Germany (Federal Republic of Germany). The country was officially reunified on October 3, 1990.\n\n   In 2023, Germany has an estimated population of 84 million people, with Berlin being the largest city. Due to a low birth rate and high death rate, Germany has been experiencing a natural population decline for five decades, making migration crucial for its population growth. In 2022, it was estimated that almost 15 percent of the population is foreign.\n\n   Economically, Germany had a nominal GDP of 3.9 trillion euros (4.1 trillion U.S. dollars) in 2022, making it the fourth largest economy in the world. It is a net exporter of goods and specializes in technologically advanced goods such as automobiles, machinery, electronics, and pharmaceuticals. The European Union trading bloc is its largest trading partner."
