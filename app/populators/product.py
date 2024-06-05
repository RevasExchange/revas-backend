import pycountry
from sqlalchemy.orm import Session
from ..models import crud


products_data = [
    {"name": "PET", "description": "Polyethylene Terephthalate"},
    {"name": "HDPE", "description": "High-Density Polyethylene"},
    {"name": "LDPE", "description": "Low-Density Polyethylene"},
    {"name": "PP", "description": "Polypropylene"},
    {"name": "PS", "description": "Polystyrene"},
    {"name": "PVC", "description": "Polyvinyl Chloride"},
    {"name": "Polycarbonate", "description": "Polycarbonate (PC)"},
    {
        "name": "Polyethylene Terephthalate Glycol",
        "description": "Polyethylene Terephthalate Glycol (PETG)",
    },
    {
        "name": "Acrylonitrile Butadiene Styrene",
        "description": "Acrylonitrile Butadiene Styrene (ABS)",
    },
    {
        "name": "Polyethylene Naphthalate",
        "description": "Polyethylene Naphthalate (PEN)",
    },
    {"name": "Polylactic Acid", "description": "Polylactic Acid (PLA)"},
    {"name": "Polyurethane", "description": "Polyurethane (PU)"},
    {
        "name": "Polyvinylidene Fluoride",
        "description": "Polyvinylidene Fluoride (PVDF)",
    },
    {"name": "Polyethylene", "description": "Polyethylene (PE)"},
    {
        "name": "Polycarbonate/Acrylonitrile Butadiene Styrene",
        "description": "Polycarbonate/Acrylonitrile Butadiene Styrene (PC/ABS) blends",
    },
    {"name": "Cold Washed Flakes", "description": "Cold Washed Flakes"},
    {"name": "Hot washed Flakes", "description": "Hot washed Flakes"},
    {"name": "Pellets or Granules", "description": "Pellets or Granules"},
    {
        "name": "Regrind or Reprocessed Plastic",
        "description": "Regrind or Reprocessed Plastic",
    },
    {"name": "Baled Plastic", "description": "Baled Plastic"},
    {"name": "Powdered Plastic", "description": "Powdered Plastic"},
    {"name": "Flakes with Additives", "description": "Flakes with Additives"},
    {"name": "Mixed Plastic Resin", "description": "Mixed Plastic Resin"},
    {"name": "Clean Regrind", "description": "Clean Regrind"},
    {"name": "Film or Sheet Rolls", "description": "Film or Sheet Rolls"},
    {
        "name": "Customized Blends or Compounds",
        "description": "Customized Blends or Compounds",
    },
]


async def populate_db(db: Session):
    """
    Asynchronously populates the database with products.

    Args:
        db (Session): The database session.

    Returns:
        None
    """
    for product in products_data:
        await crud.populate_products(db, product)

    print("Database populated with products.")
