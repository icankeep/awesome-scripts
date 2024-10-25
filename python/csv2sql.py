'''
提供建表语句 以及 数据CSV（包含header），即可生成CSV数据的INSERT SQL语句
'''


# TODO 替换为你的建表语句
create_table_sql = """
CREATE TABLE `task_meta` (
  `id` bigint(20) unsigned NOT NULL COMMENT 'task id',
  `task_group_id` bigint(20) NOT NULL COMMENT '任务所属的组',
  `task_name` varchar(256) NOT NULL COMMENT '任务名称',
  `task_desc` varchar(256) NOT NULL COMMENT '任务描述',
  PRIMARY KEY (`id`),
  KEY `idx_task_group` (`task_group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='任务元数据'
"""
csv_path = 'demo.csv'


# 1. 先通过正则表达式获取表名 (?i)create\s+table\s+`?([^\s\(`]+)`?
import re
import pandas as pd
table_name = re.search(r'(?i)create\s+table\s+`?([^\s\(`]+)`?', create_table_sql).group(1)
# print(table_name)

# 2. 再通过正则表达式获取每一列的类型, 使用正则表达式匹配 
col_pattern = r'(?i)\s*`?([^`\s]+)`?\s+(tinyint\(1\)|tinyint|smallint|int|mediumint|bigint|float|double|decimal|varchar|char|tinytext|text|mediumtext|longtext|datetime|time|date|enum|set|blob|timestamp|json)[\s,\)\(]+(.+)'
col_matches = re.finditer(col_pattern, create_table_sql)
col_types_map = {}
for match in col_matches:
    col_name = match.group(1)
    col_type = match.group(2)
    col_types_map[col_name] = col_type

# 3. 读取csv文件，并遍历生成INSERT SQL语句
pdf = pd.read_csv(csv_path)
for index, row in pdf.iterrows():
    insert_sql = f"INSERT INTO `{table_name}` ("
    values_sql = "VALUES ("
    for col_name, col_type in col_types_map.items():
        insert_sql += f"`{col_name}`,"
        if col_type in ['tinyint(1)', 'tinyint', 'smallint', 'int', 'mediumint', 'bigint', 'float', 'double', 'decimal']:
            values_sql += f"{row[col_name]},"
        else:
            # 判断为空的情况
            if pd.isna(row[col_name]):
                values_sql += "'',"
                continue
            values_sql += f"'{row[col_name]}',"
    insert_sql = insert_sql[:-1] + ") "
    values_sql = values_sql[:-1] + ") "
    print(insert_sql + values_sql + ";")

