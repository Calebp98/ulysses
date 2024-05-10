import os
import asyncio
import aiohttp
from openai import OpenAI
import streamlit as st

st.set_page_config(layout="wide", page_title="Ulysses: Grant Assistant", page_icon="🧐")
st.title("Ulysses: Grant Assistant")

# setting up OpenAI stuff
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


async def generate_responses(user_input, rubric_prompts, section):
    with st.spinner(f"Generating {section} feedback, give me a few seconds..."):
        tasks = []

        for rubric in rubric_prompts:
            task = asyncio.create_task(
                generate_response(user_input, rubric_prompts[rubric])
            )
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        for rubric, response in zip(rubric_prompts, responses):
            st.session_state.llm_responses[f"{section}_{rubric}"] = response
        # Add a small delay to keep the spinner visible for a minimum duration
        await asyncio.sleep(1)


def read_prompts(section_dir):
    prompts = {}
    for filename in os.listdir(section_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(section_dir, filename), "r") as file:
                rubric_title = filename.split(":")[0].strip()
                prompts[rubric_title] = file.read()
    return prompts


def rubric_item(title, help="", response="LLM response goes here. 5/10"):
    # Override the score from the response, which ends with a score like ". 5/10"
    score = response.split(".")[-1].strip()


    st.metric(title, score, help=help)

    with st.expander("Ulysses says:"):
        st.write(response)



# Get the list of subdirectories in the "prompts" directory
prompt_dirs = [
    d for d in os.listdir("prompts") if os.path.isdir(os.path.join("prompts", d))
]

st.write("# Your Application")

for section_dir in prompt_dirs:
    section_name = section_dir.replace("_", " ").title()
    with st.container(border=True):
        col1, col2 = st.columns([3, 2])
        with col1:
            st.write(f"## {section_name}")
            section_text = st.text_area(section_name, height=400)
            section_prompts = read_prompts(os.path.join("prompts", section_dir))
            if st.button(f"Generate {section_name} Responses"):
                asyncio.run(
                    generate_responses(section_text, section_prompts, section_dir)
                )
        with col2:
            st.write(f"## {section_name} Rubric")
            section_prompts = read_prompts(os.path.join("prompts", section_dir))
            for rubric_title in section_prompts:
                if rubric_title != "meta_prompt.txt":
                    rubric_item(
                        rubric_title,
                        response=st.session_state.llm_responses.get(
                            f"{section_dir}_{rubric_title}", ""
                        ),
                    )

