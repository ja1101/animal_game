# Copilot Instructions

## Project Overview

A small command-line "guess the animal" game in Python (requires >= 3.14). The user asks yes/no questions about a randomly chosen animal; an LLM answers the questions.

## Setup and Running

- Managed with **uv** (`pyproject.toml` + `uv.lock`). Sync dependencies with `uv sync`; run the game with `uv run animal_guess.py`.
- The game requires the `OPENROUTER_API_KEY` environment variable to be set, otherwise `glm.py` raises `KeyError` on the first question.
- There are no tests, linters, or build steps configured.

## Architecture

Three modules, single flow:

- `animal_guess.py` — entry point and game loop. Picks an animal, reads user questions, and exits when the question contains the animal name ("Correct!") or the phrase "give up".
- `animal.py` — animal selection. Fetches a JSON animal list from GitHub (dariusk/corpora) with a module-level cache (`_cached_animals`); falls back to a hardcoded list on network failure. `get_random_animal()` always returns lowercase.
- `glm.py` — LLM client. `call_gpt(prompt)` POSTs to OpenRouter's chat completions API (model `z-ai/glm-5.3-flash`, reasoning enabled) and returns the raw `message` dict (access `.["content"]` for the text), not a parsed string. Also accepts `call_gpt(prompt, messages)` to send a full multi-turn message list.

## Two-agent mode

- `agents.py` — the two agents. `GuesserAgent` asks yes/no questions (or makes a final guess) using `Q:`/`GUESS:` reply prefixes and keeps its own conversation history; `AnswererAgent` knows the secret animal and answers Yes/No only.
- `agent_game.py` — referee loop that relays messages between the two agents and prints the transcript for the human monitor. Run with `uv run agent_game.py`; optional flags: `--max-questions N` (default 20), `--animal NAME` to force the secret animal.

## Conventions

- Despite the name `call_gpt`/`glm.py`, all LLM calls go through **OpenRouter**, not OpenAI or Zhipu directly.
- Prompts must explicitly instruct the model to answer "yes or no only" — the game relies on this instruction rather than parsing.
- `.gitignore` intentionally excludes `pyproject.toml` and `uv.lock`, so dependency changes may not be tracked by git — be careful when modifying dependencies.
