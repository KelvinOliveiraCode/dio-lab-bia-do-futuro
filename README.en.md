# BIA — Intelligent Banking Assistant

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Interface-red)
![License](https://img.shields.io/badge/License-Educational-lightgrey)

Virtual financial assistant that answers questions about a client's spending, investments, and goals using only real data from a local database, with four security layers against hallucinations.

## Problem / Why it exists

The client earns well but does not know where the money goes or what to do with the surplus. Financial information is full of jargon, and generic language models can invent products, rates, or returns that do not exist — an unacceptable risk when real money is at stake. BIA exists to answer only what is in the client's database, never promise future gains, and admit when it does not know.

## What it does

- Answers "How much did I spend on leisure?" and sums the outflows of the transactions.csv category (Jan to Jul 2026), showing total and monthly average.
- Answers "Where should I invest R$ 5,000?" and lists products from produtos_financeiros.json compatible with the client's risk profile (moderate, score 65), with risk, liquidity, and minimum value for each.
- Shows progress on the four goals in perfil_investidor.json (for example, emergency reserve, R$ 15,000 of R$ 25,000, 60% complete).
- Explains concepts such as CDI, FII, and income tax using the five educational contents in the base.
- Compares two products from the catalog side by side (risk, return, liquidity, minimum).
- Simulates CDB return (compound interest, regressive income tax of 17.5% over 12 months).
- Answers out-of-scope subjects (for example, Bitcoin, weather forecast) saying it does not have the information and suggesting alternatives from the base.
- Refuses requests for sensitive data (CPF, password, card) and redirects to the bank's official app.

Every investment content includes the disclaimer "not investment advice."

## Stack

- Python 3.9+
- Streamlit: chat interface
- pandas: reading and aggregation of CSV files
- JSON: customer profile, product catalog, educational contents
- No API key: src/app.py detects intents by keywords and answers with templates (LLM simulation, ready for integration with Gemini or OpenAI)

## How it works

Message processing steps

1. The user types the question in the Streamlit interface.
2. The code classifies intent by keywords (spending, product, planning, education, comparison, simulation, greeting).
3. Reads relevant data from data/ (CSV with pandas, JSON with the json library) and builds the answer with real customer data.
4. The answer passes through the four validation layers below before being displayed.

### Layer 1: System prompt (golden rules)

Never invent products, returns, rates, or data. Never promise future returns. Always cite the risk associated with any investment. Always include the educational disclaimer. Always offer human assistance for complex decisions.

### Layer 2: Pre-processing

Detects and blocks sensitive data in the user's message (CPF in the format 000.000.000-00, credit card numbers) before generating the answer and redirects to the bank's official app.

### Layer 3: Post-processing

Checks whether every product cited in the answer exists in the produtos_financeiros.json catalog. Products outside the base are replaced with a fallback message.

### Layer 4: Fallback

When confidence is low or the subject is not in the base (market forecast, tax advice, assets outside the catalog), answers "I do not have this information for certain at the moment" and suggests two or three alternatives from the base or a human specialist.

Note: the layers are specified as business rules in docs/03-prompts.md. The current src/app.py code is a simulation — it does not call a language model and does not run pre- and post-processing filters automatically.

## How to run

```bash
git clone https://github.com/KelvinOliveiraCode/dio-lab-bia-do-futuro.git
cd dio-lab-bia-do-futuro

python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install streamlit pandas
streamlit run src/app.py
```

The application is available at http://localhost:8501. There is no requirements.txt in the repository; install streamlit and pandas as above.

## Project structure

```
dio-lab-bia-do-futuro/
├── README.md
├── src/
│   └── app.py                    # Streamlit app: intents, data analysis, answers
├── data/
│   ├── transacoes.csv            # 89 transactions, Jan to Jul 2026
│   ├── perfil_investidor.json    # Customer profile, 4 goals, moderate risk (score 65)
│   ├── produtos_financeiros.json # 8 products + 5 educational contents
│   └── historico_atendimento.csv # 12 previous attendances
├── docs/
│   ├── 01-documentacao-agente.md
│   ├── 02-base-conhecimento.md
│   ├── 03-prompts.md             # System prompt and 4 security layers
│   ├── 04-metricas.md            # Evaluation framework
│   └── 05-pitch.md
├── assets/                       # empty
└── examples/
    └── README.md                 # Implementation references
```

## Trade-offs and decisions

- Simulated answers instead of a real LLM: no API key required, runs offline, and is deterministic. Trade-off: it does not generate natural language beyond the templates and does not understand phrases outside keyword patterns.
- Intent detection by keywords: fast, with no cost or API latency. Trade-off: fragile to paraphrasing; unknown intents go to the general fallback.
- Data loaded into memory at session start: no database or configuration. Trade-off: does not support multiple clients or long history; data is reloaded every session (st.cache_data).
- Fixed constants in the simulation (CDI at 12% per year, regressive income tax of 17.5%): predictable projections for demonstration. Trade-off: they do not reflect the real market.
- Single file src/app.py: easy to read and run. Trade-off: hard to maintain as the code grows.

## Known limitations

- No integration with a real language model (Gemini or OpenAI); answers come from templates.
- No requirements.txt with pinned dependencies.
- Data is from a single client, fixed period (Jan to Jul 2026).
- No authentication, multi-client service, or conversation persistence across restarts.
- No automated tests.
- No real-time market data; the simulation uses fixed rates.
- assets/ is empty: no images or diagrams.
- Pre-processing filters (CPF and card blocking) and post-processing (cited product verification) are documented in docs/03-prompts.md, but are not executed by the current src/app.py code.

## License

Educational use. Developed for the Lab "Build Your Virtual Assistant with Artificial Intelligence" from DIO.

## Author

Kelvin Oliveira — [LinkedIn](https://www.linkedin.com/in/kelvin-oliveira-0282033b4/) | [GitHub](https://github.com/KelvinOliveiraCode)
