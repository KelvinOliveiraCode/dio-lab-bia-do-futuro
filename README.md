<<<<<<< HEAD
# BIA — Banco Inteligente Assistente

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Interface-red)
![Licenca](https://img.shields.io/badge/Licenca-Educacional-lightgrey)

Assistente financeiro virtual que responde sobre gastos, investimentos e metas de um cliente usando apenas dados reais de uma base local, com quatro camadas de seguranca contra alucinacoes.

## Problema / Por que existe

O cliente ganha bem, mas nao sabe para onde o dinheiro vai nem o que fazer com a sobra. A informacao financeira esta cheia de jargoes, e modelos de linguagem genericos podem inventar produtos, taxas ou rentabilidades que nao existem — um risco inaceitavel quando o assunto eh dinheiro de verdade. BIA existe para responder apenas o que esta na base de dados do cliente, nunca prometer ganhos futuros e admitir quando nao sabe.

## O que faz

- Responde "Quanto gastei em lazer?" e soma as saidas da categoria de transacoes.csv (jan a jul de 2026), mostrando total e media mensal.
- Responde "Onde investir R$ 5.000?" e lista produtos de produtos_financeiros.json compatíveis com o perfil de risco do cliente (moderado, score 65), com risco, liquidez e valor minimo de cada um.
- Mostra o progresso das quatro metas de perfil_investidor.json (por exemplo: reserva de emergencia, R$ 15.000 de R$ 25.000, 60% concluido).
- Explica conceitos como CDI, FII e imposto de renda com os cinco conteudos educacionais da base.
- Compara dois produtos do catalogo lado a lado (risco, rentabilidade, liquidez, minimo).
- Simula rendimento de CDB (juros compostos, IR regressivo de 17,5% em 12 meses).
- Responde a assuntos fora de escopo (ex.: Bitcoin, previsao do tempo) dizendo que nao tem a informacao e sugerindo alternativas da base.
- Recusa pedidos de dados sensiveis (CPF, senha, cartao) e redireciona para o app oficial do banco.

Todo conteudo de investimento inclui o disclaimer: nao eh recomendacao de investimento.

## Stack

- Python 3.9+
- Streamlit: interface de chat
- pandas: leitura e agregacao de arquivos CSV
- JSON: perfil do cliente, catalogo de produtos, conteudos educacionais
- Nenhuma chave de API: src/app.py detecta intencoes por palavras-chave e responde com templates (simulacao de LLM, pronto para integracao com Gemini ou OpenAI)

## Como funciona

Fluxo de uma mensagem:

1. O usuario digita a pergunta na interface do Streamlit.
2. O codigo classifica a intencao por palavras-chave (gastos, produto, planejamento, educacao, comparacao, simulacao, saudacao).
3. Le os dados relevantes de data/ (CSV com pandas, JSON com a biblioteca json) e monta a resposta com dados reais do cliente.
4. A resposta passa pelas quatro camadas de validacao abaixo antes de ser exibida.

### Camada 1: System prompt (regras de ouro)

Nunca inventar produtos, rentabilidades, taxas ou dados. Nunca prometer rentabilidade futura. Sempre citar o risco associado a qualquer investimento. Sempre incluir o disclaimer educacional. Sempre oferecer atendimento humano para decisoes complexas.

### Camada 2: Pre-processamento

Detecta e bloqueia dados sensiveis na mensagem do usuario (CPF no formato 000.000.000-00, numeros de cartao de credito) antes de gerar a resposta e redireciona para o app oficial do banco.

### Camada 3: Post-processamento

Verifica se todos os produtos citados na resposta existem no catalogo produtos_financeiros.json. Produtos fora da base sao substituidos por mensagem de fallback.

### Camada 4: Fallback

Quando a confianca eh baixa ou o assunto nao esta na base (previsao de mercado, conselho fiscal, ativos fora do catalogo), responde "nao tenho essa informacao com certeza no momento" e sugere duas a tres alternativas da base ou um especialista humano.

Observacao: as camadas estao especificadas como regras de negocio em docs/03-prompts.md. O codigo atual de src/app.py eh uma simulacao — nao chama um modelo de linguagem e nao executa os filtros de pre e pos-processamento automaticamente.

## Como rodar

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

A aplicacao fica disponível em http://localhost:8501. Nao existe requirements.txt no repositorio; instale streamlit e pandas conforme acima.

## Estrutura do projeto

```
dio-lab-bia-do-futuro/
├── README.md
├── src/
│   └── app.py                    # Aplicacao Streamlit: intencoes, analise de dados, respostas
├── data/
│   ├── transacoes.csv            # 89 transacoes, jan a jul de 2026
│   ├── perfil_investidor.json    # Perfil do cliente, 4 metas, risco moderado (score 65)
│   ├── produtos_financeiros.json # 8 produtos + 5 conteudos educacionais
│   └── historico_atendimento.csv # 12 atendimentos anteriores
├── docs/
│   ├── 01-documentacao-agente.md
│   ├── 02-base-conhecimento.md
│   ├── 03-prompts.md             # System prompt e 4 camadas de seguranca
│   ├── 04-metricas.md            # Framework de avaliacao
│   └── 05-pitch.md
├── assets/                       # vazio
└── examples/
    └── README.md                 # Referencias de implementacao
```

## Trade-offs e decisoes

- Respostas simuladas em vez de LLM real: nao exige chave de API, roda offline e eh deterministico. Troca: nao gera linguagem natural alem dos templates e nao entende frases fora dos padroes de palavras-chave.
- Detecao de intencao por palavras-chave: rapida, sem custo nem latencia de API. Troca: fragil a parafraseamento; intencoes desconhecidas vao para o fallback geral.
- Dados carregados em memoria no inicio da sessao: sem banco de dados nem configuracao. Troca: nao suporta varios clientes nem historico longo; os dados sao recarregados a cada sessao (st.cache_data).
- Constantes fixas na simulacao (CDI a 12% ao ano, IR regressivo de 17,5%): projecoes previsiveis para demonstracao. Troca: nao refletem o mercado real.
- Arquivo unico src/app.py: facil de ler e rodar. Troca: dificil de manter à medida que o codigo cresce.

## Limitações conhecidas

- Nao ha integracao com modelo de linguagem real (Gemini ou OpenAI); as respostas vem de templates.
- Nao ha requirements.txt com dependencias travadas.
- Os dados sao de um unico cliente, periodo fixo (jan a jul de 2026).
- Nao ha autenticacao, atendimento a varios clientes nem persistencia de conversa entre reinicializacoes.
- Nao ha testes automatizados.
- Sem dados de mercado em tempo real; a simulacao usa taxas fixas.
- assets/ esta vazio: sem imagens ou diagramas.
- Os filtros de pre-processamento (bloqueio de CPF e cartao) e pos-processamento (verificacao de produtos citados) estao documentados em docs/03-prompts.md, mas nao sao executados pelo codigo atual de src/app.py.

## Licenca

Uso educacional. Desenvolvido para o Lab "Construa Seu Assistente Virtual Com Inteligencia Artificial" da DIO.

## Autor

Kelvin Oliveira — [LinkedIn](https://www.linkedin.com/in/kelvin-oliveira-0282033b4/) | [GitHub](https://github.com/KelvinOliveiraCode)
=======
# BIA do Futuro — Agente Bancário com IA Generativa

![linguagem: Python](https://img.shields.io/badge/linguagem-Python-blue)  
![status: concluido](https://img.shields.io/badge/status-concluido-green)  
![licenca: MIT](https://img.shields.io/badge/licenca-MIT-blue)

### Descrição
BIA — Agente financeiro bancário com IA generativa, anti-alucinação em 4 camadas.

### O que faz
BIA — Agente financeiro bancário com IA generativa, anti-alucinação em 4 camadas.

### Tecnologias
- Python 3.9+
- IA Generativa

### Como usar
1. Instale as dependências: `pip install -r requirements.txt` (se o arquivo existir no repositório).
2. Execute os testes: `python -m pytest`.
Verifique os arquivos reais do repositório para os comandos exatos.

### Estrutura
Consulte a árvore do repositório para a organização exata de pastas e arquivos.

### Testes
Não há contagem de testes registrada nesta metadata. Adicione e execute testes apropriados à linguagem (pytest para Python, ./mvnw test para Java, npm test para JavaScript/TypeScript).

### Licença
MIT

### Autor
Kelvin Oliveira — github.com/KelvinOliveiraCode

---

# BIA of the Future — Generative AI Banking Agent

![language: Python](https://img.shields.io/badge/language-Python-blue)  
![status: concluido](https://img.shields.io/badge/status-concluido-green)  
![license: MIT](https://img.shields.io/badge/license-MIT-blue)

### Description
BIA — Banking AI agent with generative AI, 4-layer anti-hallucination.

### What it does
BIA — Banking AI agent with generative AI, 4-layer anti-hallucination.

### Technologies
- Python 3.9+
- IA Generativa

### How to use
1. Install dependencies: `pip install -r requirements.txt` (if the file exists in the repository).
2. Run tests: `python -m pytest`.
Check the actual repository files for exact commands.

### Structure
Check the repository tree for the exact folder and file organization.

### Tests
No test count recorded in this metadata. Add and run tests appropriate for the language (pytest for Python, ./mvnw test for Java, npm test for JavaScript/TypeScript).

### License
MIT

### Author
Kelvin Oliveira — github.com/KelvinOliveiraCode
>>>>>>> 9112038a18716b63bb29a559e774d6721d7e92a7
