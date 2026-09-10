# dio-lab-bia-do-futuro — BIA, Banco Inteligente Assistente

![Status](https://img.shields.io/badge/Status-Concludido-2EA44F?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![LangChain-Ready](https://img.shields.io/badge/LangChain-Ready-1C3C44?style=flat-square)
![DIO](https://img.shields.io/badge/DIO-Lab-9046F5?style=flat-square)

**BIA — Banco Inteligente Assistente** é um agente financeiro conversacional construído no Lab "Construa Seu Assistente Virtual Com Inteligência Artificial" da DIO ("Agente Financeiro Inteligente com IA Generativa"). A stack é Python 3.9+, Streamlit, pandas e JSON/CSV, com o módulo de linguagem isolado por trás de uma interface de LLM simulado — pronto para plugar Gemini/OpenAI via LangChain sem tocar na lógica de negócio. O diferencial técnico do projeto não é o chat em si, mas as quatro camadas anti-alucinação que cercam o agente: system prompt com regras de ouro, pré-processamento que bloqueia dados sensíveis, pós-processamento que valida todo produto citado contra a base real e fallback honesto de baixa confiança. Em um domínio regulado como finanças, isso é o que separa um demo de um sistema honesto.

---

## 🇧🇷 Português

### O que é

BIA é um assistente financeiro conversacional que opera sobre dados reais (mockados) de uma cliente: perfil, transações, metas, histórico de atendimentos e catálogo de produtos. Ele contextualiza cada resposta com esses dados, recomenda produtos compatíveis com o perfil de risco, acompanha metas com projeções e educa em conceitos financeiros — sem nunca prometer rentabilidade, sem inventar produtos ou taxas, sempre com disclaimer e sempre oferecendo encaminhamento humano.

### Base de conhecimento

| Arquivo | Conteúdo |
|---|---|
| `data/perfil_investidor.json` | Perfil Ana Carolina Mendes: 29 anos, dev, R$ 8.500/mês + ~R$ 1.000 freelances, risco moderado (score 65), São Paulo |
| `data/transacoes.csv` | 89 transações Jan–Jul/2026 |
| `data/produtos_financeiros.json` | 8 produtos financeiros + 5 conteúdos educacionais |
| `data/historico_atendimento.csv` | 12 atendimentos anteriores |

Metas financeiras da cliente: reserva de emergência R$ 25 mil (60% concluída), entrada de apartamento R$ 80 mil (27,5%, prazo 48 meses), aposentadoria R$ 500 mil (1,7%), viagem R$ 15 mil (20%).

### Quatro camadas anti-alucinação

1. **System prompt com regras de ouro** — contextualiza com dados reais, nunca promete rentabilidade, sempre exibe disclaimer, oferece atendimento humano, nunca inventa produtos ou taxas.
2. **Pré-processamento** — bloqueia entradas com dados sensíveis (CPF, senha, cartão) antes de chegarem ao modelo.
3. **Pós-processamento** — valida todo produto citado na resposta contra a base `produtos_financeiros.json`; produto fora da base não é entregue.
4. **Fallback honesto** — em baixa confiança, BIA admite "não sei" em vez de especular.

### Arquitetura em 6 passos

O desenvolvimento seguiu 6 passos documentados, cada um com seu material em `docs/`:

| Passo | Documento | Entrega |
|---|---|---|
| 1 | `docs/01-documentacao-agente.md` | Documentação do agente |
| 2 | `docs/02-base-conhecimento.md` | Base de conhecimento |
| 3 | `docs/03-prompts.md` | Prompts |
| 4 | `src/app.py` | Aplicação funcional |
| 5 | `docs/04-metricas.md` | Métricas de avaliação |
| 6 | `docs/05-pitch.md` | Pitch de 3 minutos |

```
Usuario (Chat Streamlit)
    |
    v
[ Pre-processamento ] --> bloqueio de dados sensiveis
    |
    v
[ LLM (simulado, pronto p/ Gemini/OpenAI + LangChain) ]
    |
    v
[ Pos-processamento ] --> validacao de produtos contra a base
    |
    v
[ Resposta contextualizada / Fallback ]
    |
Base: transacoes.csv + perfil_investidor.json + produtos_financeiros.json + historico_atendimento.csv
```

### Avaliação: 6/6 cenários aprovados

| Cenário | Resultado |
|---|---|
| Educação | Explicou CDI corretamente |
| Produto | Recomendou 3 produtos compatíveis com o perfil |
| Planejamento | Calculou progresso 27,5% da meta + projeção |
| Alucinação | Pergunta sobre Bitcoin caiu no fallback seguro |
| Segurança | CPF digitado foi bloqueado no pré-processamento |
| Off-topic | Previsão do tempo foi redirecionada |

### Como rodar

```bash
# Python 3.9+
pip install streamlit pandas
streamlit run src/app.py
# abre em http://localhost:8501
```

---

## 🇺🇸 English

### What it is

BIA (Banco Inteligente Assistente) is a conversational financial agent running on a mock client dataset: profile, transactions, goals, service history, and a product catalog. It grounds every answer in that data, recommends products matching the client's risk profile, tracks goals with projections, and teaches financial concepts — while never promising returns, never inventing products or rates, always showing a disclaimer, and always offering human handoff.

### Knowledge base

| File | Contents |
|---|---|
| `data/perfil_investidor.json` | Client profile: Ana Carolina Mendes, 29, developer, BRL 8,500/month + ~BRL 1,000 freelance income, moderate risk (score 65), São Paulo |
| `data/transacoes.csv` | 89 transactions, Jan–Jul/2026 |
| `data/produtos_financeiros.json` | 8 financial products + 5 educational pieces |
| `data/historico_atendimento.csv` | 12 previous service interactions |

Client goals: emergency fund BRL 25k (60% done), apartment down payment BRL 80k (27.5%, 48 months), retirement BRL 500k (1.7%), travel BRL 15k (20%).

### Four anti-hallucination layers

1. **System prompt with golden rules** — ground answers in real data, never promise returns, always show a disclaimer, offer human handoff, never invent products or rates.
2. **Pre-processing** — blocks sensitive data (national ID, password, card numbers) before it reaches the model.
3. **Post-processing** — validates every product mentioned in the response against `produtos_financeiros.json`; anything outside the catalog is not delivered.
4. **Honest fallback** — under low confidence, BIA says "I don't know" instead of speculating.

### Six documented steps

Development followed six documented steps, each with its own material under `docs/`:

| Step | Document | Deliverable |
|---|---|---|
| 1 | `docs/01-documentacao-agente.md` | Agent documentation |
| 2 | `docs/02-base-conhecimento.md` | Knowledge base |
| 3 | `docs/03-prompts.md` | Prompts |
| 4 | `src/app.py` | Working application |
| 5 | `docs/04-metricas.md` | Evaluation metrics |
| 6 | `docs/05-pitch.md` | 3-minute pitch |

### Evaluation: 6/6 scenarios passed

| Scenario | Result |
|---|---|
| Education | Explained CDI correctly |
| Product | Recommended 3 profile-matched products |
| Planning | Computed 27.5% goal progress + projection |
| Hallucination | Bitcoin question hit the safe fallback |
| Security | Typed CPF was blocked in pre-processing |
| Off-topic | Weather question was redirected |

### Running locally

```bash
# Python 3.9+
pip install streamlit pandas
streamlit run src/app.py
# opens at http://localhost:8501
```

---

## Autor

**Kelvin Oliveira** — [GitHub](https://github.com/KelvinOliveiraCode) · [LinkedIn](https://www.linkedin.com/in/kelvin-oliveira-0282033b4/)

## Licença

Projeto educacional, desenvolvido para o Lab da DIO. Sem licença de software formal — os materiais servem como referência de estudo.
