import mysql.connector
import os
from dotenv import load_dotenv

class conection_db():
    def __init__(self):
        load_dotenv()
        
        self.config = {
            'user': os.getenv('user_bd'),
            'password': os.getenv('password'),
            'host': os.getenv('host'),
            'database': os.getenv('database', 'test_factorsoft'),
            'port': int(os.getenv('port', 3306))
        }
        
        try:
            self.conexion = mysql.connector.connect(**self.config)
            self.cursor = self.conexion.cursor()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.conexion = None
            self.cursor = None

    def get_data_hb(self, record):
        if self.cursor is None:
            return []

        query = f'SELECT * FROM template_dba_import WHERE `Record ID` = {record} ORDER BY `Last Activity Date` DESC LIMIT 1'
        self.cursor.execute(query)
        columns = [col[0] for col in self.cursor.description]
        data = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        return data
    
    def insert_data(self, record_id, factoryfacility=None, concentration=None, contractterm=None, ach=None, wire=None, reserve=None, factoringfee=None, duediligence=None, fueladvancecharge=None, fueladvance=None, fuelcard=None, dealstage=None, closedate=None, createdate=None, lastactivity=None, dealowner=None, weightedamount=None, companie=None, dealname=None, amount=None, idCompanie=None, truckt=None):
        if self.cursor is None:
            return "No database connection."

        query = """
        INSERT INTO template_dba_import (
            `Record ID`, `Deal Name`, `Amount`, `Factoring Facility`, `P-Concentration %`, `P-Contract Term (Months)`, 
            `ACH`, `Wire`, `Reserve`, `P-Factoring Fee (%)`, `P-Due Diligence Fee $`, `Fuel Advance Charge`, 
            `Fuel Advance %`, `Fuel Card`, `Deal Stage`, `Close Date`, `Create Date`, `Last Activity Date`, 
            `Deal owner`, `Weighted amount`, `Associated Company`,`Associated Company IDs`,type_of_truck
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s
        )"""

        data = (
            record_id, dealname, amount, factoryfacility, concentration, contractterm, 
            ach, wire, reserve, factoringfee, duediligence, fueladvancecharge, fueladvance, 
            fuelcard, dealstage, closedate, createdate, lastactivity, dealowner, 
            weightedamount, companie, idCompanie, truckt
        )

        try:
            self.cursor.execute(query, data)
            self.conexion.commit()
            return 'Data inserted successfully'
        except Exception as e:
            return str(e)
