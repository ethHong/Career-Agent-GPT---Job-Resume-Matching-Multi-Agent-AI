# Career-Agent-GPT---Job-Resume-Matching-Multi-Agent-AI

# How to use

* Put your job description of interest
* Put your own resume
* Put information on role, and target company

## Multi-Agent Sysmtem

* Multi Agent LLM provide more precise evaluation of your job match. 
* Initial module: 
  * Give initial evaluation based on skils (keywords), experiences, requirements.
* Validation modeules take initial data, output from initial module, and cross-validate
  * Skill (keyword) validation module
  * Experience validataion module
  * Basic requirement validation module

## Requirements

### Dependencies

~~~shell
pip install openai
pip install requests
pip install streamlit
~~~

or simply, 

~~~
pipenv install 
~~~

to install all dependencies.

### OpenAI API Key

* This repository requires **own API Key for OpenAI.**
* Include your **own api_key.txt in file directory.**