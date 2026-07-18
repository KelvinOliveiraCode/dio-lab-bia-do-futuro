"""
BIA - Banco Inteligente Assistente
Aplicação funcional com Streamlit + Google Gemini API
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import re

# =============================================================================
# CONFIGURAÇÃO DA PÁGINA
# =============================================================================
st.set_page_config(
    page_title="BIA - Assistente Financeiro Inteligente",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CSS PERSONALIZADO
# =============================================================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a5f7a;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message-user {
        background-color: #e3f2fd;
        border-radius: 15px 15px 3px 15px;
        padding: 12px 16px;
        margin: 8px 0;
        max-width: 80%;
        align-self: flex-end;
        margin-left: auto;
    }
    .chat-message-assistant {
        background-color: #f5f5f5;
        border-radius: 15px 15px 15px 3px;
        padding: 12px 16px;
        margin: 8px 0;
        max-width: 80%;
        align-self: flex-start;
    }
    .disclaimer {
        font-size: 0.75rem;
        color: #888;
        font-style: italic;
        border-top: 1px solid #ddd;
        padding-top: 8px;
        margin-top: 8px;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        border: 1px solid #e9ecef;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1a5f7a;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #666;
    }
    .objective-card {
        background-color: #fff;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #1a5f7a;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background-color: #1a5f7a;
        color: white;
        border-radius: 20px;
        padding: 8px 20px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #134b5f;
    }
    .quick-question {
        background-color: #e8f4f8;
        border-radius: 20px;
        padding: 8px 16px;
        margin: 4px;
        display: inline-block;
        cursor: pointer;
        font-size: 0.85rem;
        color: #1a5f7a;
        border: 1px solid #1a5f7a;
    }
    .quick-question:hover {
        background-color: #1a5f7a;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# FUNÇÕES DE CARREGAMENTO DE DADOS
# =============================================================================

@st.cache_data
def carregar_dados() -> Dict:
    """Carrega todos os dados da base de conhecimento."""
    dados = {}

    # Caminho base (funciona local e no Streamlit Cloud)
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_path, "..", "data")

    # Transações
    try:
        dados["transacoes"] = pd.read_csv(os.path.join(data_path, "transacoes.csv"))
        dados["transacoes"]["data"] = pd.to_datetime(dados["transacoes"]["data"])
        dados["transacoes"]["valor"] = pd.to_numeric(dados["transacoes"]["valor"], errors="coerce")
    except Exception as e:
        st.error(f"Erro ao carregar transacoes.csv: {e}")
        dados["transacoes"] = pd.DataFrame()

    # Perfil do investidor
    try:
        with open(os.path.join(data_path, "perfil_investidor.json"), "r", encoding="utf-8") as f:
            dados["perfil"] = json.load(f)
    except Exception as e:
        st.error(f"Erro ao carregar perfil_investidor.json: {e}")
        dados["perfil"] = {}

    # Produtos financeiros
    try:
        with open(os.path.join(data_path, "produtos_financeiros.json"), "r", encoding="utf-8") as f:
            dados["produtos"] = json.load(f)
    except Exception as e:
        st.error(f"Erro ao carregar produtos_financeiros.json: {e}")
        dados["produtos"] = {"produtos": [], "educacao": []}

    # Histórico de atendimento
    try:
        dados["historico"] = pd.read_csv(os.path.join(data_path, "historico_atendimento.csv"))
    except Exception as e:
        st.error(f"Erro ao carregar historico_atendimento.csv: {e}")
        dados["historico"] = pd.DataFrame()

    return dados

# =============================================================================
# FUNÇÕES DE ANÁLISE DE DADOS
# =============================================================================

def analisar_gastos_por_categoria(df: pd.DataFrame) -> pd.DataFrame:
    """Agrupa gastos por categoria."""
    if df.empty:
        return pd.DataFrame()

    saidas = df[df["tipo"] == "SAIDA"].copy()
    saidas["valor"] = saidas["valor"].astype(float).abs()

    return saidas.groupby("categoria")["valor"].sum().astype(float).sort_values(ascending=False).reset_index()

def calcular_resumo_mensal(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula resumo mensal de entradas e saídas."""
    if df.empty:
        return pd.DataFrame()

    df["mes"] = df["data"].dt.to_period("M")

    entradas = df[df["tipo"] == "ENTRADA"].groupby("mes")["valor"].sum().astype(float).reset_index()
    entradas.columns = ["mes", "entradas"]

    saidas = df[df["tipo"] == "SAIDA"].groupby("mes")["valor"].sum().astype(float).reset_index()
    saidas.columns = ["mes", "saidas"]
    saidas["saidas"] = saidas["saidas"].astype(float).abs()

    resumo = entradas.merge(saidas, on="mes", how="outer").fillna(0)
    resumo["saldo"] = resumo["entradas"] - resumo["saidas"]

    return resumo

def calcular_progresso_objetivos(perfil: Dict) -> List[Dict]:
    """Calcula progresso percentual de cada objetivo."""
    objetivos = perfil.get("objetivos", [])
    progresso = []

    for obj in objetivos:
        meta = obj.get("valor_meta", 0)
        atual = obj.get("valor_atual", 0)
        pct = (atual / meta * 100) if meta > 0 else 0

        progresso.append({
            "id": obj.get("id"),
            "titulo": obj.get("titulo"),
            "meta": meta,
            "atual": atual,
            "progresso": round(pct, 1),
            "prazo": obj.get("prazo_meses"),
            "prioridade": obj.get("prioridade")
        })

    return progresso

# =============================================================================
# FUNÇÕES DO AGENTE (SIMULAÇÃO DE IA)
# =============================================================================

def detectar_intencao(mensagem: str) -> str:
    """Detecta a intenção da mensagem do usuário."""
    mensagem = mensagem.lower()

    if any(p in mensagem for p in ["gastei", "gasto", "despesa", "transação", "transacoes", "quanto gastei"]):
        return "transacao"
    elif any(p in mensagem for p in ["cdi", "cdb", "tesouro", "fii", "ação", "ação", "etf", "produto", "investir", "investimento", "renda fixa", "renda variável"]):
        return "produto"
    elif any(p in mensagem for p in ["meta", "objetivo", "apartamento", "viagem", "aposentadoria", "reserva", "planejar", "quanto falta"]):
        return "planejamento"
    elif any(p in mensagem for p in ["o que é", "como funciona", "entender", "explicar", "educação", "aprender"]):
        return "educacao"
    elif any(p in mensagem for p in ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite", "quem é você", "quem é voce"]):
        return "saudacao"
    elif any(p in mensagem for p in ["comparar", "melhor", "ou", "vs", "versus", "diferença", "diferenca"]):
        return "comparacao"
    elif any(p in mensagem for p in ["simular", "simulação", "quanto rende", "quanto vou ter", "projeção"]):
        return "simulacao"
    else:
        return "geral"

def gerar_resposta(mensagem: str, dados: Dict, intencao: str) -> str:
    """Gera resposta do agente com base na intenção e nos dados."""

    perfil = dados.get("perfil", {})
    transacoes = dados.get("transacoes", pd.DataFrame())
    produtos = dados.get("produtos", {})
    historico = dados.get("historico", pd.DataFrame())

    cliente = perfil.get("cliente", {})
    nome = cliente.get("nome", "Cliente")
    primeiro_nome = nome.split()[0] if nome else "Cliente"

    # ============= SAUDAÇÃO =============
    if intencao == "saudacao":
        return f"""Oi, {primeiro_nome}! 👋 Sou a **BIA**, seu assistente financeiro inteligente.

Estou aqui para te ajudar a entender melhor sua situação financeira, aprender sobre investimentos e acompanhar suas metas. Posso falar sobre:

💰 **Seus gastos** — quanto e onde você gastou
📈 **Investimentos** — produtos disponíveis e recomendações
🎯 **Suas metas** — progresso e projeções
📚 **Educação** — conceitos financeiros de forma simples

**O que você gostaria de saber hoje?** Você pode perguntar algo como:
- "Quanto gastei em lazer?"
- "O que é CDI?"
- "Estou perto da meta do apartamento?"
- "Onde investir R$ 5.000?"

*Esta conversa tem fins educacionais e não constitui recomendação de investimento.*"""

    # ============= TRANSAÇÃO / GASTOS =============
    elif intencao == "transacao":
        if transacoes.empty:
            return "Não consegui acessar seus dados de transações no momento. Tente novamente mais tarde."

        # Detectar categoria específica
        categorias = transacoes["categoria"].unique()
        categoria_detectada = None
        for cat in categorias:
            if cat.lower() in mensagem.lower():
                categoria_detectada = cat
                break

        if categoria_detectada:
            cat_data = transacoes[transacoes["categoria"] == categoria_detectada]
            cat_saidas = cat_data[cat_data["tipo"] == "SAIDA"]
            total = cat_saidas["valor"].astype(float).abs().sum()
            media_mensal = cat_saidas.groupby(cat_saidas["data"].dt.to_period("M"))["valor"].sum().astype(float).abs().mean()

            return f"""Vamos dar uma olhada nos seus gastos com **{categoria_detectada}**, {primeiro_nome}!

📊 **Resumo:**
- **Total gasto (Jan-Jul/2026):** R$ {total:,.2f}
- **Média mensal:** R$ {media_mensal:,.2f}

**Dica:** Se quiser reduzir esse gasto, posso te ajudar a criar um plano. Quer que eu mostre como isso impacta suas metas?

*Esta conversa tem fins educacionais e não constitui recomendação de investimento.*"""
        else:
            # Resumo geral de gastos
            gastos = analisar_gastos_por_categoria(transacoes)
            if not gastos.empty:
                top3 = gastos.head(3)
                top3_str = "\n".join([f"  {i+1}. **{row['categoria']}**: R$ {row['valor']:,.2f}" for i, row in top3.iterrows()])

                total_saidas = transacoes[transacoes["tipo"] == "SAIDA"]["valor"].astype(float).abs().sum()
                total_entradas = transacoes[transacoes["tipo"] == "ENTRADA"]["valor"].astype(float).sum()

                return f"""Aqui está o resumo dos seus gastos, {primeiro_nome}!

💸 **Total de saídas (Jan-Jul/2026):** R$ {total_saidas:,.2f}
💵 **Total de entradas:** R$ {total_entradas:,.2f}
✅ **Saldo acumulado:** R$ {total_entradas - total_saidas:,.2f}

**Top 3 categorias de gasto:**
{top3_str}

Você está indo bem! Sua renda está cobrindo os gastos com folga. Quer que eu sugira onde investir essa sobra?

*Esta conversa tem fins educacionais e não constitui recomendação de investimento.*"""
            else:
                return "Não consegui analisar seus gastos no momento. Tente ser mais específico, como 'Quanto gastei em lazer?'"

    # ============= PRODUTO / INVESTIMENTO =============
    elif intencao == "produto":
        produtos_list = produtos.get("produtos", [])

        # Detectar produto específico
        produto_detectado = None
        for p in produtos_list:
            if p["nome"].lower() in mensagem.lower() or p["id"].lower() in mensagem.lower():
                produto_detectado = p
                break

        if produto_detectado:
            return f"""Ótima pergunta sobre **{produto_detectado['nome']}**, {primeiro_nome}!

📋 **Detalhes do produto:**
- **Categoria:** {produto_detectado['categoria']}
- **Tipo:** {produto_detectado['tipo']}
- **Rentabilidade:** {produto_detectado['rentabilidade']}
- **Risco:** {produto_detectado['risco']}
- **Liquidez:** {produto_detectado['liquidez']}
- **Valor mínimo:** R$ {produto_detectado['valor_minimo']:,.2f}

📝 **Descrição:**
{produto_detectado['descricao']}

⚠️ **Importante:** Este produto tem risco **{produto_detectado['risco']}**. Sempre considere seu perfil de investidor antes de aplicar.

Quer que eu compare esse produto com outras opções da nossa base?

*Esta conversa tem fins educacionais e não constitui recomendação de investimento.*"""
        else:
            # Recomendação geral
            perfil_risco = perfil.get("perfil_risco", {})
            tipo_risco = perfil_risco.get("tipo", "Moderado")

            recomendados = [p for p in produtos_list if tipo_risco in p.get("recomendado_para", [])]
            if not recomendados:
                recomendados = produtos_list[:3]

            rec_str = "\n".join([f"  • **{p['nome']}** — {p['rentabilidade']} (Risco: {p['risco']})" for p in recomendados[:3]])

            return f"""Com base no seu perfil **{tipo_risco}**, aqui estão alguns produtos que podem fazer sentido para você, {primeiro_nome}:

{rec_str}

**Lembre-se:** Cada produto tem características diferentes de risco e liquidez. Quer que eu explique melhor algum deles, ou prefere uma simulação com valores específicos?

*Esta conversa tem fins educacionais e não constitui recomendação de investimento.*"""

    # ============= PLANEJAMENTO / METAS =============
    elif intencao == "planejamento":
        progresso = calcular_progresso_objetivos(perfil)

        if not progresso:
            return "Não consegui acessar seus objetivos no momento. Tente novamente mais tarde."

        # Detectar meta específica
        meta_detectada = None
        for p in progresso:
            if p["titulo"].lower() in mensagem.lower():
                meta_detectada = p
                break

        if meta_detectada:
            return f"""Vamos ver como está sua meta **{meta_detectada['titulo']}**, {primeiro_nome}!

🎯 **Progresso:**
- **Meta:** R$ {meta_detectada['meta']:,.2f}
- **Atual:** R$ {meta_detectada['atual']:,.2f}
- **Concluído:** {meta_detectada['progresso']}%
- **Prazo:** {meta_detectada['prazo']} meses
- **Prioridade:** {meta_detectada['prioridade']}

**Faltam:** R$ {meta_detectada['meta'] - meta_detectada['atual']:,.2f}

Se você mantiver o aporte atual, está no caminho certo! Quer que eu simule um cenário com aporte maior ou menor?

*Esta conversa tem fins educacionais e não constitui recomendação de investimento.*"""
        else:
            # Resumo de todas as metas
            metas_str = "\n".join([f"  • **{p['titulo']}**: {p['progresso']}% (R$ {p['atual']:,.2f} de R$ {p['meta']:,.2f})" for p in progresso])

            return f"""Aqui está o panorama das suas metas financeiras, {primeiro_nome}:

{metas_str}

Você está construindo um patrimônio sólido! A reserva de emergência é a prioridade — ela te dá segurança para os outros objetivos.

Qual meta você quer acompanhar mais de perto?

*Esta conversa tem fins educacionais e não constitui recomendação de investimento.*"""

    # ============= EDUCAÇÃO =============
    elif intencao == "educacao":
        educacao = produtos.get("educacao", [])

        # Detectar tema
        tema = None
        for e in educacao:
            if any(tag.lower() in mensagem.lower() for tag in e.get("tags", [])):
                tema = e
                break

        if tema:
            return f"""Vamos aprender sobre **{tema['titulo']}**, {primeiro_nome}!

📚 **Conteúdo disponível:**
- **Nível:** {tema['nivel']}
- **Duração:** {tema['duracao']}
- **Formato:** {tema['formato']}

**Resumo:**
Este conteúdo vai te ajudar a entender melhor sobre {tema['tags'][0] if tema['tags'] else 'este tema'} de forma prática e aplicável ao seu dia a dia.

Quer que eu te explique o conceito principal agora, ou prefere acessar o material completo?

*Esta conversa tem fins educacionais e não constitui recomendação de investimento.*"""
        else:
            # Sugerir conteúdos
            conteudos_str = "\n".join([f"  • **{e['titulo']}** ({e['nivel']}, {e['duracao']})" for e in educacao[:3]])

            return f"""Adoro ver sua curiosidade sobre finanças, {primeiro_nome}! 📚

Aqui estão alguns conteúdos que podem te interessar:

{conteudos_str}

Sobre qual desses temas você quer aprender? Ou me pergunte algo específico como "O que é CDI?" ou "Como funciona um FII?"

*Esta conversa tem fins educacionais e não constitui recomendação de investimento.*"""

    # ============= COMPARAÇÃO =============
    elif intencao == "comparacao":
        produtos_list = produtos.get("produtos", [])

        # Detectar produtos na mensagem
        produtos_mencionados = []
        for p in produtos_list:
            if p["nome"].lower() in mensagem.lower() or p["id"].lower() in mensagem.lower():
                produtos_mencionados.append(p)

        if len(produtos_mencionados) >= 2:
            p1, p2 = produtos_mencionados[0], produtos_mencionados[1]
            return f"""Vamos comparar **{p1['nome']}** vs **{p2['nome']}**, {primeiro_nome}!

| Característica | {p1['nome']} | {p2['nome']} |
|----------------|--------------|--------------|
| **Categoria** | {p1['categoria']} | {p2['categoria']} |
| **Rentabilidade** | {p1['rentabilidade']} | {p2['rentabilidade']} |
| **Risco** | {p1['risco']} | {p2['risco']} |
| **Liquidez** | {p1['liquidez']} | {p2['liquidez']} |
| **Mínimo** | R$ {p1['valor_minimo']:,.2f} | R$ {p2['valor_minimo']:,.2f} |

**Qual faz mais sentido para você?** Depende do seu objetivo:
- Se precisa de **segurança e liquidez** → {p1['nome'] if p1['risco'] < p2['risco'] else p2['nome']}
- Se busca **maior retorno** e aceita risco → {p1['nome'] if p1['risco'] > p2['risco'] else p2['nome']}

Quer que eu simule um investimento em cada um?

*Esta conversa tem fins educacionais e não constitui recomendação de investimento.*"""
        else:
            return f"""Para fazer uma comparação justa, {primeiro_nome}, me diga quais dois produtos você quer comparar.

Por exemplo:
- "CDB ou Tesouro Selic?"
- "FII ou Ações?"
- "Tesouro ou Fundo DI?"

Assim posso mostrar as diferenças de risco, rentabilidade e liquidez de forma clara!

*Esta conversa tem fins educacionais e não constitui recomendação de investimento.*"""

    # ============= SIMULAÇÃO =============
    elif intencao == "simulacao":
        # Extrair valor da mensagem
        valor_match = re.search(r'R?\$?\s?(\d+[\.,]?\d*)', mensagem.replace('.', '').replace(',', '.'))
        valor = float(valor_match.group(1)) if valor_match else 1000

        # Simular CDB 120% CDI a 12% a.a.
        cdi_anual = 0.12
        cdb_rendimento = cdi_anual * 1.20

        # Juros compostos
        meses = 12
        taxa_mensal = (1 + cdb_rendimento) ** (1/12) - 1
        valor_final = valor * (1 + taxa_mensal) ** meses
        rendimento = valor_final - valor

        # IR regressivo (1 ano = 17.5%)
        ir = rendimento * 0.175
        liquido = valor_final - ir

        return f"""Vamos simular! 💰

**Cenário:** R$ {valor:,.2f} no **CDB 120% CDI** por 12 meses

📊 **Projeção (estimativa):**
- **Valor investido:** R$ {valor:,.2f}
- **Rentabilidade bruta estimada:** {cdb_rendimento*100:.1f}% a.a.
- **Valor bruto após 1 ano:** R$ {valor_final:,.2f}
- **Rendimento bruto:** R$ {rendimento:,.2f}
- **IR (17,5%):** -R$ {ir:,.2f}
- **Valor líquido:** R$ {liquido:,.2f}
- **Ganho real:** R$ {liquido - valor:,.2f}

⚠️ **Importante:** Esta é uma projeção baseada em taxas atuais. O CDI pode mudar, e o rendimento real pode ser diferente. Não é garantia de lucro.

Quer simular outro produto ou prazo?

*Esta conversa tem fins educacionais e não constitui recomendação de investimento.*"""

    # ============= GERAL / FALLBACK =============
    else:
        return f"""Entendi, {primeiro_nome}! 😊

Posso te ajudar com várias coisas relacionadas às suas finanças:

💰 **Gastos** — "Quanto gastei em lazer?"
📈 **Investimentos** — "O que é CDB?" ou "Onde investir?"
🎯 **Metas** — "Estou perto da meta do apartamento?"
📚 **Educação** — "Como funciona um FII?"
🔍 **Comparação** — "CDB ou Tesouro Selic?"
📊 **Simulação** — "Quanto rende R$ 5.000 em 1 ano?"

**O que você gostaria de explorar?**

*Esta conversa tem fins educacionais e não constitui recomendação de investimento.*"""

# =============================================================================
# INTERFACE STREAMLIT
# =============================================================================

def main():
    # Header
    st.markdown('<div class="main-header">🤖 BIA</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Banco Inteligente Assistente — Seu parceiro financeiro</div>', unsafe_allow_html=True)

    # Sidebar com dados do cliente
    with st.sidebar:
        st.header("👤 Perfil do Cliente")

        dados = carregar_dados()
        perfil = dados.get("perfil", {})
        cliente = perfil.get("cliente", {})
        perfil_risco = perfil.get("perfil_risco", {})

        st.subheader(f"{cliente.get('nome', 'Ana Carolina Mendes')}")
        st.write(f"**Profissão:** {cliente.get('profissao', 'Desenvolvedora')}")
        st.write(f"**Renda:** R$ {cliente.get('renda_mensal', 8500):,.2f}/mês")
        st.write(f"**Perfil:** {perfil_risco.get('tipo', 'Moderado')} (Score: {perfil_risco.get('score', 65)})")

        st.divider()

        # Métricas rápidas
        st.subheader("📊 Resumo Financeiro")
        transacoes = dados.get("transacoes", pd.DataFrame())
        if not transacoes.empty:
            total_entradas = transacoes[transacoes["tipo"] == "ENTRADA"]["valor"].astype(float).sum()
            total_saidas = transacoes[transacoes["tipo"] == "SAIDA"]["valor"].astype(float).abs().sum()
            saldo = total_entradas - total_saidas

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'<div class="metric-card"><div class="metric-value">R$ {saldo:,.0f}</div><div class="metric-label">Saldo Acumulado</div></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="metric-card"><div class="metric-value">R$ {(total_entradas - total_saidas)/7:,.0f}</div><div class="metric-label">Média Mensal</div></div>', unsafe_allow_html=True)

        st.divider()

        # Objetivos
        st.subheader("🎯 Objetivos")
        progresso = calcular_progresso_objetivos(perfil)
        for p in progresso:
            with st.container():
                st.markdown(f'<div class="objective-card"><b>{p["titulo"]}</b><br>Progresso: {p["progresso"]}% | Meta: R$ {p["meta"]:,.0f}</div>', unsafe_allow_html=True)
                st.progress(p["progresso"] / 100)

    # Área principal - Chat
    st.divider()

    # Inicializar histórico de chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Saudação inicial
        saudacao = gerar_resposta("oi", dados, "saudacao")
        st.session_state.messages.append({"role": "assistant", "content": saudacao})

    # Exibir mensagens
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message-user">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message-assistant">{message["content"]}</div>', unsafe_allow_html=True)

    # Input do usuário
    st.divider()

    # Perguntas rápidas
    st.markdown("**Perguntas rápidas:**")
    cols = st.columns(4)
    quick_questions = [
        "Quanto gastei em lazer?",
        "O que é CDI?",
        "Estou perto da meta?",
        "Onde investir R$ 5.000?"
    ]

    for i, q in enumerate(quick_questions):
        with cols[i]:
            if st.button(q, key=f"quick_{i}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": q})
                intencao = detectar_intencao(q)
                resposta = gerar_resposta(q, dados, intencao)
                st.session_state.messages.append({"role": "assistant", "content": resposta})
                st.rerun()

    # Input de texto
    prompt = st.chat_input("Digite sua mensagem...")

    if prompt:
        # Adicionar mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Detectar intenção e gerar resposta
        intencao = detectar_intencao(prompt)
        resposta = gerar_resposta(prompt, dados, intencao)

        # Adicionar resposta do assistente
        st.session_state.messages.append({"role": "assistant", "content": resposta})

        st.rerun()

if __name__ == "__main__":
    main()
