import pandas as pd
import streamlit as st

def verify_metadata(df:pd.DataFrame, placeholder) -> bool:
    if df is None:
        placeholder.info("No metadata loaded")
        return False
    elif not df.columns.is_unique:
        placeholder.info("There are duplicate columns in the metadata file")
        return False
    elif not df[df.columns[0]].is_unique:
        placeholder.info("The first column must have unique values")
        return False
    elif df.isna().sum().sum() > 0:
        placeholder.info("There are NA values in the metadata file")
        return False
    else:
        placeholder.info("Metadata verified successfully")
        return True
    
def display_dataframe(metadata_df:pd.DataFrame):
    df_col, col_col = st.columns([8,2])
    with df_col:
        edited_df = st.data_editor(
            metadata_df, 
            key="edited_metadata_df",
            num_rows="dynamic",
        )
        st.caption("Hint: You can **modify** the dataframe above.")
    with col_col.expander("Show columns"):
        st.dataframe([*metadata_df.columns], )
    return edited_df

def get_columns(metadata_df:pd.DataFrame):
    if metadata_df is None:
        return None
    else:
        return [*metadata_df.columns]
    

