import pandas as pd
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

data = pd.read_csv('/Users/madsfrandsen/Documents/DIS/Group_Project/twizzle/dataset/MOCK_DATA.csv')

data['hashed_password'] = data['password'].apply(lambda password: bcrypt.generate_password_hash(password).decode('utf-8'))

data.to_csv('/Users/madsfrandsen/Documents/DIS/Group_Project/twizzle/dataset/data_with_hashed.csv', index=False)



data = pd.read_csv('/Users/madsfrandsen/Documents/DIS/Group_Project/twizzle/dataset/data_with_hashed.csv')

data = data.drop('password', axis=1)

new_csv_file_path = '/Users/madsfrandsen/Documents/DIS/Group_Project/twizzle/dataset/only_hashed.csv'

data.to_csv(new_csv_file_path, index=False)