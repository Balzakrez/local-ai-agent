import requests
from typing import Any, Optional
from rich.console import Console
from requests.exceptions import RequestException 

class LocalAgent:
    model : str = ""
    base_url : str = "http://127.0.0.1:1234/v1"
    api_key : str = "NO_API_KEY"
    context : list[dict[str, Any]] = []
    
    def __init__(
        self, 
        model: str = "qwen3.5", 
        base_url: str = "http://127.0.0.1:1234/v1",
        api_key: str = "NO_API_KEY",
        system_prompt: Optional[str] = None
    ) -> None:

        self.model = model
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

        self.context : list[dict[str, Any]] = []

        if system_prompt: 
            self.context.append({"role": "system", "content": system_prompt})

        
    def chat(self, user_message: str) -> str:
        self.context.append({"role": "user", "content": user_message})
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}", 
            "Content-Type": "application/json"
        }
        
        try:
            req = requests.post(
                url, 
                headers=headers, 
                json={"model":self.model, "messages": self.context}, 
                timeout=300
            )
            req.raise_for_status()
            
        except RequestException as e:
            self.context.pop() # Remove the last user message if the request failed
            return f"[red]Connection error to the server: {e}[/red]"

        data = req.json()
        choices = data.get("choices") 
        if not choices: 
            raise RuntimeError("Model response missing choices")
        
        message = choices[0].get("message")
        if message is None: 
            raise RuntimeError("Model response missing message")

        content = message.get("content") or ""
        self.context.append({"role": "assistant", "content": content})

        return content

def main():
    agent = LocalAgent(
        model="qwen3.5",
        system_prompt="You are a helpful assistant, concise and always respond in Italian."
    )

    console = Console()
    console.print("[bold green]Agent started! Write 'quit' or 'exit' to quit.[/bold green]\n")

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