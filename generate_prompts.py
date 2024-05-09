import streamlit as st
from openai import OpenAI
import os

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def generate_meta_prompt(quality: str):
    # meta_prompt = "we are in testing, just say the number 987"

    prompts_folder = "prompts"
    # generating a meta_prompt

    meta_prompt_file_w = open("prompts/meta_prompt.txt", "w")

    meta_prompt_file_w.write("Here are some example prompts \n\n")
    meta_prompt_file_w = open("prompts/meta_prompt.txt", "a")

    for filename in os.listdir(prompts_folder):
        # Check if the item is a file (not a directory) and not metaprompt and not quality prompt
        if (
            os.path.isfile(os.path.join(prompts_folder, filename))
            and filename != "meta_prompt.txt"
            and filename != (quality + ".txt")
        ):
            meta_prompt_file_w.write("Quality:" + filename[:-4])
            prompt_file_r = open("prompts/" + filename, "r")
            prompt = prompt_file_r.read()
            meta_prompt_file_w.write("\n\n Prompt: \n\n" + prompt + "\n\n")
    meta_prompt_file_w.write(
        "Please write a prompt for the following quality. Make sure to use the same examples as used in the previous prompt examples.\n\n Quality:"
        + quality
        + "\n\n Prompt: "
    )


def generate_prompt(quality: str, meta_prompt: str) -> str:
    prompt_file = open("prompts/" + quality + ".txt", "w")

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": meta_prompt},
            {"role": "user", "content": quality},
        ],
    )
    response = response.choices[0].message.content
    prompt_file.write(response)
    return response


quality = "Past projects: If the applicant has done similar projects in the past, are there reflections on the successes and (especially) failures?"
generate_meta_prompt(quality)
meta_prompt = open("prompts/meta_prompt.txt", "r").read()
generate_prompt(quality, meta_prompt)
