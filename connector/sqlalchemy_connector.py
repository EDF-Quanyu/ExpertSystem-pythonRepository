# coding=utf-8
import logging
from time import sleep
import pandas as pd
from sqlalchemy import create_engine


class SQLAlchemyConnector(object):
    """description of class""" 

    def __init__(self, dbDict):
        self.__connexionDict = dbDict
        self.__engineStr = '{driveType}://{username}:{password}@{ip}/{db}'.format_map(self.__connexionDict)
        self.__connexion = create_engine(self.__engineStr)
        self.server = self.__connexionDict['ip']
        self.database = self.__connexionDict['db']
        self.username = self.__connexionDict['username']
        self.password = self.__connexionDict['password']

    @property
    def connexion(self):
        """Get RDS service property"""
        return self.__connexion

    def execute(self, query):
        logging.debug(f'Execute query : {query}')

        nb_retry = 10
        while True:
            try:
                df = pd.read_sql_query(query, self.__connexion)
                break
            except Exception as e:
                logging.warning("Retry {} : {} received : {}".format(nb_retry, type(e).__name__, e))
                nb_retry -= 1
                if (nb_retry < 0):
                    raise e
                sleep(15)
        return df

    def lastRecordInsert(self, tableName, dateset, dtypes):
        logging.debug('Update the last record table')

        nb_retry = 10
        while True:
            try:
                dateset.to_sql(tableName, self.__connexion, if_exists = 'replace', index = False, dtype = dtypes)
                break
            except Exception as e:
                logging.warning("Retry {} : {} received: {}".format(nb_retry, type(e).__name__, e))
                nb_retry -= 1
                if (nb_retry < 0):
                    raise e
                sleep(15)
        return
