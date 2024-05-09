import asyncio
import aiohttp
from openai import OpenAI
import streamlit as st

st.title("Ulysses Grant Assistant")

# setting up openAI stuff
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-turbo"
if "llm_responses" not in st.session_state:
    st.session_state.llm_responses = {}


async def generate_response(user_response, rubric_prompt):
    async with aiohttp.ClientSession() as session:
        messages = [
            {"role": "system", "content": rubric_prompt},
            {"role": "user", "content": user_response},
        ]
        async with session.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {st.secrets['OPENAI_API_KEY']}"},
            json={
                "model": st.session_state["openai_model"],
                "messages": messages,
            },
        ) as response:
            result = await response.json()
            return result["choices"][0]["message"]["content"].strip()


async def generate_responses(track_record, rubric_prompts):
    with st.spinner("Generating feedback, give me a few seconds..."):
        tasks = []
        for rubric in rubric_prompts:
            task = asyncio.create_task(
                generate_response(track_record, rubric_prompts[rubric])
            )
            tasks.append(task)

        responses = await asyncio.gather(*tasks)

        for rubric, response in zip(rubric_prompts, responses):
            st.session_state.llm_responses[rubric] = response

        # Add a small delay to keep the spinner visible for a minimum duration
        await asyncio.sleep(1)


col1, col2 = st.columns([3, 2])

honesty_prompt = ""
with open("prompts/honest.txt", "r") as file:
    honesty_prompt = file.read()

bragging_prompt = ""
with open("prompts/bragging.txt", "r") as file:
    bragging_prompt = file.read()

with col1:
    st.write("# Your Application")
    trackRecord = st.text_area("Track Record", height=400)
    if st.button("Generate Responses"):
        rubric_prompts = {
            "Honesty and accuracy": honesty_prompt,
            "Bragging": bragging_prompt,
        }
        asyncio.run(generate_responses(trackRecord, rubric_prompts))
        print(trackRecord, rubric_prompts)


def rubric_item(title, score, response="LLM response goes here. 5/10"):
    # Override the score from the response, which ends with a score like ". 5/10"
    score = response.split(".")[-1].strip()
    st.metric(title, score)
    with st.expander("Ulysses says:"):
        st.write(response)


with col2:
    st.write("## Rubric")
    rubric_item(
        "Honesty and accuracy",
        "6/10",
        response=st.session_state.llm_responses.get("Honesty and accuracy", ""),
    )
    rubric_item(
        "Bragging",
        "8/10",
        response=st.session_state.llm_responses.get("Bragging", ""),
    )
