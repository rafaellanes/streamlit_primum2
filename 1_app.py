import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd
import streamlit as st

load_dotenv()

DB_USER     = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_TABLE    = os.getenv('DB_TABLE') 
DB_HOST     = os.getenv('DB_HOST')


print(DB_PASSWORD)
print(DB_USER)
def conectando_bd():
# Conectando ao banco de dados
    conn = psycopg2.connect(
        dbname=DB_TABLE,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )

    # Criando um cursor

    return conn

connect_bd = conectando_bd()

query = """
    select
        "SK_TEMPO_DATA_PAGAMENTO"
        ,"TIPO_VENDA"
        ,SUM("RECEITA_CONTRATADA")
    from receita_contratada
    where "SK_TEMPO_DATA_PAGAMENTO" >= '2024-08-01'
    group by "SK_TEMPO_DATA_PAGAMENTO","TIPO_VENDA"
    order by "SK_TEMPO_DATA_PAGAMENTO" ASC
"""

df_vendas = pd.read_sql_query(query,connect_bd)

st.dataframe(df_vendas)