import subprocess
import requests
import yaml
import json

def main():
    #
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    
    swagger_url = config['backend']['swaggerUrl']

    private_base_url = config['backend']['privateBaseURL']

    name = config['backend']['name']

    path = config['backend']['path']

    response = requests.get(swagger_url)
    paths = get_paths_from_response(response)

    if paths is not None:

        filename = ''
        
        if 'v3' in swagger_url:
            yaml_dict = build_yaml_dict(response, private_base_url,is_v3=True)
            filename = f'{path}/{name}.yaml'
        else:
            yaml_dict = build_yaml_dict(response, private_base_url)
            filename = path + '/' + yaml_dict['metadata']['name'] + '.yaml'
        
        yaml_data = convert_dict_to_yaml(yaml_dict)

        print(yaml_data)


        print('Saving to file: ' + filename)

        save_yaml_to_file(yaml_dict, filename)


    else:
        print('Error: ' + str(response.status_code))

def get_paths_from_response(response):
    if response.status_code == 200:
        return response.json()['paths']
    else:
        return None


def build_yaml_dict(response, private_base_url,is_v3=False):

    if is_v3:
        host = response.json()['servers'][0]['url']
    else:
        host = response.json()['host']



    paths = get_paths_from_response(response)

    if paths is None:
        return None

    backend_name = str(host).split('.')[0]

    yaml_dict = {
        'apiVersion': 'capabilities.3scale.net/v1beta1',
        'kind': 'Backend',
        'metadata': {
            'name': backend_name
        },
        'spec': {
            'name': backend_name,
            'privateBaseURL': private_base_url,
            'mappingRules': [],
            'metrics': {}
        }
    }

    i = 0
    for path in paths:
        i += 1
        for method in paths[path]:
            mapping_rule = {
                'httpMethod': method.upper(),
                'pattern': path,
                'metricMethodRef': f'{method}-{path.split("/")[1]}-{i}'
            }
            yaml_dict['spec']['mappingRules'].append(mapping_rule)

    i = 0
    for path, methods in paths.items():
        i += 1
        for method in methods:
            metric_name = f'{method}-{path.split("/")[1]}-{i}'
            metric = {
                'friendlyName': metric_name,
                'unit': 'hit'
            }
            yaml_dict['spec']['metrics'][metric_name] = metric

    return yaml_dict


def convert_dict_to_yaml(yaml_dict):
    if yaml_dict is None:
        return None

    return yaml.dump(yaml_dict)


def save_yaml_to_file(yaml_data, filename):
    if yaml_data is None:
        return

    with open(filename, 'w') as file:
        yaml.dump(yaml_data, file)


def execute_command(cmd, trace=False):
    out = subprocess.check_output(cmd, shell=True, text=True)
    if trace:
        print(out)
    return out


if __name__ == '__main__':
    main()
