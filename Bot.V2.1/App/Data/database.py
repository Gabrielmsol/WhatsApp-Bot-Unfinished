# Objetivo Criar, ler e alterar arquivos de DataBase
# - Formatação base dos arquivos sql estarão em um arquivo YAML
#   - Deixe os arquivos Yaml em uma pasta chamada Templet junto desse arquivo.py
# - Informações da Data Base estarão numa pasta chamada DataBase
# Meu padrão sera sempre 
# 1. Wrappers
# 2. Funções
# 3. Classes

import sqlite3 as sql 
import yaml

# Wrappers
def try_execute(func):
    '''
    Wrapper tenta executar uma ligação com a data base se possivel
    Privilegio deste metodo é que evita erros no programa
    e não trava a data base em alguma operação problematica..
    '''
    def wrapper(self, *args, **kwargs):
        try:
            conn = sql.connect('App/Data/DataBase/'+self.file_name)
            self.cursor = conn.cursor()
            result = func(self, *args, **kwargs)
            self.cursor.close()
            conn.commit()
            conn.close()
            return result

        except Exception as error:
            return error

    return wrapper


# Funções
def generate_table_query(table_templete):
    'Gera um query que o sql consegue interpretar'
    table_name = list(table_templete.keys())[0]
    columns = table_templete[table_name]['columns']
    table_options = table_templete[table_name]['table_options']

    column_list = []

    for column in columns:
        col_str = f'{column['name']} {column['type']}'
        options = column.get('options')

        if options:
            if isinstance(options, list):
                col_str += ' ' + ' '.join(options)
            else:
                col_str += ' ' + options

        column_list.append(col_str)

    if table_options:
        if isinstance(table_options, list):
                column_list.extend(table_options)
        else:
            column_list.append(table_options)            

    query = f'CREATE TABLE IF NOT EXISTS {table_name} (\n '+',\n '.join(column_list)+'\n)'

    return query+';'

# Classes
class DbConnect:
    'Se conecta a uma data base'
    def __init__(self, file_name: str):
        self.file_name = file_name

    @try_execute
    def create_tables(self, yaml_file_name: str):
        'Nome bem explicativo, sempre importante iniciar este.'
        with open(yaml_file_name, 'r') as file: # Cata o arquivo templete yaml
            self.yaml_content = yaml.safe_load(file)

        for table_name, table_content in self.yaml_content.items():
            query = generate_table_query({table_name: table_content}) 
            self.cursor.execute(query)

    @try_execute
    def insert_into(self, table_name: str, **what):
        'Acho que essas funções estão bem explicativas'
        keys = ', '.join(what.keys())
        placeholders = ', '.join(['?'] * len(what))
        values = tuple(what.values())
        query = f'''
            INSERT OR IGNORE INTO {table_name} ({keys})
            VALUES ({placeholders})
''' 
        self.cursor.execute(query, values)
    
    @try_execute
    def update_into(self, table_name: str, where: str, where_value, **to_update):
        update = ', '.join([f'{key}' for key in to_update.keys()])
        values = tuple(to_update.values()) + (where_value,)
        query = f'''
        UPDATE {table_name}
        SET {update} = ?
        WHERE {where} = ?
''' 
        self.cursor.execute(query, values)     

    @try_execute
    def fetch_one(self, table_name, what, where, where_value):
        query = f'''
        SELECT {what}
        FROM {table_name}
        WHERE {where} = ?
''' 
        self.cursor.execute(query, (where_value,))
        return self.cursor.fetchone()
    
    @try_execute
    def fetch_all(self, table_name, what):
        query = f'SELECT {what} FROM {table_name}'
        self.cursor.execute(query)
        return self.cursor.fetchall()
    

    @try_execute
    def fetch_all_abt(self, table_name, where, where_value, *what):
        
        to_fetch = ', '. join([f'{key}' for key in what ])
        query = f'''
        SELECT {to_fetch}
        FROM {table_name}
        WHERE {where} = ?
'''
        self.cursor.execute(query, (where_value,))
        return self.cursor.fetchall()
        
    


# Exemplo de uso:
# data = DbConnect('TestFile')
# data.create_tables('semester.yaml') -> Cria as mesas
# data.get_list_names() -> Cospe nome das Tabelas que estão no arquivo
# data.what_about('Semester') -> Cospe informações dos dados da tabela
# data.insert_into('Semester', year=2001, period=1)
# data.fetch_all_abt('Semester', 'year', 2001, 'period', 'start', 'end') -> OUTPUT: [(1, None, None)]
# data.update_into('Semester', 'year', 2001, end='never')
# data.fetch_all_abt('Semester', 'year', 2001, 'period', 'start', 'end') -> OUTPUT: [(1, None, 'never')]
