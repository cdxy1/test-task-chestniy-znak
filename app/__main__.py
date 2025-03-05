from app.data_filler import fill_whole_data
from app.handler import process_document

if __name__ == "__main__":
    fill_whole_data()

    while True:
        result = process_document()
        if not result:
            break
