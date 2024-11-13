import os
import textract

path_to_templates = 'app/doc_templates'

class TemplateControleer:
    def __init__(self):
        pass

    def create_template(self, name='', file=''):
        
        try:
            os.mkdir('app/temp')
        except Exception as e:
            print(e)

        try:
            os.mkdir(path_to_templates)
        except Exception as e:
            print(e)

        filename = file.filename
        file.save(f'app/temp/{filename}')
        
        try:
            with open(f'app/temp/{filename}', 'r', encoding='utf-8') as file:
                text = file.read()
        except:
            text = textract.process(f'app/temp/{filename}').decode("utf-8")
            
        if (name == '' or text == ''):
            return {'err': 'Название / Текст пустые'}

        with open(f'{path_to_templates}/{name}.txt', 'w', encoding='utf-8') as file:
            file.write(text)

        return {'msg': 'ОК'}
    
    
    def delete_template(self, name=''):
        
        if (name == ''):
            return {'err': 'Название пустое'}
        
        try:
            os.remove(f'{path_to_templates}/{name}')
        except:
            return {'err': 'Шаблона не существует'}

        return {'msg': 'ОК'}
        

    def load_template(self, name=''):
        
        if (name == ''):
            return {'err': 'Название пустое'}
        
        text = ''
        with open(f'{path_to_templates}/{name}', 'r', encoding='utf-8') as file:
            text = file.read()

        if (text == ''):
            return {'err': 'Шаблон пустой'}
        
        return {'msg': text}


    def get_template_names(self):
        
        templates = []
        for item in os.listdir(f'{path_to_templates}/'):
            templates.append(item)

        if (len(templates) == 0):
            return {'err': 'Шаблонов нет'}
        
        return {'msg': templates}
    
    def save_users_to_template(self, template_name, addresses):
        
        template = self.load_template(template_name)['msg']
        
        if ('DEBUGING_SPLIT_ROW' not in template):
            new_template = template + 'DEBUGING_SPLIT_ROW' + addresses
        else:
            new_template = template.split('DEBUGING_SPLIT_ROW')[0] + 'DEBUGING_SPLIT_ROW' + addresses

        with open(f'{path_to_templates}/{template_name}', 'w', encoding='utf-8') as file:
            file.write(new_template.replace('\r\n', '\r')) # Remove other spaces
        
        return {'msg': 'Ok'}
        
    def load_users_from_template(self, template_name):
        
        template = self.load_template(template_name)['msg']
        
        addresses = 'nothing' if ('DEBUGING_SPLIT_ROW' not in template) else template.split('DEBUGING_SPLIT_ROW')[1]
        
        return addresses