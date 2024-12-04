import yaml


def load_config(app):
    'Carrega dados importantes em config.yaml'
    with open('App/SetUp/Config/config.yaml', 'r') as file:
        yaml_content = yaml.safe_load(file)

    for key, value in yaml_content.items():
        app.config[key] = value 