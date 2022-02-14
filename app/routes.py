from app import app
from flask import g, render_template, url_for, session, redirect, flash
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, RegisterForm, AddServiceForm, DelServiceForm, DateForm, DelMasterForm, AddMasterForm, \
    RedirectMasterTtForm, AddServiceTtForm, DelServTtMasterForm, RedirectServiceTtForm, UpServiceTtForm, SelClientForm
from app.DataBase import DataBase


# Подключение к СУБД через драйвер psycopg2
def connect_db():
    conn = psycopg2.connect(dbname="ddfqj5phvktno8",
                            user="wmhzwpaaeiomkd",
                            password="1bdc597125dd496d07c73761cf9cbe0ef8af5ddca5f6e79113c71cfc79596212",
                            host="ec2-54-195-76-73.eu-west-1.compute.amazonaws.com")
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.before_request
def before_request():
    db = get_db()
    global dbase
    dbase = DataBase(db)  # экземпляр DataBase


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


# маршрут главной страницы
@app.route('/')
def home():
    return render_template('home.html')


# маршрут страницы регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    reg_form = RegisterForm()
    session.permanent = False
    session.modified = True

    if reg_form.validate_on_submit():

        _hashed_password = generate_password_hash(reg_form.password_regform.data)

        if reg_form.select_regform.data == 'master':
            account = dbase.get_master(reg_form.login_regform.data)

            # If account exists show error and validation checks
            if account:
                flash('Account already exists!')
            else:
                dbase.add_account_master(reg_form.login_regform.data, _hashed_password, reg_form.fcs_regform.data)
                flash('You have successfully registered!')
                return redirect(url_for('login'))

        elif reg_form.select_regform.data == 'admin':
            account = dbase.get_admin(reg_form.login_regform.data)

            # If account exists show error and validation checks
            if account:
                flash('Account already exists!')
            else:
                dbase.add_account_admin(reg_form.login_regform.data, _hashed_password, reg_form.fcs_regform.data)
                flash('You have successfully registered!')
                return redirect(url_for('login'))

            # Show registration form with message (if any)
    return render_template('register.html', reg_form=reg_form)


# маршрут страницы логирования
@app.route('/login', methods=['GET', 'POST'])
def login():
    session.permanent = False
    login_form = LoginForm()

    if login_form.validate_on_submit():

        master = dbase.get_master(login_form.login_loginform.data)
        admin = dbase.get_admin(login_form.login_loginform.data)

        if master:
            password_rs = master['password']

            if check_password_hash(password_rs, login_form.password_loginform.data):
                session['loggedin'] = True
                session['id_employee_master'] = master['id_employee_master']
                session['role'] = "master"
                return redirect(url_for('home'))

        elif admin:
            password_rs = admin['password']

            if check_password_hash(password_rs, login_form.password_loginform.data):
                session['loggedin'] = True
                session['role'] = "admin"
                session['id_employee_admin'] = admin['id_employee_admin']
                return redirect(url_for('home'))
            else:
                flash('Incorrect login or password')
        else:
            flash('Incorrect login or password')

    return render_template('login.html', login_form=login_form), session


# маршрут выхода из аккаунта
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.clear()
    return redirect(url_for('home'))


# маршрут страницы панели админа
@app.route('/paneladmin')
def paneladmin():
    return render_template('paneladmin.html')


# маршрут страницы расписания
@app.route('/timetable', methods=['GET', 'POST'])
def timetable():
    session.permanent = False
    session.modified = True

    date_form = DateForm()

    if session['role'] == 'admin':

        delmaster_form = DelMasterForm()
        redir_mastertt_form = RedirectMasterTtForm()

        if date_form.submitdate_regform.data:
            delmaster_form.date_del_regform.data = date_form.date_regform.data
            redir_mastertt_form.idredirtt_time.data = date_form.date_regform.data

            master_date = date_form.date_regform.data
            db_master = dbase.get_ttmaster(date_form.date_regform.data)
            master_len = len(db_master)

        elif delmaster_form.idmastersubmit_regform.data:
            dbase.del_master(delmaster_form.idmasterhidden_regform.data, delmaster_form.date_del_regform.data)
            return redirect(url_for('timetable'))

        elif redir_mastertt_form.idredirtt_submit_regform.data:
            id_master = redir_mastertt_form.idredirtt_hidden_regform.data
            return redirect(url_for('ttmaster', id_master=id_master,
                                    master_date=redir_mastertt_form.idredirtt_time.data))
        else:
            db_master = None
            master_len = None
            master_date = "2020-02-15"

        return render_template('timetable.html', delmaster_form=delmaster_form, date_form=date_form,
                               db_master=db_master, master_len=master_len, master_date=master_date,
                               redir_mastertt_form=redir_mastertt_form)

    if session['role'] == 'master':

        if date_form.submitdate_regform.data:
            master_tt = dbase.get_ttvisit(date_form.date_regform.data, session['id_employee_master'])
            master_tt_len = len(master_tt)

            return render_template("timetable.html", date_form=date_form, master_tt=master_tt, master_tt_len=master_tt_len)
        return render_template("timetable.html", date_form=date_form)

# маршрут страницы добавления мастера на смену
@app.route('/addmastertt/<master_date>', methods=['GET', 'POST'])
def addmastertt(master_date):
    session.permanent = False
    session.modified = True

    addmastertt_form = AddMasterForm()
    addmastertt_form.selectmastertt_regform.choices = dbase.getsel_master()

    if addmastertt_form.submitaddtt_regform.data:
        dbase.add_mastertt(addmastertt_form.selectmastertt_regform.data, master_date)
        return redirect(url_for('addmastertt', master_date=master_date))

    return render_template('addmastertt.html', addmastertt_form=addmastertt_form, master_date=master_date)


# маршрут страницы расписания мастера
@app.route('/ttmaster/<id_master>/<master_date>', methods=['GET', 'POST'])
def ttmaster(id_master, master_date):
    session.permanent = False
    session.modified = True

    delserv_ttmaster_form = DelServTtMasterForm()
    redir_servicett_form = RedirectServiceTtForm()

    db_ttvisit = dbase.get_ttvisit(master_date, id_master)
    ttvisit_len = len(db_ttvisit)

    if delserv_ttmaster_form.idservtt_submit_regform.data:
        dbase.del_servicett(delserv_ttmaster_form.idservtt_hidden_regform.data)
        return redirect(url_for('ttmaster', master_date=master_date, id_master=id_master))

    if redir_servicett_form.redirservtt_submit_regform.data:
        session['record_time'] = redir_servicett_form.redirservtt_hidden_regform.data
        return redirect(url_for('up_servicett', id_master=id_master, master_date=master_date))

    return render_template('ttmaster.html', master_date=master_date, id_master=id_master, db_ttvisit=db_ttvisit,
                           ttvisit_len=ttvisit_len, delserv_ttmaster_form=delserv_ttmaster_form,
                           redir_servicett_form=redir_servicett_form)

# маршрут страницы обновления данных о посещении
@app.route('/up_servicett/<id_master>/<master_date>', methods=['GET', 'POST'])
def up_servicett(id_master, master_date):
    session.permanent = False
    session.modified = True

    up_servicett_form = UpServiceTtForm()
    print(session['record_time'])
    record_time = session['record_time']
    if up_servicett_form.submit_upservtt_regform.data:
        dbase.up_servisett(up_servicett_form.select_upturnout_regform.data,
                           up_servicett_form.select_uppayment_regform.data, id_master, record_time)
        return redirect(url_for('ttmaster', id_master=id_master, master_date=master_date))

    return render_template('up_servicett.html', id_master=id_master, up_servicett_form=up_servicett_form,
                           master_date=master_date)


# маршрут страницы добавления записи в расписание
@app.route('/add_servicett/<id_master>/<master_date>', methods=['GET', 'POST'])
def add_servicett(id_master, master_date):
    session.permanent = False
    session.modified = True

    add_servicett_form = AddServiceTtForm()

    if add_servicett_form.submit_addservtt_regform.data:

        client = dbase.get_client_by_phone(add_servicett_form.number_regform.data)

        if not client:
            dbase.add_client(add_servicett_form.number_regform.data, add_servicett_form.fcs_regform.data)

        dbase.add_servisett(add_servicett_form.time_addservtt_regform.data, add_servicett_form.number_regform.data,
                            add_servicett_form.date_addservtt_regform.data,
                            add_servicett_form.idserv_addservtt_regform.data,
                            add_servicett_form.idmast_addservtt_regform.data)
        return redirect(url_for('ttmaster', master_date=master_date, id_master=id_master))

    return render_template('add_servicett.html', add_servicett_form=add_servicett_form, master_date=master_date,
                           id_master=id_master)


# маршрут страницы списка услуг
@app.route('/service', methods=['GET', 'POST'])
def service():
    session.permanent = False
    session.modified = True

    delservice_form = DelServiceForm()

    if delservice_form.idsubmit_regform.data:
        dbase.del_service(delservice_form.idhidden_regform.data)
        return redirect(url_for('service'))

    db_service = dbase.get_service()
    service_len = len(db_service)
    return render_template('service.html', db_service=db_service, service_len=service_len,
                           delservice_form=delservice_form)


# маршрут страницы добавления услуг
@app.route('/addservice', methods=['GET', 'POST'])
def addservice():
    session.permanent = False
    session.modified = True

    addservice_form = AddServiceForm()

    if addservice_form.submitadd_regform.data:
        dbase.add_service(addservice_form.idservice_regform.data, addservice_form.service_regform.data,
                          addservice_form.time_regform.data, addservice_form.cost_regform.data,
                          addservice_form.idtypeservice_regform.data)
        return redirect(url_for('addservice'))

    return render_template('addservice.html', addservice_form=addservice_form)

# маршрут страницы сведений об услугах
@app.route('/editservice', methods=['GET', 'POST'])
def editservice():
    session.permanent = False
    session.modified = True

    db_catmaster = dbase.get_catmaster()
    catmaster_len = len(db_catmaster)

    db_category = dbase.get_category()
    category_len = len(db_category)

    db_type = dbase.get_type()
    type_len = len(db_type)

    db_idservice = dbase.get_idservice()
    idservice_len = len(db_idservice)

    return render_template('editservice.html', db_catmaster=db_catmaster, catmaster_len=catmaster_len,
                           db_category=db_category, category_len=category_len, db_type=db_type, type_len=type_len,
                           db_idservice=db_idservice, idservice_len=idservice_len)

# маршрут страницы списка клиентов
@app.route('/selectclients', methods=['GET', 'POST'])
def selectclients():
    session.permanent = False
    session.modified = True

    sel = False

    selclient_form = SelClientForm()
    selclient_form.selectclient_regform.choices = dbase.getsel_client()

    if selclient_form.submitclient_regform.data:
        sel = True

        db_visclient = dbase.get_visclient(selclient_form.selectclient_regform.data)
        visclient_len = len(db_visclient)

        return render_template('selectclients.html', selclient_form=selclient_form,
                               db_visclient=db_visclient, visclient_len=visclient_len, sel=sel)

    return render_template('selectclients.html', selclient_form=selclient_form)
