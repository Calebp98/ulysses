import streamlit as st

col1, col2 = st.columns([3, 2])
with col1:
  st.write("# Your Application")
  st.text_area("Track Record", height=400)

def rubric_item(title, score, help_text, response="LLM response goes here"):
  st.metric(title, score, help=help_text)
  with st.expander("Ulysses says:"):
    st.write(response)

with col2:
  st.write("## Rubric")
  rubric_item("Honesty and accuracy", "6/10", "Did the track record section look like an honest and accurate self-assessment, rather than trying to “sell” the grantmakers on something?")
  rubric_item("Context for unfamiliar items", "3/10", "For track record items that are unlikely to be familiar to the fund managers, are there context given to help qualify or quantify it? (For example, “I scored 138 points on the Examplestan Graduation Exams, which is evidence of my academic ability” is bad, “As a homeschooler, I scored 138 points on the Examplestan college entrance exams, the second highest score for the entire country in 2018. This is evidence of my ability to independently study difficult subjects.” is good).")
  rubric_item("Relevance to the project", "8/10", "If the applicant has salient experiences to the project they’re applying for, are they clearly mentioned and highlighted? If the applicant does NOT have important relevant experiences for the project they’re applying for, is it mentioned upfront rather than hidden?")
  rubric_item("Past projects", "4/10", "If the applicant has done similar projects in the past, are there reflections on the successes and (especially) failures?")
  rubric_item("Past funding", "2/10", "If the applicant has gotten funding from us in the past, did the application mention the project in a way that’s easy for us to identify?")
  rubric_item("Bragging", "8/10", "Did the applicants highlight their biggest accomplishments somewhere, especially ones relevant to the project?")
