# Guideline Generation — README

This doc walks you through generating **annotation guidelines** for event extraction in **six stages**:

1. **Prep raw data** → per-event example files
2. **Build prompts** (P / PN / PS)
3. **Call the LLM** to synthesize **base guidelines** (P / PN / PS)
4. **Build INT prompts** (PN-INT / PS-INT) from the base guidelines
5. **Call the LLM** to synthesize **INT guidelines** (PN-INT / PS-INT)
6. **Consolidate** per-event files into **one JSON per variant**

Everything below assumes you run commands **from `guideline_generation/`**.

---

## 1) Requirements

### Python

* Python 3.9+ recommended
* Create/activate a venv if you want:

```bash
python -m venv env
source env/bin/activate
```

### Install deps

```bash
pip install -U pip
pip install tqdm backoff openai
```

> If you’ll use **Azure OpenAI**, you still install `openai`; the same SDK supports both.

---

## 2) Directory layout (what this repo expects)

```
PyCode-TextEE/
├─ data/
│  ├─ <dataset-name>/
│  │  └─ split1/
│  │     └─ train.json                  # Raw (processed) data you already have
│
└─ guideline_generation/
   ├─ pre_processing/
   │  ├─ create_guideline_gen_dataset.py
   │  ├─ full_schema.json
   │  ├─ mapper.json
   │  ├─ generate_guidelines.sh
   │  └─ utils.py
   │
   ├─ generate_prompts/
   │  ├─ create_prompts.py               # Creates P / PN / PS prompts
   │  ├─ create_prompts_INT.py           # Creates PN-INT / PS-INT prompts from guidelinePN / guidelinePS
   │  └─ prompts.py                      # Prompt templates
   │
   ├─ prompting/
   │  ├─ prompt_llms.py                  # Calls OpenAI/Azure to produce P / PN / PS guidelines
   │  ├─ prompt_llm_adv.py               # Advanced LLM prompting script
   │  └─ prompt_llms_INT.py              # Calls OpenAI/Azure to produce PN-INT / PS-INT guidelines
   │
   ├─ post_processing/
   │  └─ consolidate_guidelines.py       # Merges per-event JSONs into one per variant
   │
   ├─ Dataset/
   │  ├─ pre_req_data/                   # (created in Step 1)
   │  │  └─ <dataset-name>/
   │  ├─ prompts/                        # (created in Step 2 and Step 4)
   │  │  └─ <dataset-name>/
   │  │     ├─ P/
   │  │     ├─ PN/
   │  │     ├─ PS/
   │  │     ├─ PN-INT/
   │  │     └─ PS-INT/
   │  └─ annotation_guidelines/          # (created in Step 3 and Step 5)
   │     └─ <dataset-name>/
   │        ├─ guidelineP/
   │        ├─ guidelinePN/
   │        ├─ guidelinePS/
   │        ├─ guidelinePN-INT/
   │        └─ guidelinePS-INT/
   │           └─ all_event_annotations_guideline_<variant>.json  # Consolidated file (per variant)
   │
   ├─ logs/
   │  └─ <dataset-name>/
   │     ├─ guidelineP/
   │     ├─ guidelinePN/
   │     ├─ guidelinePS/
   │     ├─ guidelinePN-INT/
   │     └─ guidelinePS-INT/
   │
   └─ README.md
```

---

## 3) Environment variables (only for Steps 3 & 5)

### OpenAI (default)

```bash
export OPENAI_API_KEY=sk-...
```

### Azure OpenAI (optional)

```bash
export AZURE_OPENAI_API_KEY=...
export AZURE_OPENAI_ENDPOINT="https://<your-resource>.openai.azure.com/"
# Optional (defaults provided):
export AZURE_OPENAI_API_VERSION="2024-04-01-preview"
```

---

## 4.1) Run through One-Command via `guideline_generation.sh`

If you prefer to run the whole pipeline (base, INT, or both) with **one command**, use the provided orchestrator script.

From `guideline_generation/`:

```bash
# First-time setup (only once)
chmod +x guideline_generation.sh

# Set your API key (required for --provider openai)
export OPENAI_API_KEY=sk-...

# For Azure:
# export AZURE_OPENAI_API_KEY=...
# export AZURE_OPENAI_ENDPOINT="https://<your-resource>.openai.azure.com/"
# export AZURE_OPENAI_API_VERSION="2024-04-01-preview"
```

> 💡 **Reminder:**
>
> * `--provider openai` → requires `OPENAI_API_KEY`
> * `--provider azure` → requires `AZURE_OPENAI_API_KEY` and `AZURE_OPENAI_ENDPOINT`

### **Examples**

* **Base guidelines (P, PN, PS all together):**

```bash
bash guideline_generation.sh -d <dataset_name> --mode ALL --provider openai
```

* **INT guidelines (PN-INT + PS-INT, assumes PN & PS already generated):**

```bash
bash guideline_generation.sh -d <dataset_name> --mode ALL-INT --provider openai
```

* **Full run: base + INT in one shot:**

```bash
bash guideline_generation.sh -d <dataset_name> --mode ALL-FULL --provider openai
```

* **Single modes:**

```bash
# Base only:
bash guideline_generation.sh -d <dataset_name> --mode PN --provider openai

# INT only:
bash guideline_generation.sh -d <dataset_name> --mode PS-INT --provider openai
```

> The `.sh` orchestrator **automatically runs consolidation** at the end of each flow, creating
> `Dataset/annotation_guidelines/<dataset>/<variant>/all_event_annotations_guideline_<variant>.json`.

### **Options**

| Flag                      | Description                                                               |
| ------------------------- | ------------------------------------------------------------------------- |
| `-d / --dataset`          | Dataset name under `../data/`                                             |
| `--mode`                  | One of: `P`, `PN`, `PS`, `ALL`, `PN-INT`, `PS-INT`, `ALL-INT`, `ALL-FULL` |
| `--provider`              | `openai` (default) or `azure`                                             |
| `--llm`                   | Model key (default: `gpt-4o`)                                             |
| `--top_n` / `--neg_top_n` | Positive/negative examples per event (default: 5)                         |
| `--max_tokens`            | Decoding limit for API (default: 4096)                                    |

> ℹ **Tip:** If your environment requires a specific interpreter, run:
> `PYTHON_BIN=python3 bash guideline_generation.sh -d <dataset_name> --mode ALL --provider openai`

---

## 4.2) Run Step-by-step

### Step 1 — Create per-event example files (pre-req data)

This script reads your raw dataset and writes the *top-N* examples per event type to:

```
guideline_generation/Dataset/pre_req_data/<dataset-name>/*.json
```

**Run:**

```bash
cd guideline_generation

python pre_processing/create_guideline_gen_dataset.py \
  -d <dataset_name> \
  -i ../data/
```

**Outputs:**

* `Dataset/pre_req_data/<dataset>/meta_data/{meta_data.json, ontology.json}`
* `Dataset/pre_req_data/<dataset>/*.json` — per-event files (up to 10 selected examples with context)

---

### Step 2 — Create prompts (P / PN / PS)

Writes prompts to:

```
guideline_generation/Dataset/prompts/<dataset>/<mode>/prompt_<EventType>.txt
```

**Run (all modes):**

```bash
python generate_prompts/create_prompts.py \
  -d <dataset_name> \
  -m ALL \
  --top_n 5 \
  --neg_top_n 5
```

(You can also run single modes `P`, `PN`, or `PS`.)

---

### Step 3 — Prompt the LLM to produce base guidelines

Writes per-event guideline JSONs to:

```
guideline_generation/Dataset/annotation_guidelines/<dataset>/(guidelineP|guidelinePN|guidelinePS)/*.json
```

**Run (all modes):**

```bash
python prompting/prompt_llms.py \
  -d <dataset_name> \
  --mode ALL \
  --provider openai
```

---

### Step 4 — Generate INT prompts (PN-INT / PS-INT)

Reads base guidelines and builds INT prompts:

```
python generate_prompts/create_prompts_INT.py -d <dataset_name> -m ALL
```

Outputs to:

```
Dataset/prompts/<dataset>/(PN-INT|PS-INT)/*.txt
```

---

### Step 5 — Prompt the LLM for INT guidelines

Writes per-event INT JSONs to:

```
Dataset/annotation_guidelines/<dataset>/(guidelinePN-INT|guidelinePS-INT)/*.json
```

**Run:**

```bash
python prompting/prompt_llms_INT.py \
    -d <dataset_name> \
    --mode ALL-INT \
    --provider openai
```

---

### Step 6 — Consolidate per-event JSONs (one file per variant)

Create a single JSON per variant that merges all per-event files.

**Dataset scope (does every variant under the dataset):**

```bash
python post_processing/consolidate_guidelines.py -d <dataset_name>
```

**Single-variant scope (just one folder):**

```bash
python post_processing/consolidate_guidelines.py \
  -v Dataset/annotation_guidelines/<dataset_name>/guideline<variant>
```

**Outputs (one per variant):**

```
Dataset/annotation_guidelines/<dataset>/<variant>/all_event_annotations_guideline_<variant>.json
```

---

## 5) Quickstart (TL;DR)

From `guideline_generation/`:

```bash
# Step 1
python pre_processing/create_guideline_gen_dataset.py -d <dataset_name> -i ../data/

# Step 2
python generate_prompts/create_prompts.py -d <dataset_name> -m ALL --top_n 5 --neg_top_n 5

# Step 3
export OPENAI_API_KEY=sk-...
python prompting/prompt_llms.py -d <dataset_name> --mode ALL --provider openai

# Step 4
python generate_prompts/create_prompts_INT.py -d <dataset_name> -m ALL

# Step 5
python prompting/prompt_llms_INT.py -d <dataset_name> --mode ALL-INT --provider openai

# Step 6 (consolidate per variant)
python post_processing/consolidate_guidelines.py -d <dataset_name>
```

**Final outputs (Example ACE):**

```
# Base per-event files
Dataset/annotation_guidelines/ace05-en/guidelineP/*.json
Dataset/annotation_guidelines/ace05-en/guidelinePN/*.json
Dataset/annotation_guidelines/ace05-en/guidelinePS/*.json

# INT per-event files
Dataset/annotation_guidelines/ace05-en/guidelinePN-INT/*.json
Dataset/annotation_guidelines/ace05-en/guidelinePS-INT/*.json

# Consolidated (one file per variant)
Dataset/annotation_guidelines/ace05-en/guidelineP/all_event_annotations_guideline_guidelineP.json
Dataset/annotation_guidelines/ace05-en/guidelinePN/all_event_annotations_guideline_guidelinePN.json
Dataset/annotation_guidelines/ace05-en/guidelinePS/all_event_annotations_guideline_guidelinePS.json
Dataset/annotation_guidelines/ace05-en/guidelinePN-INT/all_event_annotations_guideline_guidelinePN-INT.json
Dataset/annotation_guidelines/ace05-en/guidelinePS-INT/all_event_annotations_guideline_guidelinePS-INT.json
```

---

## 6) Troubleshooting

* **No prompts found error**
  You skipped Step 2 or pointed `--prompt_dir` wrong. Check:
  `Dataset/prompts/<dataset>/<mode>/*.txt`

* **OpenAI SDK client not available**
  `pip install --upgrade openai` and try again.

* **401 / auth errors**
  Ensure `OPENAI_API_KEY` or Azure env vars are set correctly in the same shell.

* **Rate limits / timeouts**
  The scripts include backoff/cooldown. Re-run; they skip already-generated outputs.

* **Different working dir**
  This README assumes commands are run from **`guideline_generation/`**. Paths are relative to that.

---
