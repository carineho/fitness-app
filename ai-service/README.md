# AI Service
This app generates workout plans (weekly and adhoc sessions) based on past progress.


# Local Development
- Activate the virtual environment under the ai-service directory `source venv/bin/activate`
- Start the server `uvicorn app.main:app --reload --port 8001`
    - If the server is already in use, run `lsof -i :8001` to find the port and then `kill -9 <pid>` to kill it
- Test curl: `curl -X POST http://127.0.0.1:8001/generate-session \
  -H "Content-Type: application/json" \
  -d '{"difficulty": "Moderate", "sport_type": "Strength", "focus_area": "core", "duration_minutes": 30}'`
- Swagger UI: `http://localhost:8001/docs`


# R&D
|       | Groq | Together AI | Fireworks AI | OpenAI | Anthropic |
| ----- | ---- | ----------- | ------------ | ------ | --------- |
| Models | Open-weight only (Llama etc) | Open-weight, broadest catalog (Llama 4, DeepSeek, Qwen3, Mistral, GLM-5, Kimi K2, gpt-oss) | Open-weight, curated | Proprietary (GPT family) | Proprietary (Claude family) |
| Cheapest tier | Free tier available, low-cost paid | Free tier via some models, competitive paid | Competitive paid | GPT-4.1 nano: $0.10/$0.40 per million tokens | Claude Haiku 4.5: $1/$5 per million tokens |
| Flagship tier | N/A | N/A | N/A | GPT-5.5: $5 input / $30 output per million tokens | Claude Opus 4.7: $5 input / $25 output per million tokens |
| Caching discount | Not typically offered | Varies	| Varies | 50% off cached input | 90% off cached input |
| Speed | Fastest — 700-800 tok/sec, custom LPU chips | Standard GPU-based | Standard, latency-optimized | Standard	| Standard |
| Structured output support | Good, works with Pydantic AI | Good | Best-in-class, purpose-built for it | Strong, native JSON mode | Strong, native tool-use based |
| Ease of use w/ Pydantic AI | Easiest — native provider string, zero config | Moderate — needs OpenAI-compatible wrapper | Moderate — similar wrapper needed | Easy — native support | Easy — native support |
| Advantages | Fastest inference; generous free tier; simplest integration | Broadest catalog (100+ models); fine-tuning available; good for experimenting across model families | Most reliable structured output; production-grade JSON/function-calling | Cheapest budget tier by far; huge model selection (64 models); mature ecosystem | Best caching economics; strong reasoning quality; SDK you're likely already familiar with |
| Disadvantages | Narrow catalog; has deprecated models with short notice | More setup than Groq; tier-gated model access adds cost complexity | Smaller free tier; less beginner-friendly docs | No meaningful free tier; pricier than needed at flagship end for your workload | No ultra-cheap tier — cheapest model starts higher than OpenAI's nano |