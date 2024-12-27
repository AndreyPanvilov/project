## Стуктура БД
файлы table_Department.py, table_Students.py, table_archive.py, table_graduation_work.py - создают таблицы в БД postgress

В БД созданы два пользователя (админ и пользователь) для каждого сушествует собственный пароль,
подключение идет через

url: "postgresql://user_name:pass@localhost/bd_name"

Админ имеет права на любые манипуляции с БД

Пользователь может просматривать, заносить информацию, редактировать поля для students, graduation_work, department;
также просматривать информацию из архива(archive).

Все манипуляции с БД происходят посредством методов get и post API;

Для пользователя не имеющего прав на то или иное действие сервер вернет ошибку 403 Forbidden.

## API
в файле schema.py представлена структура API.

Для запуска сервера необходимо в терминале прописать команду "uvicorn schema:app --reload"

После запуска сервера открыть веб-браузер и перейти по адресу http://127.0.0.1:8000

Документацию можно также открыть по адресу http://127.0.0.1:8000/docs

В начале файла schema.py описаны классы необходимые для валидации данных в методах, далее описаны методы post и get осуществляющие манипуляции с таблицами БД.

Описаны следующие методы:

a) Get:

    1) /student/all - вывод всей информации из таблицы students
    
    2) /grad_work/all - вывод всей информации из таблицы graduation_work
    
    3) /department/all - вывод всей информации из таблицы department
    
    4)/student - вывод информации из таблицы students по id(номеру студенческого) студента
    
    5) /find_info/ - вывод информации по студенту;
    пользователь указывает имя поля, по которому будет происходить отбор и значение этого поля,
    также поля для сортировки и тип сортировки(по возрастанию, убыванию, без сортировки)
    
    6) /all/archive - вывод всех данных из архива
    
b) Post:

    1) /update - обновляет информацию по необходимой таблице и полю
    
    2) /add/student_info - добавляет нового студента
    
    3) /add/cafedra_info - добавляет новую кафедру
    
    4) /add/archive добавляет запись в архив
    
    5) /update/arch - обновляет запись в архиве, метод доступен лишь админу, для пользователя вернет ошибку 403 Forbidden

Валидация данных построена на классах, наследуемых от Basemodel sqlaclchemy, данный инструмент позволяет описывать структуру входных данных, если она не соблюдается, то возвращается ошибка 400 Bad Request

Тесты указаны в файле test.docx
