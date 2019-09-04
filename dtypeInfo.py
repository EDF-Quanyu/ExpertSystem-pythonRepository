import sqlalchemy

def weatherForecast24h():
    dtypes = {
        'DT': sqlalchemy.types.DATETIME,
        'updateDT': sqlalchemy.types.DATETIME,
        'highTemperature': sqlalchemy.types.FLOAT,
        'lowTemperature': sqlalchemy.types.FLOAT,
        'DT_Extraction': sqlalchemy.types.DATETIME
    }
    return dtypes

def indoorTempLastRecord():
    dtypes = {
        'meterID': sqlalchemy.types.VARCHAR(20),
        'DT': sqlalchemy.types.DATETIME,
        'value': sqlalchemy.types.FLOAT
    }

def get_dbLogDtypes():
    dtypes = {
        'log_level': sqlalchemy.types.VARCHAR(20),
        'log_levelname': sqlalchemy.types.VARCHAR(40),
        'log': sqlalchemy.types.VARCHAR(2048),
        'created_at': sqlalchemy.types.DATETIME,
        'created_by': sqlalchemy.types.VARCHAR(40),
        'DT': sqlalchemy.types.DATETIME
    }
    return dtypes

def get_levelDict():
    level_Dict = {
            'NOTSET': 0,
            'DEBUG': 10,
            'INFO': 20,
            'WARNING': 30,
            'ERROR': 40,
            'CRITICAL': 50}
    return level_Dict

def get_indoorWeightDict():
    dtypes = {
        "DT_EXTRACTION": sqlalchemy.types.DATETIME,
        "CODE": sqlalchemy.types.VARCHAR(20),
        "SKIDID": sqlalchemy.types.VARCHAR(20),
        "ADDRESS": sqlalchemy.types.VARCHAR(400),
        "POSITION": sqlalchemy.types.VARCHAR(400),
        "ALTITUDE": sqlalchemy.types.VARCHAR(400),
        "ISEXTERNWALL": sqlalchemy.types.VARCHAR(20),
        "OWNER": sqlalchemy.types.VARCHAR(400),
        "ORIENTATION": sqlalchemy.types.VARCHAR(400),
        "AREA": sqlalchemy.types.INT,
        "WEIGHTPERCENTAGE": sqlalchemy.types.DECIMAL(20, 5),
        "SKIDNAME": sqlalchemy.types.VARCHAR(400),
        "MS": sqlalchemy.types.VARCHAR(20),
        "NW": sqlalchemy.types.VARCHAR(20),
        "CREATEID": sqlalchemy.types.VARCHAR(32),
        "CREATENAME": sqlalchemy.types.NVARCHAR(50),
        "CREATETIME": sqlalchemy.types.DATETIME,
        "CUSTOMSTATUS": sqlalchemy.types.VARCHAR(32),
        "CUSTOMSTATUSNAME": sqlalchemy.types.VARCHAR(50),
        "ISDEL": sqlalchemy.types.INT,
        "UPDATETIME": sqlalchemy.types.DATETIME,
        "WORKFLOWSTATUS": sqlalchemy.types.INT,
        "CFID": sqlalchemy.types.VARCHAR(32)}
    return dtypes

def get_LCindoorWeightDict():
    dtypes = {
        "DT_Extraction": sqlalchemy.types.DATETIME,
        "skidID": sqlalchemy.types.VARCHAR(20),
        "meterID": sqlalchemy.types.VARCHAR(20),
        "weight": sqlalchemy.types.FLOAT}
    return dtypes

def get_TFakeTableColumns_config():
    columns = ['Substation', 'T_ext_forecast_max', 'delta_text_sp_auto', 't_indoor_min_day', 'lv_ITM', 'Kp_prop_gain',
             'delta_text_sp_auto_corrected', 'formula', 'DT', 'T_ext_forecast_mean', 'STATUS', 'ERROR']
    return columns

def get_estimatedIndoorTableColumns_config():
    columns = ['Producer', 'skidID', 'meterID', 'DT_Extraction', 'DT', 'Temp']
    return columns


defaultLevelDict = {
    'NOTSET': 0,
    'DEBUG': 10,
    'INFO': 20,
    'WARNING': 30,
    'ERROR': 40,
    'CRITICAL': 50}

defaultLogDtypes = {
    'log_level': sqlalchemy.types.VARCHAR(20),
    'log_levelname': sqlalchemy.types.VARCHAR(40),
    'log': sqlalchemy.types.VARCHAR(2048),
    'created_at': sqlalchemy.types.DATETIME,
    'created_by': sqlalchemy.types.VARCHAR(200),
    'DT': sqlalchemy.types.DATETIME
}
