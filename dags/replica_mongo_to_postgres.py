import logging
import pendulum
import kagglehub
from psycopg2.extras import Json, execute_batch

from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.sensors.python import PythonSensor
from airflow.providers.postgres.hooks.postgres import PostgresHook
import os
import json
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
from airflow.providers.mongo.hooks.mongo import MongoHook

# Конфигурация DAG
OWNER = "a.sorokin"
DAG_ID = "replica_mongo_to_postgresql"


SHORT_DESCRIPTION = "DAG для реплики данных из MongoDB в Postgresql"
LONG_DESCRIPTION = """ 123 """

args = {
    "owner": OWNER,
    "start_date": pendulum.datetime(year=2026, month=2, day=7),
    "retries": 3,
    "depends_on_past": False
}

def check_connect_to_Mongo():
    hook = MongoHook(mongo_conn_id='mongo-db')
    try:
        client = hook.get_conn()
        client.server_info()
        print("Сервер ответил")
        return True
    except Exception as e:
        print("Сервер не ответил")
        return False

def mongo_to_postgres():
    mongo_hook = MongoHook(mongo_conn_id='mongo-db')
    postgres_hook = PostgresHook(postgres_conn_id='postgres-db')

    mongo_client = mongo_hook.get_conn()
    db = mongo_client["replica_db"]
    
    pg_conn = postgres_hook.get_conn()
    cursor = pg_conn.cursor()

    # -------------------------
    # UserSessions
    # -------------------------
    rows = []
    for doc in db["UserSessions"].find():
        rows.append((
            str(doc["_id"]),
            doc.get("user_id"),
            doc.get("start_time"),
            doc.get("end_time"),
            Json(doc.get("pages_visited", {})),
            Json(doc.get("device", {})),
            doc.get("actions", [])
        ))

    execute_batch(cursor, """
        INSERT INTO UserSessions (
                        session_id,
                        user_id,
                        start_time,
                        end_time,
                        pages_visited,
                        device,actions
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (session_id) DO NOTHING
    """, rows)
    pg_conn.commit()


    # -------------------------
    # EventLogs
    # -------------------------
    rows = []
    for doc in db["EventLogs"].find():
        rows.append((
            str(doc["_id"]),
            doc.get("timestamp"),
            doc.get("event_type"),
            Json(doc.get("details", {}))
        ))

    execute_batch(cursor, """
        INSERT INTO EventLogs (
            event_id,timestamp,event_type,details
        )
        VALUES (%s,%s,%s,%s)
        ON CONFLICT (event_id) DO NOTHING
    """, rows)

    pg_conn.commit()

    # -------------------------
    # SupportTickets
    # -------------------------
    rows = []
    for doc in db["SupportTickets"].find():
        rows.append((
            str(doc["_id"]),
            doc.get("user_id"),
            doc.get("status"),
            doc.get("issue_type"),
            Json(doc.get("message", {})),
            doc.get("created_at"),
            doc.get("updated_at")
        ))

    execute_batch(cursor, """
        INSERT INTO SupportTickets (
                    ticket_id,
                    user_id,
                    status,
                    issue_type,
                    message,
                    created_at,
                    updated_at
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (ticket_id) DO NOTHING
    """, rows)
    
    pg_conn.commit()

    # -------------------------
    # UserRecommendations
    # -------------------------
    rows = []
    for doc in db["UserRecommendations"].find():
        rows.append((
            doc.get("user_id"),
            doc.get("last_updated"),
            doc.get("recommended_products", [])
        ))

    execute_batch(cursor, """
        INSERT INTO UserRecommendations (
                        user_id,
                        last_updated,
                        recommended_products
        )
        VALUES (%s,%s,%s)
        ON CONFLICT (user_id) DO NOTHING
    """, rows)

    pg_conn.commit()

    # -------------------------
    # ModerationQueue
    # -------------------------
    rows = []
    for doc in db["ModerationQueue"].find():
        rows.append((
            str(doc["_id"]),
            doc.get("user_id"),
            doc.get("product_id"),
            doc.get("review_text"),
            doc.get("rating"),
            doc.get("moderation_status"),
            doc.get("flags", []),
            doc.get("submitted_at")
        ))

    execute_batch(cursor, """
        INSERT INTO ModerationQueue (
                    review_id,
                    user_id,
                    product_id,
                    review_text,
                    rating,
                    moderation_status,
                    flags,
                    submitted_at
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (review_id) DO NOTHING
    """, rows)
    pg_conn.commit()
    cursor.close()
    

def check_connect_to_Postgres():
    hook = PostgresHook(postgres_conn_id="postgres-db")

    status, msg = hook.test_connection()

    if not status:
        print(f"Подключение не удалось {msg}")
        return False
    print(f"Подключение удалось {msg}")
    return True

def load_csv_to_postgres():
    hook = PostgresHook(postgres_conn_id="postgres-db")

    csv_path = "/opt/airflow/data/IOT-temp_clean.csv"   # путь к CSV
    table_name = "raw_data"

    df = pd.read_csv(csv_path)

    df.to_sql(table_name, hook.get_sqlalchemy_engine(), if_exists='replace', index=False)

    print(f"Данные успешно загружены в таблицу {table_name}")


with DAG(
    dag_id=DAG_ID,
    description=SHORT_DESCRIPTION,
    default_args=args,
    schedule_interval="0 10 * * *",
    tags=["download", "postgres", "convert"],
    concurrency=1
) as dag:

    dag.doc_md=LONG_DESCRIPTION

    start = EmptyOperator(
        task_id = "start"
    )

    end = EmptyOperator(
        task_id = "end"
    )
    
    check_connect_to_Mongo = PythonSensor(
        task_id="check_connect_to_Mongo",
				python_callable=check_connect_to_Mongo
    )

    mongo_to_postgres = PythonOperator(
        task_id="mongo_to_postgres",
        python_callable=mongo_to_postgres
    )


#    load_csv_to_postgres = PythonOperator(
#        task_id="load_csv_to_postgres",
#        python_callable=load_csv_to_postgres
#    )

start >> check_connect_to_Mongo >> mongo_to_postgres >> end

