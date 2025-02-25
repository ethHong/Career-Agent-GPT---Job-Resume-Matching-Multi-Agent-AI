import streamlit as st
from gen_ai_agents import gen_AI_call, fit_prompt_to_api_calls
import json
import re


# Function to extract JSON from response
def extract_json(response):
    match = re.search(r"\{.*\}", response, re.DOTALL)
    if match:
        return match.group(0)
    else:
        return "{}"


# Safe JSON loader
def safe_json_load(response):
    try:
        extracted_json = extract_json(response)
        return json.loads(extracted_json)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return {}


# App Title with Emojis
st.title("🤖 Candidate Screening Agent")

# Input Section with Columns
st.subheader("📋 Choose a Position You Are Hiring For")
col1, col2 = st.columns(2)
role = col1.text_input("🔍 Job Role", "Data Scientist Intern")
company = col2.text_input("🏢 Company Name", "Dell")

# Job Description and Resume Input
jd = st.text_area("📄 Paste Job Description")
resume = st.text_area("📝 Paste Candidate Resume")

# Text prompt for AI agent
text_prompt_agent_1 = f"""
You are a hiring agent to recruit {role} for {company}.
Your job is to screen the candidate for the job. 

Job Description: {jd}
Candidate Resume: {resume}

* Keep output strictly in the following JSON format:
{{
    "is_appropriate": "True / False",
    "Skillset": "Explanation on matching / lacking skillset, keywords",
    "Experience": "Explanation on relevant experiences",
    "Other reqruiements": "Explanation on if the candidate meets requirements"
}}
"""

# Button to Start Evaluation
start_rec = st.button("🚀 Start Evaluation")

if start_rec:
    with st.spinner("🔍 Initial Evaluation in Progress..."):
        try:
            call = fit_prompt_to_api_calls(text_prompt_agent_1)
            response = gen_AI_call(call)
            response_json = safe_json_load(response)
        except:
            call = fit_prompt_to_api_calls(
                text_prompt_agent_1 + "\n Make sure to strictly output JSON format"
            )
            response = gen_AI_call(call)
            response_json = safe_json_load(response)

    st.success("✅ Initial Evaluation Complete!")
    st.json(response_json)

    # Skillset, Experience, and Requirements Validation Agents
    validation_prompts = {
        "Skillset Match": f"""
            You are a hiring validation module specialized in Skillset (keyword) match.
            Initial result: {response}
            Candidate Resume: {resume}
            Job Description: {jd}
            Output format:
            {{
                "From JD": [List of skillsets from JD],
                "From Resume": [List of skillsets from Resume],
                "Elaboration": [Explanation on matching and lacking skillsets]
            }}
        """,
        "Experience Match": f"""
            You are a hiring validation module specialized in Experience match.
            Initial result: {response}
            Candidate Resume: {resume}
            Job Description: {jd}
            Output format:
            {{
                "From JD": [List of experience requirements from JD],
                "From Resume": [List of experience details from Resume],
                "Elaboration": [Explanation on relevant experiences]
            }}
        """,
        "Requirements Match": f"""
            You are a hiring validation module specialized in Requirements match.
            Initial result: {response}
            Candidate Resume: {resume}
            Job Description: {jd}
            Output format:
            {{
                "From JD": [List of basic requirements from JD],
                "Elaboration": [Explanation on matching basic requirements]
            }}
        """,
    }

    st.info("🔍 Running Detailed Validation Checks...")
    validation_results = {}
    progress = st.progress(0)

    for i, (key, prompt) in enumerate(validation_prompts.items(), start=1):
        with st.spinner(f"⚙️ {key} in Progress..."):
            call = fit_prompt_to_api_calls(prompt)
            response = gen_AI_call(call)
            validation_results[key] = safe_json_load(response)
            st.success(f"✅ {key} Completed!")
            st.json(validation_results[key])
            progress.progress(i / len(validation_prompts))

    # Final Decision Making
    st.info("🏁 Compiling Final Decision...")
    final_prompt = f"""
        You are a final decision-maker in the hiring process for {role} at {company}.
        Based on the previous evaluations, provide a final decision with a brief comment.
        
        Initial Evaluation: {response_json}
        Skillset Evaluation: {validation_results['Skillset Match']}
        Experience Evaluation: {validation_results['Experience Match']}
        Requirements Evaluation: {validation_results['Requirements Match']}
        
        Also, Basic Reqruiements should be the initial top priority - if there are any basic requirements missing (geographic location, years, degree, etc.)
    """

    final_call = fit_prompt_to_api_calls(final_prompt)
    final_response = gen_AI_call(final_call)

    st.success("🎯 Final Evaluation Complete!")
    st.markdown(f"### 📢 Final Decision\n{final_response}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Ethan")
