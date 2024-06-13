from bd_conexion import conection_db
from hb_api import hbapi
from datetime import datetime as dt
import time

if __name__=='__main__':
    inicio_tiempo = time.time()
    api = hbapi()
    dba = conection_db()
    
    datoshb = api.get_deals_date(dt.today())
    # datoshb = api.get_deals_date('2024-06-12')
    print(len(datoshb))
    
    for i in range(len(datoshb)):
        propiedades = datoshb[i]['properties']
        objectdba=dba.get_data_hb(propiedades['hs_object_id'])
        if objectdba:
            objectdba=objectdba[0]
       
        
        if objectdba:
            if (api.transform_dealstage(propiedades['dealstage'])!=objectdba['Deal Stage']) or (api.get_user(propiedades['hubspot_owner_id'])!=objectdba['Deal owner']) :
                    if objectdba['Deal Stage']!='CLOSED WON':
                        print(dba.insert_data(
                                record_id=propiedades['hs_object_id'],                  # record_id
                                dealname=propiedades['dealname'],     # dealname
                                amount=propiedades['amount'],                # amount
                                factoryfacility=propiedades['factoring_facility'],  # factoryfacility
                                concentration=propiedades['p_concentration__'],                    # concentration
                                contractterm=propiedades['p_contract_term__months_'],                      # contractterm
                                ach=propiedades['ach'],                    # ach
                                wire=propiedades['wire'],                    # wire
                                reserve=propiedades['reserve'],                     # reserve
                                factoringfee=propiedades['pfactoringfee'],                     # factoringfee
                                duediligence=propiedades['p_due_diligence_fee__'],                 # duediligence
                                fueladvancecharge=propiedades['fuel_advance_charge'],                  # fueladvancecharge
                                fueladvance=propiedades['fuel_advance__'],                     # fueladvance
                                fuelcard=propiedades['fuel_card'],           # fuelcard
                                dealstage=api.transform_dealstage(propiedades['dealstage']),               # dealstage
                                closedate=api.date_format(propiedades['closedate']),            # closedate
                                createdate=api.date_format(propiedades['createdate']),            # createdate
                                lastactivity=api.date_format(propiedades['hs_lastmodifieddate']),            # lastactivity
                                dealowner=api.get_user(propiedades['hubspot_owner_id']),              # dealowner
                                weightedamount=propiedades['hs_projected_amount'],                # weightedamount
                                companie=api.get_companie(api.get_associations(propiedades['hs_object_id']))['name'],              # companie
                                idCompanie=api.get_companie(api.get_associations(propiedades['hs_object_id']))['id'],             # companieid
                                truckt=api.get_companie(api.get_associations(propiedades['hs_object_id']))['type_of_truck']
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
                record_id=propiedades['hs_object_id'],                  # record_id
                dealname=propiedades['dealname'],     # dealname
                amount=propiedades['amount'],                # amount
                factoryfacility=propiedades['factoring_facility'],  # factoryfacility
                concentration=propiedades['p_concentration__'],                    # concentration
                contractterm=propiedades['p_contract_term__months_'],                      # contractterm
                ach=propiedades['ach'],                    # ach
                wire=propiedades['wire'],                    # wire
                reserve=propiedades['reserve'],                     # reserve
                factoringfee=propiedades['pfactoringfee'],                     # factoringfee
                duediligence=propiedades['p_due_diligence_fee__'],                 # duediligence
                fueladvancecharge=propiedades['fuel_advance_charge'],                  # fueladvancecharge
                fueladvance=propiedades['fuel_advance__'],                     # fueladvance
                fuelcard=propiedades['fuel_card'],           # fuelcard
                dealstage=api.transform_dealstage(propiedades['dealstage']),               # dealstage
                closedate=api.date_format(propiedades['closedate']),            # closedate
                createdate=api.date_format(propiedades['createdate']),            # createdate
                lastactivity=api.date_format(propiedades['notes_last_updated']),            # lastactivity
                dealowner=api.get_user(propiedades['hubspot_owner_id']),              # dealowner
                weightedamount=propiedades['hs_projected_amount'],                # weightedamount
                companie=api.get_companie(api.get_associations(propiedades['hs_object_id']))['name'],              # companie
                idCompanie=api.get_companie(api.get_associations(propiedades['hs_object_id']))['id'],
                truckt=api.get_companie(api.get_associations(propiedades['hs_object_id']))['type_of_truck']
            ))
    fin_tiempo = time.time()
    print('\n\n----------\n')
    tiempo_transcurrido = fin_tiempo-inicio_tiempo
    print('tiempo transcurrido: ',tiempo_transcurrido/60,' minutos')
    
    print('ejecutado a las : ',dt.now())