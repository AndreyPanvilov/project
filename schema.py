import datetime
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import and_
from sqlalchemy.orm import Session
from database import SessionLocal
import datetime
from table_Students import students
from table_Department import Department
from table_graduation_work import Grad_work
from table_archive import archive

app = FastAPI()


class DepartmentGet(BaseModel):
    id: int
    name: str
    head_name: str

    class Config:
        orm_mode = True


class StudentGet(BaseModel):
    name: str
    student_card: int
    year_of_admission: datetime.date
    stage_of_education: str
    year_of_graduation: datetime.date
    indicator: str
    id_department: int

    class Config:
        from_attributes = True


class Graduation_workGet(BaseModel):
    id: int
    name: str
    mark: int
    id_student: int

    class Config:
        from_attributes = True


class StudentInfo(BaseModel):
    name: str
    student_card: int
    year_of_admission: datetime.date
    stage_of_education: str
    year_of_graduation: datetime.date
    indicator: str
    dep_name: str
    work_name: str
    work_mark: int

    class Config:
        from_attributes = True


class upd_val(BaseModel):
    info: str
    id: int
    att_name: str
    new_val: str

    class Config:
        from_attributes = True


class New_dep(BaseModel):
    name: str
    head_name: str

    class Config:
        from_attributes = True


class output_info_student(BaseModel):
    name: str
    student_card: int
    stage_of_education: str
    indicator: str
    dep_name: str
    work_name: str


class getarch(BaseModel):
    name: str
    student_card: int
    year_of_admission: datetime.date
    stage_of_education: str
    year_of_graduation: datetime.date
    dep_name: str
    work_name: str
    work_mark: int

    class Config:
        from_attributes = True


def get_db():
    with SessionLocal() as db:
        return db


@app.get("/student/all", response_model=List[StudentGet])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(students).all()


@app.get("/grad_work/all", response_model=List[Graduation_workGet])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(Grad_work).all()


@app.get("/department/all", response_model=List[DepartmentGet])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(Department).all()


@app.get("/student")
def find_by_id(id, db: Session = Depends(get_db)):
    q = db.query(students).get(id)
    return q


@app.get("/find_info/")
def find_and_ord(name_col, val, ord_col_name, ord, db: Session = Depends(get_db)):
    """
    вывод инф о студенте с возможностью сортировки вывода


    :param name_col: str = имя колонки с приставкой от сущности для кафедры и дипломной работы:
    dep_name, dep_head_name, grad_name, grad_mark, ...


    :param val: str - значение колонки, по которому происходит отбор
    :param ord_col_name: str - колонка сортировки
    :param ord: str = ['desc', 'asc', 'none'] - парам сортировки
    :param db: объект сессии
    :return: List[dict{}]
    """
    q = db.query(Department, students, Grad_work).join(Grad_work, Grad_work.id_student == students.student_card) \
                    .join(Department, Department.id == students.id_department).all()
    l = []
    if name_col[:3] == "dep":
        for i in range(len(q)):
            if getattr(q[i].Department, name_col[4:]) == val:
                l.append(q[i])
        if ord == "asc":
            if ord_col_name[:3] == "dep":
                for i in range(len(l)):
                    for j in range(len(l)):
                        if getattr(l[i].Department, ord_col_name[4:]) < getattr(l[j].Department, ord_col_name[4:]):
                            l[i], l[j] = l[j], l[i]
                return l
            elif ord_col_name[:4] == "grad":
                for i in range(len(l)):
                    for j in range(len(l)):
                        if getattr(l[i].Grad_work, ord_col_name[5:]) < getattr(l[j].Grad_work, ord_col_name[5:]):
                            l[i], l[j] = l[j], l[i]
                return l
            else:
                for i in range(len(l)):
                    for j in range(len(l)):
                        if getattr(l[i].students, ord_col_name) < getattr(l[j].students, ord_col_name):
                            l[i], l[j] = l[j], l[i]
                return l
        elif ord == "desc":
            if ord_col_name[:3] == "dep":
                for i in range(len(l)):
                    for j in range(len(l)):
                        if getattr(l[i].Department, ord_col_name[4:]) > getattr(l[j].Department, ord_col_name[4:]):
                            l[i], l[j] = l[j], l[i]
                return l
            elif ord_col_name[:4] == "grad":
                for i in range(len(l)):
                    for j in range(len(l)):
                        if getattr(l[i].Grad_work, ord_col_name[5:]) > getattr(l[j].Grad_work, ord_col_name[5:]):
                            l[i], l[j] = l[j], l[i]
                return l
            else:
                for i in range(len(l)):
                    for j in range(len(l)):
                        if getattr(l[i].students, ord_col_name) > getattr(l[j].students, ord_col_name):
                            l[i], l[j] = l[j], l[i]
                return l
        else:
            return l
    elif name_col[:4] == "grad":
        for i in range(len(q)):
            if name_col == "grad_mark":
                if getattr(q[i].Grad_work, name_col[5:]) == int(val):
                    l.append(q[i])
            elif getattr(q[i].Grad_work, name_col[5:]) == val:
                l.append(q[i])
        if ord == "asc":
            if ord_col_name[:3] == "dep":
                for i in range(len(l)):
                    for j in range(len(l)):
                        if getattr(l[i].Department, ord_col_name[4:]) < getattr(l[j].Department, ord_col_name[4:]):
                            l[i], l[j] = l[j], l[i]
                return l
            elif ord_col_name[:4] == "grad":
                for i in range(len(l)):
                    for j in range(len(l)):
                        if getattr(l[i].Grad_work, ord_col_name[5:]) < getattr(l[j].Grad_work, ord_col_name[5:]):
                            l[i], l[j] = l[j], l[i]
                return l
            else:
                for i in range(len(l)):
                    for j in range(len(l)):
                        if getattr(l[i].students, ord_col_name) < getattr(l[j].students, ord_col_name):
                            l[i], l[j] = l[j], l[i]
                return l
        elif ord == "desc":
            if ord_col_name[:3] == "dep":
                for i in range(len(l)):
                    for j in range(len(l)):
                        if getattr(l[i].Department, ord_col_name[4:]) > getattr(l[j].Department, ord_col_name[4:]):
                            l[i], l[j] = l[j], l[i]
                return l
            elif ord_col_name[:4] == "grad":
                for i in range(len(l)):
                    for j in range(len(l)):
                        if getattr(l[i].Grad_work, ord_col_name[5:]) > getattr(l[j].Grad_work, ord_col_name[5:]):
                            l[i], l[j] = l[j], l[i]
                return l
            else:
                for i in range(len(l)):
                    for j in range(len(l)):
                        if getattr(l[i].students, ord_col_name) > getattr(l[j].students, ord_col_name):
                            l[i], l[j] = l[j], l[i]
                return l
        else:
            return l
    else:
        for i in range(len(q)):
            if getattr(q[i].students, name_col) == val:
                l.append(q[i])
        if ord == "asc":
            if ord_col_name[:3] == "dep":
                for i in range(len(l)):
                    for j in range(len(l)):
                        if getattr(l[i].Department, ord_col_name[4:]) < getattr(l[j].Department, ord_col_name[4:]):
                            l[i], l[j] = l[j], l[i]
                return l
            elif ord_col_name[:4] == "grad":
                for i in range(len(l)):
                    for j in range(len(l)):
                        if getattr(l[i].Grad_work, ord_col_name[5:]) < getattr(l[j].Grad_work, ord_col_name[5:]):
                            l[i], l[j] = l[j], l[i]
                return l
            else:
                for i in range(len(l)):
                    for j in range(len(l)):
                        if getattr(l[i].students, ord_col_name) < getattr(l[j].students, ord_col_name):
                            l[i], l[j] = l[j], l[i]
                return l
        elif ord == "desc":
            if ord_col_name[:3] == "dep":
                for i in range(len(l)):
                    for j in range(len(l)):
                        if getattr(l[i].Department, ord_col_name[4:]) > getattr(l[j].Department, ord_col_name[4:]):
                            l[i], l[j] = l[j], l[i]
                return l
            elif ord_col_name[:4] == "grad":
                for i in range(len(l)):
                    for j in range(len(l)):
                        if getattr(l[i].Grad_work, ord_col_name[5:]) > getattr(l[j].Grad_work, ord_col_name[5:]):
                            l[i], l[j] = l[j], l[i]
                return l
            else:
                for i in range(len(l)):
                    for j in range(len(l)):
                        if getattr(l[i].students, ord_col_name) > getattr(l[j].students, ord_col_name):
                            l[i], l[j] = l[j], l[i]
                return l


@app.post("/update")
def update(data: upd_val, db: Session = Depends(get_db)):
    """
    :param data:
        :param info: str = [student, grad_work, cafedra]
        :param id: int - id записи для обновления
        :param att_name: str - поле для обновления
        :param new_val: str - новое значение
    :param db:  объект сессии
    """
    if data.info == "student":
        l = ["name", "student_card", "year_of_admission", "stage_of_education", "year_of_graduation", "indicator",
             "id_department"]
        if data.att_name in l:
            q = db.query(students).get(data.id)
            if q:
                if data.att_name == "student_card":
                    #db.commit()
                    #return q1
                    q1 = db.query(Grad_work).filter(Grad_work.id_student == q.student_card).one()
                    q1.id_student = db.query(students).filter(students.student_card != q.student_card).limit(1).one()\
                        .student_card
                    db.commit()
                    setattr(q, data.att_name, int(data.new_val))
                    q1.id_student = data.new_val
                    #return q, q1
                    db.commit()
                else:
                    setattr(q, data.att_name, data.new_val)
                    db.commit()
            else:
                return "данного student_card не существует"
        else:
            raise HTTPException(400)
    elif data.info == "grad_work":
        l = ["name", "mark", "id_student"]
        if data.att_name in l:
            q = db.query(Grad_work).get(data.id)
            if q:
                if data.att_name == "mark":
                    setattr(q, data.att_name, int(data.new_val))
                    db.commit()
                else:
                    setattr(q, data.att_name, data.new_val)
                    db.commit()
            else:
                return "данного id не существует"
        else:
            raise HTTPException(400)

    elif data.info == "cafedra":
        l = ["name", "head_name"]
        if data.att_name in l:
            q = db.query(Department).get(data.id)
            if q:
                setattr(q, data.att_name, data.new_val)
                db.commit()
            else:
                return "кафедры с таким id не существует"
        else:
            raise HTTPException(400)
    else:
        return "в поле info можно ввести 3 значения: student, cafedra, grad_work"


@app.post("/add/student_info")
def add(df: List[StudentInfo], db: Session = Depends(get_db)):
    """
    добавляет необходмую инф по студенту
    :param df: List[class StudentInfo]
    :param db:
    """
    for data in df:
        try:
            q = db.query(Department).filter(Department.name == data.dep_name).one()
            q1 = db.query(Grad_work).order_by(Grad_work.id.desc()).limit(1).one()
            s = students(student_card=data.student_card, name=data.name, year_of_admission=data.year_of_admission,
                           indicator=data.indicator, stage_of_education=data.stage_of_education,
                           year_of_graduation=data.year_of_graduation, id_department=q.id)
            g = Grad_work(name=data.work_name, mark=data.work_mark, id=q1.id + 1, id_student=data.student_card)
            db.add(s)
            db.add(g)
            db.commit()

        except:
            print()
            continue


@app.post("/add/cafedra_info")
def add(data: List[New_dep], db: Session = Depends(get_db)):
    """
    :param data: List[class New_dep]
    :param db:
    """
    q = db.query(Department).order_by(Department.id.desc()).limit(1).one()
    id = q.id
    for i in data:
        ans = Department(name=i.name, id=id+1, head_name=i.head_name)
        id += 1
        db.add(ans)
        db.commit()
    return "запись успено добавлена"


@app.post("/add/archive")
def add_arch(df: List[getarch], db: Session = Depends(get_db)):
    for data in df:
        a = archive(name=data.name, student_card=data.student_card, year_of_admission=data.year_of_admission,
                    stage_of_education=data.stage_of_education, year_of_graduation=data.year_of_graduation,
                    department_name=data.dep_name, graduated_work_name=data.work_name, graduated_work_mark=data.work_mark)
        db.add(a)
        db.commit()


@app.post("/update/arch")
def upd_arch(id, col_name, val, db: Session = Depends(get_db)):
    q = db.query(archive).get(id)
    setattr(q, col_name, val)
    db.commit()


