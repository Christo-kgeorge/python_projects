import json
import google.generativeai as genai
import streamlit as st
import logging
from banks import banks_prompt
from flights import flights_prompt
from restaurant import restaurants_prompt
import plotly.graph_objects as go
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone

# Api configuration
gemini_api_key = ""
pinecone_api_key = ""
pinecone_env=""
google_api_key=""
google_api_key_str = str(google_api_key)



# Logging for debugging
logging.basicConfig(level=logging.DEBUG)  
# Model configuration
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-1.5-pro')



Scenario = """
You are an evaluator agent responsible for assessing and rating customer support conversations across various domains.
Your task is to evaluate the conversations and rate them on a scale from 0 to 10, providing reasons for your ratings.
"""

Goal = """
Your primary goal is to analyze the conversations, determine the relevant domain, and evaluate the conversations based on
predefined criteria. Evaluate the conversation using the specified metrics and guidelines.
"""
domain_knowledge="""
this is your domain knowledge base, take details from here:
{domain_knowledge}
and consider this domain details while evaluating and giving rating score, cross check these details with the conversation.
if there is any contradiction then specify it in the reason part for rating score.
"""
Guidelines_Template = """
For the user input metrics the default metrics are:
Summary: summary of the conversation,
Highlights: highlights of the conversation,
Tone: Evaluate how positive, neutral, or negative the conversation is,
Toxicity: Identify any presence of toxic or inappropriate language and unwelcoming language.
And the user given metrics are:
{metrics}
"""

additional = """{additional_info}"""

Remember = """
When rating the metrics:
For positive metrics (e.g., tone, clarity), evaluate based on how good the conversation is. The rating scale is from 0 to 10, where 0 is the lowest and 10 is the highest.
For negative metrics (e.g., toxicity,racism), evaluate based on how negative the conversation is. The rating scale is from 10 to 0, where 10 is the lowest and 0 is the highest.
Use float values up to 2 decimal places if needed.

To calculate the overall score:

Sum up all the scores from the metrics.
Divide the total score by the number of metrics to get the average score.
Use this average score as the overall score.
"""

Format_Template = """
The format for the response output should look like this:

{{
  "Overall_score": <overall score of the conversation evaluation based on default metrics and user given metrics>,
  "Summary": "<summary of the conversation>",
  "Highlights": "<highlights of the conversation>",
  "Tone": {{
    "score": <score>,
    "tone_reason": "<detailed reason for Tone score>"
  }},
  "Toxicity": {{
    "score": <score>,
    "toxic_reason": "<detailed reason for Toxicity score>"
  }},
  "evaluation": {{
    {metrics_format}
  }}
}}
"""

instruction_prompt = """
Your Input is:
{input}
"""



# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

col1, col2 = st.columns([6,2])

with col1:
    st.title("LoopHumane")

with col2:
    domain_options = ["General","flight", "Banks", "Restaurants"]
    selected_domain = st.selectbox("Select the domain", domain_options, index=0)

json_file = st.file_uploader("Upload a JSON file for evaluation", type=["json"],label_visibility="hidden")
if selected_domain and json_file:
    input_metrics_string = st.text_input("Enter the metrics you want to be evaluate (comma-separated)", placeholder="e.g.,relevance, clarity")
    additional_info_input = st.text_area("Enter any additional information (*optional)", placeholder="Add any additional context or details")

if st.button("Submit"):
    if json_file and input_metrics_string:
        try:
            # Read and parse the uploaded JSON file
            input_json = json.load(json_file)
            metrics = [metric.strip() for metric in input_metrics_string.split(",") if metric.strip()]
            additional_info = additional_info_input.strip() if additional_info_input else None

            logging.debug(f"Parsed metrics: {metrics}")

            metrics_guidelines = "\n".join([f"{metric}" for metric in metrics])
            metrics_format = ",\n  ".join([f'"{metric}":{{"score": <score>,"reason": "<detailed reason for {metric} score>"}}' for metric in metrics])

            guidelines = Guidelines_Template.format(metrics=metrics_guidelines)
            formatted_output = Format_Template.format(metrics_format=metrics_format, metrics=metrics_guidelines)


            # Select the appropriate prompt based on the selected domain
            if selected_domain == "Banks":
                complete_prompt = banks_prompt(input_json, metrics)+ additional.format(additional_info=additional_info)
            elif selected_domain == "flight":
                complete_prompt = flights_prompt(input_json, metrics)+ additional.format(additional_info=additional_info)
            elif selected_domain == "Restaurants":
                complete_prompt = restaurants_prompt(input_json, metrics)+ additional.format(additional_info=additional_info)
            elif selected_domain == "General":
                complete_prompt = Scenario + Goal + guidelines+ additional.format(additional_info=additional_info)+Remember + formatted_output + instruction_prompt.format(input=json.dumps(input_json))
            logging.debug(f"Complete prompt: {complete_prompt}")

            # Generating response
            response = model.generate_content(
                contents=complete_prompt,
                generation_config={'temperature': 0.0}
            )
            logging.debug(f"Response from model: {response}")

            # Parsing the response
            if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                text_content = response.candidates[0].content.parts[0].text
                logging.debug(f"Raw response text: {text_content}")

                if text_content.startswith('```json') and text_content.endswith('```'):
                    text_content = text_content[7:-3].strip()
                elif text_content.startswith('```') and text_content.endswith('```'):
                    text_content = text_content[3:-3].strip()

                if "Domain-Mismatch" in text_content:
                    parsed_json = {"Domain-Mismatch"}
                    overall_score = None
                    summary=None
                    Highlights=None
                    Tone=False
                    Toxicity=False
                else:
                    parsed_json = json.loads(text_content)
                    overall_score = parsed_json["Overall_score"]
                    summary=parsed_json["Summary"]
                    Highlights=parsed_json["Highlights"]
                    tone_score = parsed_json["Tone"]["score"]
                    tone_reason = parsed_json["Tone"]["tone_reason"]
                    toxic_score = parsed_json["Toxicity"]["score"]
                    toxic_reason = parsed_json["Toxicity"]["toxic_reason"]
                    

                logging.debug(f"Parsed JSON: {parsed_json}")
            else:
                parsed_json = {"error": "error in parsing"}
                st.subheader("Warning")
                st.warning("Your action is blocked due to safety concerns")
                logging.error("Error in parsing the model response")
                overall_score = 0
                summary=None
                Highlights=None
                Tone=None
                Toxicity=None
               
 
            if summary and Highlights!=None:
                st.subheader("Evaluation Result") 
                st.write("-- 0-4 - bad")
                st.write("-- 4-7 - okay")
                st.write("-- 7-10 - good")
                with st.container():
                    col3,col4=st.columns(2)
                    with col3:
                        st.subheader("Overall score")
                        labels = ['Score', 'Remaining']
                        values = [overall_score, 10 - overall_score]
                        colors = ['#45c49a', '#f2f5f4']

                    # Create the pie chart
                        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.8, marker=dict(colors=colors), textinfo='none')])

                    # Set chart title
                        fig.update_layout(
                            annotations=[dict(text=f'{overall_score}/10', x=0.5, y=0.5, font_size=20, showarrow=False)],
                            showlegend=True,
                            width=350,
                            height=350,
                         )

                    # Display the pie chart in Streamlit
                        st.plotly_chart(fig)
                    with col4:
                        st.subheader("Summary")
                        st.markdown(summary)
                        st.subheader("Highlights")
                        st.markdown(Highlights)

                # Container for summary and highlights
                with st.container():
                    col6,col7= st.columns(2)
                    with col6:
                        st.subheader("Tone - "+str(tone_score))
                        st.markdown(tone_reason)
                    with col7:
                        st.subheader("Toxicity - "+str(toxic_score))
                        st.markdown(toxic_reason)



                st.subheader("Metrics Evaluation")
                for metric in metrics:
                    st.markdown(f"### {metric.capitalize()}")
                    st.markdown(f"**Score:** {parsed_json['evaluation'][metric]['score']}")
                    st.markdown(f"**Reason:** {parsed_json['evaluation'][metric]['reason']}")
                    st.markdown("---")
        



                st.subheader("Visualization")
                
                metric_scores = [parsed_json["evaluation"][metric]["score"] for metric in metrics] 
                y_val=metric_scores+[tone_score,toxic_score]
                x_val=metrics+["tone","toxicity"]
                bar_fig = go.Figure(data=[go.Bar(x=x_val, y=y_val, marker=dict(color='#45c49a'),width=0.2)])

                # Set chart title and labels
                bar_fig.update_layout(
                    title_text='Metric Scores',
                    xaxis_title='Metrics',
                    yaxis_title='Scores',
                    yaxis=dict(range=[0, 10],tickmode='linear', dtick=1)
                )

                # Display the bar chart in Streamlit
                st.plotly_chart(bar_fig)

            elif Tone and Toxicity is False:
                st.subheader("Warning")
                print(response.candidates[0])
                st.warning("Domain Mismatch: Please ensure you are using the correct domain for evaluation. If you are unsure of the domain, consider using the general domain for a generic evaluation.")

                
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON string entered: {e}")
            st.error("Invalid JSON string. Please enter a valid JSON.")
    else:
        st.warning("Please upload a JSON file for evaluation and enter the metrics.")