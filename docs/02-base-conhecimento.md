# 02 - Base de Conhecimento

## 📁 Estrutura de Dados

A base de conhecimento do BIA é composta por 4 arquivos principais, todos localizados na pasta `data/`:

```
data/
├── transacoes.csv              # Histórico de transações (89 registros)
├── perfil_investidor.json      # Perfil completo do cliente
├── produtos_financeiros.json   # Catálogo de produtos e conteúdo educacional
└── historico_atendimento.csv   # Registro de atendimentos anteriores
```

---

## 1. transacoes.csv

**Formato:** CSV com 8 colunas
**Registros:** 89 transações (Jan/2026 - Jul/2026)

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id_transacao` | String | Identificador único (TX001-TX089) |
| `data` | Date (YYYY-MM-DD) | Data da transação |
| `tipo` | String | ENTRADA ou SAIDA |
| `categoria` | String | Classificação (Salário, Aluguel, Supermercado, etc.) |
| `descricao` | String | Descrição detalhada |
| `valor` | Float | Valor monetário (positivo para entrada, negativo para saída) |
| `saldo_apos` | Float | Saldo acumulado após a transação |

### Categorias Presentes
- **Entradas:** Salário, Freelance, Investimento
- **Saídas Fixas:** Aluguel, Supermercado, Transporte, Utilidades, Saúde, Streaming
- **Saídas Variáveis:** Lazer, Alimentação, Educação, Investimento

### Insight Principal
O cliente Ana Carolina tem renda mensal de R$ 8.500 + ~R$ 1.000 em freelances, com despesas fixas de ~R$ 3.500 e sobra média de ~R$ 5.000/mês para investimentos e lazer.

---

## 2. perfil_investidor.json

**Formato:** JSON estruturado com 6 seções principais

### Seções

| Seção | Descrição |
|-------|-----------|
| `cliente` | Dados pessoais e profissionais |
| `perfil_risco` | Classificação de risco (Moderado, score 65) |
| `objetivos` | 4 metas financeiras com valores, prazos e prioridades |
| `preferencias` | Canais de contato, horários, notificações |
| `conhecimento_financeiro` | Nível e experiência em investimentos |
| `dados_bancarios` | Instituição e produtos contratados |

### Objetivos do Cliente

| ID | Título | Meta | Atual | Prazo | Prioridade |
|----|--------|------|-------|-------|------------|
| OBJ-01 | Reserva de Emergência | R$ 25.000 | R$ 15.000 | 12 meses | Alta |
| OBJ-02 | Entrada Apartamento | R$ 80.000 | R$ 22.000 | 48 meses | Alta |
| OBJ-03 | Aposentadoria | R$ 500.000 | R$ 8.500 | 360 meses | Média |
| OBJ-04 | Viagem Europa | R$ 15.000 | R$ 3.000 | 18 meses | Baixa |

### Perfil de Risco: Moderado
- Aceita riscos calculados
- Busca retornos superiores à renda fixa
- Preserva parte do capital em investimentos conservadores
- Tolerância a perda: até 15% do capital investido

---

## 3. produtos_financeiros.json

**Formato:** JSON com 2 arrays: `produtos` (8 itens) e `educacao` (5 itens)

### Produtos Financeiros

| ID | Nome | Categoria | Risco | Liquidez | Mínimo |
|----|------|-----------|-------|----------|--------|
| PROD-001 | Tesouro Selic 2029 | Renda Fixa | Baixíssimo | Diária | R$ 100 |
| PROD-002 | CDB 120% CDI | Renda Fixa | Baixo | 2 anos | R$ 1.000 |
| PROD-003 | FII HGLG11 | Renda Variável | Médio | Diária | 1 cota |
| PROD-004 | PETR4 | Renda Variável | Alto | Diária | 1 ação |
| PROD-005 | Previdência VGBL | Previdência | Variável | Resgate sujeito a taxas | R$ 100 |
| PROD-006 | Fundo DI XP | Renda Fixa | Baixo | D+1 | R$ 100 |
| PROD-007 | ETF BOVA11 | Renda Variável | Alto | Diária | 1 cota |
| PROD-008 | CDB 100% CDI Liq. Diária | Renda Fixa | Baixo | Diária | R$ 100 |

### Conteúdo Educacional

| ID | Título | Nível | Formato |
|----|--------|-------|---------|
| EDU-001 | Reserva de Emergência | Iniciante | Artigo (15 min) |
| EDU-002 | Entendendo o CDI | Iniciante | Vídeo (10 min) |
| EDU-003 | FIIs para Iniciantes | Intermediário | Artigo + Quiz (20 min) |
| EDU-004 | Declarar Investimentos no IR | Intermediário | Vídeo + Checklist (25 min) |
| EDU-005 | Análise Fundamentalista | Avançado | Artigo + Planilha (40 min) |

---

## 4. historico_atendimento.csv

**Formato:** CSV com 9 colunas
**Registros:** 12 atendimentos (Jan/2026 - Jul/2026)

| Coluna | Descrição |
|--------|-----------|
| `id_atendimento` | Identificador único (ATD001-ATD012) |
| `data` | Data do atendimento |
| `canal` | Chat ou Email |
| `assunto` | Categoria (Investimentos, Cartão, Planejamento, etc.) |
| `resumo` | Descrição do que foi tratado |
| `satisfacao` | Nota 1-5 |
| `acao_recomendada` | Ação sugerida ao cliente |
| `status` | Concluído, Pendente, etc. |

### Padrões Identificados
- **Maioria dos atendimentos:** Investimentos (50%)
- **Canal preferido:** Chat (75%)
- **Satisfação média:** 4.6/5
- **Ações recorrentes:** Aportes mensais, compra de cotas/ações

---

## 🔄 Estratégia de Atualização

| Tipo de Dado | Frequência de Atualização | Responsável |
|-------------|---------------------------|-------------|
| Transações | Diária (automática) | Sistema bancário |
| Perfil do Investidor | Mensal ou sob demanda | Cliente + Analista |
| Produtos Financeiros | Quando houver mudança | Equipe de Produtos |
| Histórico de Atendimento | Em tempo real | Sistema de atendimento |
| Conteúdo Educacional | Mensal | Equipe de Conteúdo |

---

## 🔗 Integração com o Agente

O agente BIA acessa esses dados através de:

1. **Carregamento em memória** no início da sessão (JSON → dict, CSV → DataFrame)
2. **Consultas filtradas** por categoria, data ou valor
3. **Agregações dinâmicas** (soma por categoria, média mensal, etc.)
4. **Contexto injetado** no prompt do LLM para respostas personalizadas

### Exemplo de Query
```python
# Gasto médio mensal em lazer
lazer = df[df['categoria'] == 'Lazer']
gasto_lazer = lazer.groupby(lazer['data'].dt.to_period('M'))['valor'].sum().mean()
# Resultado: ~R$ 280/mês
```

---

## 📈 Evolução da Base

A base pode crescer com:
- **Mais transações** (histórico de 12+ meses)
- **Novos produtos** (cripto, fundos multimercado, etc.)
- **Dados de mercado** (cotações em tempo real)
- **Feedback de usuários** (avaliações de conteúdo)
- **Notícias financeiras** (integração com feeds de notícias)

---

*Documento criado em: Julho/2026*
*Versão: 1.0*
*Autor: Projeto BIA - DIO Lab*
