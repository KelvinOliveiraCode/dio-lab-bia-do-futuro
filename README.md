# 🤖 BIA — Banco Inteligente Assistente

> **Agente Financeiro Inteligente com IA Generativa**  
> Projeto desenvolvido para o Lab "Construa Seu Assistente Virtual Com Inteligência Artificial" da [DIO](https://www.dio.me/)

---

## 👨‍💻 Autor

**Kelvin Oliveira**  
[LinkedIn](https://www.linkedin.com/in/kelvin-oliveira-0282033b4/) | [GitHub](https://github.com/KelvinOliveiraCode)

---

## 🎯 Sobre o Projeto

**BIA** é um assistente virtual financeiro que utiliza IA generativa para educar e orientar jovens profissionais na jornada de organização financeira e investimentos. Diferente de chatbots tradicionais reativos, BIA é **proativa, personalizada e segura** — antecipando necessidades com base nos dados reais do cliente.

### O que BIA faz:
- 💰 **Analisa gastos** com base no histórico de transações
- 📈 **Recomenda investimentos** alinhados ao perfil de risco
- 🎯 **Acompanha metas** financeiras com projeções
- 📚 **Educa** sobre conceitos financeiros de forma simples
- 🔒 **Garante segurança** — nunca inventa produtos ou dados

---

## 🏗️ Arquitetura

```
Usuario (Chat/App)
    |
    v
[ Streamlit Interface ]  <--->  [ Python Orquestrador ]
    |                                    |
    |                            [ Analise de Dados ]
    |                                    |
    +----------------------------+-------+-------+
                                 |               |
                         [ Base de Conhecimento ]  [ LLM (Simulado) ]
                         - transacoes.csv         - Respostas
                         - perfil_investidor.json   contextualizadas
                         - produtos_financeiros.json
                         - historico_atendimento.csv
```

---

## 📁 Estrutura do Repositório

```
dio-lab-bia-do-futuro/
|
├── README.md                          # Este arquivo
|
├── data/                              # Dados mockados do cliente
│   ├── transacoes.csv                  # 89 transacoes (Jan-Jul/2026)
│   ├── perfil_investidor.json          # Perfil completo: Ana Carolina Mendes
│   ├── produtos_financeiros.json      # 8 produtos + 5 conteudos educacionais
│   └── historico_atendimento.csv      # 12 atendimentos anteriores
|
├── docs/                              # Documentacao do projeto (6 passos)
│   ├── 01-documentacao-agente.md       # Caso de uso, persona, arquitetura, seguranca
│   ├── 02-base-conhecimento.md       # Estrategia e estrutura de dados
│   ├── 03-prompts.md                 # System prompt, exemplos e edge cases
│   ├── 04-metricas.md                # Framework de avaliacao e testes
│   └── 05-pitch.md                   # Roteiro do pitch de 3 minutos
|
├── src/                               # Codigo da aplicacao
│   ├── app.py                         # Aplicacao Streamlit funcional
│   └── requirements.txt               # Dependencias Python
|
├── assets/                            # Imagens e diagramas (vazio)
│
└── examples/                          # Referencias e exemplos
    └── README.md                      # Dicas de implementacao
```

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.9+
- pip

### Instalação

```bash
# Clone o repositorio
git clone https://github.com/KelvinOliveiraCode/dio-lab-bia-do-futuro.git
cd dio-lab-bia-do-futuro

# Crie um ambiente virtual (opcional, mas recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate   # Windows

# Instale as dependencias
pip install -r src/requirements.txt
```

### Executar a aplicação

```bash
streamlit run src/app.py
```

A aplicação estará disponível em `http://localhost:8501`

---

## 📊 Dados do Cliente (Mock)

### Perfil: Ana Carolina Mendes
- **Idade:** 29 anos
- **Profissão:** Desenvolvedora de Software
- **Renda:** R$ 8.500/mês + ~R$ 1.000 em freelances
- **Perfil de Risco:** Moderado (Score: 65)
- **Cidade:** São Paulo

### Objetivos Financeiros

| Objetivo | Meta | Atual | Prazo | Progresso |
|----------|------|-------|-------|-----------|
| Reserva de Emergência | R$ 25.000 | R$ 15.000 | 12 meses | 60% |
| Entrada Apartamento | R$ 80.000 | R$ 22.000 | 48 meses | 27,5% |
| Aposentadoria | R$ 500.000 | R$ 8.500 | 360 meses | 1,7% |
| Viagem Europa | R$ 15.000 | R$ 3.000 | 18 meses | 20% |

---

## 🛡️ Segurança e Anti-Alucinação

BIA implementa **4 camadas de segurança**:

1. **System Prompt** com regras de ouro (nunca inventar produtos, sempre citar riscos)
2. **Pre-processing** que bloqueia dados sensíveis (CPF, senha, cartão)
3. **Post-processing** que valida se produtos citados existem na base
4. **Fallback** para "não sei" quando a confiança é baixa

### Regras de Ouro
- ✅ Sempre contextualiza com dados reais do cliente
- ✅ Nunca promete rentabilidade futura
- ✅ Sempre inclui disclaimer de investimento
- ✅ Oferece falar com humano para decisões complexas
- ❌ Nunca inventa produtos, taxas ou dados

---

## 📋 Os 6 Passos do Desafio

| Passo | Documento | Status |
|-------|-----------|--------|
| 1. Documentação do Agente | `docs/01-documentacao-agente.md` | ✅ Completo |
| 2. Base de Conhecimento | `docs/02-base-conhecimento.md` | ✅ Completo |
| 3. Prompts do Agente | `docs/03-prompts.md` | ✅ Completo |
| 4. Aplicação Funcional | `src/app.py` | ✅ Completo |
| 5. Avaliação e Métricas | `docs/04-metricas.md` | ✅ Completo |
| 6. Pitch | `docs/05-pitch.md` | ✅ Completo |

---

## 🧪 Testes Realizados

| Cenário | Resultado |
|---------|-----------|
| Educação ("O que é CDI?") | ✅ Explicou com analogia e dados do cliente |
| Produto ("Recomende investimento") | ✅ Sugeriu 3 produtos adequados ao perfil |
| Planejamento ("Estou perto da meta?") | ✅ Mostrou progresso 27,5% + projeção |
| Alucinação ("O que acha de Bitcoin?") | ✅ Fallback seguro + alternativas |
| Segurança ("Meu CPF é...") | ✅ Bloqueou e redirecionou |
| Off-topic ("Previsão do tempo?") | ✅ Resposta educada e direcionada |

**Resultado:** 6/6 cenários aprovados

---

## 🛠️ Tecnologias Utilizadas

| Categoria | Ferramenta |
|-----------|------------|
| Interface | Streamlit |
| Linguagem | Python 3.9+ |
| Dados | Pandas, JSON, CSV |
| LLM | Simulado (pronto para integração com Gemini/OpenAI) |
| Orquestração | Python nativo (pronto para LangChain) |

---

## 📈 Próximos Passos

- [ ] Integrar com API do Google Gemini ou OpenAI para respostas mais naturais
- [ ] Adicionar gráficos de evolução de metas (Plotly/Matplotlib)
- [ ] Implementar memória de conversa entre sessões
- [ ] Adicionar alertas proativos ("Você gastou 30% a mais em lazer")
- [ ] Criar testes automatizados com pytest
- [ ] Deploy no Streamlit Cloud

---

## 📬 Contato

**Kelvin Oliveira**  
🔗 [LinkedIn](https://www.linkedin.com/in/kelvin-oliveira-0282033b4/)  
💻 [GitHub](https://github.com/KelvinOliveiraCode)

---

## 📄 Licença

Este projeto é de uso educacional, desenvolvido para fins de aprendizado no bootcamp da DIO.

---

> *"BIA não é só um chatbot. É o primeiro passo para uma relação bancária verdadeiramente inteligente e personalizada."* 🚀
