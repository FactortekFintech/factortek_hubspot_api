import requests
import datetime
from datetime import datetime as dt
import os 
from dotenv import load_dotenv

class hbapi():
    load_dotenv()
    url = 'https://api.hubspot.com/crm/v3/'
    token = os.getenv('apikey')
    today = dt.today()
    
    
    
    def transform_date(self,date):
        # Asegurarse de que la fecha sea una cadena en el formato adecuado
        if isinstance(date, datetime.datetime):
            date_string = date.strftime("%Y-%m-%d")
        else:
            date_string = date

        # Convertir la cadena de fecha a un objeto datetime
        date_object = datetime.datetime.strptime(date_string, "%Y-%m-%d")

        # Obtener el timestamp en segundos
        timestamp_s = date_object.timestamp()

        # Convertir el timestamp a milisegundos
        timestamp_ms = int(timestamp_s * 1000)    
        
        return timestamp_ms
    
    
    def transform_dealstage(self,dealstage):
        if dealstage =='contractsent':
            return 'PROSPECT F/U'
        if dealstage == 'appointmentscheduled':
            return 'PROPOSAL SENT'
        if dealstage =='qualifiedtobuy':
            return 'AGREEMENT SENT'
        if dealstage == 'presentationscheduled':
            return 'AGREEMENT SIGNED'
        if dealstage == 'decisionmakerboughtin':
            return 'UNDERWRITING'
        if dealstage == '13029817':
            return 'ACCOUNT CREATED'
        if dealstage == 'closedwon':
            return 'CLOSED WON'
        if dealstage == 'closedlost':
            return 'CLOSED LOST'
    

    def get_user(self,id_user):
        url = f'{self.url}objects/users/search'
        headers = {'Authorization':f'Bearer {self.token}','Content-Type':'application/json'}
        data ={
            
    "limit": 100,
    "properties":["hs_given_name","hs_family_name"],
    "filterGroups": [
        {
            "filters": [
                {
                    "propertyName": "id",
                    "operator": "EQ",
                    "value": id_user
                }
            ]
        }
    ]
    
}
        
        response = requests.post(url=url,json=data,headers=headers)
        hbresult=response.json()
        
        results = hbresult['results'][0]
        user = results['properties']
        
        strike = user['hs_given_name']+' '+user['hs_family_name']
       
        
        return strike
        

    def get_deals_date(self,date):
        url = f'{self.url}objects/deals/search'
        headers = {'Authorization':f'Bearer {self.token}','Content-Type':'application/json'}
        data = {
    "properties": [
        "dealname",
        "amount",
        "factoring_facility",
        "p_concentration__",
        "p_contract_term__months_",
        "ach",
        "wire",
        "reserve",
        "pfactoringfee",
        "p_due_diligence_fee__",
        "fuel_advance_charge",
        "fuel_advance__",
        "fuel_card",
        "closedate",
        "createdate",
        "dealstage",
        "notes_last_updated",
        "hubspot_owner_id",
        "quote"
    ],

     "filterGroups": [
        {
            "filters": [
                {
                    "propertyName": "notes_last_updated",
                    "operator": "GTE",
                    "value": self.transform_date(date)
                }
            ]
        }
    ],
    "limit":100

}
        response = requests.post(url=url, json=data, headers=headers)
        hbresult = response.json()
        results = hbresult['results']
        return results
       
        


if __name__=='__main__':
    api = hbapi()
    datos = api.get_deals_date(dt.today())
    
    for i in range(len(datos)):
        print(datos[i]['id'])
        propiedades = datos[i]['properties']
        print(propiedades['dealname'])
        print(api.transform_dealstage(propiedades['dealstage']))
        print('---------------------------------------')
