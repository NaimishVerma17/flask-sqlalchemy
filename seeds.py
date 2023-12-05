from main import db, app
from sqlalchemyseed import load_entities_from_json
from sqlalchemyseed import Seeder

with app.app_context():

    entities = load_entities_from_json('cars.json')

    # Initializing Seeder
    seeder = Seeder(db.session)

    # Seeding
    seeder.seed(entities)

    # Committing
    db.session.commit()  # or seeder.session.commit()