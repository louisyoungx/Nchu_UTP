# -*- coding: utf-8 -*

# 配置数据库MySQL
import pymysql

pymysql.version_info = (1, 4, 0, "final", 0)

pymysql.install_as_MySQLdb()
