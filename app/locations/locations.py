import pycountry
from sqlalchemy.orm import Session
from ..models import crud


async def get_countries():
    countries = []
    for country in pycountry.countries:
        countries.append(
            {
                "name": country.name,
                "alpha_2": country.alpha_2,
                "alpha_3": country.alpha_3,
            }
        )
    return countries


async def get_states(country_alpha_2):
    subdivisions = pycountry.subdivisions.get(country_code=country_alpha_2)
    states = []
    if subdivisions:
        for subdivision in subdivisions:
            states.append({"name": subdivision.name})
    return states


async def populate_db(db: Session):
    countries = await get_countries()
    for country_data in countries:
        cnty = {
            "name": country_data["name"],
            "alpha_2": country_data["alpha_2"],
            "alpha_3": country_data["alpha_3"],
        }
        country = await crud.create_country(db, cnty)

        states = await get_states(country.alpha_2)
        for state_data in states:
            ste = {"name": state_data["name"], "country_id": country.id}
            await crud.create_state(db, ste)

    print("Database populated with countries and states.")
