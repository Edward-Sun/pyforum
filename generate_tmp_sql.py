import config
with open('tmp1.sql', 'w') as fout:
    fout.write("DROP DATABASE IF EXISTS `"+config.MYSQL_NAME+"`;\n")
    fout.write("CREATE DATABASE `"+config.MYSQL_NAME+"`;\n")
    fout.write("USE "+config.MYSQL_NAME+";\n")