# Code Llama Demo

## Installation and Usage
### Python and environement
Make sure to have python installed (I used python@3.11) and install the project dependencies with `pip install -r requirements.txt` once you have properly setup an environement (`conda create -n code-llama-demo-env python=3.11` and `conda activate code-llama-demo-env` if using anconda and miniconda, `python -m venv code-llama-demo-env` and `source code-llama-demo-env/bin/activate` if using python venv).

### Running the streamlit app

Once the environement is setup, you can run the project with `steamlit run .\Home.py` and access the web app at `http://localhost:8501/`.

At any time you can stop the server with `Ctrl+C` (MacOS and Windows).

WARNING /!\ Always execute the start command at the root of the project folder (i.e. not with `steamlit run .\path\to\Home.py`).

If needed, more information can be found at https://docs.streamlit.io/library/get-started or by running `streamlit docs`.

### Structure of the repo and the app

The repository is structured as follows:
- `Home.py` is the main file of the app, it is the app entry file, and defines the homepage where the user choose some configuration and can learn more about some strategies.
- `pages/` the files here are read by streamlit in alphabetic order and defines the different pages of the app. More information on how it works can be found [here](https://docs.streamlit.io/library/get-started/multipage-apps).
  - `0_Pipeline.py` displays the pipeline of the LLMs requests and is where the user is intended to query the LLMs.
  - `1_Data_and_Metadata.py` makes the user select the metadata and data to be used in the pipeline.
  - `2_Prompts.py` makes the user select/write/modify the prompts to be used for the selected strategy.
  - `3_Model.py` is where the user chooses between different APIs to be used to run the LLM queries. He/she can also tweak the parameters related to the inference.
- `utils/` this folder contains multiple script helpers that will be imported in the application pages
  - Each `example_control.py` contains control methods related to _example_.
  - `strategies.py`, `strategy_schema.json` and `strategies.json` are were the strategies are defined.

## Create and test a new strategy

To automatically create a new strategy, you need to follow these simple steps:
- Go in the `utils\srategies.json`
- Copy paste a current strategy to get a structured template
- Replace the name, display_name (name displayed when choosing the strategy), prompts (list the description for the prompts), and explanations (which are the explanations displayed on the Home page of the app that explains the strategy).
- And that's it!

_Explanations_ are just subtitle/markdown pairs and are rendered as such in the streamlit app.

The _prompts_ key consists of one to two prompts with a *title*, a _keys_ property to choose the origin of the key (between metadata_columns and response_schema) and an _examples_ list to be choosen among when selecting the prompt. 