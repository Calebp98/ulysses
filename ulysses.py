from openai import OpenAI
import streamlit as st

st.title("Ulysses Grant Assistant")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-turbo"

with open("track_record_prompt.txt", "r") as file:
    system_prompt = file.read()


txt = st.text_area("Track record section goes here")

st.write(f"You wrote {len(txt)} characters.")


if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

if prompt := st.chat_input("Describe your track record:"):
    st.session_state.messages.append({"role": "user", "content": system_prompt})
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
