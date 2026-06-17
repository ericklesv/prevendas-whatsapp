"""
Automatizador de Pré-Vendas WhatsApp
Especializado em miniaturas colecionáveis
"""

import streamlit as st
import math

st.set_page_config(
    page_title="Pré-Vendas WhatsApp - Miniaturas",
    page_icon="🚗",
    layout="wide"
)

DISTRIBUIDORES = [
    "ALISSON",
    "MINI GT",
    "JCAR",
    "MINI DELAS",
    "MATTEL CREATIONS",
    "MG PRO ALISSON",
    "EBAY",
    "SUPER MINI",
    "DIECAST USA",
    "VEIGA"
]

# Distribuidores cujo preço já está em reais (sem conversão de dólar)
DISTRIBUIDORES_SEM_DOLAR = ["VEIGA"]

TIPOS_PREVENDA = ["PRÉ VENDA EUA", "LONGO PRAZO"]


def calcular_custo(distribuidor: str, preco: float, dolar: float, frete: float) -> float:
    if distribuidor == "ALISSON":
        return (preco * dolar) + dolar + frete
    elif distribuidor == "MINI GT":
        return ((dolar + 0.38) * preco) + 10
    elif distribuidor == "JCAR":
        return ((preco * dolar) * 1.25) + frete
    elif distribuidor == "MINI DELAS":
        return (preco * dolar) + dolar + frete + (dolar * 1.74)
    elif distribuidor == "MATTEL CREATIONS":
        return ((dolar + 1.25) * preco) + frete
    elif distribuidor == "MG PRO ALISSON":
        return (preco * (dolar + 0.28)) + frete + 20
    elif distribuidor == "EBAY":
        return (preco * dolar) + dolar + frete
    elif distribuidor == "SUPER MINI":
        return ((preco * 1) * 1.25) + frete
    elif distribuidor == "DIECAST USA":
        return (preco * dolar) + frete
    elif distribuidor == "VEIGA":
        return preco + frete
    return 0


def calcular_preco(distribuidor: str, preco: float, dolar: float, frete: float) -> float:
    if distribuidor == "ALISSON":
        return ((preco * dolar) + dolar + frete) * 1.26
    elif distribuidor == "MINI GT":
        return (((dolar + 0.38) * preco) + 10) * 1.26
    elif distribuidor == "JCAR":
        return (((preco * dolar) * 1.25) + frete) * 1.25
    elif distribuidor == "MINI DELAS":
        return ((preco * dolar) + dolar + frete + (dolar * 1.74)) * 1.26
    elif distribuidor == "MATTEL CREATIONS":
        return (((dolar + 1.25) * preco) + frete) * 1.5
    elif distribuidor == "MG PRO ALISSON":
        return ((preco * (dolar + 0.28)) + frete + 20) * 1.25
    elif distribuidor == "EBAY":
        return ((preco * dolar) + dolar + frete) * 1.27
    elif distribuidor == "SUPER MINI":
        return (((preco * 1) * 1.25) + frete) * 1.25
    elif distribuidor == "DIECAST USA":
        return ((preco * dolar) + frete) * 1.26
    elif distribuidor == "VEIGA":
        return (preco + frete) * 1.31
    return 0


# ── Layout ──────────────────────────────────────────────────────────────────

st.title("🚗 Pré-Vendas WhatsApp")
st.caption("Miniaturas Colecionáveis")

col_form, col_result = st.columns([1, 1], gap="large")

with col_form:
    nome = st.text_input("Nome da Miniatura", placeholder="Ex: Porsche 911 GT3 RS")

    distribuidor = st.selectbox("Distribuidor", DISTRIBUIDORES)

    tipo = st.selectbox("Tipo de Pré-Venda", TIPOS_PREVENDA)

    sem_dolar = distribuidor in DISTRIBUIDORES_SEM_DOLAR

    c1, c2, c3 = st.columns(3)
    with c1:
        label_preco = "Preço (R$)" if sem_dolar else "Preço (USD)"
        preco_str = st.text_input(label_preco, placeholder="Ex: 29.99")
    with c2:
        dolar_str = st.text_input(
            "Dólar (R$)",
            placeholder="Ex: 5.50",
            disabled=sem_dolar,
            help="Não usado neste distribuidor (preço já em reais)." if sem_dolar else None,
        )
    with c3:
        frete_str = st.text_input("Frete (R$)", placeholder="Ex: 15.00")

    entrada_fixa_check = st.checkbox("Entrada Fixa")
    entrada_fixa_str = ""
    if entrada_fixa_check:
        entrada_fixa_str = st.text_input("Valor da Entrada (R$)", placeholder="Ex: 30.00")

    data = ""
    if tipo == "LONGO PRAZO":
        data = st.text_input("Data Prevista de Lançamento", placeholder="Ex: Março/2026")

    gerar = st.button("📝 Gerar Mensagem", use_container_width=True, type="primary")

with col_result:
    st.subheader("📋 Mensagem Gerada")

    if gerar:
        erros = []
        if not nome.strip():
            erros.append("Informe o nome da miniatura.")
        if sem_dolar:
            if not preco_str.strip() or not frete_str.strip():
                erros.append("Preencha todos os valores (Preço, Frete).")
        else:
            if not preco_str.strip() or not dolar_str.strip() or not frete_str.strip():
                erros.append("Preencha todos os valores (Preço, Dólar, Frete).")
        if entrada_fixa_check and not entrada_fixa_str.strip():
            erros.append("Informe o valor da entrada fixa.")
        if tipo == "LONGO PRAZO" and not data.strip():
            erros.append("Informe a data prevista de lançamento.")

        if erros:
            for e in erros:
                st.error(e)
        else:
            try:
                preco = float(preco_str.replace(",", "."))
                dolar = 0.0 if sem_dolar else float(dolar_str.replace(",", "."))
                frete = float(frete_str.replace(",", "."))

                valor_total = math.ceil(calcular_preco(distribuidor, preco, dolar, frete))
                custo = calcular_custo(distribuidor, preco, dolar, frete)

                entrada_fixa = None
                if entrada_fixa_check:
                    entrada_fixa = float(entrada_fixa_str.replace(",", "."))

                if tipo == "PRÉ VENDA EUA":
                    if entrada_fixa is not None:
                        valor_restante_pv = round(valor_total - entrada_fixa, 2)
                        mensagem = f"*PRÉ VENDA EUA*\n\n{nome}\n\n💰 R${valor_total:.2f}\n\n➗ R${entrada_fixa:.2f} agora + R${valor_restante_pv:.2f} quando chegar\n\n📦 Será enviado em até 2 meses"
                    else:
                        valor_50 = valor_total / 2
                        mensagem = f"*PRÉ VENDA EUA*\n\n{nome}\n\n💰 R${valor_total:.2f}\n\n➗ R${valor_50:.2f} agora + R${valor_50:.2f} quando chegar\n\n📦 Será enviado em até 2 meses"
                else:
                    if entrada_fixa is not None:
                        valor_restante = round(valor_total - entrada_fixa, 2)
                        mensagem = f"{nome}\n\n💰 R${valor_total:.2f}\n\n➗ R${entrada_fixa:.2f} na reserva e R${valor_restante:.2f} quando chegar\n\n📅 Previsão de lançamento é {data}\n(podendo ocorrer antecipadamente ou posterior ao prazo informado)."
                    else:
                        valor_restante = round(valor_total - 25, 2)
                        mensagem = f"{nome}\n\n💰 R${valor_total:.2f}\n\n➗ R$25,00 na reserva e R${valor_restante:.2f} quando chegar\n\n📅 Previsão de lançamento é {data}\n(podendo ocorrer antecipadamente ou posterior ao prazo informado)."

                st.session_state["mensagem"] = mensagem
                st.session_state["custo"] = custo

            except ValueError:
                st.error("Valores inválidos! Use números válidos (ex: 29.99).")

    mensagem_atual = st.session_state.get("mensagem", "")
    custo_atual = st.session_state.get("custo", None)

    if mensagem_atual:
        st.code(mensagem_atual, language=None)
        st.info("💡 Clique no ícone de cópia no canto superior direito da caixa acima para copiar.")

        if custo_atual is not None:
            st.divider()
            st.markdown("**📊 Informação Interna**")
            st.success(f"Custo: R$ {custo_atual:.2f}")
    else:
        st.markdown("*Preencha o formulário e clique em **Gerar Mensagem**.*")
