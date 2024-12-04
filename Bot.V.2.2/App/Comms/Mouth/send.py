#
import requests
import json
import yaml


def get_templet():
    with open('App/Comms/Mouth/Templets/formats.yaml', 'r') as file:
        yaml_content = yaml.safe_load(file)

    return yaml_content


def update_dict_at_path(dictionary, path, value):
    current = dictionary
    for key in path[:-1]:  
        current = current.setdefault(key, {})  # Move dentro do dicionario 
    current[path[-1]] = value 



    


# Função temporaria/ melhorar
def send(app, RECIPIENT_WAID, data):
    data['to'] = RECIPIENT_WAID

    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {app.config['ACCESS_TOKEN']}", 
    }

    url = f"https://graph.facebook.com/{app.config['VERSION']}/{app.config['PHONE_NUMBER_ID']}/messages"

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        print("Message sent successfully!")
        print("Response:", response.json())
    else:
        print("Failed to send message")
        print("Status Code:", response.status_code)
        print("Response:", response.json())