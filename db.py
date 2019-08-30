import json
from sqlalchemy import create_engine
import logging

log = logging.getLogger(__name__)


def get_database():
    """

    gets the database connection
    :return: None upon failure.
    """
    try:
        engine = get_connection_from_profile()
        log.info('Connected to postgreSQL database.')
        return engine
    except IOError:
        log.exception('Failed to get database connection.')
        return None, 'fail'


def get_connection_from_profile(config_file='config.json'):
    """
    sets up database connection from config file.
    :param config_file: the postgres config file containing host, user, password, database, port
    :return:
    """
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)

    if not (filter(lambda val: val in data['db'].keys(), ['user', 'database', 'host', 'password', 'port'])):
        raise Exception('Bad config file: ' + config_file)

    return get_engine(data['db'])


def get_engine(db):
    """
    get SQLalchemy engine using credentials.
    :param db: the database object with the user, database host, password, and port.
    :return:
    """
    # url = 'postgresql://{user}:{passwd}@{host}:{port}/{db}'.format(
    #     user=db['user'], passwd=db['password'], host=db['host'], port=db['port'], db=db['database']
    # )
    url = 'sqlite:///{db}'.format(db=db['database'])
    engine = create_engine(url)
    return engine


