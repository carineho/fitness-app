# ai-service

ai-service is a FastAPI service that generates workout plans using an LLM (Groq, accessed through Pydantic AI). It supports two modes: a weekly plan informed by the past week's logged activity (retrieved from data-sync), and an ad-hoc single-session plan generated directly from user-specified preferences. Generated weekly plans are persisted back to data-sync for later retrieval.

<br>

# Project Structure
- `app/main.py`: The FastAPI entry point. Defines the `/generate-session` and `/generate-plan` endpoints, and builds the prompt sent to each agent.
- `app/agent.py`: Defines the two Pydantic AI agents (`weekly_agent` and `adhoc_agent`), including their system prompts and the Groq model used.
- `app/schemas.py`: Defines the request and response schemas, including the structured output types enforced on the LLM's response.
- `test_llm.py`: A standalone manual script, run directly rather than through the test suite, used to verify that a Groq model call and structured output parsing succeed.

<br>

# Environment Variables
The following variables must be defined in a `.env` file in this directory:
- `GROQ_API_KEY`: The API key used to authenticate with Groq.
- `DATA_SYNC_URL`: The base URL of the data-sync service, queried for recent activity statistics and used to persist generated weekly plans.

<br>

# Virtual Environment
Creating the virtual environment:
- Change directory into the ai-service folder: `cd ai-service`
- Create a virtual environment: `python3 -m venv venv`

Activating the virtual environment:
- Activate the virtual environment:
    - `source venv/bin/activate` (macOS/Linux)
    - `venv\Scripts\activate` (Windows)
- Install dependencies (only required the first time, or after `requirements.txt` changes): `pip install -r requirements.txt`

<br>

# API Endpoints
| Method | Path | Description |
| ------ | ---- | ----------- |
| POST | `/generate-session` | Generates a single ad-hoc workout session from the requested difficulty, sport type, focus area, and duration. |
| POST | `/generate-plan` | Generates a full 7-day weekly plan informed by the past week's activity retrieved from data-sync, and persists the result. |

<br>

# Local Development
- Activate the virtual environment under the ai-service directory: `source venv/bin/activate`.
- Start the server: `uvicorn app.main:app --reload --port 8001`.
    - If the port is already in use, run `lsof -i :8001` to find the running process id, then `kill -9 <pid>` to terminate it.
- Test with curl:
```
curl -X POST http://127.0.0.1:8001/generate-session \
  -H "Content-Type: application/json" \
  -d '{"difficulty": "Moderate", "sport_type": "Strength", "focus_area": "core", "duration_minutes": 30}'
```
- Swagger UI is available at `http://localhost:8001/docs`.

<br>

# Known Issues
These were identified while documenting this service and are noted here (work in progress to resolve) .

1. **`WorkoutSession` is defined twice in `app/schemas.py`** (once without an `exercises` field, once with it). Because `WeeklyPlan` and `AdhocSession` are defined between the two class statements, they bind to the first definition, which has no `exercises` field. As a result, the `exercises` field that `WEEKLY_SYSTEM_PROMPT` in `app/agent.py` explicitly instructs the model to populate for Strength sessions is silently dropped from the enforced output schema and never actually reaches the API response.
2. **`build_weekly_prompt` in `app/main.py` does not forward `request.difficulty`, `request.focus_area`, or `request.remarks` into the prompt** sent to `weekly_agent` (those lines are present but commented out). As a result, the difficulty, focus area, and remarks selected when calling `/generate-plan` currently have no effect on the generated weekly plan, even though they are still saved alongside it when the plan is persisted. `build_adhoc_prompt`, used for `/generate-session`, is not affected by this and correctly includes all requested fields.

<br>

# R&D
|       | Groq | Together AI | Fireworks AI | OpenAI | Anthropic |
| ----- | ---- | ----------- | ------------ | ------ | --------- |
| Models | Open-weight only (Llama etc) | Open-weight, broadest catalog (Llama 4, DeepSeek, Qwen3, Mistral, GLM-5, Kimi K2, gpt-oss) | Open-weight, curated | Proprietary (GPT family) | Proprietary (Claude family) |
| Cheapest tier | Free tier available, low-cost paid | Free tier via some models, competitive paid | Competitive paid | GPT-4.1 nano: $0.10/$0.40 per million tokens | Claude Haiku 4.5: $1/$5 per million tokens |
| Flagship tier | N/A | N/A | N/A | GPT-5.5: $5 input / $30 output per million tokens | Claude Opus 4.7: $5 input / $25 output per million tokens |
| Caching discount | Not typically offered | Varies | Varies | 50% off cached input | 90% off cached input |
| Speed | Fastest, 700-800 tokens/sec on custom LPU chips | Standard, GPU-based | Standard, latency-optimized | Standard | Standard |
| Structured output support | Good, works with Pydantic AI | Good | Best-in-class, purpose-built for it | Strong, native JSON mode | Strong, native tool-use based |
| Ease of use with Pydantic AI | Easiest: native provider string, zero configuration | Moderate: requires an OpenAI-compatible wrapper | Moderate: requires a similar wrapper | Easy: native support | Easy: native support |
| Advantages | Fastest inference; generous free tier; simplest integration | Broadest catalog (100+ models); fine-tuning available; suitable for experimenting across model families | Most reliable structured output; production-grade JSON and function-calling | Cheapest budget tier by far; large model selection (64 models); mature ecosystem | Best caching economics; strong reasoning quality; an SDK that may already be familiar |
| Disadvantages | Narrow catalog; has deprecated models with short notice | More setup than Groq; tier-gated model access adds cost complexity | Smaller free tier; less beginner-friendly documentation | No meaningful free tier; pricier than necessary at the flagship end for this workload | No ultra-cheap tier; the cheapest model starts higher than OpenAI's nano tier |