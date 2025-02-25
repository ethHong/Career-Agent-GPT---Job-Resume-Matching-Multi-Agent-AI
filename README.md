# Career-Agent-GPT---Job-Resume-Matching-Multi-Agent-AI

<img width="865" alt="Image" src="https://github.com/user-attachments/assets/1c506cee-ba49-452a-993c-e603e8a2f132" />

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
* Final Decision module

## Output

### Sample outputs

* **For initial evaluation module**

~~~JSON
{
  "is_appropriate": "True",
  "Skillset": "The candidate demonstrates a strong technical skillset relevant to the position, including proficiency in SQL, Python, and programming basics like HTML and JavaScript, all of which are essential for data analysis and automation tasks in pricing strategies. Furthermore, they are familiar with MS Office, which is necessary for report preparation.",
  "Experience": "The candidate has relevant experience as a Data Analyst Intern at AWS where they automated processes using Python, improving efficiency and reducing errors. Their role as a Product Manager/Analyst at Match Group involved extensive use of data analytics, leading projects that align closely with the responsibilities of pricing reviews and market data analysis outlined in the job description.",
  "Other reqruiements": "The candidate is currently pursuing an MS in Business Analytics, directly aligning with the educational requirement. They are fluent in English and have demonstrated strong communication and collaboration skills, which are desirable for teamwork in a global environment. Their background in product management and analytics suggests a solid interest in IT business."
}
~~~

* **Skill evaluation module**

~~~JSON
{
  "From JD": [
    "MS Office (Work, PowerPoint, Excel)",
    "SQL",
    "MS Power BI",
    "Python",
    "HTML",
    "JavaScript programming skills",
    "Fluent English language",
    "Background in Marketing, Economics, Finance, Computer/Data science or Mathematics"
  ],
  "From Resume": [
    "MS Office",
    "SQL",
    "Python",
    "HTML",
    "JavaScript",
    "Fluent English language",
    "MS in Business Analytics (related to Computer/Data science)",
    "Experience in data analysis and visualization"
  ],
  "Elaboration": "The candidate possesses nearly all the essential skills listed in the job description. They are proficient in SQL, Python, HTML, and JavaScript, which directly aligns with the job's technical requirements. Additionally, their familiarity with MS Office tools such as Excel supports the need for report preparation and data analysis. While the job description specifies knowledge of MS Power BI, the candidate has experience with Tableau, which serves a similar purpose in data visualization. The candidate is currently pursuing a Master’s degree in Business Analytics, which is relevant to the required academic background. Overall, the skillsets match closely, with a minor gap in specific tools, but their overall experience and demonstrated ability in data analytics position the candidate as a strong fit for the internship."
}
~~~

* **Experience evaluation module**

~~~JSON
{
  "From JD": [
    "Daily university student at Slovak university (2nd-4th year) with a Marketing, Economic, Finance, Computer/Data science or Mathematics background",
    "Fluent English language",
    "Knowledge of MS Office (Work, PowerPoint, Excel)",
    "SQL, MS Power BI, Python, HTML, JavaScript programming skills",
    "Interest in IT business in general",
    "Communication and presentation skills",
    "Willingness to learn"
  ],
  "From Resume": [
    "Currently pursuing an MS in Business Analytics at UCLA Anderson",
    "Proficient in SQL, Python, HTML, JavaScript, and MS Office",
    "Fluent in English",
    "3+ years of experience as a Product Manager / Analyst across global enterprises",
    "Led analytical projects and utilized data analysis to improve business outcomes",
    "Experience automating processes and improving data workflows",
    "Strong communication and collaboration skills demonstrated through leadership roles"
  ],
  "Elaboration": "The candidate is pursuing an MS in Business Analytics, aligning closely with the educational requirement and demonstrating a strong foundation in data science principles. They possess the essential skills mentioned in the job description, including proficiency in SQL, Python, HTML, and JavaScript, as well as MS Office for report preparation. Their experiences as a Data Analyst Intern at AWS and as a Product Manager/Analyst at Match Group show their practical application of these skills through process automation, data analysis, and contributions to project success. Additionally, their fluency in English and proven communication skills suggest they can effectively collaborate within the global pricing team. Their interest in IT business is implied through their background and roles, indicating a willingness to learn and adapt to dynamic business environments."
}
~~~

* **Requirement evaluation module**

~~~JSON
{
  "From JD": [
    "Daily university student at Slovak university (2nd-4th year) with a Marketing, Economic, Finance, Computer/Data science or Mathematics background",
    "Fluent English language",
    "Knowledge of MS Office (Work, PowerPoint, Excel)",
    "SQL, MS Power BI, Python, HTML, JavaScript programming skills"
  ],
  "Elaboration": "While the candidate is a graduate student at UCLA Anderson pursuing an MS in Business Analytics, they do not meet the requirement of being a daily university student at a Slovak university. However, they are fluent in English and have extensive knowledge of MS Office, along with significant programming skills in SQL, Python, HTML, and JavaScript. Their skillset in data analytics and product management, along with proven experience in automation and data analysis, aligns with the core responsibilities of the data science internship, just not the location requirement."
}
~~~

* **Final Decision module: Plain Text**

~~~
Final Decision: Reject

Comment: While the candidate possesses a strong technical skillset and relevant experience, they do not meet the fundamental geographic requirement of being a daily university student at a Slovak university, which is critical for the position. Despite their impressive qualifications in data analytics and product management, adherence to all basic requirements is essential in this hiring process.
~~~

From this example, we could see that through initial agent the candidate was passed through the screening, but through muilti-agent it captured geographical limitation, and finally rejected the candidate.

### Output formatting

* Output of each modules are printed in form of JSON (if possible)

* Prompt include these line to ensure output of response to be JSON type:

  ~~~python
  """
  ...
  * Keep output strictly in the following JSON format:
  {{
      "is_appropriate": "True / False",
      "Skillset": "Explanation on matching / lacking skillset, keywords",
      "Experience": "Explanation on relevant experiences",
      "Other reqruiements": "Explanation on if the candidate meets requirements"
  }}
  """
  ~~~

* The following codes,  tries to manage output format to be JSON:

  ~~~python
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
  ~~~

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

