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
   git clone https://github.com/Balzakrez/local-ai-agent.git
   cd local-ai-agent
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

## Usage Examples

### 1) Quick startup check
If you run the agent with the built-in `get_time` context function, you can ask for current info immediately.

```text
Agent started! Write 'quit' or 'exit' to quit.

You: What's the time and who am I?

Assistant: L'ora è 18:13 e sei Giuseppe.
```

### 2) Follow-up in the same conversation
Because chat messages are stored in memory, the assistant can continue from previous replies.

```text
You: Ottimo, tu chi sei, un agente?
Assistant: No, non sono un agente. Sono un'intelligenza artificiale progettata per aiutarti con informazioni, risposte alle domande e compiti vari in modo rapido e preciso. Posso assisterti come il tuo assistente virtuale!
```

### 3) Register your own context function
You can inject dynamic context (time, user, app state) by registering a function.

```python
def get_time() -> str:
   return "Current date and time: 2026-04-17 18:13:00\nCurrent user: Giuseppe"

agent.add_context_function(get_time)
```

## Configuration
You can initialize the agent with a specific model name and/or system prompt:
```python
agent = LocalAgent(
    model="qwen3.5",
    system_prompt="You are a helpful assistant, concise and always respond in Italian."
)
```

## License
This project is distributed under the MIT License.
