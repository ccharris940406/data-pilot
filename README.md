# Data Pilot — NL2SQL Chat Agent

Conversational agent that translates natural language questions into SQL, executes them, and responds in natural language.

## Setup

```bash
cp .env.example .env  # fill in your values
python -m app.main
```

## .env

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o
EMBEDDING_PROVIDER=openai
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
DB_TYPE=sqlite
DB_PATH=data/Chinook.sqlite
```

## Run

```bash
python -m app.main
```

## Test

```bash
python -m tests.test_connection
```

## Supported Databases

| Database   | Variable  |
|------------|-----------|
| SQLite     | `DB_PATH` |
| PostgreSQL | `DB_URI`  |
| MySQL      | `DB_URI`  |

## Supported LLM Providers

| Provider  | `LLM_PROVIDER` |
|-----------|----------------|
| OpenAI    | `openai`       |
| Anthropic | `anthropic`    |
| DeepSeek  | `deepseek`     |
