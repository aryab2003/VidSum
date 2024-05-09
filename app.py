import streamlit as st
from dotenv import load_dotenv

load_dotenv()
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import fitz

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = "A transcipt of an youtube video and provide its summary and key points.The transcipt is:"


# summarization of transcript based on prompt
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text


# geeting the transcript of the video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([x["text"] for x in transcript_text])
        return transcript

    except Exception as e:
        raise e


# Summarization of a paragraph
def summarize_paragraph(text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + text)
    return response.text


def summarize_pdf(pdf_bytes, prompt):
    try:
        text = ""
        with fitz.open("pdf", pdf_bytes) as pdf_document:
            for page in pdf_document:
                text += page.get_text()
        summary = summarize_paragraph(text, prompt)
        return summary
    except Exception as e:
        raise e


# Streamlit app
st.title("YouTube Video, Paragraph, and PDF Summarizer App")
st.write("This app generates a summary of the video transcript, a paragraph, or a PDF.")

option = st.radio(
    "Choose an option:",
    ("Summarize YouTube Video Transcript", "Summarize Paragraph", "Summarize PDF"),
)

if option == "Summarize YouTube Video Transcript":
    youtube_link = st.text_input("Enter the YouTube video URL")
    if youtube_link:
        video_id = youtube_link.split("=")[1]
        st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg")
    if st.button("Generate Summary"):
        transcript_text = extract_transcript_details(youtube_link)
        if transcript_text:
            summary = generate_gemini_content(transcript_text, prompt)
            st.write(summary)

elif option == "Summarize Paragraph":
    paragraph = st.text_area("Enter the paragraph to summarize", "")
    if st.button("Generate Summary"):
        if paragraph:
            summary = summarize_paragraph(paragraph, prompt)
            st.write(summary)

elif option == "Summarize PDF":
    pdf_file = st.file_uploader("Upload a PDF file", type="pdf")
    if pdf_file is not None:
        if st.button("Generate Summary"):
            pdf_bytes = pdf_file.read()
            summary = summarize_pdf(pdf_bytes, prompt)
            st.write(summary)
