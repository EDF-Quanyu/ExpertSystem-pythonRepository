import logging
import time
from datetime import datetime

import pandas as pd

from connector.email_connector import *
from connector.sqlalchemy_connector import SQLAlchemyConnector
from connector.account_config import get_logDB_config
from dtypeInfo import defaultLevelDict, defaultLogDtypes


def logAlarm(method):
    def wrapper(selfArg, *args, **kwargs):
        alarmRecord = args[0]
        if alarmRecord.levelno >= 40 and selfArg.emailEnable:
            mailGroup = alarmGroupAdmin()
            content = f"{alarmRecord.levelname}: {alarmRecord.name}: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(alarmRecord.created))}: \
                 {alarmRecord.msg}"
            subject = f"Code execution alarm - {alarmRecord.name}"
            result = emailSend(mailGroup=mailGroup, subject=subject, content=content)
        method(selfArg, *args, **kwargs)

    return wrapper


class LogDBHandler(logging.Handler):
    def __init__(self, engineTarget, tableName, dtypes, emailEnable, codeExecutedTime, msgLevel='NOTSET'):
        logging.Handler.__init__(self)
        self.engineTarget = engineTarget
        self.tableName = tableName
        self.dtypes = dtypes
        self.__level = msgLevel
        self.__levelDict = defaultLevelDict
        self.emailEnable = emailEnable
        self.codeExecutedTime = codeExecutedTime

    @property
    def setLevel(self):
        return self.__level

    @setLevel.setter
    def setLevel(self, level):
        self.__level = level

    @logAlarm
    def emit(self, record):
        if int(record.levelno) >= self.__levelDict[self.__level]:
            dfDict = {
                'log_level': int(record.levelno),
                'log_levelname': str(record.levelname),
                'log': str(record.msg),
                'created_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(record.created)),
                'created_by': self.tableName,
                'DT': self.codeExecutedTime
            }
            dfLog = pd.DataFrame([dfDict])

            try:
                dfLog.to_sql(self.tableName, self.engineTarget, if_exists='append', index=False, dtype=self.dtypes)
            except Exception as e:
                root = logging.getLogger()
                if root.handlers:
                    for handler in root.handlers:
                        if not isinstance(handler, LogDBHandler):
                            logging.error(e)


defaultLogEngine = SQLAlchemyConnector(get_logDB_config).connexion
class LogInstant():
    def __init__(self, logName, logLevel='DEBUG', logFormat='%(levelname)s: %(name)s: %(asctime)s: %(message)s',
                 fileHandlerEnable=True, fileHandlerLevel='INFO',
                 streamHandlerEnable=True, streamHandlerLevel='DEBUG',
                 dbHandlerEnable=True, dbHandlerLevel='INFO', dbLogEngine=defaultLogEngine,
                 dbTableType=defaultLogDtypes,
                 emailNotification=True, logInitiatedTime=datetime.now()):

        self.__logger = logging.getLogger()
        self.__logger.setLevel(logLevel)
        formatter = logging.Formatter(logFormat)
        self.__loggerDT = datetime.strftime(logInitiatedTime, '%Y-%m-%d %H:%M:00')

        if fileHandlerEnable:
            file_handler = logging.FileHandler(f'{logName}.log')
            file_handler.setLevel(fileHandlerLevel)
            file_handler.setFormatter(formatter)
            self.__logger.addHandler(file_handler)

        if streamHandlerEnable:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(streamHandlerLevel)
            stream_handler.setFormatter(formatter)
            self.__logger.addHandler(stream_handler)

        if dbHandlerEnable:
            self.__logdb = LogDBHandler(dbLogEngine, logName, dbTableType, emailNotification, self.__loggerDT)
            self.__logdb.setLevel = dbHandlerLevel
            self.__logger.addHandler(self.__logdb)

    @property
    def logConnexion(self):
        return self.__logger

    @property
    def logdb(self):
        return self.__logdb
