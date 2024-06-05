import pycountry
from sqlalchemy.orm import Session
from ..models import crud


async def get_countries():
    """
    Asynchronously retrieves a list of countries from the `pycountry` library.

    Returns:
        A list of dictionaries, where each dictionary contains the following keys:
        - "name" (str): The name of the country.
        - "alpha_2" (str): The two-letter ISO 3166-1 alpha-2 country code.
        - "alpha_3" (str): The three-letter ISO 3166-1 alpha-3 country code.
    """
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
    """
    Asynchronously retrieves a list of states from a given country code.

    Args:
        country_alpha_2 (str): The two-letter ISO 3166-1 alpha-2 country code.

    Returns:
        List[Dict[str, str]]: A list of dictionaries, where each dictionary contains the name of a state.
            The keys in the dictionary are "name" (str).

    Example:
        >>> await get_states("US")
        [{"name": "Alabama"}, {"name": "Alaska"}, ...]
    """
    subdivisions = pycountry.subdivisions.get(country_code=country_alpha_2)
    states = []
    if subdivisions:
        for subdivision in subdivisions:
            states.append({"name": subdivision.name})
    return states


async def populate_db(db: Session):
    """
    Asynchronously populates the database with countries and their respective states.

    Args:
        db (Session): The database session.

    Returns:
        None

    Raises:
        None

    Example:
        >>> async with Session() as session:
        ...     await populate_db(session)
        Database populated with countries and states.
    """
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
