import psycopg2
import psycopg2.extras
from flask import flash


class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

# вносим данные в бд о регистрации админа
    def add_account_admin(self, login, password, fcs):
        self.__cursor.execute("INSERT INTO admin (login, password, fcs) VALUES (%s,%s,%s)",
                              (login, password, fcs))
        self.__db.commit()

# вносим данные в бд о регистрации мастера
    def add_account_master(self, login, password, fcs):
        self.__cursor.execute("INSERT INTO master (login, password, fcs) VALUES (%s,%s,%s)",
                              (login, password, fcs))
        self.__db.commit()

# получаем данные об админе при логировании
    def get_admin(self, login):
        self.__cursor.execute('SELECT * FROM admin WHERE login = %s', (login,))
        admin = self.__cursor.fetchone()
        return admin

# получаем данные о мастере при логировании
    def get_master(self, login):
        self.__cursor.execute('SELECT * FROM master WHERE login = %s', (login,))
        master = self.__cursor.fetchone()
        return master

# получаем данные об услугах
    def get_service(self):
        self.__cursor.execute("SELECT name_of_the_service, time, cost, id_service FROM service")
        service = self.__cursor.fetchall()
        return service

# добавляем данные об услугах
    def add_service(self, id_service, name_of_the_service, time, cost, id_type_service):
        try:
            self.__cursor.execute("""INSERT INTO service (id_service, name_of_the_service, time, cost, id_type_service)
                                  VALUES (%s,%s,%s,%s,%s)""",
                                  (id_service, name_of_the_service, time, cost, id_type_service))
            self.__db.commit()
        except:
            flash('Ошибка')
            return redirect(url_for('addservice'))

# удаляем данные об услугах
    def del_service(self, id_service):
        self.__cursor.execute(f"DELETE FROM service WHERE id_service='{id_service}'")
        self.__db.commit()

# выбираем дату рабочей смены
    def get_date(self, date):
        self.__cursor.execute(f"SELECT date FROM work_day WHERE date='{date}'")
        timetable = self.__cursor.fetchall()
        return timetable

 # добавляем мастера на смену
    def add_mastertt(self, id_employee_master, date):
        self.__cursor.execute("""INSERT INTO master_work_day (id_employee_master, date)
                                VALUES (%s,%s)""",
                                (id_employee_master, date))
        self.__db.commit()


# получаем мастеров для селекта
    def getsel_master(self):
        self.__cursor.execute("SELECT id_employee_master, fcs FROM master")
        gsel_master = self.__cursor.fetchall()
        return gsel_master


# удаляем мастера из расписания
    def del_master(self, id_employee_master, date):
        self.__cursor.execute(f"""DELETE FROM master_work_day WHERE id_employee_master='{id_employee_master}'
                              AND date='{date}'""")
        self.__db.commit()

# получаем данные о зарегистировавшемся мастере при активном сеансе админа (?)
    def get_ttmaster(self, date):
        self.__cursor.execute(f"""SELECT fcs, master_work_day.id_employee_master FROM master JOIN master_work_day
                              ON master.id_employee_master=master_work_day.id_employee_master
                              WHERE date='{date}'""")
        tt_master = self.__cursor.fetchall()
        return tt_master

# получаем данные о записях в расписании мастера
    def get_ttvisit(self, date, id_employee_master):
        self.__cursor.execute(f"""SELECT DISTINCT visit.record_time, service.name_of_the_service, service.time,
                              client.fcs, client.phone_number, master_work_day.date, master_work_day.id_employee_master
                              FROM visit JOIN client
                              ON visit.phone_number=client.phone_number JOIN service
                              ON visit.id_service=service.id_service JOIN master_work_day
                              ON visit.date=master_work_day.date
                              WHERE master_work_day.date='{date}'
                              AND master_work_day.id_employee_master='{id_employee_master}'""")
        get_ttvisit = self.__cursor.fetchall()
        return get_ttvisit

# получаем услуги для селекта
    def getsel_servise(self):
        self.__cursor.execute("SELECT id_service, fcs FROM service")
        gsel_servise = self.__cursor.fetchall()
        return gsel_servise

# добавляем запись в расписание мастера
    def add_servisett(self, record_time, phone_number, date, id_service, id_employee_master):
        self.__cursor.execute("""INSERT INTO visit (record_time, phone_number, date, id_service, id_employee_master)
                                 VALUES (%s,%s,%s,%s,%s)""",
                              (record_time, phone_number, date, id_service, id_employee_master))
        self.__db.commit()

# дополняем данные о посещении в запись
    def up_servisett(self, turnout, payment, id_employee_master, record_time):
        self.__cursor.execute(f"""UPDATE visit SET turnout='{turnout}', payment='{payment}'
                                  WHERE id_employee_master='{id_employee_master}'
                                  AND record_time='{record_time}'""")
        self.__db.commit()

# удаляем запись из расписания мастера на конкретный день
    def del_servicett(self, record_time):
        self.__cursor.execute(f"DELETE FROM visit WHERE record_time='{record_time}'")
        self.__db.commit()

# получаем номер клиента для записи
    def get_client_by_phone(self, phone_number):
        self.__cursor.execute(f"""SELECT phone_number FROM client WHERE phone_number ='{phone_number}'""")
        client = self.__cursor.fetchone()
        return client

# добавляем клиента в бд
    def add_client(self, phone_number, fcs):
        self.__cursor.execute(f"""INSERT INTO client VALUES('{phone_number}', '{fcs}')""")
        self.__db.commit()
        flash('Клиент успешно добавлен')

# получаем клиента для селекта
    def getsel_client(self):
        self.__cursor.execute("SELECT phone_number, fcs FROM client")
        gsel_client = self.__cursor.fetchall()
        return gsel_client

# получаем данные клиента о посещениях
    def get_visclient(self, phone_number):
        self.__cursor.execute(f"""SELECT client.phone_number, master_work_day.date,
                              visit.record_time, service.name_of_the_service, visit.turnout, 
                              visit.payment, master.fcs
                              FROM client JOIN visit
                              ON client.phone_number=visit.phone_number JOIN service
                              ON visit.id_service=service.id_service JOIN master_work_day
                              ON visit.date=master_work_day.date JOIN master
                              ON master_work_day.id_employee_master=master.id_employee_master
                              WHERE visit.phone_number='{phone_number}'""")
        visclient = self.__cursor.fetchall()
        return visclient

# получаем сведения о категории мастера
    def get_catmaster(self):
        self.__cursor.execute(f"""SELECT master.fcs, category_master.id_employee_master, 
                                  category.name_of_the_category_service, category.id_category_service 
                                  FROM master JOIN category_master
                                  ON master.id_employee_master=category_master.id_employee_master JOIN category
                                  ON category_master.id_category_service=category.id_category_service""")
        catmaster = self.__cursor.fetchall()
        return catmaster

# получаем сведения о категории услуги
    def get_category(self):
        self.__cursor.execute("SELECT name_of_the_category_service, id_category_service FROM category")
        category = self.__cursor.fetchall()
        return category

# получаем сведения о виде услуги
    def get_type(self):
        self.__cursor.execute("SELECT name_of_the_type_service, id_type_service FROM type_service")
        type = self.__cursor.fetchall()
        return type

# получаем сведения об услуге
    def get_idservice(self):
        self.__cursor.execute("SELECT name_of_the_service, id_service FROM service")
        idservice = self.__cursor.fetchall()
        return idservice

