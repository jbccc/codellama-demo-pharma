import streamlit as st
import re
from utils.strategy import add_strats, pop_strats

system_prompts_ex = [
    "You are a Data Scientist working for a big pharma company. You are working with clinical trial data.",
    "You are a Data Scientist working for a big pharma company. You are working with clinical trial data. When asked to generate instructions, you must write in clear English. Instructions are written to be understood by a human. Any code that you write must be working and correct. When asked to write code, you must write the code in {lang}. You are not allowed to use any other programming language. You are not allowed to use any other software.",
]

response_schema_ex = [
    ["code", "Answer the instruction with working {lang} code."],
]


def extract_variables_with_replacement(text, replace_with=r":red[\1]"):
    pattern = r'\{([^}]*)\}'  # This pattern matches arnything between brackets (i.e. variables)
    matches = [match.group(1) for match in re.finditer(pattern, text)]
    replaced_text = re.sub(pattern, r'**{replacement}**'.format(replacement=replace_with), text)
    return matches, replaced_text


def error_matching_colids(matches, columns):
    if columns is None and len(matches) > 0:
        return False
    error = False
    
    for match in matches:
        if match not in columns:
            st.error(f"Variable **{match}** is not useable in this prompt. Please update the prompt to meet validation criteria.")
            error = True
    
    if len(set(matches)) < len(set(columns)):
        st.warning(f"Warning: Some useable columns are not used in the prompt. This could result in incorrect results. Columns missing: {', '.join(set(columns) - set(matches))}")
    
    return error

def prompt_selection(key_prompt, select_options):
    key_select = f"{key_prompt}_select"
    key_text = f"{key_prompt}_text"
    key_glob = f"{key_prompt}_prompt"
    
    select = st.selectbox(
        f"Choose an example", 
        options=select_options, 
        key=key_select,
        on_change=lambda: st.session_state.update(
            {key_glob:st.session_state.get(key_select)}
        ), 
    )

    text = st.text_area(
        f"Prompt", 
        value=st.session_state.get(key_glob) or select,
        key=key_text,
        on_change=lambda: st.session_state.update(
            {key_glob:st.session_state.get(key_text)}
        ),
        height=len(select)//3*2,
    )

    if st.session_state.get(key_glob) is None:
        st.session_state.update({key_glob:text})
    
def add_example_to_strategy(strat_id, prompt_id, example, info):
    if st.button("Add example", key=f"add_example{prompt_id}"):
        add_strats(strat_id, prompt_id, example, info)
        st.rerun()

def pop_example_from_strategy(strat_id, prompt_id, example, info):
    if st.button("Remove example", key=f"pop_example{prompt_id}"):
        pop_strats(strat_id, prompt_id, example, info)
        st.rerun()