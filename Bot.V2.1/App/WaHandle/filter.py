# Objetivo
#
# Filtrar informações fornecidas pelo facebook na classe Ear responsavel por escutar webhooks

class WhatsData:
    """Filtra informações do facebook como nome do usuario, id, mensagem etc"""
    def __init__(self, data):
        self.data = data
        self.process_data()

    
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

        # essa linha esta mal implementada,
        # se o dono do número não tiver o 9 no numero, ele adere.
        # contudo, so funciona pra numeros do brasil..

        def split(string):
            string = str(string)
            if len(string) == 12:
                self.string = string[:4] + '9' + string[4:]
            else:
                self.string = string

        def check_nested_path(path):
            """Checa se um caminho existe."""
            current_level = self.data
            for key in path:
                if isinstance(current_level, dict) and key in current_level:
                    current_level = current_level[key]
                elif isinstance(current_level, list):
                    try:
                        current_level = current_level[int(key)]
                    except (ValueError, IndexError):
                        return False
                else:
                    return False
            return True
        
        def go_to_nested_path(path):
            """Vai para um caminho se existe."""
            current_level = self.data
            for key in path:
                if isinstance(current_level, dict) and key in current_level:
                    current_level = current_level[key]
                elif isinstance(current_level, list):
                    try:
                        current_level = current_level[int(key)]
                    except (ValueError, IndexError):
                        return None
                else:
                    return None
            return current_level


        def process_read_confirmation():
            split(go_to_nested_path(path['read_wa_id']))
            self.wa_id = self.string
            self.name = None
            self.type = 'read'
            self.text = None

        def process_message():
            split(go_to_nested_path(path['messanger_wa_id']))
            self.wa_id = self.string
            self.name = go_to_nested_path(path['messanger_name'])
            self.type = go_to_nested_path(path['message_type'])
            self.text = go_to_nested_path(path['message_text']) if self.type == 'text' else None

        if check_nested_path(path['is_read']):
            process_read_confirmation()

        if check_nested_path(path['is_message']):
            process_message()