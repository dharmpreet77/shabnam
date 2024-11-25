import os
import json
import streamlit as st
from groq import Groq
import speech_recognition as sr


# Streamlit page configuration
st.set_page_config(
    page_title="Amber Salon - ChatBot",
    page_icon="💇‍♀️",
    layout="wide"
)
# Adding custom CSS styles
custom_css = """
<style>
/* Style for the title */
h1 {
    font-size:2rem;
    padding-top:0;
   
}


</style>
"""
st.markdown(
    """
    <style>
    /* Background styling */
    [data-testid="stAppViewContainer"] {
        background-color: #fdfcfa;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# Embedding CSS in the app
st.markdown(custom_css, unsafe_allow_html=True)


def record_audio_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # Create a placeholder for the "Listening..." message
        message_placeholder = st.empty()
        message_placeholder.info("Listening... Speak now!")
        try:
            audio_data = recognizer.listen(source, timeout=5)
            message_placeholder.empty()  # Remove the "Listening..." message
            return recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            message_placeholder.empty()  # Remove the message on error
            st.error("Sorry, could not understand the audio.")
        except sr.RequestError as e:
            message_placeholder.empty()  # Remove the message on error
            st.error(f"Could not request results; {e}")
        except Exception as e:
            message_placeholder.empty()  # Remove the message on error
            st.error(f"An error occurred: {e}")
        return ""

    
# App title
st.title("💇‍♀️ Amber Salon - ChatBot")


# Load API Key from config file
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))
GROQ_API_KEY = config_data["GROQ_API_KEY"]

# Save the API key to environment variable
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Initialize Groq client
client = Groq()

# Initialize the chat history as Streamlit session state if not present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.chat_history.append(
        {"role": "assistant", "content": "Hello! Welcome to Amber Salon. How can I assist you today? 😊"}
    )

# Load salon details from the JSON file
salon_info_file = os.path.join(working_dir, "salon_info.json")
with open(salon_info_file, "r") as f:
    salon_details = json.load(f)

# Extract details dynamically from salon_details
about_salon = salon_details.get("about_salon", "Details not available.")
services_offered = salon_details.get("services_offered", {})
working_hours = salon_details.get("working_hours", {})
faqs = salon_details.get("faqs", {})
appointment_booking = salon_details.get("appointment_booking", {})
branches = salon_details.get("branches", [])

# Function to handle specific keywords or phrases
def handle_specific_queries(user_input):
    user_input = user_input.lower()

    # Check for the chatbot's name
    if "your name" in user_input or "who are you" in user_input:
        return "My name is Shabnam, your friendly salon assistant! 😊"

    # Check for payment methods
    elif "payment method" in user_input or "accept payment" in user_input:
        return "We accept all types of credit and debit cards."

    # If no specific match, return None
    return None


# Create tabs
tabs = st.tabs(["Get Started", "Men Hair Cut Styles", "Women Hair Cut Styles", "Nail Shapes"])

# Quick Links Tab
with tabs[0]:
    # Add service suggestion buttons
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])  # Adjust ratios to control button widths and spacing

    # Button Presses with Automated Responses (independent `if` conditions)

    if col1.button("💇‍♀️ What services do you provide?"):
        user_prompt = "What type of services do you offer?"
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})

        assistant_response = (
            "We offer a wide range of services:\n" +
            "\n".join(f"- {service}" for service in services_offered)
        )
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    if col2.button("📅 Make an appointment now"):
        user_prompt = "I want to book an appointment."
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})

        assistant_response = f"Sure! To book your haircut appointment, please visit our website at {appointment_booking.get('booking_url', 'N/A')}."
        st.markdown("<script>scrollToInput();</script>", unsafe_allow_html=True)
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})


    if col3.button("⏰ What are your salon timings?"):
        user_prompt = "What are your salon working hours?"
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})

        assistant_response = (
            f"Monday to Saturday: {working_hours.get('monday_to_saturday', 'N/A')}\n"
            f"Sunday: {working_hours.get('sunday', 'N/A')}"
        )
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    if col4.button("📞 Where are your salons located?"):
        user_prompt = "Where is your salon located?"
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        if branches:
            assistant_response = "We have the following branches near Kamloops:"
            # Create a list with branch details
            for branch in branches:
                branch_details = (
                    f"- **{branch['name']}**\n"
                    f"  - **Address:** {branch['address']}\n"
                    f"  - **Phone:** {branch['phone']}\n"
                    f"  - **Email:** {branch['email']}\n"
                    f"  - **Website:** [Visit Website]({branch['website']})"
        )
                assistant_response += f"\n\n{branch_details}"
        else:
            assistant_response = "Sorry, we currently do not have information about our branches."
    
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})


   
# Men Hair Cut Styles Tab
with tabs[1]:
    # Create columns for row-wise layout
    col1, col2, col3, col4 = st.columns(4)  # Adjust the number of columns as needed

    with col1:
        st.image("images/slicked_back_undercut.jpg", caption="Slicked Back Undercut")
    
    with col2:
        st.image("images/curly_taper_fade.jpg", caption="Curly Taper Fade")
    
    with col3:
        st.image("images/medium_shaggy_hair.jpg", caption="Medium Shaggy Hair")
    
    with col4:
        st.image("images/man_bun_undercut.jpg", caption="Man Bun Undercut")

# Women Hair Cut Styles Tab
with tabs[2]:
    
    # Create columns for row-wise layout
    col1, col2, col3, col4 = st.columns(4)  # Adjust the number of columns as needed

    with col1:
        st.image("images/asymmetrical_bob.jpg", caption="Asymmetrical Bob")
    
    with col2:
        st.image("images/edgy_undercut_with_curls.jpg", caption="Edgy Undercut with Curls")
    
    with col3:
        st.image("images/soft_textured_waves.jpg", caption="Soft Textured Waves")
    
    with col4:
        st.image("images/sleek_layered_straight_hair.jpg", caption="Sleek Layered Straight Hair")


# Nail Shapes Tab
with tabs[3]:
    st.image("images/nail_shapes.jpg", caption="Nail Shapes")


# Initialize `user_prompt` as an empty string to avoid NameError
user_prompt = ""



# Combine dynamic context from JSON data
salon_context = (
    f"About Salon:\n{about_salon}\n\n"
    f"Working Hours:\n"
    f"Monday to Saturday: {working_hours.get('monday_to_saturday', 'N/A')}\n"
    f"Sunday: {working_hours.get('sunday', 'N/A')}\n\n"
    f"Services Offered:\n"
    f"- Men:\n"
    + "\n".join([f"  - {service}" for service in services_offered.get("men", {}).get("hair_services", [])])
    + "\n- Women:\n"
    + "\n".join([f"  - {service}" for service in services_offered.get("women", {}).get("hair_services", [])]) +
    "\n\nFAQs:\n" + "\n".join([f"- {q}: {a}" for q, a in faqs.items()])
)

# Function to generate concise, business-aligned responses based on keywords for hair, skin, and general salon services
def recommend_service(user_input):
    user_input = user_input.lower()

    

# Display manicure-specific details if requested
def get_manicure_details():
    manicure_info = services_offered.get("women", {}).get("other_services", {}).get("Manicure", {})
    description = manicure_info.get("description", "Manicure details are not available.")
    nail_shapes = manicure_info.get("nail_shapes", [])
    response = description
    if nail_shapes:
        response += "\n\nWe offer the following nail shapes:\n" + "\n".join(f"- {shape}" for shape in nail_shapes)
    return response

# Function to generate concise, business-aligned responses based on keywords for hair, skin, and general salon services
def recommend_service(user_input):
    user_input = user_input.lower()

    # Keyword-based responses for hair care
    if "dry hair" in user_input or "hair is dry" in user_input:
        return "Our hydrating hair treatment is great for adding moisture and softness to dry hair."
    elif "curly hair" in user_input or "manage curls" in user_input:
        return "Our curl-defining treatment helps enhance and control curls beautifully."
    elif "damaged hair" in user_input or "repair hair" in user_input:
        return "Our repair treatment restores strength and shine to damaged hair."
    elif "frizzy hair" in user_input:
        return "Our smoothing treatment helps control frizz and leaves hair sleek and manageable."

    # Keyword-based responses for skin care
    elif "dry skin" in user_input or "moisturize skin" in user_input:
        return "Our hydrating facial is perfect for adding moisture to dry skin."
    elif "oily skin" in user_input or "balance oil" in user_input:
        return "Our clarifying facial helps balance oily skin, leaving it fresh and clean."
    elif "dull skin" in user_input or "brighten skin" in user_input:
        return "Our brightening facial revitalizes dull skin for a fresh, glowing complexion."
    elif "sensitive skin" in user_input:
        return "Our calming facial is gentle on sensitive skin, reducing redness and soothing irritation."
    elif "acne" in user_input or "acne scars" in user_input:
        return "Our skin renewal facial is effective for addressing acne and acne scars."

    # General salon service inquiries
    elif "facial" in user_input:
        return "We offer a range of facials tailored to different skin types and needs."
    elif "massage" in user_input:
        return "Our relaxing massages are designed to relieve stress and rejuvenate you."
    elif "manicure" in user_input or "pedicure" in user_input:
        return "Our manicure and pedicure services keep your hands and feet looking and feeling their best."
    elif "bridal package" in user_input:
        return "We offer customized bridal packages to make you look your best on your special day."

    else:
        return None




# Append the user prompt and automated response to chat history if a button is pressed
if user_prompt:
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

# Ensure session state variables are initialized
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""  # For text input box

if "voice_input" not in st.session_state:
    st.session_state["voice_input"] = ""  # For voice input


# Function to handle voice commands
def handle_voice_command():
    """Handle voice input when the Voice Command button is pressed."""
    audio_text = record_audio_to_text()  # Transcribe the audio to text
    if audio_text:
        # Add the transcribed text to chat history as user input
        st.session_state.chat_history.append({"role": "user", "content": audio_text})

        # Handle specific queries first
        assistant_response = handle_specific_queries(audio_text)
        if assistant_response:  # If a match is found, respond and skip further processing
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
        else:
            # Check for recommendation requests
            assistant_response = recommend_service(audio_text)
            if assistant_response:
                st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
            else:
                # Default to fallback logic
                messages = [
                    {"role": "system", "content": "You are a helpful assistant at a salon."},
                    *st.session_state.chat_history
                ]
                try:
                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=messages
                    )
                    assistant_response = response.choices[0].message.content
                except Exception as e:
                    assistant_response = "Sorry, something went wrong. Please try again."
                    st.error(f"Error: {e}")

                st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})


# Function to handle user text input
def handle_user_input():
    """Handle user input when 'Enter' is pressed."""
    user_prompt = st.session_state["user_input"]
    if user_prompt:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})

        # Generate assistant response using the model
        assistant_response = generate_response_from_model(user_prompt)
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

        # Clear the input box after processing
        st.session_state["user_input"] = ""  # Reset input box to empty

# Function to generate assistant response using the model
def generate_response_from_model(user_prompt):
    """Generate a response from the model."""
    # Prepare the chat history for the model
    messages = [
        {"role": "system", "content": "You are a helpful assistant at a salon."},
        *st.session_state.chat_history
    ]
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error: {e}")
        return "Sorry, something went wrong. Please try again."

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


# Input field for user's message
user_prompt = st.chat_input("Ask a question...")

if user_prompt:
    handle_user_input()

# Add a button for voice input (optional)
if st.button("🎙️ Voice Command"):
    handle_voice_command()

if user_prompt:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Handle specific queries (e.g., name, payment methods)
    assistant_response = handle_specific_queries(user_prompt)
    if assistant_response:  # If a match is found, respond and skip further processing
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
    else:
        # Check for recommendation requests
        assistant_response = recommend_service(user_prompt)
        if assistant_response:
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
        else:
            # Fallback to salon details or API responses
            if "about your salon" in user_prompt.lower() or "tell me about your salon" in user_prompt.lower():
                assistant_response = salon_details.get("about_salon", "Details not available.")
            elif "faq" in user_prompt.lower():
                assistant_response = "Here are some common questions:\n" + "\n".join(f"- {q}: {a}" for q, a in salon_details["faqs"].items())
            elif "book appointment" in user_prompt.lower() or "appointment" in user_prompt.lower():
                assistant_response = f"Sure! To book your haircut appointment, please visit our website at {appointment_booking.get('booking_url', 'N/A')}."
            elif "nail shape" in user_prompt.lower() or "nail" in user_prompt.lower():
                nail_shapes = salon_details["services_offered"]["women"]["other_services"]["Manicure"]["nail_shapes"]
                assistant_response = "Here are the nail shapes we offer:\n" + "\n".join(f"- {shape}" for shape in nail_shapes)
            elif "branches" in user_prompt.lower() or "locations" in user_prompt.lower() or "where are you located" in user_prompt.lower():
                if branches:
                    assistant_response = "We have the following branches near Kamloops:\n"
                    assistant_response += "\n".join([f"- {branch['name']}, Address: {branch['address']}, Phone: {branch['phone']}, Email: {branch['email']}, Website: {branch['website']}" for branch in branches])
                else:
                    assistant_response = "Sorry, we currently do not have information about our branches."
            else:
                # Use API for other queries
                messages = [
                    {"role": "system", "content": "You are a helpful assistant at a salon."},
                    {"role": "system", "content": salon_context},
                    *st.session_state.chat_history
                ]
                try:
                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=messages
                    )
                    assistant_response = response.choices[0].message.content
                except Exception as e:
                    assistant_response = "Sorry, something went wrong. Please try again."
                    st.error(f"Error: {e}")

        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # Clear the input box after processing
    st.session_state["user_input"] = ""


# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
