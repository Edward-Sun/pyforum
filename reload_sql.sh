mysql -u root -p < statement.sql
python -u generate_fake_sql.py
mysql -u root -p < add_fake_data.sql