import streamlit as st
import time

from utils.page_control import check_prev_step
from utils.model_control import get_model_test_prompt_answer, sys_test_prompt

import os
from dotenv import load_dotenv
load_dotenv()

check_prev_step("Home", "config")
st.session_state.update({"model_selection_done":True})
use_llama = st.session_state.config["use_llama"]
st.caption(f"Using {'Llama' if use_llama else 'GPT'}")
st.header("Model Configuration")
if use_llama:
    default_key = os.getenv("ANYSCALE_DEFAULT_KEY")
else:
    default_key = os.getenv("OPENAI_DEFAULT_KEY")

def display_model_selection(use_llama):
    params = {}

    API_KEY = st.text_input(f"Enter {'AnyScale' if use_llama else 'OpenAI'} API key (optional)", key="API_key", placeholder=f"{'esecret_...' if use_llama else 'sk-...'}",)
    if not API_KEY: st.write("__Using default key__")
    params["api_key"] = API_KEY if API_KEY else os.getenv("ANYSCALE_DEFAULT_KEY") if use_llama else os.getenv("OPENAI_DEFAULT_KEY")

    params["api_base"] = "https://api.{}.com/v1".format("endpoints.anyscale" if use_llama else "openai")

    params["temp"] = st.slider("Choose temperature", min_value=0.0, max_value=1.0, value=0.1, step=0.01, key="temperature")

    llama_models = [
        "meta-llama/Llama-2-7b-chat-hf","meta-llama/Llama-2-13b-chat-hf",
        "meta-llama/Llama-2-70b-chat-hf", "mistralai/Mistral-7B-Instruct-v0.1"
    ]

    params["llm_name"] = st.radio(
        "Choose LLM",
        llama_models if use_llama 
        else ["gpt-3.5-turbo"],
        llama_models.index(st.session_state.get("llm_name")) if hasattr(st.session_state, "llm_name") else 2 if use_llama else 0,

    )

    params["code_llm_name"] = st.radio(
        "Choose Code LLM", 
        ["codellama/CodeLlama-34b-Instruct-hf"] if use_llama 
        else ["gpt-3.5-turbo"],
    )


    return params

params = display_model_selection(use_llama)
st.session_state.update(params)
st.divider()

prompt = st.text_area("Test prompt", value="Define the SDTM and ADaM models in the context of clinical trials.", key="prompt", max_chars=140)
st.caption(f"System Prompt: *{sys_test_prompt}*")

if st.button("Test Model", key="test_model"):
    with st.spinner("Fetching answer..."):
        tic = time.time()
        reply = get_model_test_prompt_answer(prompt, **params)
    tac = time.time()
    st.write("Time taken: {:.1f} seconds".format(tac-tic))
    st.markdown(reply["choices"][0]["message"]["content"])