from bd_conexion import conection_db
from hb_api import hbapi
from datetime import datetime as dt
import time

if __name__ == '__main__':
    inicio_tiempo = time.time()
    api = hbapi()
    dba = conection_db()
    
    if dba.conexion is None:
        print("Failed to connect to the database.")
        exit(1)

    datoshb = api.get_deals_date(dt.today())
    print(len(datoshb))
    
    for i in range(len(datoshb)):
        propiedades = datoshb[i]['properties']
        objectdba = dba.get_data_hb(propiedades['hs_object_id'])
        if objectdba:
            objectdba = objectdba[0]
        
        if objectdba:
            if (api.transform_dealstage(propiedades['dealstage']) != objectdba['Deal Stage']) or (api.get_user(propiedades['hubspot_owner_id']) != objectdba['Deal owner']):
                if objectdba['Deal Stage'] != 'CLOSED WON':
                    print(dba.insert_data(
                        record_id=propiedades['hs_object_id'], dealname=propiedades['dealname'], amount=propiedades['amount'], factoryfacility=propiedades['factoring_facility'], concentration=propiedades['p_concentration__'], contractterm=propiedades['p_contract_term__months_'], ach=propiedades['ach'], wire=propiedades['wire'], reserve=propiedades['reserve'], factoringfee=propiedades['pfactoringfee'], duediligence=propiedades['p_due_diligence_fee__'], fueladvancecharge=propiedades['fuel_advance_charge'], fueladvance=propiedades['fuel_advance__'], fuelcard=propiedades['fuel_card'], dealstage=api.transform_dealstage(propiedades['dealstage']), closedate=api.date_format(propiedades['closedate']), createdate=api.date_format(propiedades['createdate']), lastactivity=api.date_format(propiedades['hs_lastmodifieddate']), dealowner=api.get_user(propiedades['hubspot_owner_id']), weightedamount=propiedades['hs_projected_amount'], companie=api.get_companie(api.get_associations(propiedades['hs_object_id']))['name'], idCompanie=api.get_companie(api.get_associations(propiedades['hs_object_id']))['id'], truckt=api.get_companie(api.get_associations(propiedades['hs_object_id']))['type_of_truck']
                    ))
                    print(i)
                    print(propiedades['hs_object_id'])
                    print('-----------------------------\n\n')
                else:
                    print(propiedades['hs_object_id'])
                    print('Already CLOSED WON')
                    print('-----------------\n\n')
            else:
                print(i)
                print('last updated ok')
                print(propiedades['hs_object_id'])
                print('----------------------------\n')
        else:
            print(dba.insert_data(
                record_id=propiedades['hs_object_id'], dealname=propiedades['dealname'], amount=propiedades['amount'], factoryfacility=propiedades['factoring_facility'], concentration=propiedades['p_concentration__'], contractterm=propiedades['p_contract_term__months_'], ach=propiedades['ach'], wire=propiedades['wire'], reserve=propiedades['reserve'], factoringfee=propiedades['pfactoringfee'], duediligence=propiedades['p_due_diligence_fee__'], fueladvancecharge=propiedades['fuel_advance_charge'], fueladvance=propiedades['fuel_advance__'], fuelcard=propiedades['fuel_card'], dealstage=api.transform_dealstage(propiedades['dealstage']), closedate=api.date_format(propiedades['closedate']), createdate=api.date_format(propiedades['createdate']), lastactivity=api.date_format(propiedades['hs_lastmodifieddate']), dealowner=api.get_user(propiedades['hubspot_owner_id']), weightedamount=propiedades['hs_projected_amount'], companie=api.get_companie(api.get_associations(propiedades['hs_object_id']))['name'], idCompanie=api.get_companie(api.get_associations(propiedades['hs_object_id']))['id'], truckt=api.get_companie(api.get_associations(propiedades['hs_object_id']))['type_of_truck']
            ))
            print(i)
            print(propiedades['hs_object_id'])
            
    fin_tiempo = time.time()
    print('\n\n----------\n')
    tiempo_transcurrido = fin_tiempo - inicio_tiempo
    print('tiempo transcurrido: ', tiempo_transcurrido / 60, ' minutos')
    print('ejecutado a las : ', dt.now())
    print('by : Juan José Jara Alvarez')
