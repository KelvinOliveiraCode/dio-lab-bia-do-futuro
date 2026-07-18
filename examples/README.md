# Examples

Esta pasta contém referências e exemplos adicionais para o desafio.

## Estrutura

- `README.md` - Este arquivo

## Recursos Externos

### Repositório de Exemplo do Instrutor
**Venilton Falvo Jr.** — Edu, Educador Financeiro Inteligente
- URL: https://github.com/falvojr/dio-lab-bia-do-futuro
- Tecnologias: React + TypeScript + IA Generativa
- Descrição: Implementação completa usada nas videoaulas do desafio

## Dicas de Implementação

### Streamlit (Python)
```bash
pip install streamlit pandas
streamlit run src/app.py
```

### Gradio (Python)
```python
import gradio as gr

def chat(message, history):
    # Sua logica do agente aqui
    return resposta

gr.ChatInterface(chat).launch()
```

### Integracao com LLM (Google Gemini)
```python
import google.generativeai as genai

genai.configure(api_key="SUA_CHAVE_API")
model = genai.GenerativeModel('gemini-pro')

response = model.generate_content(prompt)
print(response.text)
```

### Integracao com LLM (OpenAI)
```python
from openai import OpenAI

client = OpenAI(api_key="SUA_CHAVE_API")

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
)
print(response.choices[0].message.content)
```

### LangChain (Orquestracao)
```python
from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI

llm = OpenAI()
template = "Voce e um assistente financeiro... {input}"
prompt = PromptTemplate(template=template, input_variables=["input"])
chain = LLMChain(llm=llm, prompt=prompt)

result = chain.run("O que e CDI?")
```
