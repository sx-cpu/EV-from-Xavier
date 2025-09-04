# import libraries
import argparse
import json
import warnings
warnings.filterwarnings('ignore')


def main(args):
    config = json.load(open('config.json'))
    config['Year'] = int(args['Year'])
    config['slot_mins'] = int(args['Slotmins'])
    config['verbose'] = int(args['verbose'])
    config['create_plots'] = bool(args['create_plots'])
    config['transactions_filename'] = str(args['Sessions_filename'])
    config['data_collector'] = 'Y'


    json.dump(config, open('config.json', 'w'), indent=4)

    # create directories
    from dir_gen import dir_create
    val = dir_create(folder_name=str(args['res_folder']))
    if not(val):
        print("Raw Data file not found at: ", config['dir_names']['res_folder_name'])

        return
    
    # generate processed data
    from preprocess.prepare_clustered_data import create_processed_data
    create_processed_data()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Arguments to preprocess data: \n'
                                                   'Creates session and pole clusters and time series data for modeling')
    parser.add_argument('--Year', default=2022,
                        help='Year for modeling (integer)')
    parser.add_argument('--Slotmins', default=60,
                        help='Minutes in each timeslot (integer)')
    parser.add_argument('--create_plots', default=True,
                        help='Indicator for creating plots.')
    parser.add_argument('--Sessions_filename', default='transactions.csv',
                        help='Name of the file contaning raw data. This file must be present in res_folder. (string)')
    parser.add_argument('--res_folder', default='res',
                        help='Locaiton for raw data file. default is "./res" inside this directory'
                             'EV sessions files must be present here. (string)')
    parser.add_argument('--verbose', default=3,
                        help='0 to print nothing; >0 values for printing more information. '
                             'Possible values: 0, 1, 2, 3. (integer)')

    args = parser.parse_args()
    main(vars(args))
