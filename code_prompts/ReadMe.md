# Code Prompts — README

Turn TextEE-style datasets into **instruction-tuning code prompts** for event tasks (ED / EAE / E2E).
This folder builds `"instruction" + code-like "input" + gold "output"` records that your LLM can learn from.

Supports three task flavors (auto-selected per dataset):

* **ED** (Event Detection): triggers + types
* **EAE** (Event Argument Extraction): arguments given a (trigger, type)
* **E2E** (End-to-End): triggers + types + arguments

The task flavor is controlled via `dataset_to_task_mapper` in `utils.py`.

---

## What you get

For each split, JSON arrays saved to:

```
<output_dir>/<dataset_name>/train.json
<output_dir>/<dataset_name>/dev.json
<output_dir>/<dataset_name>/test.json
```

Each item looks like:

```json
{
  "instruction": "# This is an event extraction task ...",
  "input": "# The following lines describe the task definition\n\n@dataclass\nclass Die(LifeEvent):\n    ...\n\n# This is the text to analyze\ntext = \"Five Iraqi civilians ...\" \n\n# The list called result ...\nresult = ",
  "output": "[Die(mention='killed', time=[], place=['houses'], instrument=['missile'], victim=['civilians','woman'], person=[], agent=['coalition'])]"
}
```

> For **EAE**, the pipeline expands outputs to one record per predicted instance and fills the footer placeholders (`{trigger}`, `{event_name}`).

---

## Requirements

* Python **3.9+**
* `pip install -U pip`
* `pip install tqdm`

---

## Inputs the script expects

1. **TextEE-style JSONL** (one JSON per line) under:

```
<input_dir>/<dataset_name>/split1/{train,dev,test}.json
```

Each JSON has fields like `text`, `wnd_id`, and `event_mentions` (with `event_type`, `trigger`, `arguments`, …).

2. **Event class stubs** (for quick eval/verification):

```
../PyCode-TextEE/code_schema_generation/python_event_defs/<dataset_name>_definitions_new.py
```

> The code dynamically imports this module to make sure outputs like `Die(...)` can be parsed.
> Keep the folder structure **as-is** or place a symlink so the default relative path resolves.

3. (Optional) **Guidelines JSON** if you want annotated schemas (`--annotate_schema True`): a consolidated file mapping each event to a list of descriptions and per-argument notes. Example:

```
.../all_event_annotations_guideline_guidelineP.json
```

You can generate this from your guideline\_generation pipeline and its `consolidate_guidelines.py`.

---

## Quickstart

From this folder:

```bash
python prepare_dataset.py \
  --input_dir ../data \
  --dataset_name ace05-en \
  --annotate_schema True \
  --guideline_file ../guideline_generation/Dataset/annotation_guidelines/ace05-en/guidelineP/all_event_annotations_guideline_guidelineP.json \
  --output_dir ./processed_code_prompts/
```

Minimal (no guidelines / plain schemas):

```bash
python prepare_dataset.py \
  --input_dir ../data \
  --dataset_name ace05-en \
  --output_dir ./processed_code_prompts/
```

With **negative samples** (adds extra “no event” candidates per instance):

```bash
python prepare_dataset.py \
  --input_dir ../data \
  --dataset_name ace05-en \
  --add_negative_samples True \
  --negative_sample_count 15 \
  --output_dir ./processed_code_prompts/
```

---

## CLI Arguments

| Argument                  | Description                                                                                                       |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `--input_dir`             | Path to TextEE-formatted JSONL (default: `../../TextEE/processed_data`)                                           |
| `--dataset_name`          | Dataset key (e.g., `ace05-en`)                                                                                    |
| `--annotate_schema`       | If `True`, inject guideline docstrings + per-argument comments into the schema shown in prompts (default `False`) |
| `--guideline_file`        | Path to consolidated guideline JSON (required when `--annotate_schema True`)                                      |
| `--add_negative_samples`  | Add synthetic negatives to **train** (default `False`)                                                            |
| `--negative_sample_count` | How many negatives to consider per instance (default `15`)                                                        |
| `--output_dir`            | Where to write the final JSON arrays (default `./processed_code_prompts/`)                                        |

---

## How it works (high level)

* **Schema strings** come from `code_schema_generation/init_prompts/<dataset>.txt`.
  We parse the `@dataclass` blocks to know argument order; this drives output formatting.

* **Event names** are normalized (`clean_event_name`) per dataset via `schema_splitters` so `"Life:Die"` → `"Die(LifeEvent)"` → key `"Die"`.

* **Grouping**: training samples are split into one sample per event type (`group_by_event_type`).
  Dev/test add “non-present” event schemas to the same text to encourage discrimination.

* **Outputs** are “python-call-like” strings:

  * E2E/ED: `[Event(mention=..., role1=[...], ...)]`
  * EAE: expanded per instance; footer includes `{trigger}` / `{event_name}` filled in.

* **Annotated schemas** (`--annotate_schema True`): we insert a docstring under the class and inline `#` comments per field using the guideline JSON. This improves interpretability and often helps LLMs.

---

## Supported datasets & task flavors

See `dataset_to_task_mapper` in `utils.py`. Out of the box:

* `ace05-en, casie, genia2011/2013, m2e2, mlee, phee, richere-en` → **E2E**
* `speed, maven, mee, fewevent` → **ED**
* `rams, geneva, muc4, wikievents` → **EAE**

If you add a new dataset, update:

* `dataset_to_task_mapper`
* `schema_splitters`
* `code_schema_generation/init_prompts/<dataset>.txt`
* `python_event_defs/<dataset>_definitions_new.py`

---

## Negative sampling (optional)

`--add_negative_samples True` will add prompts where the text is paired with **schemas for events not present** in that text, with `"output": "[]"`. This is useful to stabilize training (e.g., DEGREE-style setups). Control the breadth via `--negative_sample_count`.

---

## Troubleshooting

**1) `ModuleNotFoundError: <dataset>_definitions_new`**
Ensure the event class stubs exist at:

```
../PyCode-TextEE/code_schema_generation/python_event_defs/<dataset_name>_definitions_new.py
```

and that the relative path matches `PY_ADD` in the script (or keep the repo layout unchanged).

**2) `KeyError` while annotating (e.g., `'org'` vs `'Org'`)**
Your guideline JSON keys must match schema field names **after normalization**.
Use the consolidator with **schema alignment** (from your guideline\_generation pipeline) to remap attributes to the canonical names present in `init_prompts/<dataset>.txt`.

**3) `json.decoder.JSONDecodeError` when loading input**
Inputs must be **JSONL** (one JSON object per line). Verify `split1/{train,dev,test}.json` are not full JSON arrays.

**4) `eval(...)` errors in verification**
We eval outputs to sanity-check structure. If it fails:

* Make sure event classes are importable (see #1).
* Look for stray characters in gold outputs or mismatched class names.

**5) Wrong event label shapes in outputs**
Check `clean_event_name` rules and `schema_splitters` for your dataset.
