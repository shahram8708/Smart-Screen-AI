# Smart Screen AI

`Smart Screen AI` is a Python application that allows users to record their screen, process the recording with Google Gemini AI, and interact with the processed content. The application also includes features for text-to-speech, copying text to the clipboard, and a responsive UI for seamless interaction.

## Features

- **Screen Recording:** Start and stop screen recording with options to save the video.
- **AI Processing:** Upload the recorded video to Google Gemini AI for analysis.
- **Text-to-Speech:** Play and stop the audio generated from the response.
- **Clipboard Operations:** Copy the response text to the clipboard.
- **Interactive UI:** Provides a clean and user-friendly interface.

## Installation

### Prerequisites

Ensure you have Python installed on your system. You can download Python from [python.org](https://www.python.org/downloads/).

### Clone the Repository

```bash
git clone https://github.com/shahram8708/smart-screen-ai.git
cd smart-screen-ai
```

### Install Dependencies

Install the required Python libraries using `pip`. Create a `requirements.txt` file as described below or install directly:

```bash
pip install -r requirements.txt
```

### Creating `requirements.txt`

To create the `requirements.txt` file, use the following content:

```plaintext
opencv-python
pyautogui
numpy
google-generativeai
Pillow
pyttsx3
pyperclip
markdown
tkhtmlview
```

## Configuration

Before running the application, set up your Google Gemini API key. 

1. Obtain your API key from the [Google Gemini AI platform](https://example.com).
2. Set the environment variable `API_KEY` in your operating system.

   ```bash
   export API_KEY=your_api_key_here
   ```

## Running the Application

To run the application, execute the following command:

```bash
python smart_screen_ai.py
```

### Usage

1. **Start Recording:** Click on the "Start Recording 🎥" button to begin capturing your screen.
2. **Stop Recording:** Click on the "Stop Recording ⏹️" button to stop capturing.
3. **Enter Prompt:** Type your prompt in the "Enter Prompt 💬" field and press Enter.
4. **Play Audio:** Click the ▶️ button to hear the AI-generated response.
5. **Stop Audio:** Click the ⏹️ button to stop audio playback.
6. **Copy Response:** Click the 📋 button to copy the response text to the clipboard.

## Building the Executable

To build the executable file, use `PyInstaller`:

1. Install PyInstaller:

   ```bash
   pip install pyinstaller
   ```

2. Build the executable:

   ```bash
   pyinstaller --onefile --noconsole --add-data "path_to_your_file;." smart_screen_ai.py
   ```

   Replace `path_to_your_file` with the path to any additional files your application requires.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.
