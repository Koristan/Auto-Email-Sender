# python
import os, sys
from flask import Flask, render_template, redirect, url_for, request, session, flash, app, Blueprint, jsonify
# custom
import app.config as cf
from app.create_new_template import TemplateControleer
from app.template_sender import SenderController

fApp = Flask(
    __name__,
    template_folder='templates'
)

fApp.config['MAIL_SERVER'] = 'smtp.yandex.com'
fApp.config['MAIL_PORT'] = 465
# fApp.config['MAIL_USE_TLS'] = True
fApp.config['MAIL_USE_SSL'] = True
fApp.config['MAIL_USERNAME'] = cf.ACCOUNT_NAME 
fApp.config['MAIL_PASSWORD'] = cf.ACCOUNT_OUT_PASSWORD

@fApp.route("/")
def index():
    return render_template('index.html')

@fApp.route('/send', methods=['GET', 'POST'])
def send():
    return render_template('send.html')

@fApp.route('/create', methods=['GET', 'POST'])
def create():
    return render_template('create.html')

# API

@fApp.route('/api/templates/get', methods=['GET', 'POST'])
def api_template_get():
    contr = TemplateControleer()
    templates_names = contr.get_template_names()
    return templates_names

@fApp.route('/api/templates/create', methods=['GET', 'POST'])
def api_template_create():

    template_name = request.form.get('template_name')
    template_file = request.files.get('template_file')

    contr = TemplateControleer()
    template_status = contr.create_template(template_name, template_file)
    return template_status

@fApp.route('/api/templates/delete', methods=['GET', 'POST'])
def api_template_delete():

    template_name = request.form.get('template_name')

    contr = TemplateControleer()
    template_status = contr.delete_template(template_name)
    return template_status

@fApp.route('/api/presend', methods=['GET', 'POST'])
def api_presend():

    template = request.form.get('template')
    addresses = request.form.get('addresses')
    title = request.form.get('title')
    fields = request.form.get('fields')

    contr = SenderController(fApp)
    example = contr.check_example(addresses, template, fields)
    return example


@fApp.route('/api/send', methods=['GET', 'POST'])
def api_send():

    template = request.form.get('template')
    addresses = request.form.get('addresses')
    title = request.form.get('title')
    fields = request.form.get('fields')

    contr = SenderController(fApp)
    status = contr.send_mails(addresses, template, title, fields)
    return status

@fApp.route('/api/load_addresses', methods=['GET', 'POST'])
def load_addresses():

    template = request.form.get('template')
    contr = TemplateControleer()
    addresses = contr.load_users_from_template(template)
    return addresses


if __name__ == '__main__':
    fApp.run(debug=True)