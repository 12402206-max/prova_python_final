import streamlit as st
import pandas as pd
import plotly.express as px

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Painel  SAEB 2023 - Belo Horizonte", layout="wide")

ARQUIVO = "saeb_aprendizado_territorios-7-2023-EM.xlsx"

@st.cache_data
def carregar(caminho):
    if caminho.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(caminho)
    for sep in [";", ","]:
        for enc in ["utf-8", "latin-1"]:
            try:
                d = pd.read_csv(caminho, sep=sep, encoding=enc, decimal=",")
                if d.shape[1] > 1:
                    return d
            except Exception:
                pass
    return pd.read_csv(caminho)

df = carregar(ARQUIVO)
df.columns = df.columns.str.strip()   

for col in ["uf", "lingua portuguesa adequado", "matematica adequado", "lingua portguesa insuficiente", "lingua portuguesa basico", "lingua portguesa proficiente", "lingua portguesa avancado", "matematica basico", "matematica proficiente", "matematica avancado"]:
    if col in df.columns and df[col].dtype == object:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "."), errors="coerce")

UF1 = "MG"
UF2 = "BA"
UF3 = "CE"
UF4 = "PR"
COR_1 = "#FF6B6B"
COR_2 = "#00F5D4"
CORES = {UF1: COR_1, UF2: COR_2, UF3: COR_1, UF4: COR_2}

df_filtrado = df[
   (df["uf"].isin([UF1, UF2, UF3, UF4])) 
].copy()

df_tabela = df_filtrado[["uf", "lingua portuguesa insuficiente", "matematica insuficiente"]]

st.title(f"Painel Streamlit do SAEB 2023 de Belo Horizonte — {UF1}, {UF2}, {UF3}, E {UF4}")

st.sidebar.header("Controles")
opcao = st.sidebar.radio("Selecione a visualização:", ["Tabela", "Gráficos"])

if opcao == "Tabela":
    st.header("Tabela do  SAEB 2023")
    st.dataframe(df_tabela, use_container_width=True, hide_index=True)

elif opcao == "Gráficos":
    st.header(f"Gráficos do  SAEB 2023 — {UF1}, {UF2}, {UF3}, {UF4}. NAO DEU TEMPO DE FAZER PROFESSORA, PERDAO")

 