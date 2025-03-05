# test_task_doc_process

## Подготовка: 
Запустить этот скрипт data_filler.py для генерации данных для задачи, перенести данные в базу

    
## Легенда: 
есть таблица documents с условными документами, которые поступают от клиентов,
есть таблица data с условными объектами, которые содержатся в документах, они могут быть связаны полем parent, 
в этом случае условный объект считаем упаковкой, а дочерние элементы, 
у которых он заполнен в поле parent - содержимым упаковки

## Критерии оценки решения:
- результат работы соответствует ТЗ
- читабельность кода
- удобство поддержки
  
_Представьте, что ваше решение досталось вам и теперь нужного поддерживать и развивать_

## Создание таблиц в postgres для задачи:
```
CREATE TABLE IF NOT EXISTS public.data
(
    object character varying(50) COLLATE pg_catalog."default" NOT NULL,
    status integer,
    level integer,
    parent character varying COLLATE pg_catalog."default",
    owner character varying(14) COLLATE pg_catalog."default",
    CONSTRAINT data_pkey PRIMARY KEY (object)
)
```
```
CREATE TABLE IF NOT EXISTS public.documents
(
    doc_id character varying COLLATE pg_catalog."default" NOT NULL,
    recieved_at timestamp without time zone,
    document_type character varying COLLATE pg_catalog."default",
    document_data jsonb,
    processed_at timestamp without time zone,
    CONSTRAINT documents_pkey PRIMARY KEY (doc_id)
)
```


## Тестовое задание:
Написать алгоритм обработки документов из таблицы documents по условиям

Пример структуры json документа из поля document_data:
```
{
    "document_data": {
        "document_id": "25e91d56-696e-4be6-952c-4089593877a7",
        "document_type": "transfer_document"
    },
    "objects": [
        "p_effe6195-cc7f-44c2-a02c-46fc07dcd3e6",
        "p_8943e9fb-a2e7-4344-8c48-91d3a4fbdb0c",
    ],
    "operation_details": {
        "owner": {
            "new": "owner_4",
            "old": "owner_3"
        }
    }
}
```

После запуска скрипта он должен брать из таблицы documents 1 необработанный документ (сортировка по полю recived_at ASC) с типом transfer_document и обрабатывать по алгоритму: 


1. взять объекты из ключа objects
2. собрать полный список объектов из таблицы data, учитывая, что в ключе objects содержатся объекты, у которых 
   есть связанные дочерние объекты (связь по полю parent таблицы datа)
3. изменить данные для объектов в таблице data, если они подходят под условие блока operation_details, где каждый ключ это название поля, внутри блок со старым значением в ключе old, которое нужно 
   проверить, и новое значение в ключе new, на которое нужно изменить данные.

   Пример: 
   ```
    "owner": {
        "new": "owner_4",
        "old": "owner_3"
    },
   "название поля в бд": {
        "new": "значение, на которое меняем",
        "old": "старое значение, которе нужно проверить, может быть массивом"
    }
    ```

5. после обработки документа в таблице documents поставить отметку времени в поле processed_at, это будет означать, что документ обработан
6. Если всё завершилось успешно, возвращаем True, если нет - False
