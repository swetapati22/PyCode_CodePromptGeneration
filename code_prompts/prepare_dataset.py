#code_prompts/prepare_dataset.py
import re
import os
import copy
import json
import random
import argparse
from utils import *
from glob import glob
from tqdm import tqdm

# Points the verifier to the generated Python event class stubs
PY_ADD = "./../PyCode-TextEE/code_schema_generation/python_event_defs/"

parser = argparse.ArgumentParser()
# Location of raw/split data (train/dev/test). Example: ../data
parser.add_argument("--input_dir", type=str, default="./../../TextEE/processed_data")
# Dataset name key that drives schema mapping and task templates. Example: "ace05-en"
parser.add_argument("--dataset_name", type=str, default="ace05-en")
# If True, injects guideline docstrings and per-argument comments into the schema strings used in prompts
parser.add_argument("--annotate_schema", default=False)
# Path to the consolidated guideline JSON (or a token that falls back to ../guidelines/<dataset>_event_guidelines.json)
parser.add_argument("--guideline_file", type=str, default="ace05-en")
# Whether to augment training with extra negative samples (dataset-specific util)
parser.add_argument("--add_negative_samples", default=False)
# Output directory for the final instruction/input/output triplets
parser.add_argument("--output_dir", type=str, default="./processed_code_prompts/")
# How many synthetic negatives to add if negative sampling is enabled
parser.add_argument("--negative_sample_count", type=int, default=15)

# Global cache of annotated schemas per event; used to enumerate schemas in dev/test non-event prompts
all_annotated_schema = {}

def annotate_schema_fun(schema, guidelines, do_print = False):
    """
    Add human-readable guidance (event definition + per-argument comments) into a Python @dataclass schema.

    Example (before):
        @dataclass
        class Die(LifeEvent):
            mention: str
            victim: List

    Example (after, with annotations):
        @dataclass
        class Die(LifeEvent):
            \"\"\"The 'Die' event involves ...\"\"\"
            mention: str # The text span that triggers the event.
            victim: List # The 'victim' argument specifies ...
    """
    assert type(schema) == str, "Schema should be a string"
    if(do_print):
        print("Schema: ", schema)
        # xxx
    # These track which event class we're currently annotating and its guideline block
    event_name, annotated_guidelines = None, None
    annotated_schema = ""
    # Walk the schema line-by-line so we can: (1) attach a docstring after the class line, (2) add inline comments after each field
    for line in schema.split("\n"):
        # Keep the dataclass decorator verbatim
        if(line.strip()=="@dataclass"):
            annotated_schema += line + "\n"
        # When we see the class line, locate the event key and attach a random definition variant as a docstring
        elif(line.strip().startswith("class")):
            # event_name parsing: "class Die(LifeEvent):" → "Die"
            # event_name = line.replace("class", "").replace(":", "").replace("(", "").replace(")", "").replace("Event", "").strip()
            event_name = line.split("(")[0].replace("class", "").strip()
            # Look up the consolidated guideline block for this event (produced by the guideline_generation pipeline)
            # print("Event Name: ", event_name)
            annotated_guidelines = guidelines[event_name]
            # # --- DEBUG: show what we have for this event
            # print(f"[DBG] Processing event: {event_name}")
            # print(f"[DBG]   description type={type(annotated_guidelines.get('description'))}")
            # print(f"[DBG]   attributes keys={list((annotated_guidelines.get('attributes') or {}).keys())}")
            # # ---
            # Choose one of the definition strings (helps diversify the natural language guidance across prompts)
            docstring = random.choice(annotated_guidelines["description"])
            annotated_schema += line + f"\n    \"\"\"{docstring}\"\"\"\n"
        # Skip truly blank schema lines to avoid noisy output
        elif (line.strip()==""):
            continue
        else:
            # Field line, e.g., "victim: List" → we’ll attach a guideline comment for that field
            arg_name = line.split(":")[0].strip()
            # Standardize mention: always "str" with a canonical inline explanation
            if(arg_name=="mention"):
                random_comments = "The text span that triggers the event."#random.choice(annotated_guidelines["Event Definition"])
                line = f"    {arg_name}: str # {random_comments}"
            else:
                # For other arguments, sample one of the guideline sentences from the consolidated JSON
                # NOTE: This assumes keys in guidelines match the schema field names; consolidate script aligns names for you.
                random_comments = random.choice(annotated_guidelines["attributes"][arg_name])
                # # --- DEBUG: show which arg we're about to fetch and whether it's present
                # attrs = annotated_guidelines.get("attributes", {})
                # if arg_name not in attrs:
                #     print(f"[DBG]   MISSING attribute in guidelines for event='{event_name}': "
                #           f"schema_arg='{arg_name}' not in {list(attrs.keys())}")
                # else:
                #     v = attrs[arg_name]
                #     print(f"[DBG]   Using attribute '{arg_name}' (type={type(v)}) "
                #           f"example={v[:1] if isinstance(v, list) else v}")
                # # ---
                line = f"    {arg_name}: List # {random_comments}"
            annotated_schema += line + "\n"
    # Cache at least one annotated schema per event so test/dev enumeration can iterate schemas across all events
    if(all_annotated_schema.get(event_name) is None):
        all_annotated_schema[event_name] = []
    all_annotated_schema[event_name].append(annotated_schema)
    # print(annotated_schema)
    assert type(annotated_schema) == str, "Annotated schema should be a string"
    return annotated_schema
        
# Markers used when assembling the code prompt: we first show task definition (schema), then the text under analysis
text_sep = "# This is the text to analyze"
task_sep = "# The following lines describe the task definition"

def group_by_event_type(sample):
    """
    Split a single sample with multiple event mentions into a list of per-event samples.
    Each per-event sample:
      * preserves the same 'text' and 'wnd_id'
      * only contains 'event_mentions' belonging to a single 'event_type'

    This lets the training pipeline produce one prompt per (text, event type).
    """
    new_samples = []
    current_text = sample["text"]
    current_wnd_id = sample["wnd_id"]
    if(len(sample["event_mentions"]) == 0):# if there are no event mentions, return the sample as is
        return [sample]
    #otherwise, group the events by their event type
    grouped_events = {}
    for event in sample["event_mentions"]:
        event_type = event["event_type"]
        # Create a shell with the same keys as an event but an empty 'event_mentions' list; we will append only the matching ones
        if(event_type not in grouped_events):
            grouped_events[event_type] = dict([(key, val) for key, val in event.items() if key != "event_mentions"])
            grouped_events[event_type].update({"event_mentions": []})# set it to empty list so that we can group by event type
        grouped_events[event_type]["event_mentions"].append(event)
    # Turn each grouped bucket into a new per-event sample (with shared text and wnd_id)
    for event_type, event in grouped_events.items():
        new_event = copy.deepcopy(event)
        new_event["text"] = current_text
        new_event["wnd_id"] = current_wnd_id
        new_samples.append(new_event)
    return new_samples

#given an input text, converts it into code format.
def prepare_input(sample, text, event_schemas, task_type, dataset_name, is_dev_test_data = False, current_event = None, do_annotate_schema = False, guidelines = None):
    """
    Build the instruction + input prompt for a single (text, event) example.

    Flow:
      1) Resolve which event we’re targeting.
      2) Normalize event name to match the schema keys (clean_event_name).
      3) Optionally annotate the schema with guideline docstrings/comments.
      4) Assemble the final code prompt:
         <task_sep>
         <annotated schema>
         <text_sep>
         text = "<escaped text>"

    Returns:
      (instruction, prompt)
    """
    footer = task_to_prompts[task_type]["footer"]
    try:
        event_name = sample["event_mentions"][0]["event_type"]# get the current event name
    except:
        # Non-event example: pick a random event schema so the model still practices event matching on negative cases
        event_name = random.choice(list(event_schemas.keys()))# if there is no event name, get a random event name. This happens for non-event instances
    if(is_dev_test_data):# when we are preparing the test/dev datasets, we "may" pass the current event name because we are going to enumerate over all the events.
        event_name = current_event
    original_event_name = event_name + ""# a copy for debug
    # Unify dataset-specific surface (e.g., "Life:Die") to the canonical key used in schema (e.g., "Die")
    event_name = clean_event_name(event_name, dataset_name).split("(")[0].strip()#normalize the event name
    # event_schemas maps event → a Python @dataclass schema string; pick the one we need
    schema = event_schemas[event_name]# we pass the list of schemas for the event name and extract corresponding to current event type
    # If annotate_schema, weave guideline text into the schema, otherwise use the plain schema
    annotated_schema = schema if not do_annotate_schema else annotate_schema_fun(schema, guidelines, False)# optionally, add guidelines to the schema
    # print(f"Annotated Schema:\n{annotated_schema}")
    # xxx
    # Code prompt layout mirrors the templates used in training so the model learns a consistent "contract"
    prompt = task_sep + "\n\n" + annotated_schema + "\n\n" + text_sep + f"\ntext = \"{text}\"\n\n{footer}"
    instruction = task_to_prompts[task_type]["header"]
    return instruction, prompt    

def prepare_test_dev_input(text, sample, event_schemas, event_name, dataset_name, is_dev_test_data = False, do_annotate_schema = False, guidelines = None):
    """
    Produce dev/test instances:
      * If event_name is None (non-event text), enumerate ALL event schemas across this same text.
      * Else, create a single instance for the specified event_name.

    Benefit:
      This yields balanced evaluation: for a single text, the model must decide which event schema (if any) applies.
    """
    header = task_to_prompts[dataset_to_task_mapper[dataset_name]]["header"]
    footer = task_to_prompts[dataset_to_task_mapper[dataset_name]]["footer"]
    new_instances = []
    if(event_name is None):# if there is no event name, get a random event name. This happens for non-event instances
        # Enumerate all cached annotated schemas (one prompt per event) to form negative candidates
        for event in all_annotated_schema:
            annotated_schema = random.choice(all_annotated_schema[event])
            prompt = task_sep + "\n\n" + annotated_schema + "\n\n" + text_sep + f"\ntext = \"{text}\"\n\n{footer}"
            instruction = header
            new_instance = copy.deepcopy(sample)
            new_instance["input"] = prompt
            new_instance["instruction"] = instruction
            new_instance["output"] = "[]"
            new_instances.append(new_instance)
    else:# 
        # print(sample)
        # Normalize the event type to match our schema keys
        event_name = clean_event_name(event_name, dataset_name).split("(")[0].strip()#normalize the event name
        instruction, prompt = prepare_input(sample, text, event_schemas, dataset_to_task_mapper[dataset_name], dataset_name, is_dev_test_data = is_dev_test_data, current_event = event_name, do_annotate_schema = do_annotate_schema, guidelines=guidelines)
        assert type(prompt) == str, "Prompt should be a string"
        new_instance = copy.deepcopy(sample)
        new_instance["input"] = prompt
        new_instance["instruction"] = header
        # In dev/test, we may prefer empty outputs; here we keep gold for train-like flows and [] for enumerations
        if not is_dev_test_data:
            new_instance["output"] = prepare_train_output(sample["event_mentions"], dataset_name)
        else:
            new_instance["output"] = "[]"
        # Sanity-check the output string is a valid Python literal representing a list of calls
        eval(new_instance["output"])# if this doesn't work: I have written something wrong, please reach out.
        new_instances.append(new_instance)
    return new_instances


def prepare_train_output(labels, dataset_name):
    """
    Turn gold labels into a canonical "Python-call-like" string the model learns to emit.

    Example output:
        [Die(mention='killed', victim=['civilians','woman'], place=['houses'], instrument=['missile'], agent=['coalition']), ...]

    Key ideas:
      * Roles are lowercased for stability.
      * Argument ordering follows the schema order for the event.
      * Missing roles are emitted as empty lists.
    """
    event_schema = load_clean_schema(dataset_name)
    if(len(labels) == 0):
        return "[]"
    output_string = "["
    for label in labels:
        event_name = label["event_type"]
        # Normalize label type to the canonical event key used by schema (e.g., "Life:Die" → "Die")
        event_name = clean_event_name(event_name, dataset_name).split("(")[0].strip()
        # Start a call with the trigger mention pinned first (always string)
        output_string += event_name + f"(mention={label['trigger']['text']!r}, "
        arg_gold = {}
        # Aggregate arguments by lowercased role; multiple spans per role are permitted
        for g_arg in label["arguments"]:
            g_arg["role"] = g_arg["role"].lower()
            arg_name = g_arg["role"]
            if(arg_name not in arg_gold):
                arg_gold[arg_name] = []
            arg_gold[arg_name].append(g_arg["text"])
        # Follow the canonical argument order from schema to make outputs deterministic
        for schema_arg in event_schema[event_name]:
            if(schema_arg in arg_gold):
                arg_string = f"{schema_arg}={arg_gold[schema_arg]}"
            else:
                arg_string = f"{schema_arg}=[]"
            output_string += arg_string + ", "
        output_string += "), "
    output_string +=  "]"
    # Tidy up trailing commas/parentheses to ensure syntactic correctness
    output_string = output_string[:-4] + ")]"
    return output_string.replace(", )", ")")

def prepare_test_dev_dataset(dataset, dataset_name, do_annotate_schema = False, is_dev_test_data = False, add_negative_sample = False, guidelines = None):
    """
    Build the dev/test split as prompts:
      * For texts with events: create prompts per present event + fill in non-present events (negative enumeration).
      * For texts with no events: enumerate all event schemas (pure negatives).

    This enforces an evaluation setting where the model must discriminate which schema applies to a given text.
    """
    all_schema = load_init_prompts(dataset_name)
    # print(all_schema.keys())
    # xxx
    event_counts = 0
    new_dataset = []
    for sample in tqdm(dataset, total = len(dataset)):
        # Track which normalized events appear in this sample
        events = set([clean_event_name(x["event_type"], dataset_name) for x in sample["event_mentions"]])
        # clean_event_name(event_name, dataset_name).split("(")[0].strip()
        # event_counts += (dataset_event_counts[dataset_name])# - len(events))
        
        if(len(sample["event_mentions"])==0):# if there are no event mentions, then simply enumerate all the events" (text, sample, event_name, dataset_name, is_dev_test_data = False):
            # print("Here....")
            # print(json.dumps(sample, indent=4))
            # Non-event: produce one instance per event type using cached annotated schemas
            non_event_instances = prepare_test_dev_input(sample["text"], sample, all_schema, None, dataset_name, is_dev_test_data = True, guidelines=guidelines, do_annotate_schema = do_annotate_schema)
            new_dataset.extend(non_event_instances)
            continue
        grouped_events, covered_events = {}, set()
        # Regroup mentions by event type to create per-event prompts for events actually present
        for event in sample["event_mentions"]:
            event_type = event["event_type"]
            covered_events.add(clean_event_name(event_type, dataset_name).split("(")[0].strip())
            if(event_type not in grouped_events):
                grouped_events[event_type] = dict([(key, val) for key, val in event.items() if key != "event_mentions"])
                grouped_events[event_type].update({"event_mentions": []})
            grouped_events[event_type]["event_mentions"].append(event)
        # Build prompts for present event types
        for event_type, event in grouped_events.items():
            new_event_instances = prepare_test_dev_input(sample["text"], event, all_schema, event_type, dataset_name, guidelines=guidelines, do_annotate_schema = do_annotate_schema)
            new_dataset.extend(new_event_instances)
        # Also produce non-event enumerations for event types not present in this text, to keep evaluation balanced
        uncovered_events = set(all_schema.keys()) - covered_events
        # print("Uncovered Events: ", uncovered_events, len(uncovered_events), "covered_events: ", covered_events, len(covered_events))
        # xxx
        for event_type in uncovered_events:
            new_non_event_instance = prepare_test_dev_input(sample["text"], sample, all_schema, event_type, dataset_name, do_annotate_schema=do_annotate_schema, guidelines=guidelines, is_dev_test_data = True)
            new_dataset.extend(new_non_event_instance)
    # print("Event Counts: ", event_counts)
    return new_dataset



def annotate_dataset(dataset, dataset_name, task_type, do_annotate_schema = False, is_dev_test_data = False, guidelines = None):
    """
    Convert grouped training data into instruction-tuning records.

    For each (text, event_type) sample:
      * Build an instruction + code prompt with (optionally) annotated schema.
      * Serialize gold labels via prepare_train_output.
      * Validate that the gold string parses as a Python literal (quick structural check).
    """
    all_schema = load_init_prompts(dataset_name)
    # print(all_schema.keys())
    new_dataset = []
    for sample in tqdm(dataset, total = len(dataset)):
        instruction, code_input_text = prepare_input(sample, sample["text"], all_schema, task_type, dataset_name, is_dev_test_data = is_dev_test_data, current_event = None, do_annotate_schema = do_annotate_schema, guidelines = guidelines)
        label = prepare_train_output(sample["event_mentions"], dataset_name)
        assert type(code_input_text) == str, "Code input text should be a string"

        sample["input"] = code_input_text
        sample["instruction"] = instruction
        sample["output"] = label
        ### verify
        hhh = eval(label) # if this doesn't work: I have written something wrong, please reach out.
        # print(f"Verified: {len(hhh)}")
        ### verify
        new_dataset.append(sample)
    return new_dataset


def prepare_dataset(input_dir, dataset_name, add_negative_sample = False, annotate_schema = False, guidelines = None, output_dir = "./processed_code_prompts/", nagative_sample_count = None):
    """
    Orchestrate the full pipeline:
      1) Load train/dev/test splits.
      2) Group train by event type; create prompts + gold labels.
      3) Build dev/test via enumeration (present & non-present events).
      4) (Optional) Add synthetic negative samples to train.
      5) Final cleanup & write JSON/JSONL to output_dir/<dataset>.
    """
    dataset = load_dataset(input_dir, dataset_name)
    train_data, dev_data, test_data = dataset["train"], dataset["dev"], dataset["test"]
    task_type = dataset_to_task_mapper[dataset_name]
    grouped_train, grouped_dev, grouped_test = [], [], []
    annotated_train, annotated_dev, annotated_test = [], [], []
    # If requested, compute a batch of negative samples (implementation is dataset-specific inside utils)
    if(add_negative_sample):
        train_negative_samples = get_negative_samples(train_data, dataset_name, guidelines, nagative_sample_count, do_annotate_schema=annotate_schema)
    # Expand train so that each sample has at most one event type (one prompt per event)
    for sample in train_data:
        grouped_train.extend(group_by_event_type(sample))
    # for sample in dev_data:                              ---
    #     grouped_dev.extend(group_by_event_type(sample))    |
    #                                                         \
    #                                                           - Not Needed but kept for debugging
    #                                                         / 
    # for sample in test_data:                               |
    #     grouped_test.extend(group_by_event_type(sample)) ---
    # Turn grouped train into instruction/input/output triplets (with optional schema annotation)
    annotated_train = annotate_dataset(grouped_train, dataset_name, dataset_to_task_mapper[dataset_name], annotate_schema, guidelines=guidelines)
    # Build dev/test using schema enumeration so each text is assessed against all schemas
    annotated_dev = prepare_test_dev_dataset(dev_data, dataset_name, do_annotate_schema=annotate_schema, guidelines=guidelines)
    annotated_test = prepare_test_dev_dataset(test_data, dataset_name, do_annotate_schema=annotate_schema, guidelines=guidelines)
    # Final pass to standardize record shape, sanitize fields, etc.
    clean_train = final_clean_dataset(annotated_train, dataset_name)
    clean_dev = final_clean_dataset(annotated_dev, dataset_name)
    clean_test = final_clean_dataset(annotated_test, dataset_name)
    # Optionally append negatives to the train split
    if(add_negative_sample):
        clean_train = clean_train + train_negative_samples
    ###
    # Persist all three splits to disk under output_dir/dataset_name
    save_dataset(output_dir, dataset_name, {"train": clean_train,
                                           "dev":   clean_dev,
                                           "test":  clean_test})

if __name__ == "__main__":
    # Parse CLI args and wire everything together
    args = parser.parse_args()
    # dir = "./../../TextEE/processed_data"
    dataset_name = args.dataset_name
    dir = args.input_dir
    annotate_schema = args.annotate_schema
    add_negative_samples = args.add_negative_samples
    guidelines_files = args.guideline_file
    output_dir = args.output_dir
    ###
    # Dynamically import the event class definitions so that output strings (like Die(...)) can be sanity-checked
    import_star(dataset_name, PY_ADD)### used to verify if the output follows the python format.
    ###
    # Load consolidated guidelines if annotation is requested; else leave None
    guidelines = None
    if(annotate_schema):
        # If user provided a token instead of a JSON path, fall back to ../guidelines/<dataset>_event_guidelines.json
        if(not guidelines_files.endswith(".json")):    
            guidelines = load_guidelines(f"./../guidelines/{dataset_name}_event_guidelines.json")
        else:
            guidelines = load_guidelines(guidelines_files)
    # Run the full dataset preparation pipeline
    prepare_dataset(dir, dataset_name, add_negative_sample = add_negative_samples, annotate_schema = annotate_schema, guidelines=guidelines, output_dir = output_dir, nagative_sample_count=args.negative_sample_count)
    # Quick insight: how many event types have at least one cached annotated schema (used for dev/test enumeration)
    print("Length of all annotated schema: ", len(all_annotated_schema))
