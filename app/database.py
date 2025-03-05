import psycopg2

from app.config import Config
from app.logger import get_logger

logger = get_logger()


def execute_query(query: str, values: tuple = None):
    with psycopg2.connect(**Config.DB_DICT) as conn:
        with conn.cursor() as cur:

            try:
                if values:
                    cur.execute(query, values)
                else:
                    cur.execute(query)
                conn.commit()
                if cur.description:
                    return cur.fetchall()
                return None
            except psycopg2.Error as e:
                conn.rollback()
                logger.error(f"Error: {e}")


def create_tables():
    stmt = """
                CREATE TABLE IF NOT EXISTS public.data
            (
                object character varying(50) COLLATE pg_catalog."default" NOT NULL,
                status integer,
                level integer,
                parent character varying COLLATE pg_catalog."default",
                owner character varying(14) COLLATE pg_catalog."default",
                CONSTRAINT data_pkey PRIMARY KEY (object)
            );
                CREATE TABLE IF NOT EXISTS public.documents
            (
                doc_id character varying COLLATE pg_catalog."default" NOT NULL,
                recieved_at timestamp without time zone,
                document_type character varying COLLATE pg_catalog."default",
                document_data jsonb,
                processed_at timestamp without time zone,
                CONSTRAINT documents_pkey PRIMARY KEY (doc_id)
            )
            """

    execute_query(stmt)
