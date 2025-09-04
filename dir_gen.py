import os
import sys
import json
config = json.load(open('config.json'))

def dir_create(folder_name):
    abspath = os.path.abspath(__file__)
    print(f'__file__{__file__}')
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    sys.path.append(dname)
    sys.path.append(os.path.join(dname, 'preprocess'))

    if config['verbose'] > 0:
        print(' ------------------- SYSTEM SPECIFICATIONS --------------------')
        print(f'\t\t Python {sys.version} on {sys.platform}')
        print(' \t\t Working Directory', os.getcwd())

    config['dir_names'] = {}
    config['dir_names']['res_folder_name'] = folder_name
    config['dir_names']['preprocess_folder_name'] = os.path.join(folder_name, 'preprocess')
    config['dir_names']['sessions_folder_name'] = os.path.join(folder_name, 'preprocess/session_cluster')
    config['dir_names']['pole_folder_name'] = os.path.join(folder_name, 'preprocess/pole_cluster')

    config['dir_names']['models_logs_folder_name'] = os.path.join(folder_name, 'models')
    config['dir_names']['models_folder_name'] = os.path.join(folder_name, 'models/saved_models')

    config['dir_names']['generated_samples_name'] = os.path.join(folder_name, 'generated_samples')


    for dirs in config['dir_names']:
        os.makedirs(config['dir_names'][dirs], exist_ok=True)
    json.dump(config, open('config.json', 'w'))

    if os.path.isfile(os.path.join(folder_name, config['transactions_filename'])):
        return True
    else:
        return False