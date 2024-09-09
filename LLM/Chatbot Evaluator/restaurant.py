import json
import google.generativeai as genai
import streamlit as st
import logging
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone
from dotenv import load_dotenv
import os

# Api configuration
gemini_api_key = "AIzaSyDCuJ8CKk6yDiCy4tOB174aNZ6PjYPIu_Q"
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_env = os.getenv("PINECONE_ENV")


# Logging for debugging
logging.basicConfig(level=logging.DEBUG)  
# Model configuration
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-1.5-pro')

pc = Pinecone(api_key=pinecone_api_key, environment=pinecone_env)
def get_conversation_topic(conversation):
    prompt = """
    Given the following conversation, identify the main topic of the conversation. 
    Focus on what the user is primarily concerned about or asking for. Try to limit words and make sure your
    response contains the conversation topic. If it has multiple topics, try to include every topic in your response as a single response.
    don't generate any characters like ('-',':',';') 

    Conversation:
    {conversation}
    """
    formatted_prompt = prompt.format(conversation=json.dumps(conversation))
    logging.debug(f"Formatted Prompt: {formatted_prompt}")
    response = model.generate_content(
        contents=formatted_prompt,
        generation_config={'temperature': 0.0}
    )
    return response

def get_relevant_chunks(query, selected_domain):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",api_key=google_api_key)
    
    logging.debug(f"Query Type: {type(query)}")
    logging.debug(f"Query Content: {query}")
    
    try:
        query_vector = embeddings.embed_query(query)
    except Exception as e:
        st.error(f"Error embedding query: {e}")
        logging.error(f"Error embedding query: {e}")
        return []

    if not isinstance(query_vector, list):
        query_vector = list(query_vector)

    if not all(isinstance(i, float) for i in query_vector):
        st.error("Query vector is not in the expected format (list of floats).")
        st.write("Query Vector Elements Type:", [type(i) for i in query_vector])
        return []

    index_name = f"{selected_domain}-pdf-vector"
    if index_name not in pc.list_indexes().names():
        st.error(f"Index {index_name} does not exist.")
        return []

    index = pc.Index(index_name)
    results = index.query(vector=query_vector, top_k=5, include_metadata=True)
    
    logging.debug(f"Results Structure: {results}")

    chunks = []
    if 'matches' in results:
        for match in results['matches']:
            if 'metadata' in match and 'text' in match['metadata']:
                chunks.append(match['metadata']['text'])
            else:
                st.write("Match without metadata or text:", match)
    else:
        st.write("No matches found in results")

    return chunks

def restaurants_prompt(input_json, metrics):
    Scenario = """
    You are an evaluator agent responsible for assessing and rating customer support conversations based on restaurants domain. Your task is to evaluate the conversations and rate them on a scale from 0 to 10, providing reasons for your ratings.
    """
    Goal = """
    Your primary goal is to analyze the conversations, determine the relevant domain, and evaluate the conversations based on predefined criteria. You must identify the domain related to the conversation and ensure it matches the provided domain input. If there is a mismatch, indicate it. Evaluate the conversation using the specified metrics and guidelines.
    """
    Domains = """
    your domain is airline and flights
    try to check if the conversation domain and your domain is matching
    If the domain of the conversation in the file does not match the provided domain input flights , indicate a domain mismatch.
    """
    domain_knowledge="""
    this is your domain knowledge base, take details from here:
    {domain_knowledge}
    and consider this domain details while evaluating and giving rating score, cross check these details with the conversation.
    if there is any contradiction then specify it in the reason part for rating score , 
    don't say "provided knowledge base" use "my knowledge base" for stating reasons
    """
    Guidelines_Template = """
    For the user input metrics:
    Summary: summary of the conversation,
    Highlights: highlights of the conversation, 
    Tone: Evaluate how positive, neutral, or negative the conversation is,
    Toxicity: Identify any presence of toxic or inappropriate language and unwelcoming language.
    And the user given metrices are:
    {metrics}
    """
    
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

    if domain mismatch then show:
   {{
    "Domain-Mismatch"
    }}

    """

    instruction_prompt = """
    Your Input is: 
    {input}
    """
    metrics_guidelines = "\n".join([f"{metric}" for metric in metrics])
    metrics_format = ",\n  ".join([f'"{metric}":{{"score": <score>,"reason": "<detailed reason for {metric} score>"}}' for metric in metrics])

    guidelines = Guidelines_Template.format(metrics=metrics_guidelines)
    formatted_output = Format_Template.format(metrics_format=metrics_format, metrics=metrics_guidelines)
    query = get_conversation_topic(conversation=input_json)
    new_query=query.candidates[0].content.parts[0].text
            
    logging.debug(f"Generated Query: {query}")
    dom="Restaurants"
    rel_chunk = get_relevant_chunks(query=new_query,selected_domain=dom)
    logging.debug(f"Relevant Chunks: {rel_chunk}")

    complete_prompt = Scenario + Goal + Domains +domain_knowledge.format(domain_knowledge=rel_chunk)+ guidelines + Remember + formatted_output + instruction_prompt.format(input=json.dumps(input_json))
    return complete_prompt