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
        query = f'select * from template_dba_import where `Record ID` = {record} order by `Last Activity Date` desc limit 1'
        self.cursor.execute(query)
        columns = []
        data = []
        for colum in self.cursor.description:
            columns.append(colum[0])
            
        for row in self.cursor.fetchall():
            data.append(dict(zip(columns, row)))
        
        return data
    
    def insert_data(self, record_id, factoryfacility=None, concentration=None, contractterm=None, ach=None, wire=None, reserve=None, factoringfee=None, duediligence=None, fueladvancecharge=None, fueladvance=None, fuelcard=None, dealstage=None, closedate=None, createdate=None, lastactivity=None, dealowner=None, weightedamount=None, companie=None, dealname=None, amount=None):
        query = """
        INSERT INTO template_dba_import (
            `Record ID`, `Deal Name`, `Amount`, `Factoring Facility`, `P-Concentration %`, `P-Contract Term (Months)`, 
            `ACH`, `Wire`, `Reserve`, `P-Factoring Fee (%)`, `P-Due Diligence Fee $`, `Fuel Advance Charge`, 
            `Fuel Advance %`, `Fuel Card`, `Deal Stage`, `Close Date`, `Create Date`, `Last Activity Date`, 
            `Deal owner`, `Weighted amount`, `Associated Company`
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )"""

        data = (
            record_id, dealname, amount, factoryfacility, concentration, contractterm, 
            ach, wire, reserve, factoringfee, duediligence, fueladvancecharge, fueladvance, 
            fuelcard, dealstage, closedate, createdate, lastactivity, dealowner, 
            weightedamount, companie
        )

        try:
            self.cursor.execute(query, data)
            self.conexion.commit()
            return 'Data inserted successfully'
        except Exception as e:
            return str(e)
    
# if __name__=='__main__':
#     db = conection_db()
# #     print(db.insert_data(
# #     156165,                  # record_id
# #     'Deal Name Example',     # dealname
# #     50000.00,                # amount
# #     'Factoring Facility A',  # factoryfacility
# #     10.5,                    # concentration
# #     12,                      # contractterm
# #     True,                    # ach
# #     True,                    # wire
# #     5.0,                     # reserve
# #     2.5,                     # factoringfee
# #     1000.00,                 # duediligence
# #     150.00,                  # fueladvancecharge
# #     3.0,                     # fueladvance
# #     'Fuel Card A',           # fuelcard
# #     'Stage 1',               # dealstage
# #     '2024-05-30',            # closedate
# #     '2024-05-15',            # createdate
# #     '2024-05-29 12:05:01',            # lastactivity
# #     'John Doe',              # dealowner
# #     48000.00,                # weightedamount
# #     'Company A'              # companie
# # ))
#     hb_data_test = {
#         "Record ID": 156165,
#         'dealstage': 'Stage 1',
#         'Deal owner': 'John Doe',
        
#     }
#     id = hb_data_test['Record ID']
#     data = db.get_data_hb(int(id))

   
#     if data:
#         deal = data[0]
#         if int(deal['Record ID']) == hb_data_test['Record ID']:
#             if deal['Deal Stage'] != hb_data_test['dealstage'] or deal['Deal owner']!= hb_data_test['Deal owner']:
#                 print(' aca si ingresa')
#             else:
#                 print('el registro del log se encuentra en su ultimo update')
#         else:
#             print('por defecto se tiene que ingresar el registro para el log')
#     else:
#         print('no existe este registro')
        
    
 
    