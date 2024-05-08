from openai import OpenAI
import streamlit as st

st.title("Ulysses Grant Assistant")

# setting up openAI stuff
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-turbo"

if "llm_responses" not in st.session_state:
    st.session_state.llm_responses = {}


def generate_response(user_response, rubric_prompt):
    messages = [
        {"role": "system", "content": rubric_prompt},
        {"role": "user", "content": user_response}]

    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=messages,
    )

    return response.choices[0].message.content.strip()


col1, col2 = st.columns([3, 2])

honesty_prompt = ""
with open("honest.txt", "r") as file:
    honesty_prompt = file.read()

with col1:
    st.write("# Your Application")
    trackRecord = st.text_area("Track Record", height=400)

    if st.button("Generate Responses"):
        rubric_prompts = {
            "Honesty and accuracy": honesty_prompt,
            # "Respond with response to honesty and accuracy for testing",
            # "Context for unfamiliar items": "Respond with response to context for unfamiliar items for testing",
            "Relevance to the project": "Respond with response to relevance to the project for testing",
            # "Past projects": "Respond with response to past projects for testing",
            "Past funding": "Respond with response to past funding for testing",
            # "Bragging": "Respond with response to bragging for testing",
        }

        for rubric in rubric_prompts:
            st.session_state.llm_responses[rubric] = generate_response(
                trackRecord, rubric_prompts[rubric]
            )
            print(trackRecord, rubric_prompts[rubric])


def rubric_item(title, score, help="", response="LLM response goes here. 5/10"):
    # Override the score from the response, which ends with a score like ". 5/10"
    score = response.split(".")[-1].strip()

    st.metric(title, score, help=help)
    with st.expander("Ulysses says:"):
        st.write(response)


with col2:
    st.write("## Rubric")
    rubric_item(
        "Honesty and accuracy",
        "6/10",
        "Did the track record section look like an honest and accurate self-assessment, rather than trying to “sell” the grantmakers on something?",
        response=st.session_state.llm_responses.get("Honesty and accuracy", ""),
    )
    # rubric_item(
    #     "Context for unfamiliar items",
    #     "3/10",
    #     response=st.session_state.llm_responses.get("Context for unfamiliar items", ""),
    # )
    rubric_item(
        "Relevance to the project",
        "8/10",
        "If the applicant has salient experiences to the project they’re applying for, are they clearly mentioned and highlighted? If the applicant does NOT have important relevant experiences for the project they’re applying for, is it mentioned upfront rather than hidden?",
        response=st.session_state.llm_responses.get("Relevance to the project", ""),
    )
    # rubric_item(
    #     "Past projects",
    #     "4/10",
    #     response=st.session_state.llm_responses.get("Past projects", ""),
    # )
    rubric_item(
        "Past funding",
        "2/10",
        "If the applicant has gotten funding from us in the past, did the application mention the project in a way that’s easy for us to identify?",
        response=st.session_state.llm_responses.get("Past funding", ""),
    )
    # rubric_item(
    #     "Bragging",
    #     "8/10",
    #     response=st.session_state.llm_responses.get("Bragging", ""),
    # )
