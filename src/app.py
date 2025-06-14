import streamlit as st
from pathlib import Path
from PIL import Image
import torch
from transformers import (
    AutoProcessor,
    AutoModelForCausalLM
)
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="MedLensAI - Diagnostic Assistant",
    page_icon="🏥",
    layout="wide"
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Define model paths
MODEL_NAME = "google/medgemma-4b-it"
MODEL_DIR = Path("data/models/medgemma-4b-it")

def get_device():
    """Get the appropriate device for the current system."""
    if torch.backends.mps.is_available():
        return torch.device("mps")
    elif torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")

def save_model_locally(processor, model):
    """Save the model and processor locally."""
    try:
        # Create model directory if it doesn't exist
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        
        # Save processor
        processor.save_pretrained(MODEL_DIR)
        
        # Save model
        model.save_pretrained(MODEL_DIR)
        
        st.sidebar.success("Model saved successfully!")
    except Exception as e:
        st.sidebar.error(f"Error saving model: {str(e)}")

def load_models():
    """Load the MedGemma model and processor."""
    try:
        device = get_device()
        
        # Check if model exists locally
        if MODEL_DIR.exists():
            st.sidebar.info("Loading model from local storage...")
            processor = AutoProcessor.from_pretrained(MODEL_DIR)
            model = AutoModelForCausalLM.from_pretrained(
                MODEL_DIR,
                torch_dtype=torch.float16 if device.type != "cpu" else torch.float32,
                device_map="auto",
                trust_remote_code=True
            )
        else:
            st.sidebar.info("Downloading model from Hugging Face...")
            processor = AutoProcessor.from_pretrained(MODEL_NAME)
            model = AutoModelForCausalLM.from_pretrained(
                MODEL_NAME,
                torch_dtype=torch.float16 if device.type != "cpu" else torch.float32,
                device_map="auto",
                trust_remote_code=True
            )
            
            # Save model locally
            save_model_locally(processor, model)
        
        return processor, model
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        return None, None

def format_prompt(prompt: str) -> str:
    """Format the prompt for MedGemma."""
    # MedGemma expects the image token to be at the start of the prompt
    return f"<image_placeholder>\n{prompt}"

def process_image(image, prompt):
    """Process the uploaded image with the given prompt."""
    try:
        processor, model = load_models()
        if any(x is None for x in [processor, model]):
            return "Error: Models not loaded properly."

        device = get_device()
        
        # Format the prompt
        formatted_prompt = format_prompt(prompt)
        
        # First, process the image
        image_inputs = processor(
            images=image,
            return_tensors="pt"
        ).to(device)
        
        # Then, process the text
        text_inputs = processor(
            text=formatted_prompt,
            return_tensors="pt",
            add_special_tokens=True
        ).to(device)
        
        # Combine the inputs
        inputs = {
            "pixel_values": image_inputs.pixel_values,
            "input_ids": text_inputs.input_ids,
            "attention_mask": text_inputs.attention_mask
        }

        # Generate response
        outputs = model.generate(
            **inputs,
            max_length=512,
            num_return_sequences=1,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            pad_token_id=processor.tokenizer.pad_token_id,
            eos_token_id=processor.tokenizer.eos_token_id
        )

        # Decode and return the response
        response = processor.decode(outputs[0], skip_special_tokens=True)
        # Remove the input prompt from the response
        response = response.replace(formatted_prompt, "").strip()
        return response
    except Exception as e:
        st.error(f"Error details: {str(e)}")
        return f"Error processing image: {str(e)}"

def main():
    st.title("🏥 MedLensAI - Diagnostic Assistant")
    st.markdown("""
    Upload medical images and ask questions to get AI-powered diagnostic assistance.
    """)

    # Display system info
    device = get_device()
    st.sidebar.info(f"Running on: {device.type.upper()}")

    # Sidebar for patient information
    with st.sidebar:
        st.header("Patient Information")
        patient_id = st.text_input("Patient ID")
        symptoms = st.text_area("Reported Symptoms")
        previous_diagnosis = st.text_area("Previous Diagnosis")

    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Upload Medical Image")
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=["png", "jpg", "jpeg", "dicom"]
        )

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

    with col2:
        st.subheader("Ask Questions")
        prompt = st.text_area(
            "Enter your question about the image",
            placeholder="e.g., What abnormalities do you see in this X-ray?"
        )

        if st.button("Analyze") and uploaded_file is not None and prompt:
            with st.spinner("Analyzing image..."):
                response = process_image(image, prompt)
                st.session_state.chat_history.append({
                    "prompt": prompt,
                    "response": response
                })

    # Display chat history
    st.subheader("Analysis History")
    for chat in st.session_state.chat_history:
        with st.expander(f"Q: {chat['prompt']}"):
            st.write(f"A: {chat['response']}")

if __name__ == "__main__":
    main() 