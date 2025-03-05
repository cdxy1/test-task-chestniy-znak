import json
from datetime import datetime, timezone
from typing import Optional, Tuple, List, Dict, Any

from app.database import execute_query
from .logger import get_logger

logger = get_logger()


def get_unprocessed_document() -> Optional[Tuple[str, Dict[str, Any]]]:
    query = """
        SELECT doc_id, document_data
        FROM documents
        WHERE document_type = 'transfer_document' AND processed_at IS NULL
        ORDER BY recieved_at ASC
        LIMIT 1
        FOR UPDATE SKIP LOCKED;
    """
    result = execute_query(query)
    if result:
        doc_id, document_data = result[0]
        if isinstance(document_data, str):
            return doc_id, json.loads(document_data)
        return doc_id, document_data
    return None


def get_all_related_objects(parent_objects: List[str]) -> List[str]:
    all_objects = set(parent_objects)
    for obj in parent_objects:
        query = """
            SELECT object FROM data WHERE parent = %s;
        """
        result = execute_query(query, (obj,))
        if result:
            all_objects.update([row[0] for row in result])
    return list(all_objects)


def update_data_objects(objects: List[str], operation_details: Dict[str, Dict[str, Any]]) -> bool:
    try:
        for field, details in operation_details.items():
            old_value = details['old']
            new_value = details['new']

            if isinstance(old_value, list):
                query = f"""
                    UPDATE data
                    SET {field} = %s
                    WHERE object = ANY(%s) AND {field} = ANY(%s);
                """
                execute_query(query, (new_value, objects, old_value))
            else:
                query = f"""
                    UPDATE data
                    SET {field} = %s
                    WHERE object = ANY(%s) AND {field} = %s;
                """
                execute_query(query, (new_value, objects, old_value))
        return True
    except Exception as e:
        logger.error(f"Error updating data: {e}")
        return False


def mark_document_as_processed(doc_id: str) -> bool:
    query = """
        UPDATE documents
        SET processed_at = %s
        WHERE doc_id = %s;
    """
    try:
        execute_query(query, (datetime.now(timezone.utc), doc_id))
        return True
    except Exception as e:
        logger.error(f"Error marking document {doc_id} as processed: {e}")
        return False


def process_document() -> bool:
    document = get_unprocessed_document()
    if not document:
        logger.warning("No documents to process.")
        return False

    doc_id, doc_data = document
    logger.info(f"Processing document: {doc_id}")

    objects_to_update = get_all_related_objects(doc_data['objects'])
    logger.info(f"Objects to update: {objects_to_update}")

    operation_details = doc_data.get('operation_details', {})
    if not update_data_objects(objects_to_update, operation_details):
        logger.error("Failed to update data objects.")
        return False

    if not mark_document_as_processed(doc_id):
        logger.error("Failed to mark document as processed.")
        return False

    logger.info(f"Document {doc_id} processed successfully.")
    return True
