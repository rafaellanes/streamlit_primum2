import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta



# Data de hoje menos 1 dia
data_ontem = datetime.now() - timedelta(days=1)

# Apenas a data, sem hora
data1 = data_ontem.date()

load_dotenv()

DB_USER     = os.getenv('DB_USER') + ".lanes"
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_TABLE    = os.getenv('DB_TABLE') 
DB_HOST     = os.getenv('DB_HOST')

def conectando_bd(DB_PASSWORD,DB_TABLE,DB_HOST):
# Conectando ao banco de dados
    conn = psycopg2.connect(
        dbname=DB_TABLE,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )

    # Criando um cursor

    return conn

connect_bd = conectando_bd(DB_PASSWORD,DB_TABLE,DB_HOST)

query = """
    select
        "SK_TEMPO_DATA_PAGAMENTO" AS DT_PAGAMENTO
        ,"TIPO_VENDA" AS TIPO
        ,'R$ '|| TO_CHAR(SUM("RECEITA_CONTRATADA"),'999G999G999D00') AS SOMA
    from receita_contratada
    where "SK_TEMPO_DATA_PAGAMENTO" >= '2024-08-01'
    group by "SK_TEMPO_DATA_PAGAMENTO","TIPO_VENDA"
    order by "SK_TEMPO_DATA_PAGAMENTO" ASC
"""

query_class ="""
with
base
as
(
	SELECT
		"NOME_ASSINATURA" as curso
		,cast(COUNT("NOME_ASSINATURA") as numeric) AS quantidade
		,'R$ ' || TO_CHAR(SUM("RECEITA_CONTRATADA"), '999G999G999D00') AS soma_receita
		,round((SUM("RECEITA_CONTRATADA") / (SELECT SUM("RECEITA_CONTRATADA") FROM receita_contratada WHERE "SK_TEMPO_DATA_PAGAMENTO" >= '2024-08-01')) *100,2) AS proporcao_receita
		,round((cast(COUNT("NOME_ASSINATURA") as numeric)/  (SELECT cast(COUNT("NOME_ASSINATURA") as numeric) FROM receita_contratada WHERE "SK_TEMPO_DATA_PAGAMENTO" >= '2024-08-01'))*100,2) AS proporcao_qtd
	FROM receita_contratada
	WHERE "SK_TEMPO_DATA_PAGAMENTO" >= '2024-08-01'
	GROUP BY "NOME_ASSINATURA"
	ORDER BY quantidade DESC
	LIMIT 5
	)
select 
	curso
	,quantidade
	,soma_receita
	,proporcao_receita AS FREQ_RELATIVA_RECEITA
	,proporcao_qtd AS FREQ_RELATIVA_QTD
from base
    """

df_vendas = pd.read_sql_query(query,connect_bd)

df_classificacao = pd.read_sql_query(query_class,connect_bd)

col1,col2 = st.columns(2)

st.title("Vendas referente Agosto Solidário")

st.header("Atualização do dia 14-08-2024 ainda está acontecendo")

st.subheader("O dia 14-08-2024 ainda não foi contemplado totalmente")


st.write(f"Vendas filtradas do dia 2024-08-01 até {data1}")
st.dataframe(df_vendas)

st.write ("Top 5 Cursos mais vendido")
st.dataframe(df_classificacao)
