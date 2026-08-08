# 🤖 Multi-Agent Content Pipeline

A **CrewAI-powered** multi-agent pipeline where 4 specialized AI agents collaborate to research, plan, write, and review content on any topic — all from a beautiful Streamlit web interface.

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_UI-red?logo=streamlit)
![CrewAI](https://img.shields.io/badge/CrewAI-Multi_Agent-purple)
![Groq](https://img.shields.io/badge/Groq-LLM_API-green)

## ✨ Features

- **4 Specialized AI Agents** working in sequence:
  - 🔍 **Researcher** — Searches the web for facts, statistics, and references
  - 📋 **Planner** — Organizes research into a structured narrative outline
  - ✍️ **Writer** — Crafts an engaging, polished article with embedded images
  - 🔎 **Reviewer** — Edits and polishes the final draft for production quality

- **Custom Tools**:
  - `WebSearchTool` — Real-time DuckDuckGo web search
  - `WebsiteScraperTool` — Scrapes and summarizes website content
  - `ImageSearchTool` — Finds and embeds real images via DuckDuckGo Image Search

- **Streamlit Web UI** with:
  - Customizable agent roles and backstories via sidebar
  - Download reports as **Markdown (.md)** or **PDF (.pdf)**
  - Real-time status updates during generation

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/multi-agent-content-pipeline.git
cd multi-agent-content-pipeline
```

### 2. Create a `.env` file
```bash
GROQ_API_KEY=your_groq_api_key_here
```
> Get a free API key at [console.groq.com](https://console.groq.com)

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

## 📁 Project Structure

```
├── app.py              # Streamlit web interface
├── main.py             # CrewAI pipeline orchestrator
├── agents.py           # Agent definitions (Researcher, Planner, Writer, Reviewer)
├── tasks.py            # Task definitions for each agent
├── tools.py            # Custom tools (WebSearch, ImageSearch, WebsiteScraper)
├── requirements.txt    # Python dependencies
├── .env_example        # Example environment file
└── .gitignore          # Git ignore rules
```

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| AI Framework | [CrewAI](https://www.crewai.com/) |
| LLM Provider | [Groq](https://groq.com/) (Llama 3.3 70B) |
| Web UI | [Streamlit](https://streamlit.io/) |
| Web Search | [DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/) |
| PDF Export | [fpdf2](https://py-pdf.github.io/fpdf2/) |

## 📝 License

MIT License — feel free to use, modify, and share!

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
