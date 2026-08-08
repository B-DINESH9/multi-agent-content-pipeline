import os
import sys

# Force UTF-8 encoding for standard output to fix Windows charmap issues with emojis/Kanji
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

import streamlit as st
from decouple import config
import tempfile
from fpdf import FPDF
from textwrap import dedent
import re

# Import our Crew setup
from main import ContentCreationCrew

import textwrap

def markdown_to_pdf(markdown_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # 1. Strip markdown image syntax: ![alt](url) → [Image]
    text = re.sub(r'!\[.*?\]\(.*?\)', '[Image]', markdown_text)
    # 2. Convert markdown links: [text](url) → text
    text = re.sub(r'\[([^\]]*)\]\([^\)]*\)', r'\1', text)
    # 3. Remove any remaining raw URLs
    text = re.sub(r'https?://\S+', '[link]', text)
    # 4. Strip bold/italic markers
    text = re.sub(r'\*{1,3}([^*]+)\*{1,3}', r'\1', text)
    
    for line in text.split('\n'):
        if line.startswith('#'):
            pdf.set_font("Helvetica", 'B', 13)
            line = line.lstrip('#').strip()
        else:
            pdf.set_font("Helvetica", size=10)
        
        # Encode for latin-1 compatibility
        line_clean = line.encode('latin-1', 'replace').decode('latin-1')
        
        if not line_clean.strip():
            pdf.ln(6)
            continue
        
        # new_x="LMARGIN" resets cursor to left margin after each cell (critical fix!)
        # new_y="NEXT" moves cursor to the next line
        pdf.multi_cell(w=0, h=6, text=line_clean, new_x="LMARGIN", new_y="NEXT")
    
    return bytes(pdf.output())

def main():
    st.set_page_config(page_title="Multi-Agent Content Creator", page_icon="🤖", layout="wide")

    st.title("🤖 Multi-Agent Content Creator")
    st.markdown("A CrewAI pipeline where a Researcher, Planner, Writer, and Reviewer work together to generate content.")

    # Sidebar for Agent Configuration
    st.sidebar.header("Agent Configurations")
    
    with st.sidebar.expander("Researcher Agent"):
        r_role = st.text_input("Researcher Role", "Senior Content Researcher")
        r_backstory = st.text_area("Researcher Backstory", "You are a world-class researcher, able to find precise, accurate, and up-to-date information on any given topic. You have a keen eye for facts and data.")

    with st.sidebar.expander("Planner Agent"):
        p_role = st.text_input("Planner Role", "Content Strategist & Planner")
        p_backstory = st.text_area("Planner Backstory", "You are a highly analytical Content Strategist. You excel at taking raw research and structuring it into a logical, compelling narrative outline.")

    with st.sidebar.expander("Writer Agent"):
        w_role = st.text_input("Writer Role", "Senior Writer")
        w_backstory = st.text_area("Writer Backstory", "You are a masterful writer, capable of creating engaging, insightful, and well-crafted content. You take an outline and facts and weave them into a polished draft. You use the ImageSearchTool to find REAL images and embed them directly into the report using Markdown syntax (e.g., ![alt text](url)). Never use fake placeholders.")

    with st.sidebar.expander("Reviewer Agent"):
        rev_role = st.text_input("Reviewer Role", "Expert Editor and Reviewer")
        rev_backstory = st.text_area("Reviewer Backstory", "You are a meticulous editor with an eye for detail. You ensure that the content flows well, is grammatically correct, maintains the right tone, and accurately reflects the research.")

    agent_configs = {
        "researcher": {"role": r_role, "backstory": r_backstory},
        "planner": {"role": p_role, "backstory": p_backstory},
        "writer": {"role": w_role, "backstory": w_backstory},
        "reviewer": {"role": rev_role, "backstory": rev_backstory}
    }

    # Check for API key
    try:
        api_key = config("GROQ_API_KEY")
        if not api_key:
            st.error("Groq API Key not found in .env file.")
            st.stop()
        os.environ["GROQ_API_KEY"] = api_key
    except Exception as e:
        st.error(f"Error loading API Key: {e}")
        st.stop()
        
    topic = st.text_input("Enter a topic for the agents to research and write about:", 
                          value="Artificial Intelligence in Healthcare")

    if st.button("Generate Content"):
        if not topic.strip():
            st.warning("Please enter a topic.")
        else:
            st.info(f"Agents are starting to work on: **{topic}**. This may take a few minutes...")
            
            with st.spinner('The Crew is researching, planning, writing, and reviewing...'):
                try:
                    crew_runner = ContentCreationCrew(topic, agent_configs=agent_configs)
                    final_result_obj = crew_runner.run()
                    
                    # Convert CrewOutput object to string
                    final_result = str(final_result_obj)
                    
                    st.success("Content successfully generated!")
                    st.markdown("### Final Content")
                    st.markdown(final_result)
                    
                    # Download Buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="Download as Markdown (.md)",
                            data=final_result,
                            file_name="report.md",
                            mime="text/markdown"
                        )
                    with col2:
                        pdf_bytes = markdown_to_pdf(final_result)
                        st.download_button(
                            label="Download as PDF (.pdf)",
                            data=pdf_bytes,
                            file_name="report.pdf",
                            mime="application/pdf"
                        )
                    
                except Exception as e:
                    st.error(f"An error occurred during execution: {e}")

if __name__ == "__main__":
    main()
