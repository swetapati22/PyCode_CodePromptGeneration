# Code Schema Generation

Tools to **derive event schemas from TextEE-formatted data** and emit:

* `schema.json` – merged event→argument schema across all datasets
* `mapper.json` – original event names → cleaned Python class names
* `init_prompts/<dataset>.txt` – lightweight `@dataclass` skeletons for prompting
* `python_event_defs/<dataset>_definitions_new.py` – runnable class defs per dataset
* `python_event_defs/all_ee_definitions_new.py` – combined class defs across datasets

---

## Input

TextEE-style datasets organized as:

```
<data_root>/
└── ace05-en/
    └── split1/
        ├── train.json
        ├── dev.json
        └── test.json
└── maven/
    └── split1/...
```

Each `*.json` is **JSONL** (one JSON object per line) with the fields:

* `event_mentions[*].event_type` (e.g., `"Conflict:Attack"`)
* `event_mentions[*].arguments[*].role` (e.g., `"Attacker"`)

---

## Usage

From this folder:

```bash
# Run over ALL datasets inside ../data
python generate_schema.py --dataset_folder ../data
```

> **Important:** `--dataset_folder` must be the **parent directory** that contains dataset folders (e.g., `../data`), **not** a single dataset like `../data/ace05-en`.

---

## What the scripts do

1. **`process_dataset()`**
   Builds a raw schema per dataset:

   ```
   {"Conflict:Attack": ["attacker","target","place","mention"], ...}
   ```

2. **`clean_schema()`**
   Converts raw names → Python-friendly class names using `schema_splitters`:
   * ACE05: `Conflict:Attack` → `Attack(ConflictEvent)`
   * CASIE: parent TitleCase: `Attack:Phishing` → `Phishing(AttackEvent)`
   * RAMS: dotted → `conflict.attack.Na` → `conflict_attack_Na(Event)`
   * “None” splitter (e.g., MAVEN): `Military_operation` → `Military_operation(Event)`

   Also emits a mapper of original → cleaned names.

3. **`create_init_prompt()`**
   Writes `init_prompts/<dataset>.txt` with minimal `@dataclass` skeletons (for prompting LLMs).

4. **`generate_python_definitions()`**
   Emits runnable Python modules (`python_event_defs/...`) with:

   * parent base stubs (e.g., `ConflictEvent`)
   * child classes with `__init__` and `__repr__`

---

## Outputs

* `schema.json` – global union of `{ CleanClassName: [roles...] }`
* `mapper.json` – `{ dataset_name: { RawName: CleanClassName } }`
* `init_prompts/<dataset>.txt` – promptable class skeletons
* `python_event_defs/<dataset>_definitions_new.py` – per-dataset classes
* `python_event_defs/all_ee_definitions_new.py` – combined classes

Example cleaned class (ACE05):

```python
@dataclass
class Attack(ConflictEvent):
    def __init__(self, mention: Optional[str] = None, instrument: Optional[List] = None, target: Optional[List] = None, victim: Optional[List] = None, place: Optional[List] = None, agent: Optional[List] = None, attacker: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.instrument = instrument if instrument is not None else []
        self.target = target if target is not None else []
        self.victim = victim if victim is not None else []
        self.place = place if place is not None else []
        self.agent = agent if agent is not None else []
        self.attacker = attacker if attacker is not None else []
    def __repr__(self):
        return f"Attack(mention='{self.mention}', instrument={self.instrument}, target={self.target}, victim={self.victim}, place={self.place}, agent={self.agent}, attacker={self.attacker})"
```

---

## Config: `schema_splitters`

Defined in `generate_schema.py`. Key points:

* `":"` → split like `Parent:Child` (ACE05, CASIE)
* `"."` → split like `parent.child` (RAMS)
* `"None"` (literal string) → **no split**; just normalize punctuation (MAVEN, GENIA, etc.)
* Special cases:

  * CASIE: parent TitleCase
  * RAMS: format `Parent_Child(Event)`
  * SPEED: TitleCase the whole class in no-split branch

---

This folder turns TextEE data into clean, importable event class definitions and helpful prompt skeletons.
