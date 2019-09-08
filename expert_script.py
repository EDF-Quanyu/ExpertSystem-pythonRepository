from connector.expert_connector import ExpertConnector

para_list = ['TT00', 'TT11', 'TT12', 'TT21', 'TT22', 'TT01',
             'PT11', 'PT12', 'PT21', 'PT22',
             'FT11', 'HT11', 'FT30', 'CP01', 'CV01']
expert_connector = ExpertConnector(skid_id='BFD', para_list=para_list)
data_frame_state, df = expert_connector.data_source_acquisition()

"""
data_frame_state: 返回的DataFrame的状态
    0：正常
    1：结果为空，表示在近15分钟未获取到任何数据
    2：DataFrame中的元素不完整，缺少para_list中的部分元素
    3：在脚本执行过程中产生了未知的异常
    
df: 近15分钟的DataFrame数组，可通过调整参数进行不同的查询：
    skid_id: 查询的机组编号
    para_list: 查询的参数列表
    time_scope: 时间周期，缺省为15，表示使用近15分钟的分钟数据进行聚合运算
"""
