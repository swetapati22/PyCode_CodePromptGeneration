# Instruction Tuning with Annotation Guidelines for Event Extraction (Findings of ACL 2025)
> Efficient and extensible Event Extraction with Code Prompts and Annotation Guidelines, built on top of [TextEE](https://github.com/ej0cl6/TextEE). 

This repository is a submodule of our paper source code [PyCode_EventExtraction](https://github.com/swetapati22/PyCode_EventExtraction) that includes code for:
- `PyCode-Code Prompt Generation`: The scipt to obtain code prompts for 15 event extraction datasets supported by TextEE. This sub-module from the source code of our paper is used to reproduce [our work in generating train, dev and test data (instruction, prompt, response pairs) in python code format from natural language instruction format](https://arxiv.org/abs/2502.16377).

<div align="center">

[![🛠️ Updates](https://img.shields.io/badge/🛠️%20Updates-Click%20Here-informational?style=flat-square)](#updates) •
[![📂 Datasets](https://img.shields.io/badge/📂%20Datasets-15%20Supported-brightgreen?style=flat-square)](#datasets) •
[![⚙️ Environment](https://img.shields.io/badge/⚙️%20Environment-Setup-orange?style=flat-square)](#environment) •
[![🚀 Running](https://img.shields.io/badge/🚀%20Running-Instructions-blueviolet?style=flat-square)](#running) •
[![📄 Paper](https://img.shields.io/badge/📄%20arXiv-2502.16377-b31b1b?style=flat-square)](https://arxiv.org/abs/2502.16377)


</div>

---

**Authors**:  
Saurabh Srivastava*, Sweta Pati*, Ziyu Yao

---

## 🧩 Introduction

**PyCode-TextEE** extends [TextEE](https://github.com/ej0cl6/TextEE), bringing **event extraction into the era of prompt-based large language models**.

While **TextEE** standardizes 10+ event extraction datasets into a unified JSON format—making them reproducible and comparable—**PyCode-TextEE** takes the next leap:

> ✨ We transform TextEE-formatted data into **code-style prompts**—a format that is both readable and executable by LLMs and ideal for structured evaluation. In addition, we annotate the code-prompts with annotation guidelines. Below, we provide an example of code prompt and how we integrate annotation guidelines within them:

### What are Code Prompts and Annotation Guidelines?
- `Code prompting` is a technique that enhances reasoning abilities in text+code LLMs by transforming natural language (NL) tasks into code representations. Instead of executing the code, the model uses it as a structured input format to reason and generate answers. *The labels such event classes and arguments are represented as Python classes, and the guidelines or instructions are introduced as docstrings.* The model start generating after the `result =`  line.

- `Annotation Guidelines` involve defining how to identify and classify events and their arguments within a text or other data. These guidelines help ensure consistency and quality in the annotation process, which is crucial for training machine learning models for event extraction. The performance of current SoTA models heavily depends
on the quantity of human-annotated data, as the model learns the guidelines from these examples. 

⚠️ Note that not all datasets release their annotation guidelines. We provide code to generate these annotation guidelines automatically using a few training samples.

#### An example for a code prompt with annotation guidelines is shown below:
```python
# This is an event extraction task where the goal is to extract structured events from the text. A structured event contains an event trigger word, an event type, the arguments participating in the event, and their roles in the event. For each different event type, please output the extracted information from the text into python-style dictionaries where the first key will be 'mention' with the value of the event trigger. Next, please output the arguments and their roles following the same format. The event type definitions and their argument roles are defined next.

# Here are the event definitions:

@dataclass
class Meet(ContactEvent):
    """A 'Meet(ContactEvent)' is triggered by interactions where individuals or groups come together for a specific purpose, either physically or virtually. This event involves direct interaction, distinguishing it from remote communication events like 'PhoneWrite'. It encompasses formal and informal gatherings such as diplomatic talks, business meetings, press conferences, and forums, but excludes casual or unplanned encounters."""
    mention: str  # The text span that triggers the event.
    entity: List  # Entities are individuals, groups, organizations, or countries participating in the meeting. They represent the participants involved in the event.
    place: List  # The place is the location where the meeting occurs, providing context for the event. It can be a city, building, specific venue, or virtual platform. 

# This is the text to analyze
text = "The meeting concluded with the delegates voting by show of hands to meet again in 10 days."

result = [
    Meet(mention='meeting', entity=['delegates'], time=[], place=[]), 
    Meet(mention='meet', entity=['delegates'], time=['10 days'], place=[])
]
```
> PyCode-TextEE transforms EE datasets into the above format which have shown to perform well with LLMs. For more details, please refer to our paper [Instruction-Tuning LLMs for Event Extraction with Annotation Guidelines](https://arxiv.org/abs/2502.16377).
---

### 🚀 What’s New in PyCode-TextEE?

- **CodePrompt Format Conversion**  
  We convert event structures (event triggers, arguments—if available) into Python-like prompts (e.g., `Attack(mention="...", attacker=[...], target=[...])`) to help LLMs handle structured outputs.

- **Annotation Guideline Generation**
  While annotation guidelines have helped LLMs achieve SOTA results for EE, previous approaches assume that these guidelines are made available which is not always true. We take the next steps in generating these guidelines automatically from a few training samples. 

- **Plug-and-Play with TextEE**  
  Directly load standardized datasets from TextEE and transform them with one command into training-ready CodePrompts.

- **Evaluation Toolkit for Prompted LLMs**  
  We provide exact-match evaluation utilities that compute **precision, recall, and F1 scores** over structured LLM outputs.

- **Code to Reproduce LLaMAEvents**  
  Includes all data transformations and training scripts used for our paper on utilizing code prompts and annotation guidelines. Code for that will live in `LLaMAEvents/`.

<a id="updates"></a>
## 🛠️ Updates

- **April 23, 2025** — We release **PyCode-TextEE**, a modular framework for converting standardized event extraction datasets (via TextEE) into code-style prompts, along with exact-match evaluation scripts.  
  Feel free to reach out if you’d like to contribute your **models**, **datasets**, or ideas!

<a id="datasets"></a>
## 📂 Supported Datasets

We support **15 datasets** for Event Detection (ED), Event Argument Extraction (EAE), and End-to-End (E2E) Event Extraction.  All are converted into **code-style prompts** and support evaluation using our exact-match metric suite.  

The table below also shows whether annotation **guidelines** are included for each dataset.

<div align="center">
<table>
<thead>
<tr>
  <th><strong>Dataset</strong></th>
  <th><strong>Task(s)</strong></th>
  <th><strong>Paper Title</strong></th>
  <th><strong>Source</strong></th>
  <th><strong>Guidelines</strong></th>
</tr>
</thead>
<tbody>
<tr>
  <td><code>ACE05</code></td>
  <td>ED, EAE, E2E</td>
  <td>The Automatic Content Extraction (ACE) Program</td>
  <td><a href="https://www.ldc.upenn.edu/">LDC</a></td>
  <td>🔘</td>
</tr>
<tr>
  <td><code>ERE</code></td>
  <td>ED, EAE, E2E</td>
  <td>From Light to Rich ERE</td>
  <td><a href="https://www.ldc.upenn.edu/">LDC</a></td>
  <td>🔘</td>
</tr>
<tr>
  <td><code>MLEE</code></td>
  <td>ED, EAE, E2E</td>
  <td>Biological Event Extraction</td>
  <td><a href="https://academic.oup.com/bioinformatics/article/28/18/i575/245077">Bioinformatics</a></td>
  <td>⚪️</td>
</tr>
<tr>
  <td><code>Genia2011</code></td>
  <td>ED, EAE, E2E</td>
  <td>Genia Event Task (2011)</td>
  <td><a href="https://www.aclweb.org/anthology/W11-1801/">BioNLP 2011</a></td>
  <td>⚪️</td>
</tr>
<tr>
  <td><code>Genia2013</code></td>
  <td>ED, EAE, E2E</td>
  <td>Genia Event Task (2013)</td>
  <td><a href="https://www.aclweb.org/anthology/W13-5201/">BioNLP 2013</a></td>
  <td>⚪️</td>
</tr>
<tr>
  <td><code>M2E2</code></td>
  <td>ED, EAE, E2E</td>
  <td>Cross-media Structured Common Space</td>
  <td><a href="https://aclanthology.org/2020.acl-main.188/">ACL 2020</a></td>
  <td>⚪️</td>
</tr>
<tr>
  <td><code>CASIE</code></td>
  <td>ED, EAE, E2E</td>
  <td>CASIE: Cybersecurity Event Extraction</td>
  <td><a href="https://ojs.aaai.org/index.php/AAAI/article/view/6155">AAAI 2020</a></td>
  <td>⚪️</td>
</tr>
<tr>
  <td><code>PHEE</code></td>
  <td>ED, EAE, E2E</td>
  <td>Pharmacovigilance Event Extraction</td>
  <td><a href="https://aclanthology.org/2022.emnlp-main.343/">EMNLP 2022</a></td>
  <td>⚪️</td>
</tr>
<tr>
  <td><code>MEE</code></td>
  <td>ED</td>
  <td>Multilingual Event Extraction</td>
  <td><a href="https://aclanthology.org/2022.emnlp-main.428/">EMNLP 2022</a></td>
  <td>⚪️</td>
</tr>
<tr>
  <td><code>FewEvent</code></td>
  <td>ED</td>
  <td>Few-Shot Event Detection</td>
  <td><a href="https://dl.acm.org/doi/10.1145/3336191.3371962">WSDM 2020</a></td>
  <td>⚪️</td>
</tr>
<tr>
  <td><code>MAVEN</code></td>
  <td>ED</td>
  <td>Massive General-Domain ED</td>
  <td><a href="https://aclanthology.org/2020.emnlp-main.154/">EMNLP 2020</a></td>
  <td>⚪️</td>
</tr>
<tr>
  <td><code>SPPED</code></td>
  <td>ED</td>
  <td>ED from Social Media for Epidemic Prediction</td>
  <td><a href="https://aclanthology.org/2024.naacl-main.172/">NAACL 2024</a></td>
  <td>⚪️</td>
</tr>
<tr>
  <td><code>MUC-4</code></td>
  <td>EAE</td>
  <td>Fourth Message Understanding Conference</td>
  <td><a href="https://www-nlpir.nist.gov/related_projects/muc/">MUC 1992</a></td>
  <td>⚪️</td>
</tr>
<tr>
  <td><code>RAMS</code></td>
  <td>EAE</td>
  <td>Multi-Sentence Argument Linking</td>
  <td><a href="https://aclanthology.org/2020.acl-main.743/">ACL 2020</a></td>
  <td>🔘</td>
</tr>
<tr>
  <td><code>WikiEvents</code></td>
  <td>EAE</td>
  <td>Conditional Generation for Doc-level EAE</td>
  <td><a href="https://aclanthology.org/2021.naacl-main.417/">NAACL 2021</a></td>
  <td>🔘</td>
</tr>
<tr>
  <td><code>GENEVA</code></td>
  <td>EAE</td>
  <td>Benchmarking Generalizability for EAE</td>
  <td><a href="https://aclanthology.org/2023.acl-long.794/">ACL 2023</a></td>
  <td>🔘</td>
</tr>
</tbody>
</table>


</div>

<a id="environment"></a>
## ⚙️ Environment

Although there is no need of any additional package to run PyCode-TextEE, we recommend using **Python 3.9+** with a clean virtual environment (e.g., via `venv` or `conda`).

### 🔹 Install Dependencies
```bash
# Clone the repo
git clone https://github.com/yourname/PyCode-TextEE.git
cd PyCode-TextEE

# Create a virtual environment (optional)
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install requirements (optional)
pip install -r requirements.txt
```

### 🔹 Core Dependencies
> These are the minimal dependencies to run the code.
- `datasets`  
- `openai`  # (used for guideline generation)
- `wandb` # (optional for experiment tracking)  

### ⚠️ Note
Some datasets (e.g., ACE, ERE) require **LDC license** to access raw files.  We provide code for preprocessing them, but not the data itself.

<a id="running"></a>
## 🚀 Running the Code

Below is a step-by-step guide to run the `code_prompts` generation submodule from PyCode-TextEE.  
Our pipeline is divided into 3 main stages inorder to generate code prompts:

---
### ✣ Step 0 — Obtaining TextEE Format Dataset
Our code accepts data formatted after TextEE pre-processing. Please follow the instructions in `data` directory from the [TextEE repo](https://github.com/ej0cl6/TextEE/tree/main).

Make sure after running TextEE, you have data saved in the following structure:
#### 📂 Expected dataset layout:
```
<your_dataset_dir>/
├── ace05-en/
│   ├── split1/
│   │   ├── train.json
│   │   ├── dev.json
│   │   └── test.json
│   └── ...
├── casie/
└── ...
```

### 🔹 Step 1 — [Optional] Generate Code Schema

**Note**: We have already generated schema for all 15 supported datasets. This step is only required for new datasets.

---

### 🔹 Step 2: Generating Annotation Guidelines from a few Training Samples

While code prompts convert EE datasets into a structured format, annotating the schema with guidelines helps LLMs understand event and argument definitions. As shown in [our paper](https://arxiv.org/abs/2502.16377), annotated schema with these guidelines helps achieve SOTA results with LLaMA-3-8.1B. However, not all datasets release these guidelines; we propose five ways to synthesize them:

* **Guideline-P**: Uses positive (in-class) examples to generate guidelines.
* **Guideline-PN**: Adds negative examples from other event classes.
* **Guideline-PS**: Uses sibling classes in the schema as negatives.
* **Guideline-PN-INT / Guideline-PS-INT**: Integrate multiple PN/PS samples into consolidated INT guidelines.

**Note**: Pre-synthesized and human guidelines live in `guideline_generation/Dataset/annotation_guidelines/<Dataset Name>`.

### 📘 Guideline File Format (consolidated)

After consolidation, each variant folder contains a single file:

```
Dataset/annotation_guidelines/<dataset_name>/<variant>/all_event_annotations_guideline_<variant>.json
```

Each event key maps to a nested structure:

```json
{
  "EventName1": {
    "description": [
      "One possible definition.",
      "Another variation of the same."
    ],
    "attributes": {
      "mention": "The text span that triggers the event.",
      "arg_1": ["One definition for arg_1", "another definition for arg_1"]
    }
  }
}
```

- This consolidated file is what you will use downstream for annotation, multiple definitions enable randomized phrasing during conversion.
---

### 🔹 Step 3: Obtaining Code Prompts
We first need to make sure that python event definitions are in current environment to verify code prompts.
```bash
cd python_event_defs # this directory is already included in the code or can be generated using Step 1. You can find it in "PyCode-TextEE/code_schema_generation/python_event_defs"
export PYCODE_HOME=$(pwd)
export PYTHONPATH=$PYCODE_HOME:$PYCODE_HOME:$PYTHONPATH
cd ../../ # redirect the terminal to PyCode home directory
```
Run the following:

```bash
cd code_prompts
python prepare_dataset.py \
    --input_dir <your_dataset_directory> \
    --dataset_name <dataset_name> \
    --annotate_schema <True/False> \ #if unspecified, the schema will be left unannotated because the flag defaults to False.
    --guideline_file <guideline_file> \ #if unspecified, the guidelines will be generated automatically as specified in Step-2.
    --add_negative_samples <True/False> \ #used to reproduce our LLaMAEvents results.
    --output_dir ./processed_code_prompts/
```

---

### ⚙️ Argument Descriptions

| Argument               | Description |
|------------------------|-------------|
| `--input_dir`          | Path to TextEE-formatted JSONs (default: `../../TextEE/processed_data`) |
| `--dataset_name`       | Name of the dataset to process (e.g., `ace05-en`) |
| `--annotate_schema`    | Add class docstrings and inline comments using guidelines (default: `False`) |
| `--guideline_file`     | Guideline JSON file for schema annotation (required if `annotate_schema=True`) |
| `--add_negative_samples` | Add negative examples to training set (default: `False`) |
| `--output_dir`         | Where to save the converted code prompts (default: `./processed_code_prompts/`) |

---

### 🧬 Annotated Prompt Example (with Guidelines)

When `--annotate_schema=True`, we generate prompts like:

```python
@dataclass
class Event(ParentEvent):
    """the event definition"""
    mention: str  # Event trigger definition
    arg_1: List   # Definition of argument 1
    arg_2: List   # Definition of argument 2
```

This format supports **LLM-compatible** structure learning and improves interpretability.

---

### 💡 Tip
⓵ Skip `--guideline_file` and `--annotate_schema` if you're only interested in raw code prompts. If `annotate_schema` is True but the `guideline_file` is unspecified or not found, Step 2 will be executed automatically to produce `guideline_file`.

⓶ Use `--add_negative_samples` if you want to add negative sample per instance similar to [DEGREE](https://github.com/PlusLabNLP/DEGREE).

### 🧪 See the converted code prompts:

We provide a several examples of the code prompt annotated data in the `/code_prompts/processed_code_prompts/` folder:

---
## 🧩 Citation

If you find our work helpful, please cite our work:
```
@inproceedings{srivastava-etal-2025-instruction,
    title = "Instruction-Tuning {LLM}s for Event Extraction with Annotation Guidelines",
    author = "Srivastava, Saurabh  and
      Pati, Sweta  and
      Yao, Ziyu",
    editor = "Che, Wanxiang  and
      Nabende, Joyce  and
      Shutova, Ekaterina  and
      Pilehvar, Mohammad Taher",
    booktitle = "Findings of the Association for Computational Linguistics: ACL 2025",
    month = jul,
    year = "2025",
    address = "Vienna, Austria",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.findings-acl.677/",
    pages = "13055--13071",
    ISBN = "979-8-89176-256-5",
    abstract = "In this work, we study the effect of annotation guidelines{--}textual descriptions of event types and arguments, when instruction-tuning large language models for event extraction. We conducted a series of experiments with both human-provided and machine-generated guidelines in both full- and low-data settings. Our results demonstrate the promise of annotation guidelines when there is a decent amount of training data and highlight its effectiveness in improving cross-schema generalization and low-frequency event-type performance."
}
```
---