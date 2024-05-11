# import streamlit as st
# from openai import OpenAI
# import os

# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# def generate_meta_prompt(quality: str):
#     # meta_prompt = "we are in testing, just say the number 987"

#     prompts_folder = "prompts"
#     # generating a meta_prompt

#     meta_prompt_file_w = open("prompts/meta_prompt.txt", "w")

#     meta_prompt_file_w.write("Here are some example prompts \n\n")
#     meta_prompt_file_w = open("prompts/meta_prompt.txt", "a")

#     for filename in os.listdir(prompts_folder):
#         # Check if the item is a file (not a directory) and not metaprompt and not quality prompt
#         if (
#             os.path.isfile(os.path.join(prompts_folder, filename))
#             and filename != "meta_prompt.txt"
#             and filename != (quality + ".txt")
#         ):
#             meta_prompt_file_w.write("Quality:" + filename[:-4])
#             prompt_file_r = open("prompts/" + filename, "r")
#             prompt = prompt_file_r.read()
#             meta_prompt_file_w.write("\n\n Prompt: \n\n" + prompt + "\n\n")
#     meta_prompt_file_w.write(
#         "Please write a prompt for the following quality. Make sure to use the same examples as used in the previous prompt examples.\n\n Quality:"
#         + quality
#         + "\n\n Prompt: "
#     )


# def generate_prompt(quality: str, meta_prompt: str) -> str:
#     prompt_file = open("prompts/" + quality + ".txt", "w")

#     response = client.chat.completions.create(
#         model="gpt-4-turbo",
#         messages=[
#             {"role": "system", "content": meta_prompt},
#             {"role": "user", "content": quality},
#         ],
#     )
#     response = response.choices[0].message.content
#     prompt_file.write(response)
#     return response


# quality = "Past funding: If the applicant has gotten funding in the past, did the application mention the project in a way that’s easy for us to identify?"
# generate_meta_prompt(quality)
# meta_prompt = open("prompts/meta_prompt.txt", "r").read()
# generate_prompt(quality, meta_prompt)

import streamlit as st
from openai import OpenAI
import os

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def generate_meta_prompt(quality: str, prompt_folder: str):
    meta_prompt_file_w = open(f"{prompt_folder}/meta_prompt.txt", "w")
    meta_prompt_file_w.write("Here are some example prompts \n\n")
    meta_prompt_file_w = open(f"{prompt_folder}/meta_prompt.txt", "a")

    for filename in os.listdir(prompt_folder):
        if (
            os.path.isfile(os.path.join(prompt_folder, filename))
            and filename != "meta_prompt.txt"
            and filename != (quality + ".txt")
        ):
            meta_prompt_file_w.write("Quality:" + filename[:-4])
            prompt_file_r = open(f"{prompt_folder}/{filename}", "r")
            prompt = prompt_file_r.read()
            meta_prompt_file_w.write("\n\n Prompt: \n\n" + prompt + "\n\n")

    meta_prompt_file_w.write(
        "Please write a prompt for the following quality. Make sure to use the same examples as used in the previous prompt examples.\n\n Quality:"
        + quality
        + "\n\n Prompt: "
    )


def generate_prompt(quality: str, meta_prompt: str, prompt_folder: str) -> str:
    prompt_file = open(f"{prompt_folder}/{quality}.txt", "w")
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": meta_prompt},
            {"role": "user", "content": quality},
        ],
    )
    response = response.choices[0].message.content
    prompt_file.write(response)
    prompt_file.write(
        "\n\n Be concise and use plain, simple language. Limit your output to at most 3 sentences. You are narrowly interested in the question above. Include a rating out of 10 at the very end. The rating should be the last 4 chars of the response.\n\nHere is the section:"
    )
    return response


def main():
    quality = "Context for unfamiliar items: For track record items that are unlikely to be familiar to the fund managers, are there context given to help qualify or quantify it? "
    prompt_folder = "prompts/track_record"  # Specify the prompt folder here

    generate_meta_prompt(quality, prompt_folder)
    meta_prompt = open(f"{prompt_folder}/meta_prompt.txt", "r").read()
    generated_prompt = generate_prompt(quality, meta_prompt, prompt_folder)
    print(f"Generated Prompt: {generated_prompt}")


if __name__ == "__main__":
    main()
