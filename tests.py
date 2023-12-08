import unittest
from flask_testing import TestCase
import app
from config import db, app
from models import Car


# Create a test class that inherits from Flask-Testing's TestCase
class APITestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_cars(self):
        # Create some test data
        car1 = Car(name='Toyota', color='Camry', type='petrol', gear='manual', price=300, brand='Toyota', image="")
        car2 = Car(name='Honda', color='Blue', type='diesel', gear='automatic', price=500, brand='Toyota', image="")
        db.session.add_all([car1, car2])
        db.session.commit()

        # Make a request to the API endpoint that fetches the list of cars
        response = self.client.get('/cars')

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the expected data
        data = response.json
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'Toyota')
        self.assertEqual(data[0]['price'], 300)
        self.assertEqual(data[1]['name'], 'Honda')
        self.assertEqual(data[1]['price'], 500)


if __name__ == '__main__':
    unittest.main()
    app.run()
