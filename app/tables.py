import psycopg2

from .config import Config


def create_tables():
    with psycopg2.connect(**Config.DB_DICT) as conn:
        with conn.cursor() as cur:

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

            try:
                cur.execute(stmt)
                conn.commit()
            except psycopg2.Error:
                conn.rollback()
