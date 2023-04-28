import flask_unittest
from Application import create_app
from Application.objects.competency import Competency

class TestCompetenciesApi(flask_unittest.ClientTestCase):
    app = create_app()
    
    def test_get_competency(self, client):
        resp = client.get('/api/competencies/00Q2')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
    
    def test_get_competencies(self, client):
        resp = client.get('/api/competencies/')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)

    def test_get_competencies_with_argument(self, client):
        resp = client.get('/api/competencies/?id=00Q2')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
        
    def test_add_competency_with_post_and_delete(self, client):
        competency = Competency("2O23", "Hello", "Hi, how are you?", "Mandatory")

        resp = client.post('/api/competencies/', json=competency.to_json())
        self.assertEqual(resp.status_code, 201)
        
        resp = client.delete("/api/competencies/2O23")
        self.assertEqual(resp.status_code, 204)
    
    
    def test_add_competency_with_put_and_delete(self, client):
        competency = Competency("2O23", "Hello", "Hi, how are you?", "Mandatory")

        resp = client.put('/api/competencies/2O23', json=competency.to_json())
        self.assertEqual(resp.status_code, 201)
        
        resp = client.delete("/api/competencies/2O23")
        self.assertEqual(resp.status_code, 204)
        
    def test_modify_competency_and_delete(self, client):
        competency = Competency("2O23", "Hello", "Hi, how are you?", "Mandatory")
        
        resp = client.post('/api/competencies/', json=competency.to_json())
        self.assertEqual(resp.status_code, 201)
        
        competency = Competency("2O23", "HIIIIII", "Hi, how are you?", "Mandatory")
        
        resp = client.put('/api/competencies/2O23', json=competency.to_json())
        self.assertEqual(resp.status_code, 200)
        
        resp = client.delete("/api/competencies/2O23")
        self.assertEqual(resp.status_code, 204)