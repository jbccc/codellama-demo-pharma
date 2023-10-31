import json
import streamlit as st

strategies = [
    {
        "name": "per_col_gen",
        "display_name": "One snippet per column generation",
        "prompts": [
            {
                "title": "One column prompt",
                "keys": "metadata_columns",
                "is_prompt": True,
                "examples": [
                    "Please write the code that will extract the desired column {var_name} from the SDTM model. It must be derived or imputed from the domain {domain} thanks to the instruction: {source_derivation}."
                ]
            },
            {
                "title": "Aggregating prompt",
                "keys": "response_schema",
                "examples": [
                    "You are provided with code snippetras extracting columns from a dataset named SDTM. Your goal is to aggrregate those code snippets into one big working SAS code. The code provided might be incorrect and you must correct it to produce working SAS code. You must save the dataset to a new one named ADaM.\n\n{code}"
                ],
                "groupby": "last_ans"
            }
        ],
        "explanations": [
            {
                "subtitle": "First part: Per column generation",
                "markdown": "We will first make a query to the LLM for each column in the ADSL."
            },
            {
                "subtitle": "Second part: Code Aggregation",
                "markdown": "We then aggregate all the single code snippets in the query so that the LLM can generate a single code snippet."
            }
        ]
    }
]

def get_strats():
    return strategies

def get_strats_desc():
    return [strategy["display_name"] for strategy in strategies]

def add_strats(strat_id, prompt_id, new_example, info:st):
    if new_example in strategies[strat_id]["prompts"][prompt_id]["examples"]:
        info.text("This example already exists.")
    else:
        if new_example == "" or new_example == None:
            pass
        else:
            strategies[strat_id]["prompts"][prompt_id]["examples"].insert(0, new_example)
            json.dump(strategies, open("utils\strategies.json", "w"))
            st.session_state.strategy = strategies[strat_id]

def pop_strats(strat_id, prompt_id, example, info:st):
    if len(strategies[strat_id]["prompts"][prompt_id]["examples"]) > 1:
        if strategies[strat_id]["prompts"][prompt_id]["examples"].count(example) >= 1:
            strategies[strat_id]["prompts"][prompt_id]["examples"].remove(example)
            json.dump(strategies, open("utils\strategies.json", "w"))
            st.session_state.strategy = strategies[strat_id]
    else:
        info.text("Cannot remove the last example.")