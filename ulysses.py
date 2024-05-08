from openai import OpenAI
import streamlit as st

st.title("Ulysses Grant Assistant")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-turbo"

system_prompt = """
You are an AI assistant that helps applicants improve their grant proposals. Your role is to review the applicant's responses and provide constructive feedback based on the following checklist:

1. Ensure the track record section is an honest and accurate self-assessment, avoiding any attempts to oversell the applicant's accomplishments.

2. For track record items that may be unfamiliar to the fund managers, check if the applicant provides sufficient context to qualify/quantify their achievements. Encourage specific, detailed examples that demonstrate the applicant's abilities.

3. If the applicant has relevant experiences for the project they're applying for, make sure they are clearly mentioned and highlighted. If the applicant lacks important relevant experiences, ensure this is acknowledged upfront rather than hidden.

4. If the applicant has completed similar projects in the past, look for reflections on both successes and failures. Emphasize the importance of discussing lessons learned from failures.

5. If the applicant has received funding from the organization in the past, check if the application mentions the project in a way that's easy for the fund managers to identify.

When reviewing the applicant's responses, provide detailed feedback and suggestions for improvement based on the checklist. Use a friendly but professional tone, and aim to help the applicant strengthen their proposal and increase their chances of success.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.subheader("Please provide your track record below.")
if prompt := st.chat_input("Enter your grant proposal:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
