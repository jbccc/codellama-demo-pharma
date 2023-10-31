import streamlit as st
from streamlit_extras.grid import grid
from utils.page_control import check_prev_step
from utils.prompt_control import (
    extract_variables_with_replacement, 
    error_matching_colids, 
    prompt_selection,
    system_prompts_ex,
    response_schema_ex,
    add_example_to_strategy,
    pop_example_from_strategy,
)
from utils.dataframe_control import get_columns
import pandas as pd

check_prev_step("Home", "config")
check_prev_step("Data and Metadata", "metadata_done")
metadata_columns = get_columns(st.session_state.get("metadata", None))
language = st.session_state.config["lang"]
strategy = st.session_state.strategy
strat_id = st.session_state.strat_id

u_prompt1 = st.session_state.get("strategy")["prompts"][0]
u_prompt2 = st.session_state.get("strategy")["prompts"][1] if len(strategy["prompts"]) > 1 else None

st.caption(f"Using ___{language}___ for ___{strategy['name']}___ strategy")

visualizing = st.toggle("Visualize prompts", key="vizu_prompts", value=False)

if visualizing:
    st.caption("Variables in prompts are highlighted in :red[red].")
else:
    st.caption(":red[You need to visualize the prompts to save them for the pipeline.]")

my_grid = grid(2, 2)

with my_grid.container():
    st.write("#### System Prompt")

    if not visualizing:
        prompt_selection("system", system_prompts_ex)
        st.markdown(f"Variables must be in: {', '.join(map(lambda col: f'*{col}*', ['lang']))}")
    else:
        matches_sys, sys_text_formatted = extract_variables_with_replacement(st.session_state.get("system_prompt", ""),)
        st.markdown(sys_text_formatted,)
        
        if error_matching_colids(matches_sys, ["lang"]):
            st.session_state.update({"prompts_done":False})
        else:
            st.session_state.update({"prompts_done":True})

with my_grid.container():
    st.write("#### Response Schema")
    sample_response_schema = pd.DataFrame(response_schema_ex, columns=["name", "description"])
    sample_response_schema["description"] = sample_response_schema["description"].apply(lambda x: x.format(lang=language))
    data_edited = sample_response_schema
    rs_keys = data_edited["name"].tolist()
    if not visualizing:
        data_edited = st.data_editor(data_edited, num_rows="dynamic",)
        st.session_state.update({"response_schemas": data_edited})
        rs_keys = data_edited["name"].tolist()
    else:
        st.dataframe(data_edited,)

with my_grid.container():
    st.write(f"#### User Prompt - {u_prompt1['title']}")
    prompt1_ex = u_prompt1["examples"]
    if u_prompt1["keys"] == "response_schema":
        cols_to_choose = rs_keys
    elif u_prompt1["keys"] == "metadata_columns":
        cols_to_choose = metadata_columns
    else:
        cols_to_choose = []
    
    if not visualizing:
        prompt_selection("code_snip", prompt1_ex)
        st.markdown(f"Variables must be in: {', '.join(map(lambda col: f'*{col}*', cols_to_choose))}")
        cols = st.columns(2)
        info = st.empty()
        with cols[0]:
            add_example_to_strategy(strat_id, 0, st.session_state.get("code_snip"), info)
        with cols[1]:
            pop_example_from_strategy(strat_id, 0, st.session_state.get("code_snip"), info)
    else:
        matches_code1, code1_text_formatted = extract_variables_with_replacement(st.session_state.get("code_snip_prompt", ""))
        st.markdown(code1_text_formatted,)
        if error_matching_colids(matches_code1, cols_to_choose):
            st.session_state.update({"prompts_done":False})
        else:
            st.session_state.update({"prompts_done":True})

with my_grid.container():
    if u_prompt2 is None:
        st.write("#### User Prompt - No second prompt")
        st.stop()
    
    st.write(f"#### User Prompt - {u_prompt2['title']}")
    prompt2_ex = u_prompt2["examples"]

    if u_prompt2["keys"] == "response_schema":
        cols_to_choose = rs_keys
    elif u_prompt2["keys"] == "metadata_columns":	
        cols_to_choose = metadata_columns
    elif u_prompt2["keys"] == "last_prompt":
        cols_to_choose = ["last_prompt"]

    if not visualizing:
        prompt_selection("aggr_code", prompt2_ex)
        st.markdown(f"Variables must be in: {', '.join(map(lambda col: f'*{col}*', cols_to_choose))}")
        cols = st.columns(2)
        info = st.empty()
        with cols[0]:
            add_example_to_strategy(strat_id, 1, st.session_state.get("aggr_code_prompt"), info)
        with cols[1]:
            pop_example_from_strategy(strat_id, 1, st.session_state.get("aggr_code_prompt"), info)
    else:
        matches_code2, code2_text_formatted = extract_variables_with_replacement(st.session_state.get("aggr_code_prompt", ""))
        st.markdown(code2_text_formatted,)
        if error_matching_colids(matches_code2, cols_to_choose):
            st.session_state.update({"prompts_done":False})
        else:
            st.session_state.update({"prompts_done":True})

