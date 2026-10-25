# SlowCommit 🦥

**A local-first AI commit message generator for Git.** SlowCommit reads your *staged diff* and asks a locally running Ollama model to suggest one concise Conventional Commit message. You review it and decide what to do next.

> Built for the Hacktoberfest 2026 Week 3 theme, “Slow and Steady.”

## Why?

Writing useful commit messages is small but repetitive work. SlowCommit automates the first draft while keeping the developer in control.

## How it works

1. You stage changes with Git.
2. SlowCommit reads only `git diff --cached`.
3. It applies best-effort redaction for several common token/secret patterns and limits the prompt size.
4. It sends the bounded diff to the local Ollama API.
5. You review the suggested message. SlowCommit never commits automatically.

## Requirements

- Windows, macOS, or Linux
- Python 3.10+
- Git
- [Ollama](https://ollama.com/) installed and running
- A model downloaded in Ollama (default: `llama3.2:1b`)

## Install on Windows (PowerShell)

Install Python and Git if needed. Install Ollama from https://ollama.com/download/windows, then open a new PowerShell window.

```powershell
ollama pull llama3.2:1b
```

From the project directory:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install pytest
```

If PowerShell blocks activation, use the venv Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pip install pytest
```

## Use it

Inside any Git repository with staged changes:

```powershell
git add path\to\file.py
slowcommit
```

Choose another installed Ollama model:

```powershell
slowcommit --model llama3.2:1b
```

## Run tests

```powershell
python -m pytest
```

The tests do not require Ollama or a downloaded model.

## Privacy and limitations

- The default endpoint is `http://127.0.0.1:11434`; the diff is sent to the local Ollama service, not to a SlowCommit-hosted server.
- Do not configure a remote Ollama endpoint if you require local-only processing.
- Secret detection is best-effort, not a guarantee. Review staged changes before running the tool and never stage secrets.
- Only staged changes are read. The model can misunderstand a diff or suggest an inaccurate message; review every suggestion.
- Local models need disk space and RAM, and inference speed depends on your machine.
- SlowCommit does not run `git commit`, push changes, or change your repository.

## Development

```powershell
python -m pytest
python -m pip install -e .
slowcommit --help
```

## License

MIT. The model is distributed separately; review its own license and terms before use.

## Local demo
Testing staged changes with the local AI model.
