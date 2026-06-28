"""
Automatizador de Pré-Vendas WhatsApp
Especializado em miniaturas colecionáveis
"""

import streamlit as st
import streamlit.components.v1 as components
import math
import json

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

# Lembrar o último valor do dólar: o localStorage do navegador é a fonte da
# verdade. Este componente injeta o valor salvo na URL (?dolar=) para que o
# Python consiga pré-preencher o campo. Só recarrega quando estão divergentes.
components.html(
    """<script>
(function(){
    var p = window.parent;
    try {
        var params = new URLSearchParams(p.location.search);
        var saved = p.localStorage.getItem('prevendas_dolar') || '';
        var cur = params.get('dolar') || '';
        if (saved && saved !== cur) {
            params.set('dolar', saved);
            p.location.search = params.toString();
        }
    } catch(e) {}
})();
</script>""",
    height=0,
)

# Pré-preenche o campo dólar com o último valor lembrado (vindo do localStorage
# via URL). Só inicializa uma vez por sessão para não sobrescrever edições.
if "dolar_str" not in st.session_state:
    st.session_state["dolar_str"] = st.query_params.get("dolar", "")

st.title("🚗 Pré-Vendas WhatsApp")
st.caption("Miniaturas Colecionáveis")

col_form, col_result = st.columns([1, 1], gap="large")

with col_form:
    nome = st.text_input("Nome da Miniatura", placeholder="Ex: Porsche 911 GT3 RS")
    sku = st.text_input("SKU (opcional)", placeholder="Ex: HKF12")

    preco_fixo_check = st.checkbox(
        "💵 Preço fixo (informar valor de venda)",
        help="Pula o cálculo: você informa o preço final de venda e o app apenas formata a mensagem.",
    )

    if not preco_fixo_check:
        distribuidor = st.selectbox("Distribuidor", DISTRIBUIDORES)
        sem_dolar = distribuidor in DISTRIBUIDORES_SEM_DOLAR
    else:
        distribuidor = None
        sem_dolar = False

    tipo = st.selectbox("Tipo de Pré-Venda", TIPOS_PREVENDA)

    # Modo "preço fixo": pede só o preço de venda final.
    # Caso contrário: trio Preço/Dólar/Frete usado no cálculo.
    dolar_str = ""
    preco_str = ""
    frete_str = ""
    preco_venda_str = ""
    if preco_fixo_check:
        preco_venda_str = st.text_input("Preço de Venda (R$)", placeholder="Ex: 250.00")
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            label_preco = "Preço (R$)" if sem_dolar else "Preço (USD)"
            preco_str = st.text_input(label_preco, placeholder="Ex: 29.99")
        with c2:
            dolar_str = st.text_input(
                "Dólar (R$)",
                key="dolar_str",
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

    st.markdown("**Destaques (opcional)**")
    ultima_unidade = st.checkbox("ÚLTIMA UNIDADE")
    exclusiva_whatsapp = st.checkbox("EXCLUSIVA NO WHATSAPP")
    cartao_credito = st.checkbox("CARTÃO DE CRÉDITO")

    gerar = st.button("📝 Gerar Mensagem", use_container_width=True, type="primary")

with col_result:
    st.subheader("📋 Mensagem Gerada")

    if gerar:
        erros = []
        if not nome.strip():
            erros.append("Informe o nome da miniatura.")
        if preco_fixo_check:
            if not preco_venda_str.strip():
                erros.append("Informe o preço de venda.")
        elif sem_dolar:
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
                if preco_fixo_check:
                    # Preço informado manualmente: usa o valor exato, sem cálculo.
                    valor_total = float(preco_venda_str.replace(",", "."))
                    custo = None
                else:
                    preco = float(preco_str.replace(",", "."))
                    dolar = 0.0 if sem_dolar else float(dolar_str.replace(",", "."))
                    frete = float(frete_str.replace(",", "."))

                    valor_total = math.ceil(calcular_preco(distribuidor, preco, dolar, frete))
                    custo = calcular_custo(distribuidor, preco, dolar, frete)

                entrada_fixa = None
                if entrada_fixa_check:
                    entrada_fixa = float(entrada_fixa_str.replace(",", "."))

                # Bloco do nome: inclui a linha de SKU logo abaixo, se informado.
                nome_bloco = nome
                if sku.strip():
                    nome_bloco = f"{nome}\n🏷️ SKU: {sku.strip()}"

                if tipo == "PRÉ VENDA EUA":
                    if entrada_fixa is not None:
                        valor_restante_pv = round(valor_total - entrada_fixa, 2)
                        mensagem = f"*PRÉ VENDA EUA*\n\n{nome_bloco}\n\n💰 R${valor_total:.2f}\n\n➗ R${entrada_fixa:.2f} agora + R${valor_restante_pv:.2f} quando chegar\n\n📦 Será enviado em até 2 meses"
                    else:
                        valor_50 = valor_total / 2
                        mensagem = f"*PRÉ VENDA EUA*\n\n{nome_bloco}\n\n💰 R${valor_total:.2f}\n\n➗ R${valor_50:.2f} agora + R${valor_50:.2f} quando chegar\n\n📦 Será enviado em até 2 meses"
                else:
                    if entrada_fixa is not None:
                        valor_restante = round(valor_total - entrada_fixa, 2)
                        mensagem = f"{nome_bloco}\n\n💰 R${valor_total:.2f}\n\n➗ R${entrada_fixa:.2f} na reserva e R${valor_restante:.2f} quando chegar\n\n📅 Previsão de lançamento é {data}\n(podendo ocorrer antecipadamente ou posterior ao prazo informado)."
                    else:
                        valor_restante = round(valor_total - 25, 2)
                        mensagem = f"{nome_bloco}\n\n💰 R${valor_total:.2f}\n\n➗ R$25,00 na reserva e R${valor_restante:.2f} quando chegar\n\n📅 Previsão de lançamento é {data}\n(podendo ocorrer antecipadamente ou posterior ao prazo informado)."

                # Linhas de destaque (opcionais), no final da mensagem,
                # cada uma separada por uma linha em branco.
                destaques = []
                if ultima_unidade:
                    destaques.append("🔥 APENAS 1 UNIDADE")
                if exclusiva_whatsapp:
                    destaques.append("📲 PRÉ VENDA EXCLUSIVA NO WHATSAPP")
                if cartao_credito:
                    destaques.append("💳 Dividido em até 12x no cartão de crédito com apenas 10% de taxa.")
                if destaques:
                    mensagem = mensagem + "\n\n" + "\n\n".join(destaques)

                st.session_state["mensagem"] = mensagem
                st.session_state["custo"] = custo

                components.html(
                    f"""<script>
(function(){{
    var t = {json.dumps(mensagem)};
    var d = {json.dumps(dolar_str.strip())};
    var p = window.parent;
    if (p.navigator.clipboard) {{
        p.navigator.clipboard.writeText(t).catch(function() {{ fb(t); }});
    }} else {{ fb(t); }}
    function fb(t) {{
        var e = p.document.createElement('textarea');
        e.value = t;
        e.style.position = 'fixed';
        e.style.opacity = '0';
        p.document.body.appendChild(e);
        e.focus();
        e.select();
        try {{ p.document.execCommand('copy'); }} catch(err) {{}}
        p.document.body.removeChild(e);
    }}
    // Lembrar o último dólar usado (localStorage + URL, sem recarregar).
    if (d) {{
        try {{
            p.localStorage.setItem('prevendas_dolar', d);
            var u = new URL(p.location.href);
            u.searchParams.set('dolar', d);
            p.history.replaceState(null, '', u);
        }} catch(err) {{}}
    }}
}})();
</script>""",
                    height=0,
                )
                st.toast("✅ Mensagem copiada automaticamente!")

            except ValueError:
                st.error("Valores inválidos! Use números válidos (ex: 29.99).")

    mensagem_atual = st.session_state.get("mensagem", "")
    custo_atual = st.session_state.get("custo", None)

    if mensagem_atual:
        st.code(mensagem_atual, language=None)

        if custo_atual is not None:
            st.divider()
            st.markdown("**📊 Informação Interna**")
            st.success(f"Custo: R$ {custo_atual:.2f}")
    else:
        st.markdown("*Preencha o formulário e clique em **Gerar Mensagem**.*")
