import psycopg2
from psycopg2.extras import execute_values


# Подключение к базе данных postgres

#conn = psycopg2.connect(
#dbname="my_project",
#user="name",
#password="pass",
#host="localhost",
#port="5432"
#)

conn = psycopg2.connect("postgresql://postgres:1499sd9327@localhost/my_project")

cursor = conn.cursor()

# создаём таблицу people
#cursor.execute("CREATE TABLE Students(id SERIAL PRIMARY KEY, name VARCHAR(50), student_card INTEGER, "
               #"year_of_admission Date, stage_of_education VARCHAR(50), year_of_graduation Date,"
               #"indicator boolean, id_department INTEGER)")
#conn.commit()

#cursor.execute("CREATE TABLE Graduation_work(id SERIAL PRIMARY KEY, name VARCHAR(50), mark INTEGER, id_student INTEGER)")
#conn.commit()

#cursor.execute("CREATE TABLE Department(id SERIAL PRIMARY KEY, name VARCHAR(50), head_name VARCHAR(50))")
#conn.commit()

#cursor.execute("ALTER TABLE Graduation_work ADD CONSTRAINT id_student FOREIGN KEY (id_student) REFERENCES Students(id)")
#conn.commit()

#cursor.execute("ALTER TABLE Students ADD CONSTRAINT id_department FOREIGN KEY (id_department) REFERENCES Department(id)")
#conn.commit()

people = [("Иванов И.И.", 2346743, "2020.09.01", "бакалавриат", "2024.08.31", "Учится", 1),
          ("Петров П.П.", 5893455, "2020.09.01","бакалавриат", "2024.08.31", "Учится", 2),
          ("Смирнов И.И.", 1278923, "2020.09.01", "бакалавриат", "2024.08.31", "Учится", 2)]

cafedra = [("дифференциальных уравнений", "Бережной Е.И"),
           ("математического анализа", "Невский М.В."),
           ("математического моделирования", "Кащенко И.С.")]

gd_work = [("Численное решение дифференциальных уравнений", 5, 2346743), ("Математические методы в логистике", 5, 5893455),
           ("устойчивость дифференциальных уравнений", 4, 1278923)]

#execute_values(cursor, "INSERT INTO students (name, student_card, "
 #              "year_of_admission, stage_of_education, year_of_graduation,"
  #         "indicator, id_department) VALUES %s", people)
#conn.commit()
#execute_values(cursor, "insert into Department(name, head_name) values %s", cafedra)
#conn.commit()
#execute_values(cursor, "INSERT INTO graduation_work (name, mark, id_student) values %s", gd_work)
#conn.commit()

#cursor.execute("ALTER SEQUENCE graduation_work_id_seq RESTART WITH 1")
#conn.commit()

cursor.execute("Select * from students")
#cursor.
for data in cursor.fetchall():
    print(data)



cursor.close()
conn.close()