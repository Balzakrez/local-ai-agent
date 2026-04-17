import requests
import datetime
import getpass
from typing import Any, Callable
from rich.console import Console
from requests.exceptions import RequestException

class LocalAgent:
    def __init__(
        self,
        model: str = "qwen3.5",
        system_prompt: str = "You are a helpful assistant, concise and always respond in Italian.",
        base_url: str = "http://127.0.0.1:1234/v1",
        api_key: str = "NO_API_KEY",
    ) -> None:

        self.model = model
        self.system_prompt = system_prompt
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

        self.messages: list[dict[str, Any]] = []
        self.context_functions: dict[str, Callable[[], str]] = {}

    def add_context_function(self, fn: Callable[[], str]) -> None:
        fn_name = fn.__name__
        self.context_functions[fn_name] = fn

    def chat(self, user_message: str) -> str:
        self.messages.append({"role": "user", "content": user_message})

        request_messages: list[dict[str, Any]] = [
            {"role": "system", "content": self.system_prompt},
        ]

        curr_context_content: str = "\n".join(
            f"<context>\n<{fn_name}>{fn()}</{fn_name}>\n</context>"
            for fn_name, fn in self.context_functions.items()
        )
        if curr_context_content:
            request_messages.append({"role": "system", "content": curr_context_content})

        request_messages.extend(self.messages)

        endpoint = f"{self.base_url}/chat/completions"
        request_headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                endpoint,
                headers=request_headers,
                json={"model": self.model, "messages": request_messages},
                timeout=300,
            )
            response.raise_for_status()

        except RequestException as error:
            self.messages.pop()  # Remove the last user message if the request failed
            return f"[red]Connection error to the server: {error}[/red]"

        response_json = response.json()
        response_choices = response_json.get("choices")
        if not response_choices:
            raise RuntimeError("Model response missing choices")

        assistant_message = response_choices[0].get("message")
        if assistant_message is None:
            raise RuntimeError("Model response missing message")

        assistant_text = assistant_message.get("content") or ""
        self.messages.append({"role": "assistant", "content": assistant_text})

        return assistant_text


def main():
    agent = LocalAgent(
        model="qwen3.5",
        system_prompt="You are a helpful assistant, concise and always respond in Italian.",
    )

    def get_time() -> str:
        return (
            f"Current date and time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n "
            f"Current user: {getpass.getuser()}"
        )

    agent.add_context_function(get_time)

    console = Console()
    console.print("[bold green]Agent started! Write 'quit' or 'exit' to quit.[/bold green]\n")

    with console.status("[dim]Loading model...[/dim]", spinner="dots"):
        assistant_reply = agent.chat("What's the time and who am I?")

    console.print(f"[yellow]You:[/yellow] What's the time and who am I?\n")
    console.print(f"[blue]Assistant:[/blue] {assistant_reply}\n")

    while True:
        console.print("[yellow]You:[/yellow] ", end="")
        user_input = console.input()

        if user_input.strip().lower() in {"quit", "exit"}:
            console.print("[dim]Goodbye![/dim]")
            break

        with console.status("[dim]Thinking...[/dim]", spinner="arc"):
            response = agent.chat(user_input).strip()

        console.print(f"[blue]Assistant:[/blue] {response}\n")

if __name__ == "__main__":
    main()