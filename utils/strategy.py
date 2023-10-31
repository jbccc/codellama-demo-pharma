from jsonschema.protocols import Validator
import json
import streamlit as st

schema = json.load(open("utils\strategy_schema.json"))
strategies = json.load(open("utils\strategies.json"))
v = Validator(schema, registry="utils", format_checker=schema)

for strategy in strategies:
    v.validate(strategy)

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