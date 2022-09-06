from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd


def main_customer():
    df_ops = select_ops_table()
    df_dwh = select_dwh_table()
    df = unique_value(df_ops, df_dwh)
    insert_dwh_table(df)
    print('sukses')

def select_ops_table():
    # step 1: query data from postgresql db and save into text file
    hook = PostgresHook(postgres_conn_id="efishery")
    conn = hook.get_conn()
    sql = """
    select 
        c.id
        ,c.name
    from 
	    customers c 
        """
    df = pd.read_sql(sql, conn)
    return df

def select_dwh_table():
    # step 1: query data from postgresql db and save into text file
    hook = PostgresHook(postgres_conn_id="efishery_dwh")
    conn = hook.get_conn()
    sql = """
    select 
        d.id
    from 
	    dim_customer d 
        """
    df = pd.read_sql(sql, conn)
    return df

def unique_value(df_ops, df_dwh):
    df = df_ops[~df_ops.id.isin(df_dwh.id)]
    df = df.drop_duplicates().reset_index(drop=True)
    return df

def insert_dwh_table(df):
    table = "dim_customer"
    hook = PostgresHook(postgres_conn_id="efishery_dwh")
    conn = hook.get_conn()
    cursor = conn.cursor()
    cols = ",".join([str(i) for i in df.columns.tolist()])
    for i, row in df.iterrows():
        sql = "INSERT INTO "+table+" (" + cols + ") VALUES (" + "%s," * (len(row) - 1) + "%s)"
        cursor.execute(sql, tuple(row))
    return conn.commit()