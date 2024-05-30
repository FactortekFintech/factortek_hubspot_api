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
    
    def date_format(self,dateob):
        iso_date_str = dateob
        if dateob:
            try:
                dte = dt.strptime(iso_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            except :
                dte = dt.strptime(iso_date_str, '%Y-%m-%dT%H:%M:%SZ')

        # Formatear el objeto datetime a la cadena deseada
            formatted_date_str = dte.strftime('%Y-%m-%d %H:%M:%S')
            if formatted_date_str:
                return formatted_date_str
            else:
                return ''
        else: return ''
            
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
    
    
    def get_companie(self,id_companie):
        url = f'{self.url}/objects/companies/{id_companie}'
        headers = {'Authorization':f'Bearer {self.token}','Content-Type':'application/json'}
        
        response = requests.get(url=url,headers=headers)
        if response.status_code == 200:
            data = response.json()

        if data:
            propiedades = data['properties']
            return propiedades['name']

    
    def get_associations(self, deal_id):
        url = f'{self.url}objects/deals/{deal_id}/associations/Companies'
        headers = {'Authorization':f'Bearer {self.token}','Content-Type':'application/json'}
        
        response = requests.get(url=url,headers=headers )
        if response.status_code == 200:
            data = response.json()
        
        if data:
         results = data['results'][0]
         return results['id']
            
        
        
        
    
    
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
        url = f'{self.url}owners/{id_user}'
        headers = {'Authorization':f'Bearer {self.token}','Content-Type':'application/json'}
 
        
        response = requests.get(url=url,headers=headers)
        if response.status_code == 200:
            hbresult=response.json()
            return f"{hbresult['firstName']} {hbresult['lastName']}"
        else: return 'No Owner'
        
    
        


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
       "hs_projected_amount"
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
    print(len(datos))
    for i in range(len(datos)):
        
        propiedades = datos[i]['properties']
        
        print('Record ID: ',propiedades['hs_object_id'])
        print('Deal Name: '+propiedades['dealname'])
        print('Amount: '+propiedades['amount'])
        print('Factory Facility: ',propiedades['factoring_facility'])
        print('P Concentration: ',propiedades['p_concentration__'])
        print('Deal Stage: ',api.transform_dealstage(propiedades['dealstage']))
        owner = propiedades['hubspot_owner_id']
        print('Owner: ',api.get_user(int(owner)))
        print('Companie: ',api.get_companie(api.get_associations(datos[i]['id'])))
        print('Ultima actividad: ',api.date_format(propiedades['notes_last_updated']))
        print('created : ',api.date_format(propiedades['createdate']))
        print('closedated : ',api.date_format(propiedades['closedate']))
        
        
        print('---------------------------------------')


