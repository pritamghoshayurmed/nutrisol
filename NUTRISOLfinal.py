import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()  # loading all the environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompts, image, additional_text):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content(input_prompts + [image[0]] + [additional_text])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded. Please upload an image.")

st.set_page_config(page_title="NUTRISOL")

# Define a placeholder for conversation history
conversation_history = []

uploaded_file = st.file_uploader("Upload your Food Image", type=["jpg", "png", "jpeg"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
    
additional_text = st.text_input("Add additional text (optional):")

submit = st.button("Tell me about the total calories")
input_prompt = """
act as an expert nutritionist, where you need to see the food items from the image and calculate the total calories,
also provide the details of every food item with calories intake
in below table format 


give the output in table format where there are 5 columns and the number of rows are the number of food items detected and corresponding to each food item breakdown the
data for the along the column
1. Item Name
2. Calories
3. Protein
4. Fat
5. Carbs
6. sugar
give the output in **** table format only , every time ****

finally you can also mention whether the food is healthy or not and also mention the percentage split of the ratio of carbohydrates, fats, fibers, sugar
and what things should be in our diet

"""

if submit:
    input_prompts = [input_prompt]
    if additional_text:
        input_prompts.append(additional_text)
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompts, image_data, additional_text)
    
    # Add the current conversation to the history
    conversation_history.append({"user_input": input_prompts, "bot_response": response})
    
    # Display conversation history along with the current response
    for entry in conversation_history:
        st.header("The result is")
        st.header(entry["bot_response"])
        
