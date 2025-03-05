import datetime
import json
import random
import uuid

from app.database import execute_query, create_tables

inns = ["owner_1", "owner_2", "owner_3", "owner_4"]
status = [1, 2, 3, 4, 10, 13]
d_type = ["transfer_document", "not_transfer_document"]


def make_data() -> dict:
    """Генерация рандомных данных для таблицы data в базе, вернёт list, внутри dict по каждой записи"""
    parents = set()
    children = dict()
    data_table = dict()

    for _ in list(range(0, 20)):
        parents.add("p_" + str(uuid.uuid4()))

    for p in parents:
        children[p] = set()
        # Не очень понятно зачем здесь list.
        for _ in range(0, 50):
            children[p].add("ch_" + str(uuid.uuid4()))

    for k, ch in children.items():
        data_table[k] = {
            "object": k,
            "status": random.choice(status),
            "owner": random.choice(inns),
            "level": 1,
            "parent": None,
        }

        for x in ch:
            data_table[x] = {
                "object": x,
                "status": random.choice(status),
                "owner": data_table[k]["owner"],
                "level": 0,
                "parent": k,
            }
    return data_table


def make_documents(data: dict) -> list:
    """Генерация рандомных данных для таблицы documents в базе, вернёт list, внутри dict по каждой записи"""
    result = list()
    doc_count = random.choice(range(10, 20))
    for _ in range(doc_count):
        result.append(__make_doc(data))
    return result


def __make_doc(data: dict) -> dict:
    saler = reciver = random.choice(inns)
    while saler == reciver:
        reciver = random.choice(inns)

    doc = dict()
    dd = doc["document_data"] = dict()
    dd["document_id"] = id = str(uuid.uuid4())
    dd["document_type"] = random.choice(d_type)

    doc["objects"] = [
        x for x, v in data.items() if v["level"] == 1 and v["owner"] == saler
    ]

    md = doc["operation_details"] = dict()

    if random.choice([0, 1]):
        mds = md["status"] = dict()
        mds["new"] = mds["old"] = random.choice(status)
        while mds["old"] == mds["new"]:
            mds["new"] = random.choice(status)

    if dd["document_type"] == d_type[0]:
        mdo = md["owner"] = dict()
        mdo["new"] = mdo["old"] = random.choice(inns)
        while mdo["old"] == mdo["new"]:
            mdo["new"] = random.choice(inns)

    doc_data = {
        "doc_id": id,
        "recieved_at": datetime.datetime.now(),
        "document_type": dd["document_type"],
        "document_data": json.dumps(doc),
    }
    return doc_data


def add_into_data_table(data: list):
    for d in data:
        query = """INSERT INTO public.data (object, status, level, parent, owner) VALUES (%s, %s, %s, %s, %s)"""
        execute_query(query, (d['object'], d['status'], d['level'], d['parent'], d['owner']))


def add_into_documents_table(data: list):
    for d in data:
        query = """INSERT INTO public.documents (doc_id, recieved_at, document_type, document_data) VALUES (%s, %s, %s, %s)"""
        execute_query(query, (d['doc_id'], d['recieved_at'], d['document_type'], d['document_data']))


def fill_whole_data():
    data = make_data()
    # данные для базы:
    data_tbl = list(data.values())
    documents_tbl = make_documents(data)

    create_tables()
    add_into_data_table(data_tbl)
    add_into_documents_table(documents_tbl)