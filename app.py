import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Բեռնավորում ենք .env ֆայլից
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="AI Content Generator", page_icon="📝", layout="centered")

st.title("📝 AI Content Generator")
st.write("Ստեղծիր բովանդակություն արհեստական բանականությամբ։")

# Մուտքային տեքստ
user_prompt = st.text_area("Մուտքագրիր թեման կամ առաջարկը:")

# Ընտրացանկեր
content_type = st.selectbox(
    "Ընտրիր բովանդակության տեսակը",
    ["Հոդված", "Բլոգ գրառում", "Ֆեյսբուք գրառում", "Մարքեթինգային սլոգան", "Մարդկային ոճով բացատրություն"]
)

length = st.radio(
    "Տեքստի երկարությունը",
    ["Կարճ (մինչև 100 բառ)", "Միջին (100-300 բառ)", "Երկար (300+ բառ)"]
)

language = st.selectbox(
    "Լեզուն",
    ["Հայերեն", "Անգլերեն", "Ռուսերեն"]
)

# Ստեղծելու կոճակ
if st.button("Ստեղծել բովանդակություն"):
    if user_prompt:
        try:
            # Prompt ձևավորում
            length_instruction = {
                "Կարճ (մինչև 100 բառ)": "Կարճ տեքստ, մինչև 100 բառ",
                "Միջին (100-300 բառ)": "Միջին երկարության տեքստ, մոտ 200 բառ",
                "Երկար (300+ բառ)": "Երկար տեքստ, ավելի քան 300 բառ"
            }

            full_prompt = f"""
            Ստեղծիր {content_type} {language} լեզվով:
            Թեմա: {user_prompt}
            Տեքստի երկարություն՝ {length_instruction[length]}։
            """

            # Կանչում ենք մոդելին
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Դու օգնում ես գրել բովանդակություն պարզ և օգտակար ոճով։"},
                    {"role": "user", "content": full_prompt}
                ],
                max_tokens=600
            )

            ai_text = response.choices[0].message.content

            st.subheader("📌 Արդյունք")
            st.write(ai_text)

            # Պատճենելու կոճակ
            st.download_button("⬇️ Պահել որպես TXT", ai_text, file_name="content.txt")

        except Exception as e:
            st.error(f"Սխալ: {e}")
    else:
        st.warning("Խնդրում ենք մուտքագրել թեմա։")
