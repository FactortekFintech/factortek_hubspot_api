from bd_conexion import conection_db
from hb_api import hbapi
from datetime import datetime as dt


if __name__=='__main__':
    api = hbapi()
    dba = conection_db()
    
    datoshb = api.get_deals_date(dt.today())
    print(len(datoshb))
    for i in range(len(datoshb)):
        propiedades = datoshb[i]['properties']
        objectdba=dba.get_data_hb(propiedades['hs_object_id'])
        if objectdba:
            objectdba=objectdba[0]
       
        
        if objectdba:
            if (api.transform_dealstage(propiedades['dealstage'])!=objectdba['Deal Stage']) or (api.get_user(propiedades['hubspot_owner_id'])!=objectdba['Deal owner']) :
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
    companie=api.get_companie(api.get_associations(propiedades['hs_object_id']))              # companie
))
                
            else:
                print('last updated ok')
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
    companie=api.get_companie(api.get_associations(propiedades['hs_object_id']))              # companie
))
        