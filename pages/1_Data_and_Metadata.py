import streamlit as st
import pandas as pd
import os

from utils.dataframe_control import verify_metadata, display_dataframe

st.subheader("Metadata Configuration")

st.file_uploader(
    "Upload metadata file", type=["csv",], 
    key="metadata_file",
)
# if st.session_state.get("metadata", None) is None:
#     st.write("Loading default metadata")
#     st.session_state.update({"metadata": pd.read_csv("data\metadata_fin.csv")})

cache_load_status = st.columns(4)

if st.session_state.get("metadata_file", None) is not None:
    metadata_df = pd.read_csv(st.session_state.metadata_file)
    edited_metadata_df = display_dataframe(metadata_df)

elif st.session_state.get("metadata", None) is not None:
    cache_load_status[3].info("Metadata in cache")
    metadata_df = pd.DataFrame(st.session_state.get("metadata"))
    edited_metadata_df = display_dataframe(metadata_df)

btn_load = cache_load_status[0].button(
    "Save Metadata DataFrame", 
    disabled=st.session_state.get("edited_metadata_df", None) is None,
    use_container_width=True,
)

if btn_load:
    if verify_metadata(edited_metadata_df, cache_load_status[1]):
        cache_load_status[2].success("Metadata cached successfully")
        st.session_state.update({"metadata": edited_metadata_df})
        st.session_state.metadata_done = True
    else:
        cache_load_status[1].error("Error: metadata not loaded because it is not valid")

st.subheader("Data Preview")
st.caption("These data are, of course, fake, and comes from the [clinical_fd](https://github.com/sas2r/clinical_fd/) repository on GitHub. The dataset contains _both SDTM __and__ ADaM models_, as well as other data. ")
base_dataset_dir = ".\data\extdata"
list_of_domain = os.listdir(base_dataset_dir)
selected_ds = st.selectbox("Choose domain to preview", list_of_domain, key="domain")
if selected_ds:
    st.write(f"Previewing {selected_ds}")
    st.dataframe(pd.read_csv(os.path.join(base_dataset_dir, selected_ds)))

