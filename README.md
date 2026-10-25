# SlowCommit 🦥

**A local-first AI commit message generator for Git.**

SlowCommit reads your *staged Git diff* and asks a locally running Ollama model to suggest one concise Conventional Commit message. You review the suggestion and decide what to do next.

> Built for the Hacktoberfest 2026 Week 3 theme, “Slow and Steady.”

## Why?

Writing useful commit messages is small but repetitive work. SlowCommit automates the first draft while keeping the developer in control.

## How it works

1. You stage changes with Git.
2. SlowCommit reads only `git diff --cached`.
3. It applies best-effort redaction for several common token and secret patterns and limits the prompt size.
4. It sends the bounded diff to the local Ollama API.
5. You review the suggested message. SlowCommit never commits automatically.

## Requirements

- Windows, macOS, or Linux
- Python 3.10+
- Git
- [Ollama](https://ollama.com/) installed and running
- A model downloaded in Ollama (default: `llama3.2:1b`)

## Install on Windows (PowerShell)

Install Python and Git if needed. Install Ollama from [Ollama for Windows](https://ollama.com/download/windows), then open a PowerShell window.

Download the default model:

```powershell
ollama pull llama3.2:1b
```

From the project directory, create and activate a virtual environment and install SlowCommit:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install pytest
```

If PowerShell blocks virtual environment activation, use the environment's Python executable directly:

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

SlowCommit prints a suggested commit message. Review it, then copy and use it yourself if appropriate.

### Choose another installed Ollama model

For example, if you have `qwen2.5-coder:7b` installed:

```powershell
slowcommit --model qwen2.5-coder:7b
```

You can also specify a different Ollama model with the `--model` option, provided it is already available locally.

## Run tests

```powershell
python -m pytest -v
```

The tests do not require Ollama or a downloaded model.

## Privacy and limitations

- **Local processing by default:** The default endpoint is `http://127.0.0.1:11434`. The diff is sent to your local Ollama service, not to a SlowCommit-hosted server.
- **Endpoint configuration matters:** Do not configure a remote Ollama endpoint if you require local-only processing.
- **Best-effort secret redaction:** Secret detection is not guaranteed to catch every secret. Review staged changes before running SlowCommit, and never intentionally stage secrets.
- **Staged changes only:** SlowCommit reads staged Git changes, not your entire working directory.
- **Review every suggestion:** The model may misunderstand a diff or suggest an inaccurate commit message.
- **Local resource requirements:** Models require disk space and RAM. Inference speed depends on your hardware and the selected model.
- **No automatic commits:** SlowCommit does not run `git commit`, push changes, or modify your repository.

## Development

Run the tests, install the project in editable mode, and inspect the CLI options:

```powershell
python -m pytest
python -m pip install -e .
slowcommit --help
```

## Local demo

SlowCommit was tested locally with `qwen2.5-coder:7b` using a staged README change. It suggested:

```text
docs: add local demo section to README
```

The suggestion was reviewed before being committed manually.

## License

MIT. Models are distributed separately; review each model's own license and terms before use.
