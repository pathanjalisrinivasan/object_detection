# Object Detection with Claude Vision

## Overview

This project demonstrates how AI agents can detect objects purely through reasoning—no training data, no labeling, just intelligence at work! Simply provide an image and a text prompt, and Claude Vision will locate objects with high-precision confidence scores.

## Features
- **Zero-shot object detection**: No prior training needed
- **High accuracy**: AI-powered detection with confidence scores
- **No manual labeling**: Just describe what you're looking for
- **Visual bounding boxes**: Clear and color-coded indicators on images

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/claude-object-detection.git
    cd claude-object-detection
    ```
2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
3. Run the Streamlit app:
    ```sh
    streamlit run app.py
    ```

## Usage

1. **Enter your Claude API key**
2. **Upload an image** (JPG/PNG)
3. **Enter an object name** (e.g., "cat", "bottle")
4. Adjust the **confidence threshold** (if needed)
5. **View results** with bounding boxes and descriptions

## Example

Upload an image of a living room and ask the AI to find a "lamp." It will return a bounding box with confidence and a brief description of where the lamp is.

## Notes
- Requires an **Anthropic Claude API Key**
- Works best with clear images and common objects
- Confidence scores above 0.75 are highly reliable

## License
This project is licensed under the MIT License.

## Contribution
Feel free to open issues or submit pull requests. Feedback is welcome!
