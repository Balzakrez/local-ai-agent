# Local AI Agent

A simple and elegant Python CLI chat agent that connects to local Large Language Models (LLMs) through an OpenAI-compatible API.

## Features
- **Local Inference:** Connects to [LM Studio](https://lmstudio.ai/) or other local servers.
- **Context Awareness:** Maintains a conversation history so the AI remembers previous exchanges.
- **Rich UI:** Uses the `rich` library to provide a clean terminal interface with status spinners and colors.
- **OOP Design:** Clean, extensible object-oriented code.

## Prerequisites
- Python 3.10+
- [LM Studio](https://lmstudio.ai/) (or any server providing an OpenAI-compatible endpoint).

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. Install the dependencies:
   ```bash
   python -m pip install --upgrade pip
   pip install requests rich
   ```

## Usage

1. Open **LM Studio** and start the **Local Server**.
2. Make sure a model is loaded and the server is running on `http://127.0.0.1:1234`.
3. Run the agent:
   ```bash
   python agent.py
   ```
4. Type your message and press Enter.
5. Type `quit` or `exit` to close the session.

## Configuration
You can initialize the agent with a specific model name and/or system prompt:
```python
agent = LocalAgent(
    model="qwen3.5",
    system_prompt="You are a helpful assistant."
)
```

## License
This project is distributed under the MIT License.