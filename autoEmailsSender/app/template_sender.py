import os
from ast import literal_eval
from flask_mail import Mail, Message
from app.create_new_template import TemplateControleer

class SenderController:
    def __init__(self, app):
        self.app = app
        self.mail = Mail(app)
        
        self.contr = TemplateControleer()
    
    def check_example(self, addresses, template, fields):
        if (addresses == ''): return {'err': 'Не заполнены адреса'}

        self.contr.save_users_to_template(template, addresses)
        new_template = self.replace_in_template(template, fields)
        return new_template
    
    def send_mails(self, addresses, template, title, fields):
        
        if (addresses == ''): return {'err': 'Не заполнены адреса'}
        
        self.contr.save_users_to_template(template, addresses)
        new_template = self.replace_in_template(template, fields)
        
        errors = ''
        for addr in addresses.split('\n'):
            if ('@' not in addr): continue
            if (addr == ''): continue
    
            try:
                msg = Message(title, sender=self.app.config['MAIL_USERNAME'], recipients=[addr.replace('\r', '')])
                msg.body = new_template
                self.mail.send(msg)
            except Exception as e:
                print(f'\nERROR: {e}\n')
                errors += f'{addr} не обработан;\n'
                
        if (errors != ''): return {'err': f'Не все адреса были отправлены:\n{errors}'}
        
        return {'msg': 'Ok'}
    
    def replace_in_template(self, template, fields):
        fields = literal_eval(fields)
        template = self.contr.load_template(template)['msg']
        template = template.split('DEBUGING_SPLIT_ROW')[0]
        for field in fields:
            template = template.replace(field[0], field[1])
            
        return template