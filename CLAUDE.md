# CLAUDE.md — Pré-Vendas WhatsApp

> **Fluxo obrigatório:** SEMPRE ler este arquivo ANTES de qualquer alteração no projeto, e DEPOIS de implementar, atualizar este arquivo com as mudanças feitas.

## O que é

Aplicativo web para automatizar a geração de mensagens de pré-venda de **miniaturas colecionáveis** (carros diecast) para WhatsApp. Calcula o preço de venda a partir do preço em dólar, cotação e frete, aplicando a regra de cada distribuidor, e formata uma mensagem pronta para copiar e colar.

- **Repositório:** https://github.com/ericklesv/prevendas-whatsapp
- **Branch principal:** `master`
- **Idioma:** Português (BR)

## Stack

- **Python** + **Streamlit** (`streamlit>=1.32.0`) — única dependência.
- Aplicação de arquivo único: toda a lógica está em `app.py` (~171 linhas).
- Deploy via **Railway** usando o `Procfile`.

## Estrutura de arquivos

| Arquivo | Função |
|---|---|
| `app.py` | App Streamlit completo: lógica de cálculo + UI. |
| `requirements.txt` | Dependências (apenas streamlit). |
| `Procfile` | Comando de deploy Railway: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`. |
| `instalar.bat` | Instala dependências localmente (Windows). |
| `executar.bat` | Roda `python app.py` localmente. ⚠️ Desatualizado: app é Streamlit, deve rodar com `streamlit run app.py`. |
| `criar_exe.bat` | Gera `.exe` com PyInstaller (legado da versão desktop). |
| `.gitignore` | Padrão Python. |

> **Nota histórica:** o último commit (`fb165ab`) migrou o app de desktop para **Streamlit**. Os arquivos `.bat` (`executar.bat`, `criar_exe.bat`) são remanescentes da versão antiga e podem estar inconsistentes com o estado atual.

## Lógica de negócio (`app.py`)

### Distribuidores
Lista `DISTRIBUIDORES` com 10 fornecedores: `ALISSON`, `MINI GT`, `JCAR`, `MINI DELAS`, `MATTEL CREATIONS`, `MG PRO ALISSON`, `EBAY`, `SUPER MINI`, `DIECAST USA`, `VEIGA`.

**Distribuidores sem dólar:** a lista `DISTRIBUIDORES_SEM_DOLAR` (atualmente `["VEIGA"]`) marca fornecedores cujo preço **já está em reais**. Para esses:
- O campo "Preço" muda o label para `Preço (R$)` e o campo "Dólar" fica **desabilitado** e não é exigido na validação.
- No cálculo, `dolar` é forçado para `0.0`.
- Ao adicionar um novo distribuidor em reais, basta incluí-lo nessa lista além das fórmulas.

### Duas funções centrais (cada distribuidor tem fórmula própria)
- **`calcular_custo(distribuidor, preco, dolar, frete)`** — custo interno (sem margem).
- **`calcular_preco(distribuidor, preco, dolar, frete)`** — preço de venda = custo × margem (multiplicador varia por distribuidor, ex: 1.25, 1.26, 1.27, 1.5).

⚠️ **Importante:** as fórmulas de custo e preço estão duplicadas (o `calcular_preco` repete a expressão do custo e multiplica pela margem). Ao alterar uma fórmula de custo, **alterar também em `calcular_preco`** para manter consistência.

### Tipos de pré-venda (`TIPOS_PREVENDA`)
- **`PRÉ VENDA EUA`** — envio em até 2 meses. Sem entrada fixa: divide em 50% agora + 50% na chegada.
- **`LONGO PRAZO`** — exige data prevista de lançamento. Sem entrada fixa: R$25,00 na reserva + restante na chegada.

### Entrada fixa (opcional)
Checkbox que, quando marcada, substitui a divisão padrão (50/50 ou R$25) por um valor de entrada informado pelo usuário; o restante = total − entrada.

### Formatação de valores
- O preço final é arredondado para cima com `math.ceil`.
- Inputs aceitam vírgula ou ponto decimal (`.replace(",", ".")`).
- A mensagem usa markdown do WhatsApp (`*negrito*`) e emojis (💰 ➗ 📦 📅).

### UI (Streamlit)
- Layout em duas colunas: formulário (esquerda) / mensagem gerada (direita).
- Resultado guardado em `st.session_state` (`mensagem`, `custo`).
- Exibe **"Informação Interna"** com o custo (uso interno, não vai pra mensagem do cliente).

## Como rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Convenções

- Manter tudo em português.
- App de arquivo único — evitar fragmentar sem necessidade.
- Ao adicionar/alterar distribuidor: atualizar a lista `DISTRIBUIDORES` **e** as duas funções de cálculo.

## Histórico de mudanças (manter atualizado)

- **2026-06-17** — Adicionado distribuidor **VEIGA** (preço já em reais, sem dólar). Fórmula: custo = `preco + frete`; preço = `(preco + frete) * 1.31`. Criada lista `DISTRIBUIDORES_SEM_DOLAR`, campo Dólar desabilitado/opcional e validação ajustada para esses casos.
- **2026-06-17** — Criação deste CLAUDE.md a partir da análise inicial do projeto.
- **fb165ab** — Migração do app para Streamlit (deploy Railway).
