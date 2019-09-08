import pandas as pd
import logging

from connector.sqlalchemy_connector import SQLAlchemyConnector
from connector.account_config import get_scadaDB_config


class ExpertConnector:
    def __init__(self, skid_id, para_list, engine_dict=get_scadaDB_config):
        self.__skidID = skid_id
        self.__paraList = para_list
        self.__engine = SQLAlchemyConnector(engine_dict).connexion

    def data_source_acquisition(self):
        para_str = '[' + '],['.join(self.__paraList) + ']'
        sql_str = f"""
                        SELECT Keys, value FROM (
                            SELECT * FROM rawTablePVT 
                            WHERE skidID = '{self.__skidID}' AND DT >= DATEADD(MI, -15, GETDATE())) A
                        UNPIVOT (value FOR Keys IN ({para_str})) AS UPVT
                        ORDER BY Keys, DT;
                    """
        result_sta = 0

        try:
            df = pd.read_sql_query(sql_str, self.__engine)
            if df.empty:
                result_sta = 1
                df_agg = pd.DataFrame(columns=['Keys', 'max', 'min', 'mean', 'median'])
            else:
                df_agg = df.groupby(['Keys']).agg(['max', 'min', 'mean', 'median'])
                df_agg.reset_index(inplace=True)
                miss = [para for para in df_agg.Keys if para not in self.__paraList]
                if len(miss) > 0:
                    result_sta = 2

        except Exception as e:
            result_sta = 3
            df_agg = pd.DataFrame(columns=['Keys', 'max', 'min', 'mean', 'median'])
            logging.warning(e)

        return result_sta, df_agg




