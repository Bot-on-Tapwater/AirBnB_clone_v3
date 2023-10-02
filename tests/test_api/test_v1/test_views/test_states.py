import unittest
from unittest.mock import patch
from io import StringIO
from api.v1.app import app
from models.state import State
from models import storage
import json


class TestStatesAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True

    @classmethod
    def tearDownClass(cls):
        storage.close()

    def setUp(self):
        storage.reload()

    def test_get_all_states(self):
        response = self.app.get('/api/v1/states')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(isinstance(data, list))

    def test_get_state_by_id(self):
        state = State(name="California")
        state.save()
        response = self.app.get(f'/api/v1/states/{state.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['name'], "California")

    # def test_get_state_by_invalid_id(self):
    #     response = self.app.get('/api/v1/states/invalid_id')
    #     self.assertEqual(response.status_code, 404)

    def test_delete_state_by_id(self):
        state = State(name="Texas")
        state.save()
        response = self.app.delete(f'/api/v1/states/{state.id}')
        self.assertEqual(response.status_code, 200)
        state_deleted = storage.get(State, state.id)
        self.assertIsNone(state_deleted)

    # def test_delete_state_by_invalid_id(self):
    #     response = self.app.delete('/api/v1/states/invalid_id')
    #     self.assertEqual(response.status_code, 404)

    def test_create_new_state(self):
        data = {'name': 'Florida'}
        response = self.app.post('/api/v1/states',
                                 data=json.dumps(data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['name'], 'Florida')

    # def test_create_new_state_missing_name(self):
    #     data = {}
    #     response = self.app.post('/api/v1/states',
    #                              data=json.dumps(data),
    #                              content_type='application/json')
    #     self.assertEqual(response.status_code, 400)

    # def test_create_new_state_invalid_content_type(self):
    #     data = {'name': 'Nevada'}
    #     response = self.app.post('/api/v1/states',
    #                              data=json.dumps(data))
    #     self.assertEqual(response.status_code, 400)

    def test_update_state(self):
        state = State(name="Arizona")
        state.save()
        data = {'name': 'New Arizona'}
        response = self.app.put(f'/api/v1/states/{state.id}',
                                data=json.dumps(data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        state_updated = storage.get(State, state.id)
        self.assertEqual(state_updated.name, 'New Arizona')

    # def test_update_state_invalid_id(self):
    #     data = {'name': 'New York'}
    #     response = self.app.put('/api/v1/states/invalid_id',
    #                             data=json.dumps(data),
    #                             content_type='application/json')
    #     self.assertEqual(response.status_code, 404)

    # def test_update_state_invalid_content_type(self):
    #     state = State(name="Oregon")
    #     state.save()
    #     data = {'name': 'New Oregon'}
    #     response = self.app.put(f'/api/v1/states/{state.id}',
    #                             data=json.dumps(data))
    #     self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
