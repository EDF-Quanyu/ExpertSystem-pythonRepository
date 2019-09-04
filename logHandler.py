import logging
import time
from datetime import datetime
import pandas as pd
from connector.account_config import get_logDB_config
from dtypeInfo import get_dbLogDtypes, get_levelDict
from connector.sqlalchemy_connector import SQLAlchemyConnector
# from connectors.sns_connector import SNSConnector
from connector.email_connector import *

defaultLogEngine = SQLAlchemyConnector(get_logDB_config).connexion
defaultDBLogDtypes = get_dbLogDtypes()
levelDict = get_levelDict()
# defaultSNSArn = 'arn:aws-cn:sns:cn-northwest-1:829296342604:LC_Alarms'


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

# logSNSTokenDefault = get_AWSAccount_config()
#
# class LogSNSHandler(logging.Handler):
#     def __init__(self, topic_arn, tokenDictInput, logName, msgLevel = 'ERROR'):
#         logging.Handler.__init__(self)
#         self.__sns = SNSConnector(
#             access_key_id = tokenDictInput['AWS_ACCESS_KEY_ID'],
#             secret_access_key = tokenDictInput['AWS_SECRET_ACCESS_KEY'],
#             region_name = tokenDictInput['AWS_REGION_NAME'])
#         self.__topic_arn = topic_arn
#         self.__level = msgLevel
#         self.__levelDict = levelDict
#         self.__logName = logName
#
#     @property
#     def setLevel(self):
#         return self.__level
#
#     @setLevel.setter
#     def setLevel(self, level):
#         self.__level = level
#
#     def emit(self, record):
#         if int(record.levelno) >= self.__levelDict[self.__level]:
#             snsMsg = f"{record.levelname}: {self.__logName}: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(record.created))}: {record.msg}"
#             try:
#                 self.__sns.publishMsg(topic_arn = self.__topic_arn, msg = snsMsg, subject = self.__logName, dico_attributes = None)
#                 logging.debug("Sending sns complete.")
#             except Exception as e:
#                 root = logging.getLogger()
#                 if root.handlers:
#                     for handler in root.handlers:
#                         if not isinstance(handler, LogDBHandler):
#                             handler.logging.error(e)


class LogDBHandler(logging.Handler):
    def __init__(self, engineTarget, tableName, dtypes, emailEnable, codeExecutedTime, msgLevel = 'NOTSET'):
        logging.Handler.__init__(self)
        self.engineTarget = engineTarget
        self.tableName = tableName
        self.dtypes = dtypes
        self.__level = msgLevel
        self.__levelDict = levelDict
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
                dfLog.to_sql(self.tableName, self.engineTarget, if_exists = 'append', index = False, dtype = self.dtypes)
            except Exception as e:
                root = logging.getLogger()
                if root.handlers:
                    for handler in root.handlers:
                        if not isinstance(handler, LogDBHandler):
                            logging.error(e)


class LogInstant:
    def __init__(self, logName, logLevel = 'DEBUG', logFormat = '%(levelname)s: %(name)s: %(asctime)s: %(message)s',
                 fileHandlerEnable = True, fileHandlerLevel = 'INFO',
                 streamHandlerEnable = True, streamHandlerLevel = 'DEBUG',
                 dbHandlerEnable = True, dbHandlerLevel = 'INFO', dbLogEngine = defaultLogEngine, dbTableType = defaultDBLogDtypes,
                 # snsHandlerEnable = False, snsHandlerLevel = 'ERROR', snsArn = defaultSNSArn, snsToken = logSNSTokenDefault,
                 emailNotification = True, logInitiatedTime = datetime.now()):

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

        # if snsHandlerEnable:
        #     self.__logSNS = LogSNSHandler(snsArn, snsToken, logName)
        #     self.__logSNS.setLevel = snsHandlerLevel
        #     self.__logger.addHandler(self.__logSNS)

    @property
    def logConnexion(self):
        return self.__logger

