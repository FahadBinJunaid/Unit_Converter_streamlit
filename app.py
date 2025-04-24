import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Key from .env for local development
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# If running on Streamlit Share, load from secrets
if not api_key:
    api_key = st.secrets["GEMINI_API_KEY"]

# Configure Gemini 
genai.configure(api_key=api_key)

st.markdown(
    """
    <style>
        /* Apply the gradient background to the entire page */
        .stApp {
            background: linear-gradient(to right, #6A11CB, #2575FC);
            color: white;
        }

        /* Customizing Button */
        div.stButton > button {
            background-color: #FFD700; /* Gold */
            color: black;
            border-radius: 10px;
            font-weight: bold;
            padding: 10px 20px;
        }
        div.stButton > button:hover {
            background-color: #FFC107; /* Lighter Gold on Hover */
        }

        /* Selectbox & Input Styling */
        .stSelectbox, .stTextInput {
            border-radius: 10px;
            padding: 5px;
        }

        /* Make labels white */
        label {
            color: white !important;
            font-weight: bold;
        }
        
        div[data-testid="stNotification"], div.stAlert {
            background-color: white !important;
            color: black !important;
            font-weight: bold;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #FFD700; /* Gold border */
        }
        
    </style>
    """,
    unsafe_allow_html=True
)



# Streamlit App Title
st.title("🚀 Google-Like Unit Converter ⚡ Powered by Gemini 🤖")

# Define unit categories and possible conversions
unit_categories = {
    "Length": ["meters", "kilometers", "miles", "feet", "inches", "centimeters", "millimeters", "yards"],
    "Weight": ["kilograms", "grams", "pounds", "ounces", "tons"],
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Volume": ["liters", "milliliters", "gallons", "cups"],
    "Time": ["seconds", "minutes", "hours", "days", "weeks", "months", "years"],
    "Speed": ["meters per second", "kilometers per hour", "miles per hour", "knots"],
    "Energy": ["joules", "calories", "kilowatt-hours", "electronvolts"],
    "Pressure": ["pascals", "bars", "atmospheres", "psi"],
    "Data Storage": ["bytes", "kilobytes", "megabytes", "gigabytes", "terabytes", "petabytes"]
}


# Dropdown to select category
category = st.selectbox("Select unit type:", list(unit_categories.keys()))

# Dropdowns to select "From" and "To" units
from_unit = st.selectbox("Convert from:", unit_categories[category])
to_unit = st.selectbox("Convert to:", unit_categories[category])

# Input field for the value to convert (Accepts both integer and float values)
value_input = st.text_input("Enter value:", value="1")  # Default to "1" for better UX

# Convert input to the correct numerical type
try:
    if "." in value_input:
        value = float(value_input)  # Convert float values
    else:
        value = int(value_input)  # Convert whole numbers to int
except ValueError:
    st.error("Please enter a valid number.")
    st.stop()

# Function to call Gemini AI API for conversion
def convert_units(value, from_unit, to_unit):
    prompt = f"Convert {value} {from_unit} to {to_unit}."
    
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")  # Updated Model Name
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Button to trigger conversion
if st.button("Convert"):
    if value > 0:
        result = convert_units(value, from_unit, to_unit)
        if "Error" in result:
            st.error(result)
        else:
            st.success(f"Converted value: {result}")
    else:
        st.error("Please enter a valid number greater than 0.")
