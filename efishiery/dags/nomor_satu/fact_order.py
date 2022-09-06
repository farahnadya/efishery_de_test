from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd


def main_fact():
    df_ops = select_ops_table()
    df_dwh = select_dwh_table()
    df = unique_value(df_ops, df_dwh)
    insert_dwh_table(df)
    print('sukses')

def select_ops_table():
    hook = PostgresHook(postgres_conn_id="efishery")
    conn = hook.get_conn()
    sql = """
        select 
            replace(o.date ::varchar(122),'-','')::int as  order_date_id
            ,replace(i.date ::varchar(122),'-','')::int as invoice_date_id
            ,replace(p.date ::varchar(122),'-','')::int as payment_date_id		 
            ,o.order_number 
            ,o.customer_id
            ,i.invoice_number
            ,p.payment_number
            ,sum(quantity) as total_order_quantity
            ,sum(quantity * usd_amount) as total_order_usd_amount
            ,i.date - o.date as order_to_invoice_lag_days
            ,p.date - i.date as invoice_to_payment_lag_days
        from 
            orders as o  inner join 
            invoices as i on o.order_number = i.order_number inner join 
            payments as p on i.invoice_number = p.invoice_number inner join 
            order_lines as ol on o.order_number = ol.order_number
        group by 
            1,2,3,4,5,6,7,10,11
        """
    df = pd.read_sql(sql, conn)
    return df

def select_dwh_table():
    hook = PostgresHook(postgres_conn_id="efishery_dwh")
    conn = hook.get_conn()
    sql = """
    select 
        f.order_number
    from 
	    fact_order_accumulating f  
        """
    df = pd.read_sql(sql, conn)
    return df

def unique_value(df_ops, df_dwh):
    df = df_ops[~df_ops.order_number.isin(df_dwh.order_number)]
    df = df.drop_duplicates().reset_index(drop=True)
    return df

def insert_dwh_table(df):
    table = "fact_order_accumulating"
    hook = PostgresHook(postgres_conn_id="efishery_dwh")
    conn = hook.get_conn()
    cursor = conn.cursor()
    cols = ",".join([str(i) for i in df.columns.tolist()])
    for i, row in df.iterrows():
        sql = "INSERT INTO "+table+" (" + cols + ") VALUES (" + "%s," * (len(row) - 1) + "%s)"
        cursor.execute(sql, tuple(row))
    return conn.commit()