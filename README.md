# Тестовое задание "Честный Знак"
****

#### Как запустить:
1. Нужно запустить docker контейнер с бд:``docker compose up -d --build``
2. Запустить скрипт: ``python -m app``

#### Примечания:
* Провел небольшой рефакторинг, так как не понял зачем в модулу в data_filler в некоторых циклах приводит результат функции range к list.
* Добавил логгирование, чтобы было удобно отслеживать процесс выполнения.
* Также добавил точку входа для пакета, чтобы Вам протестировать модуль.
* Тесты писать не стал, так как мне показалось, что для тестового задания это излишне.
* Не стал писать докстринги, т.к. код в целом и так понятный. 