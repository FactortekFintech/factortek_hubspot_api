import mysql.connector
import os 
from dotenv import load_dotenv


class conection_db():
    load_dotenv()
    
    config = {
    'user': os.getenv('user_bd'),
    'password': os.getenv('password'),
    'host': os.getenv('host'),
    'database': 'test_factorsoft',
    'port': 3306
            }
    conexion = mysql.connector.connect(**config)

# Crea un cursor para ejecutar consultas SQL
    cursor = conexion.cursor()
    
    def get_data_hb(self,record):
        query = f'select * from template_dba_import where `Record ID` = {record}'
        self.cursor.execute(query)
        columns = []
        data = []
        for colum in self.cursor.description:
            columns.append(colum[0])
            
        for row in self.cursor.fetchall():
            data.append(dict(zip(columns, row)))
        
        return data
    
    
    
if __name__=='__main__':
    db = conection_db()
    data = db.get_data_hb(10006655075)
    if data:
        deal = data[0]
        print(deal)
        print(len(data))
    else:
        print(len(data))
        
    
 
    