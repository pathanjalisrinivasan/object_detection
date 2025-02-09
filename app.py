import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import requests
import json

def get_claude_response(image_data: bytes, prompt: str, api_key: str) -> dict:
    """Get response from Claude Vision API for object detection."""
    base64_image = base64.b64encode(image_data).decode('utf-8')
    
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    
    payload = {
        "model": "claude-3-opus-20240229",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"""
                        Analyze this image and detect the exact location of the '{prompt}'.
                        Consider objects that are partially visible or obstructed.
                        
                        Return a JSON object in this format:
                        {{
                            "found": true/false,
                            "coords": [x1, y1, x2, y2],
                            "confidence": 0.0 to 1.0,
                            "description": "brief location description"
                        }}
                    """},
                    {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": base64_image}}
                ]
            }
        ]
    }
    
    try:
        response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload)
        response_json = response.json()

        if 'content' not in response_json:
            st.error("Claude API response is missing 'content'. Check API status.")
            return {"found": False}

        try:
            return json.loads(response_json['content'][0]['text'])
        except json.JSONDecodeError:
            st.error("Failed to parse JSON response from Claude.")
            return {"found": False}
    except Exception as e:
        st.error(f"API Error: {e}")
        return {"found": False}

def draw_bounding_box(image: Image.Image, coords, confidence, label):
    """Draw bounding box on image with label."""
    image_copy = image.convert("RGBA")
    overlay = Image.new("RGBA", image_copy.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    width, height = image.size

    x1 = int(coords[0] * width)
    y1 = int(coords[1] * height)
    x2 = int(coords[2] * width)
    y2 = int(coords[3] * height)

    # Set colors based on confidence
    if confidence > 0.75:
        color = (0, 255, 0, 128)  # Green semi-transparent
    elif confidence > 0.5:
        color = (255, 255, 0, 128)  # Yellow semi-transparent
    else:
        color = (255, 0, 0, 128)  # Red semi-transparent

    draw.rectangle([x1, y1, x2, y2], outline=(color[0], color[1], color[2], 255), width=4)
    
    label_text = f"{label} ({confidence:.0%})"
    
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()  # Fallback to default font

    text_size = draw.textbbox((0, 0), label_text, font=font)
    text_width, text_height = text_size[2] - text_size[0], text_size[3] - text_size[1]
    
    draw.rectangle([x1, y1 - text_height, x1 + text_width, y1], fill=(0, 0, 0, 128))
    draw.text((x1, y1 - text_height), label_text, fill=(255, 255, 255, 255), font=font)
    
    return Image.alpha_composite(image_copy, overlay)

def main():
    st.set_page_config(layout="wide")
    st.title("Object Detection with Claude Vision")
    
    left_col, right_col = st.columns([1, 2])
    
    with left_col:
        api_key = st.text_input("Claude API Key", type="password")
        uploaded_file = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])
        prompt = st.text_input("Object to detect", placeholder="e.g., cat, bottle")
        confidence_threshold = st.slider("Confidence Threshold", 0.1, 1.0, 0.5)
        
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    
    with right_col:
        if uploaded_file and prompt:
            if not api_key:
                st.error("Please enter your Claude API key.")
                return
            
            image = Image.open(uploaded_file)
            img_byte_arr = io.BytesIO()
            image_format = "JPEG" if image.format and image.format.upper() in ["JPG", "JPEG"] else "PNG"
            image.save(img_byte_arr, format=image_format)
            img_byte_arr = img_byte_arr.getvalue()
            
            with st.spinner("Detecting objects..."):
                results = get_claude_response(img_byte_arr, prompt, api_key)
            
            if results.get("found") and results.get("confidence", 0) >= confidence_threshold:
                st.image(draw_bounding_box(image, results["coords"], results["confidence"], prompt), use_container_width=True)
                st.success(f"Detected '{prompt}' at {results['description']} with {results['confidence']:.2%} confidence.")
            else:
                st.warning(f"No '{prompt}' detected above {confidence_threshold:.0%} confidence.")
                st.image(image, use_container_width=True)
        else:
            st.info("Upload an image and enter a prompt to begin detection.")

if __name__ == "__main__":
    main()
