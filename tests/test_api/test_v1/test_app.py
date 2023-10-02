import unittest
import json
from api.v1.app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.index_response = '{"status":"OK"}\n'

    def test_index_route_status(self):
        response = self.app.get('/api/v1/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), self.index_response)

    def test_index_route_stats(self):
        response = self.app.get('/api/v1/stats')
        self.assertEqual(response.status_code, 200)

        count_dict = json.loads(response.data.decode('utf-8'))
        # self.assertEqual(response.data.decode('utf-8'), self.index_response)
        self.assertIn('amenities', count_dict)
        self.assertIn('cities', count_dict)
        self.assertIn('places', count_dict)
        self.assertIn('reviews', count_dict)
        self.assertIn('states', count_dict)
        self.assertIn('users', count_dict)

    def test_not_found_error_handler(self):
        response = self.app.get('/nonexistent-route')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['error'], 'Not found')

    # def test_bad_request_error_handler(self):
    #     response = self.app.get('/some-route-with-bad-request')
    #     self.assertEqual(response.status_code, 400)
    #     custom_message = response.data.decode('utf-8')
    #     self.assertIn('Bad Request', custom_message)

if __name__ == '__main__':
    unittest.main()
