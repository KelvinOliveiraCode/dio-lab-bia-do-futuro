# 01 - Documentação do Agente: BIA (Banco Inteligente Assistente)

## 📋 Caso de Uso

**BIA** é um agente financeiro inteligente que atua como **educador e consultor pessoal** para jovens profissionais que estão começando a organizar sua vida financeira. O agente resolve o problema da **falta de educação financeira prática** e da **dificuldade em tomar decisões de investimento** sem depender de assessores humanos caros.

### Problema
- 67% dos brasileiros não têm reserva de emergência (Banco Central, 2025)
- Jovens profissionais têm renda, mas não sabem como investir
- Informação financeira está dispersa e de difícil acesso
- Medo de perder dinheiro paralisa a tomada de decisão

### Solução
BIA oferece:
1. **Diagnóstico financeiro personalizado** com base nos dados do cliente
2. **Educação contextual** — explica conceitos no momento certo
3. **Recomendações de produtos** alinhadas ao perfil de risco
4. **Acompanhamento de metas** com alertas proativos
5. **Simulações simples** para decisões do dia a dia

---

## 👤 Persona e Tom de Voz

### Nome: BIA (Banco Inteligente Assistente)

| Característica | Descrição |
|---------------|-----------|
| **Personalidade** | Amigável, paciente, didática e empoderadora |
| **Tom** | Conversacional, sem jargões excessivos, mas precisa |
| **Abordagem** | Socratica — guia o usuário a descobrir respostas |
| **Empatia** | Reconhece ansiedades financeiras e normaliza dúvidas |
| **Proatividade** | Antecipa necessidades com base no histórico |

### Exemplos de Tom
- ❌ **Não:** "O rendimento do CDB é 120% do CDI anualizado."
- ✅ **Sim:** "Esse CDB rende 120% do CDI — ou seja, se o CDI estiver em 10% ao ano, você ganha 12%. É como ganhar um bônus de 20% sobre a taxa básica!"

### Comportamentos-chave
1. **Sempre contextualiza** com os dados do cliente
2. **Nunca inventa** produtos ou rentabilidades
3. **Admite quando não sabe** e sugere falar com humano
4. **Celebra pequenas conquistas** do usuário
5. **Alerta sobre riscos** antes de recomendar qualquer coisa

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    USUÁRIO (Chat/APP)                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│              INTERFACE (Streamlit/Gradio)                   │
│         - Input de texto/voz                                │
│         - Histórico de conversa                             │
│         - Visualização de dados                             │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│              ORQUESTRADOR (Python/LangChain)                │
│         - Roteamento de intenções                           │
│         - Recuperação de contexto                           │
│         - Gerenciamento de memória                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
┌───────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐
│   LLM       │ │  BASE DE  │ │  DADOS    │
│  (Gemini/   │ │CONHECIMENTO│ │  DO       │
│  OpenAI)    │ │ (RAG)     │ │ CLIENTE   │
└─────────────┘ └───────────┘ └───────────┘
        │             │             │
        └─────────────┴─────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│              RESPOSTA GERADA + METADADOS                    │
│         - Verificação de segurança                          │
│         - Formatação final                                  │
│         - Logging para avaliação                            │
└─────────────────────────────────────────────────────────────┘
```

### Fluxo de Dados
1. Usuário envia mensagem → Interface captura input
2. Orquestrador classifica **intenção** (educação, produto, planejamento, suporte)
3. Sistema recupera **contexto relevante** da base de conhecimento
4. Dados do cliente (transações, perfil, histórico) são **injetados no prompt**
5. LLM gera resposta com **instruções de segurança**
6. Resposta é **verificada** antes de ser enviada
7. Interação é **logada** para métricas de qualidade

---

## 🔒 Segurança e Anti-Alucinação

### Estratégias Implementadas

| Estratégia | Implementação |
|-----------|---------------|
| **Grounding em dados** | Sempre referencia transações, perfil e produtos reais do JSON/CSV |
| **Prompt de restrição** | System prompt proíbe inventar produtos, rentabilidades ou dados |
| **Verificação pós-geração** | Regex e validadores checam se produtos mencionados existem na base |
| **Fallback seguro** | Se confiança < 0.8, responde "Não tenho essa informação no momento" |
| **Disclaimer padrão** | Respostas sobre investimentos incluem "Esta não é uma recomendação de investimento" |
| **Auditoria** | Todas as interações são logadas com hash para rastreabilidade |

### Regras de Ouro
1. **Nunca recomendar produto sem citar risco**
2. **Nunca prometer rentabilidade futura**
3. **Nunca dar conselho fiscal sem disclaimer**
4. **Sempre verificar se produto existe na base antes de citar**
5. **Sempre oferecer falar com humano para decisões complexas**

---

## 🎯 Público-Alvo

- **Idade:** 25-35 anos
- **Perfil:** Profissionais da área de tecnologia e criativos
- **Renda:** R$ 5.000 - R$ 15.000/mês
- **Conhecimento:** Básico a intermediário em finanças
- **Dor principal:** Tem dinheiro sobrando, mas não sabe o que fazer
- **Objetivo:** Construir patrimônio de forma segura e educada

---

## 📊 Métricas de Sucesso Esperadas

- Taxa de resolução no primeiro contato: > 80%
- Satisfação do usuário (CSAT): > 4.2/5
- Taxa de alucinação detectada: < 2%
- Taxa de escalada para humano: < 15%
- Tempo médio de resposta: < 3 segundos

---

*Documento criado em: Julho/2026*
*Versão: 1.0*
*Autor: Projeto BIA - DIO Lab*
