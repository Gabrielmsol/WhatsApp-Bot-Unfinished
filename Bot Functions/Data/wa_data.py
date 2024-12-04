class WhatsData:
    '''
Pega informações cruciais na mensagem:
name
type
wa_id
text
    '''
    def __init__(self, data):
        self.data = data
        self.process_data()

    # essa linha esta mal implementada,
    # se o dono do número não tiver o 9 no numero, ele adere.
    # contudo, so funciona pra numeros do brasil...
    def split(self, string):
        string = str(string)
        if len(string) == 12:
            self.string = string[:4] + '9' + string[4:]
        else:
            self.string = string

    def check_nested_path(self, path):
        """Checa se um caminho existe."""
        current_level = self.data
        # Informações do whatsapp vêm bagunçadas, mistura de lista com dicionario...
        for key in path:
            if isinstance(current_level, dict):
                if key in current_level:
                    current_level = current_level[key]
                else:
                    return False
            elif isinstance(current_level, list):
                try:
                    index = int(key)
                    if 0 <= index < len(current_level):
                        current_level = current_level[index]
                    else:
                        return False
                except ValueError:
                    return False
            else:
                return False

        return True


    def go_to_nested_path(self, path):
        """Vai para o path se ele existe."""
        current_level = self.data

        for key in path:
            if isinstance(current_level, dict):
                if key in current_level:
                    current_level = current_level[key]
                else:
                    return None
            elif isinstance(current_level, list):
                try:
                    index = int(key)
                    if 0 <= index < len(current_level):
                        current_level = current_level[index]
                    else:
                        return None
                except ValueError:
                    return None
            else:
                return None

        return current_level
    
    def process_data(self):
        """Processa o tipo de informação."""
        path = {
            'is_read'        : ['entry', '0', 'changes', '0', 'value', 'statuses'],
            'is_message'     : ['entry', '0', 'changes', '0', 'value', 'contacts'],
            'read_wa_id'     : ['entry', '0', 'changes', '0', 'value', 'statuses', '0', 'recipient_id'],
            'messanger_wa_id': ['entry', '0', 'changes', '0', 'value', 'contacts', '0', 'wa_id'],
            'messanger_name' : ['entry', '0', 'changes', '0', 'value', 'contacts', '0', 'profile', 'name'],
            'message_type'   : ['entry', '0', 'changes', '0', 'value', 'messages', '0', 'type'],
            'message_text'   : ['entry', '0', 'changes', '0', 'value', 'messages', '0', 'text', 'body']
        }
        # Verifica se a mensagem é confirmação de lida
        if self.check_nested_path(path['is_read']):
            self.split(self.go_to_nested_path(path['read_wa_id']))
            self.wa_id = self.string
            self.name = None
            self.type = 'read'
            self.text = None
        # verifica se é uma mensagem
        if self.check_nested_path(path['is_message']):
            self.split(self.go_to_nested_path(path['messanger_wa_id']))
            self.wa_id = self.string
            self.name = self.go_to_nested_path(path['messanger_name'])
            self.type = self.go_to_nested_path(path['message_type'])
            if self.type == 'text':
                self.text = self.go_to_nested_path(path['message_text'])
            else:
                self.text = None

