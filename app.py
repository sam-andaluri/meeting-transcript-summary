import streamlit as st
from collections import Counter
import string
import requests
import os


def get_iam_token():
    # Get an IAM token from IBM Cloud
    apikey = os.environ["IBM_CLOUD_API_KEY"]
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = "apikey=" + apikey + "&grant_type=urn:ibm:params:oauth:grant-type:apikey"
    response = requests.post(url, headers=headers, data=data)
    iam_token = response.json()["access_token"]
    return iam_token


def summarize_transcript(transcript):

    url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"

    body = {
        "input": """Write a summary with action items for the meeting transcripts.

    Transcript: 
    """
        + transcript
        + """
    Summary:""",
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 500,
            "min_new_tokens": 100,
            "repetition_penalty": 1,
        },
        "model_id": "ibm/granite-13b-chat-v2",
        "project_id": "21720b09-c7c4-41f8-9cab-f0d45110cf9d",
    }

    token = get_iam_token()

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()["results"][0]["generated_text"]
    return data


st.title("Meeting Transcript Summarizer")
st.header("Algorithm Avengers Team Project for IBMer watsonx challenge 2024")
st.write(
    "Enter the full transcript of a meeting, and get a summary of the key points discussed."
)

transcript = st.text_area("Meeting Transcript", height=300)

if st.button("Summarize"):
    if transcript:
        summary = summarize_transcript(transcript)
        st.subheader("Summary")
        st.write(summary)
    else:
        st.write("Please enter a transcript to summarize.")
