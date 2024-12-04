import sqlite3 as sql # Banco de dados
class Connect:
    def __init__(self, file_name, *classes, **numbered_classes):
        self.conn = sql.connect(file_name)
        self.instances = set()

        # Se for args. Pode chamar pelo nome
        for cls in classes: 
            instance = cls(self.conn)
            setattr(self, cls.__name__, instance)
            self.instances.add(instance)
        # Se for kwargs. Pode chamar pela chave mais o nome
        for key, cls in numbered_classes.items():
            instance = cls(self.conn, key) # So aceita uma chave por vez
            setattr(self, cls.__name__+'_'+key, instance)
            self.instances.add(instance)

    def create_tables(self):
        'Chama a função create_table nas classes'
        for instance in self.instances:
            if callable(getattr(instance, 'create_table', None)):
                instance.create_table()

    def debug(self):
        'Fecha tudo'
        for instance in self.instances:
            if hasattr(instance, 'cursor'):
                cursor = getattr(instance, 'cursor')
                if cursor is not None and callable(getattr(cursor, 'close', None)):
                    cursor.close()

    def send(self):
        self.conn.commit()

    def end(self):
        self.conn.close()

class Functions:
    '''
    Se pertubar, adicionar
    def __init__(self):
        self.table = None

    E em todas as funções
    if self.table is none
        return
    function ....
    '''
    def check(self, what, value):
        # Inicia Cursor
        cursor = self.conn.cursor()
        # Realiza operação
        query = f'SELECT COUNT(*) FROM {self.table}  where {what} = ?'
        self.cursor.execute(query, (value,))
        result = cursor.fetchone()[0] > 0
        # Fecha Cursor
        cursor.close()
        if result:
            return True
        else:
            return False
        
        
    def insert(self, **what):
        # Inicia
        cursor = self.conn.cursor()
        # Operação
        keys = ', '.join(what.keys())
        placeholders = ', '.join(['?'] * len(what))
        values = tuple(what.values()) 
        query = f'''
            INSERT OR IGNORE INTO {self.table} ({keys})
            VALUES ({placeholders})
'''
        cursor.execute(query, values)
        # Fecha 
        cursor.close()
        
    def update(self, where, where_value, **to_update):
        # Inicia
        cursor = self.conn.cursor()
        # operação
        update = ', '.join([f'{key}' for key in to_update.keys()])
        values = tuple(to_update.values()) + (where_value,)
        query = f'''
        UPDATE {self.table}
        SET {update} = ?
        WHERE {where} = ?
'''
        cursor.execute(query, values) 
        # Fecha
        cursor.close()  
         
    def fetch_one(self, what, where, where_value):
        # Inicia
        cursor = self.conn.cursor()
        # Operação
        query = f'''
        SELECT {what}
        FROM {self.table}
        WHERE {where} = ?
'''
        cursor.execute(query, (where_value,))
        result = cursor.fetchone()
        # Fecha
        cursor.close()
        return result
    
    def fetch_all(self, what):
        # Inicia
        cursor = self.conn.cursor()
        # Operação
        query = f'SELECT {what} FROM {self.table}'
        cursor.execute(query)
        result =  cursor.fetchall()
        # Fecha
        cursor.close()
        return result
    
    def fetch_all_abt(self, where, where_value, *what):
        # Inicia
        cursor = self.conn.cursor()
        to_fetch = ', '. join([f'{key}' for key in what ])
        query = f'''
        SELECT {to_fetch}
        FROM {self.table}
        WHERE {where} = ?
'''
        cursor.execute(query, (where_value,))
        result = cursor.fetchall()
        # Fecha
        cursor.close()
        return result
    
class Sun(Functions):
    def __init__(self, conn):
        self.conn = conn
        self.table = 'Sun'

    # Cria a tabela de usuario
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {self.table} (
            wa_id TEXT PRIMARY KEY,
            name TEXT NOT NULL
        )
        ''')
        cursor.close()

class Semester(Functions):
    def __init__(self, conn):
        self.conn = conn
        self.table = 'Semester'

    # Cria a tabela de usuario
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {self.table} (
            year INTEGER NOT NULL,
            period INTEGER NOT NULL CHECK (period IN (1, 2)),
            start TEXT, 
            end TEXT,
            UNIQUE (year, period)
        )
        ''')
        cursor.close()

class UpComingEvents(Functions):
    def __init__(self, conn):
        self.conn = conn
        self.table = 'UpComingEvents'

    # Cria a tabela de usuario
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {self.table} (
            day TEXT NOT NULL,
            event TEXT
        )
        ''')
        cursor.close()

class User(Functions):
    def __init__(self, conn):
        self.conn = conn
        self.table = 'User'

    # Cria a tabela de usuario
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {self.table} (
            wa_id TEXT PRIMARY KEY,
            matr INTEGER DEFAULT 0,
            name TEXT DEFAULT 'Unknown',
            role TEXT DEFAULT 'Lua',
            age INTEGER DEFAULT 0,
            gender TEXT DEFAULT 'Unkown',
            origin TEXT DEFAULT 'Unkown',
            trancou INTEGER DEFAULT 0 CHECK (trancou IN (0, 1))
            UNIQUE (wa_id, matr) 
        )
        ''')
        cursor.close()

class Question(Functions):
    def __init__(self, conn):
        self.conn = conn
        self.table = 'User'

    # Cria a tabela de usuario
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {self.table} (
            wa_id TEXT,
            name INTEGER DEFAULT 0 CHECK (name IN (0, 1)),
            gender INTEGER DEFAULT 0 CHECK (gender IN (0, 1)),
            matr INTEGER DEFAULT 0 CHECK (matr IN (0, 1)),
            origin INTEGER DEFAULT 0 CHECK (origin IN (0, 1)),
            age INTEGER DEFAULT 0 CHECK (age IN (0, 1)),
            FOREIGN KEY (wa_id) REFERENCES User(wa_id)
        )
        ''')
        cursor.close()

class Group(Functions):
    def __init__(self, conn):
        self.conn = conn
        self.table = 'Grp'

    # Cria a tabela de usuario
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {self.table} (
            grp_id INTEGER PRIMARY KEY AUTOINCREMENT,
            grpName TEXT NOT NULL,
            narrador INTEGER NOT NULL,
            FOREIGN KEY (narrador) REFERENCES User(matr),
            UNIQUE (grpName, narrador)
        )
        ''')
        cursor.close()

class Participants(Functions):
    def __init__(self, conn):
        self.conn = conn
        self.table = 'Participants'

    # Cria a tabela de usuario
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {self.table} (
            grp_id INTEGER NOT NULL,
            members INTEGER NOT NULL,
            FOREIGN KEY (grp_id) REFERENCES Grp(gpr_id),
            FOREIGN KEY (members) REFERENCES User(matr)
        )
        ''')
        cursor.close()

class Date(Functions):
    def __init__(self, conn):
        self.conn = conn
        self.table = 'Date'

    # Cria a tabela de usuario
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {self.table} (
            day TEXT PRIMARY KEY,
            confirmation INTEGER DEFAULT 1 CHECK (confirmation IN (0, 1))
        )
        ''')
        cursor.close()

class Grade(Functions):
    def __init__(self, conn):
        self.conn = conn
        self.table = 'Grade'

    # Cria a tabela de usuario
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {self.table} (
            matr INTEGER NOT NULL,
            day TEXT NOT NULL,
            grade REAL DEFAULT 0.0, 
            repDay TEXT DEFAULT 'None',
            attend INTEGER DEFAULT 0 CHECK (attend IN (0, 1)),
            rep INTEGER DEFAULT 0 CHECK (rep IN (0, 1)),
            FOREIGN KEY (matr) REFERENCES User(matr),
            UNIQUE (matr, day)
        )
        ''')
        cursor.close()