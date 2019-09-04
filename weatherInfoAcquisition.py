import logging
from logHandler import LogInstant
from connector.account_config import get_scadaDB_config
from connector.sqlalchemy_connector import SQLAlchemyConnector
from FC.FCBasic import weatherReal

logInstant = LogInstant(logName='ImportLC_estimatedindoortemperature', emailNotification=True)

try:
    logging.info("Start")
    engineTarget = SQLAlchemyConnector(get_scadaDB_config()).connexion

    # Wuhan
    dfRealWH = weatherReal('285063')
    if dfRealWH.empty:
        logging.error("No weather info collected through API for Wuhan city.")
    else:
        dfRealWH.to_sql('weatherRealWH', engineTarget, if_exists='append', index=False)
        logging.info("Insert the weather info of Wuhan to database.")

    # Sanya
    dfRealHTW = weatherReal('285354')
    if dfRealHTW.empty:
        logging.error("No weather info collected through API for Sanya city.")
    else:
        dfRealHTW.to_sql('weatherRealHTW', engineTarget, if_exists='append', index=False)
        logging.info("Insert the weather info of Sanya to database.")

    # Sanmenxia
    dfRealSMX = weatherReal('469')
    if dfRealSMX.empty:
        logging.error("No weather info collected through API for Sanmenxia city.")
    else:
        dfRealSMX.to_sql('weatherReal', engineTarget, if_exists='append', index=False)
        logging.info("Insert the weather info of Sanmenxia to database.")

    # Lingbao
    dfRealLB = weatherReal('471')
    if dfRealLB.empty:
        logging.error("No weather info collected through API for Lingbao city.")
    else:
        dfRealLB.to_sql('weatherRealLB', engineTarget, if_exists='append', index=False)
        logging.info("Insert the weather info of Lingbao to database.")

    # Jiamusi
    dfRealJMS = weatherReal('331')
    if dfRealJMS.empty:
        logging.error("No weather info collected through API for Jiamusi city.")
    else:
        dfRealJMS.to_sql('weatherRealJMS', engineTarget, if_exists='append', index=False)
        logging.info("Insert the weather info of Jiamusi to database.")

    # Nanjing
    dfRealNJ = weatherReal('1045')
    if dfRealNJ.empty:
        logging.error("No weather info collected through API for Nanjing city.")
    else:
        dfRealNJ.to_sql('weatherRealNJ', engineTarget, if_exists='append', index=False)
        logging.info("Insert the weather info of Nanjing to database.")

    # Guangdong
    dfRealGD = weatherReal('886')
    if dfRealGD.empty:
        logging.error("No weather info collected through API for Guangdong city.")
    else:
        dfRealGD.to_sql('weatherRealGD', engineTarget, if_exists='append', index=False)
        logging.info("Insert the weather info of Guangdong to database.")

    # Songyuan
    dfRealSY = weatherReal('284764')
    if dfRealSY.empty:
        logging.error("No weather info collected through API for Songyuan city.")
    else:
        dfRealSY.to_sql('weatherRealSY', engineTarget, if_exists='append', index=False)
        logging.info("Insert the weather info of Songyuan to database.")

    # Jinan
    dfRealJN = weatherReal('284973')
    if dfRealJN.empty:
        logging.error("No weather info collected through API for Jinan city.")
    else:
        dfRealJN.to_sql('weatherRealJN', engineTarget, if_exists='append', index=False)
        logging.info("Insert the weather info of Jinan to database.")

    # Chongqing
    dfRealCQ = weatherReal('52')
    if dfRealCQ.empty:
        logging.error("No weather info collected through API for Chongqing city.")
    else:
        dfRealCQ.to_sql('weatherRealCQ', engineTarget, if_exists='append', index=False)
        logging.info("Insert the weather info of Chongqing to database.")

    # Changchun
    dfRealCC = weatherReal('182')
    if dfRealCC.empty:
        logging.error("No weather info collected through API for Changchun city.")
    else:
        dfRealCC.to_sql('weatherRealCC', engineTarget, if_exists='append', index=False)
        logging.info("Insert the weather info of Changchun to database.")

    logging.info("Complete")

except Exception as e:
    logging.error(e)
