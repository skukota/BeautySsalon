from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, HiddenField, \
    DateField, DateTimeField
from wtforms.validators import DataRequired


# форма логирования
class LoginForm(FlaskForm):
    login_loginform = StringField("ᅠ Login ᅠ ᅠ", validators=[DataRequired()])
    password_loginform = PasswordField("ᅠ Passwordᅠ ", validators=[DataRequired()])
    remember_loginform = BooleanField("Remember me ᅠᅠ ᅠ ᅠ ᅠ ᅠᅠ ᅠ", default=False)
    submit_loginform = SubmitField("Sign in")


# форма регистрации
class RegisterForm(FlaskForm):
    login_regform = StringField("ᅠ Login ᅠ ᅠ", validators=[DataRequired()])
    password_regform = PasswordField("ᅠ Passwordᅠ ", validators=[DataRequired()])
    fcs_regform = StringField("ᅠ FCsᅠ ᅠᅠ", validators=[DataRequired()])
    submit_regform = SubmitField("Register")
    select_regform = SelectField("ᅠ Select type of registration ᅠ", choices=['master', 'admin'])


# форма для добавления услуги
class AddServiceForm(FlaskForm):
    idservice_regform = IntegerField("ᅠ ID услуги ᅠ ᅠ ᅠ ᅠ ᅠ", validators=[DataRequired()])
    service_regform = StringField("ᅠ Наименование услугиᅠ", validators=[DataRequired()])
    time_regform = StringField("ᅠ Длительность услуги ᅠ", validators=[DataRequired()])
    cost_regform = IntegerField("ᅠ Стоимость услуги ᅠ ᅠ", validators=[DataRequired()])
    idtypeservice_regform = IntegerField("ᅠ ID типа услуги ᅠ ᅠ ᅠ", validators=[DataRequired()])
    submitadd_regform = SubmitField("Save")


# форма для удаления услуги
class DelServiceForm(FlaskForm):
    idhidden_regform = HiddenField()
    idsubmit_regform = SubmitField("Delete")


# форма для выбора даты
class DateForm(FlaskForm):
    date_regform = DateField("ᅠ Рабочая смена", validators=[DataRequired()])
    submitdate_regform = SubmitField("Select")


# форма для добавления мастера на смену
class AddMasterForm(FlaskForm):
    selectmastertt_regform = SelectField("ᅠ Select name", choices=[])
    submitaddtt_regform = SubmitField("Save")


# форма для удаления мастера из расписанияя
class DelMasterForm(FlaskForm):
    idmasterhidden_regform = HiddenField()
    date_del_regform = DateField(validators=[DataRequired()])
    idmastersubmit_regform = SubmitField("Delete")


# форма для перехода на страницу расписания мастера в конкретный день
class RedirectMasterTtForm(FlaskForm):
    idredirtt_hidden_regform = HiddenField()
    idredirtt_time = DateField(validators=[DataRequired()])
    idredirtt_submit_regform = SubmitField("Redirect")

# форма для удаления услуги из расписания мастера на день
class DelServTtMasterForm(FlaskForm):
    idservtt_hidden_regform = HiddenField()
    #date_servtt_regform = DateField(validators=[DataRequired()])
    idservtt_submit_regform = SubmitField("Delete")

# форма для добавления записи мастеру в конкретный день
class AddServiceTtForm(FlaskForm):
    time_addservtt_regform = DateTimeField("ᅠ Время записи ᅠᅠᅠᅠᅠᅠᅠ", format='%H:%M', validators=[DataRequired()])
    #select_turnout_regform = SelectField("ᅠ Пришел/Не пришел", choices=['Да', 'Нет'])
    #select_payment_regform = SelectField("ᅠ Способ оплаты", choices=['Наличными', 'Безналичный расчет'])
    fcs_regform = StringField("ᅠФИО клиетаᅠᅠᅠᅠᅠᅠᅠᅠ", validators=[DataRequired()])
    number_regform = IntegerField("ᅠ Номер телефона клиента ᅠ ᅠ", validators=[DataRequired()])
    date_addservtt_regform = DateField("ᅠᅠᅠДата услуги  ᅠᅠ ᅠᅠ ᅠ ᅠᅠ", validators=[DataRequired()])
    idserv_addservtt_regform = IntegerField("ᅠ ID услугиᅠᅠᅠᅠᅠᅠᅠᅠᅠ", validators=[DataRequired()])
    idmast_addservtt_regform = IntegerField("ᅠ ID мастера  ᅠ ᅠᅠ ᅠ ᅠ ᅠ ᅠ", validators=[DataRequired()])
    #select_addservtt_regform = SelectField("ᅠ Select service", choices=[])
    submit_addservtt_regform = SubmitField("Save")

# форма для перехода на страницу расписания мастера в конкретный день
class RedirectServiceTtForm(FlaskForm):
    redirservtt_hidden_regform = HiddenField()
    redirservtt_submit_regform = SubmitField("Redirect")

# форма для обнавления данных в записи мастера
class UpServiceTtForm(FlaskForm):
    select_upturnout_regform = SelectField("ᅠ Пришел/Не пришел", choices=['Да', 'Нет'])
    select_uppayment_regform = SelectField("ᅠ Способ оплаты", choices=['Наличными', 'Безналичный расчет', 'Не оплачено'])
    submit_upservtt_regform = SubmitField("Save")

# форма для выбора клиента из всех имеющихся
class SelClientForm(FlaskForm):
    selectclient_regform = SelectField("ᅠ Select name", choices=[])
    submitclient_regform = SubmitField("Save")