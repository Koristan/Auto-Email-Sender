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
        
        new_template = self.replace_in_template(template, fields)
        return new_template
    
    def send_mails(self, addresses, template, title, fields):
        
        if (addresses == ''): return {'err': 'Не заполнены адреса'}
        
        new_template = self.replace_in_template(template, fields)
        
        new_addresses = []
        for addr in addresses.split('\n'):
            if ('@' not in addr): continue
            if (addr == ''): continue
            
            new_addresses.append(addr.replace('\r', ''))
        
        print(addresses, '|', new_addresses)
        
        try:
            msg = Message(title, sender=self.app.config['MAIL_USERNAME'], recipients=new_addresses)
            msg.body = new_template
            self.mail.send(msg)
        except Exception as e:
            print(f'\nERROR: {e}\n')
            return {'err': 'Ошибка при отправке! (Возможно неправильные адресаты или не указан внешний пароль)'}
        
        return {'msg': 'Ok'}
    
    def replace_in_template(self, template, fields):
        fields = literal_eval(fields)
        template = self.contr.load_template(template)['msg']
        for field in fields:
            template = template.replace(field[0], field[1])
            
        return template