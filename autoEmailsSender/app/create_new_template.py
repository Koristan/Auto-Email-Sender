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