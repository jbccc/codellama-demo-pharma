import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import streamlit as st
import pandas as pd
import os
from utils.strategy import get_strats_desc, get_strats

st.title("Novartis GenAI Offering")
st.header("LLMs for Code Generations")


with st.expander("Global Configuration", expanded=True) as exp:
    cols = st.columns([1,1,1.5])

    models = [
        "Meta/Llama",
        "OpenAI/GPT3",
    ]
    with cols[0]:
        st.write("#### Model Source")
        model_name = st.radio(
            "Choose source",
            models,
            (0 if st.session_state.config["use_llama"] else 1) if "config" in st.session_state else 0
        )

    languages = [
        "SAS",
        "Python",
    ]
    with cols[1]:
        st.write("#### Language")
        language = st.radio(
            "Choose language",
            languages,
            languages.index(st.session_state.config["lang"]) if "config" in st.session_state else 0
        )

    strategies = get_strats_desc()
    with cols[2]:
        st.write("#### Strategy for generating the ADSL")
        strategy = st.radio(
            "Choose strategy",
            strategies,
            st.session_state.strat_id if "strategy" in st.session_state else 0   
        )

    st.button(
        "Save configuration", 
        key="save_config", 
        on_click=lambda: st.session_state.update({
            "config": {
                "use_llama": model_name=="Meta/Llama", 
                "lang": language, 
            },
            "strategy": get_strats()[strategies.index(strategy)],
            "strat_id": strategies.index(strategy),
        })
    )

if not "strategy" in st.session_state:
    st.stop()

st.header("Chosen Strategy")
for xpl in st.session_state["strategy"]["explanations"]:
    (subtitle, md) = xpl.values()
    st.subheader(subtitle)
    st.markdown(md)
