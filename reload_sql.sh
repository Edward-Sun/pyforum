python -u generate_tmp_sql.py
cat tmp1.sql statement.sql > tmp2.sql
mysql -u root -p < tmp2.sql
python -u generate_fake_sql.py
mysql -u root -p < add_fake_data.sql