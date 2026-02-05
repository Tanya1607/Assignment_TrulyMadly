# AI Operations Assistant

A multi-agent AI system designed to handle natural language tasks by planning, executing tools, and verifying results.

## Features
- **Multi-Agent Architecture**: Planner, Executor, and Verifier agents work together to fulfill requests.
- **LLM Powered**: Uses Google Gemini 2.0 Flash's structured output capabilities for reliable agent reasoning.
- **Real-world Tooling**: Integrated with GitHub Search API and OpenWeatherMap API.
- **Interactive UI**: Built with Streamlit for a seamless user experience.

## Architecture
- **Planner Agent**: Uses the LLM to decompose the user's request into specific steps and tool calls.
- **Executor Agent**: Orchestrates real-time API calls to GitHub and OpenWeatherMap.
- **Verifier Agent**: Review execution outputs, ensures query fulfillment, and formats the final response.

## Prerequisites
- Python 3.9+
- Gemini API Key (Verified free tier available)
- OpenWeatherMap API Key
- GitHub Personal Access Token (Recommended)

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-link>
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: This project uses the new `google-genai` SDK.*

3. **Configure Environment Variables**:
   Copy `.env.example` to `.env` and fill in your API keys.
   ```bash
   cp .env.example .env
   ```
   Specific variables:
   - `GEMINI_API_KEY`: Required. Must start with `AIza` (Get it from [Google AI Studio](https://aistudio.google.com/app/apikey)).
   - `OPENWEATHER_API_KEY`: Required for weather data.
   - `GITHUB_TOKEN`: Recommended for searching repositories.
   - `MODEL_NAME`: Default is `gemini-2.0-flash` (Stable).

## Running the Project
1. **Ensure your API keys are correct** (especially Gemini).
2. **Run the Streamlit app**:
   ```bash
   streamlit run main.py
   ```

The application will open in your browser at `http://localhost:8501`. Logs will appear in your terminal to show agent progress.

## Example Prompts
- "Find the most starred machine learning repositories on GitHub."
- "What's the weather like in New York right now?"
- "Search for top automation tools on GitHub and tell me the weather in San Francisco."

## Known Limitations / Tradeoffs
- **Sequential Execution**: Current implementation executes steps sequentially. Parallel execution could be implemented for faster performance.
- **Tool Scope**: Only includes GitHub and Weather tools. The architecture is easily extensible for more tools.
- **Dependency on OpenAI**: Replaces complex prompt engineering with OpenAI's `parse` method for structured outputs, which requires a compatible model.
- **Error Handling**: Basic retry logic exists, but complex API failures might require manual intervention.
