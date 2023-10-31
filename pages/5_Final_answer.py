from utils.page_control import check_prev_step
import streamlit as st
from streamlit_extras.stateful_button import button

from utils.pipeline_control import (
    get_prompt,
    parse_md_code
)
from utils.model_control import get_model
from utils.pipeline_control import (
    show_prompts_and_variables,
)

check_prev_step("Pipeline", "answers")

strategy = st.session_state.get("strategy")
answers = st.session_state.get("answers")
sys_p = st.session_state.get("system_prompt")
rs = st.session_state.get("response_schemas")
aggr_sc_p = st.session_state.get("aggr_code_prompt")
api_config = {
    "api_key": st.session_state["api_key"],
    "api_base": st.session_state["api_base"],
}


st.title("Final answer")
with st.expander("Explore prompts", ):
    st.write("#### Final Prompt")
    matches_fin = show_prompts_and_variables(aggr_sc_p)


with st.expander("Preview prompt"):
    if not strategy["prompts"][1]["groupby"] == "last_ans":
        raise ValueError("Only method aggregating last model answers are allowed for the moment.")
    aggregated_answers = "\n".join(answers)
    args = dict(zip(matches_fin, [aggregated_answers]))
    formatted_final_prompt = get_prompt(rs, aggr_sc_p, args)
    st.write("*formatted final prompt*")
    st.markdown(formatted_final_prompt)

if not button("Generate final answer", key="final_prompt"):
    st.stop()


with st.spinner("Fetching Answers..."):
    llm = get_model(api_conf=api_config)

    output = llm(
        system=sys_p,
        user=formatted_final_prompt,
        llm=st.session_state["llm_name"],
        temp=st.session_state["temp"]
    )["choices"][0]["message"]["content"]

st.subheader("Final answer")
code = parse_md_code(output)
st.session_state.update({"final_answer":code})

st.title("Final answer")
st.code(st.session_state.get("final_answer"), )

with st.expander("display raw output"):
    st.write(output)