import requests
import datetime
from datetime import datetime as dt
import os
from dotenv import load_dotenv

class hbapi():
    def __init__(self):
        load_dotenv()
        self.url = 'https://api.hubspot.com/crm/v3/'
        self.token = os.getenv('apikey')
        self.today = dt.today()

    def date_format(self, dateob):
        if not dateob:
            return ''
        iso_date_str = dateob
        try:
            dte = dt.strptime(iso_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            dte = dt.strptime(iso_date_str, '%Y-%m-%dT%H:%M:%SZ')
        formatted_date_str = dte.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_date_str

    def transform_date(self, date):
        if isinstance(date, datetime.datetime):
            date_string = date.strftime("%Y-%m-%d")
        else:
            date_string = date
        date_object = datetime.datetime.strptime(date_string, "%Y-%m-%d")
        timestamp_s = date_object.timestamp()
        timestamp_ms = int(timestamp_s * 1000)
        return timestamp_ms

    def get_companie(self, id_companie):
        url = f'{self.url}/objects/companies/{id_companie}?properties=us_dot_number,name,type_of_truck'
        headers = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            propiedades = data.get('properties', {})
            companie = {
                'name': propiedades.get('name'),
                'id': propiedades.get('hs_object_id'),
                'type_of_truck': propiedades.get('type_of_truck')
            }
            return companie
        else:
            return {'name': None, 'id': None, 'type_of_truck': None}

    def get_associations(self, deal_id):
        url = f'{self.url}objects/deals/{deal_id}/associations/Companies'
        headers = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data and data['results']:
                return data['results'][0]['id']
        return 0

    def transform_dealstage(self, dealstage):
        dealstage_mapping = {
            'contractsent': 'PROSPECT F/U',
            'appointmentscheduled': 'PROPOSAL SENT',
            'qualifiedtobuy': 'AGREEMENT SENT',
            'presentationscheduled': 'AGREEMENT SIGNED',
            'decisionmakerboughtin': 'UNDERWRITING',
            '13029817': 'ACCOUNT CREATED',
            'closedwon': 'CLOSED WON',
            'closedlost': 'CLOSED LOST'
        }
        return dealstage_mapping.get(dealstage, dealstage)

    def get_user(self, id_user):
        url = f'{self.url}owners/{id_user}'
        headers = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            hbresult = response.json()
            return f"{hbresult['firstName']} {hbresult['lastName']}"
        return 'No Owner'

    def get_deals_date(self, date):
        url = f'{self.url}objects/deals/search'
        headers = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
        data = {
            "properties": [
                "dealname", "amount", "factoring_facility", "p_concentration__", "p_contract_term__months_",
                "ach", "wire", "reserve", "pfactoringfee", "p_due_diligence_fee__", "fuel_advance_charge",
                "fuel_advance__", "fuel_card", "closedate", "createdate", "dealstage", "notes_last_updated",
                "hubspot_owner_id", "hs_projected_amount", "hs_lastmodifieddate"
            ],
            "filterGroups": [
                {
                    "filters": [
                        {"propertyName": "hs_lastmodifieddate", "operator": "GTE", "value": self.transform_date(date)}
                    ]
                }
            ],
            "limit": 100
        }
        all_results = []
        while True:
            response = requests.post(url=url, json=data, headers=headers)
            response.raise_for_status()
            hbresult = response.json()
            all_results.extend(hbresult.get('results', []))
            paging = hbresult.get('paging')
            if paging and 'next' in paging and 'after' in paging['next']:
                data['after'] = paging['next']['after']
            else:
                break
        return all_results

if __name__ == '__main__':
    api = hbapi()
    datos = api.get_deals_date(dt.today())
    print(len(datos))
    for i in range(len(datos)):
        propiedades = datos[i]['properties']
        print('Record ID: ', propiedades['hs_object_id'])
        print('Deal Name: ' + propiedades['dealname'])
        print('Amount: ' + propiedades['amount'])
        print('Factory Facility: ', propiedades['factoring_facility'])
        print('P Concentration: ', propiedades['p_concentration__'])
        print('Deal Stage: ', api.transform_dealstage(propiedades['dealstage']))
        owner = propiedades['hubspot_owner_id']
        print('Owner: ', api.get_user(int(owner)))
        print('Companie: ', api.get_companie(api.get_associations(datos[i]['id'])))
        print('Ultima actividad: ', api.date_format(propiedades['notes_last_updated']))
        print('created : ', api.date_format(propiedades['createdate']))
        print('closedated : ', api.date_format(propiedades['closedate']))
        print('---------------------------------------')
