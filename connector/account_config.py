def get_scadaDB_config():
    return {
        'driveType': 'mssql+pymssql',
        'username': 'sa',
        'password': 'edf1234',
        'ip': '172.19.254.42:1433',
        'db': 'SMXDB'
    }

def get_logDB_config():
    return {
        'driveType': 'mssql+pymssql',
        'username': 'sa',
        'password': 'edf1234',
        'ip': '172.19.254.42:1433',
        'db': 'pythonLog'
    }
