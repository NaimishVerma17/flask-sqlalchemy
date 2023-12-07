from app import db, app
from sqlalchemyseed import load_entities_from_json
from sqlalchemyseed import Seeder

with app.app_context():
    # Loading the json file with dummy data
    entities = load_entities_from_json('cars.json')

    # Initializing Seeder
    seeder = Seeder(db.session)

    # Seeding
    seeder.seed(entities)

    # Committing
    db.session.commit()
