mysql -u root -p < statement.sql $(python get_database_name.py)
python -u generate_fake_sql.py
mysql -u root -p < add_fake_data.sql