from flask import Flask, render_template, request, flash
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_wtf import Form, RecaptchaField
from flask_wtf.file import FileField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required
from spark.rooms import Room
from spark.session import Session
from spark.memberships import Membership

class SparkUtil:
    @classmethod
    def add_members(cls, key, name, members):
        retval = False
        try:
            ss = Session('https://api.ciscospark.com', key)
            room = Room.get(ss, name)
            if not isinstance(room, Room):
               room = Room()
               room.title = name
               room.create(ss)
            for m in members:
               Membership.create( ss, room.id, m)
            retval = True
        except ValueError:
            retval = False
        return retval

class SparkSimpleForm(Form):
    spark_key = TextField('SPARK_KEY', description='Copy & Paste your SPARK_KEY',
                       validators=[Required()])
    room_name = TextField('Room Name', description='Enter Room Name existing or creating one',
                       validators=[Required()])
    upload_file = FileField('Membership list upload')
    submit_button = SubmitField('Submit Form')


def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app, configfile)  # Flask-Appconfig is not necessary, but
                                # highly recommend =)
                                # https://github.com/mbr/flask-appconfig
    Bootstrap(app)

    # in a real app, these should be configured through Flask-Appconfig
    app.config['SECRET_KEY'] = 'devkey'
    app.config['RECAPTCHA_PUBLIC_KEY'] = \
        '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

    @app.route('/', methods=['GET'])
    def index():
        key = request.args.get('spark_key')
        form = SparkSimpleForm()
        #form.action='/add/'
        if key:
            form.spark_key.data = key
        form.validate_on_submit()  # to get error messages to the browser
        return render_template('index.html', form=form)

    @app.route('/add/', methods=['POST'])
    def upload():
        spark_key = request.form['spark_key']
        room = request.form['room_name']
        file = request.files['upload_file']
        members = []
        for m in file.read().split():
            if '@' not in m :
                members.append( '%s@cisco.com' %(m))
            else:
                members.append( m)
        retval = SparkUtil.add_members( spark_key, room, members)
        if retval:
            return render_template('response.html', room=room, spark_key=spark_key)
        else :
            return render_template('error.html', spark_key=spark_key)

    return app

if __name__ == '__main__':
    create_app().run(debug=True)
