from pyairtable.api.table import Table
from pyairtable.formulas import match
from manager.models import Company, Round

def get_table() -> Table:
    # api_key = os.environ['AIRTABLE_API_KEY']
    api_key = "pat26KJH4X0qIqf2n.d984b9c0b28c4b01aece932f5c161fb929517eaf20c552d8ccf56833b20c3ac0"
    base_id = "appWOVgCBFMTI9f70"
    table_name = "tblcTQLrGAeZe79iJ"
    table = Table(api_key, base_id, table_name)
    return table

def get_company(comp_number : str) -> dict | None:
    table = get_table()
    company_airtable: dict | None = table.first(formula = match({'Wayra ID Link': comp_number}))

    if(company_airtable == None): # no value found
        return None
    # print(company_airtable)
    return company_airtable['fields']

def update_all():
    for company_airtable in get_table().all() :
        comp_number:str = company_airtable['fields']['Wayra ID Link']
        company_query = Company.objects.filter(number = comp_number)
        
        company_model:Company = company_query.first() or Company.objects.create(number = comp_number)

        company_model.update_comp(company_airtable['fields'])
        for round_number in range(1,11):
            date = company_airtable['fields'].get(f"(Round {round_number}) - Date Link");
            if(date == None):
                break
            current_round = Round.objects.filter(company = company_model, round_number = round_number).first() or \
                    Round.objects.create(company = company_model, round_number = round_number)

            current_round.update_round(company_airtable['fields'])



"""
from manager.utils import airtable
airtable.get_company("W00278")
airtable.update_all()
"""
