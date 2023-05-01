import flask_unittest
from Application import create_app
from Application.objects.competency import Competency
from Application.objects.element import Element

class TestCompetenciesApi(flask_unittest.ClientTestCase):
    app = create_app()
    
    def test_get_competency(self, client):
        resp = client.get('/api/competencies/00Q2')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
    
    def test_get_competencies(self, client):
        resp = client.get('/api/competencies')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)

    def test_get_competency_with_argument(self, client):
        resp = client.get('/api/competencies?id=00Q2')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
        
    def test_add_competency_with_post_and_delete(self, client):
        competency = Competency("2O23", "Hello", "Hi, how are you?", "Mandatory")

        resp = client.post('/api/competencies', json=competency.to_json())
        self.assertEqual(resp.status_code, 201)
        
        resp = client.delete("/api/competencies/2O23")
        self.assertEqual(resp.status_code, 204)
    
    def test_add_competency_with_put_and_delete(self, client):
        competency = Competency("2O23", "Hello", "Hi, how are you?", "Mandatory")

        resp = client.put('/api/competencies/2O23', json=competency.to_json())
        self.assertEqual(resp.status_code, 201)
        
        resp = client.delete("/api/competencies/2O23")
        self.assertEqual(resp.status_code, 204)
        
    def test_modify_competency_with_put_and_delete(self, client):
        competency = Competency("2O23", "Hello", "Hi, how are you?", "Mandatory")
        
        resp = client.post('/api/competencies', json=competency.to_json())
        self.assertEqual(resp.status_code, 201)
        
        competency = Competency("2O23", "HIIIIII", "Hi, how are you?", "Mandatory")
        
        resp = client.put('/api/competencies/2O23', json=competency.to_json())
        self.assertEqual(resp.status_code, 200)
        
        resp = client.delete("/api/competencies/2O23")
        self.assertEqual(resp.status_code, 204)



    def test_get_competency_element(self, client):
        resp = client.get('/api/competencies/00Q2/elements/1')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
    
    def test_get_competency_elements(self, client):
        resp = client.get('/api/competencies/00Q2')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)

    def test_get_competency_element_with_argument(self, client):
        resp = client.get('/api/competencies/00Q2/elements?id=1')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
        
    def test_add_competency_element_with_post_and_delete(self, client):
        element = Element(1, "Hello", "Criteria", "2O23")

        resp = client.post('/api/competencies/2O23', json=element.to_json())
        self.assertEqual(resp.status_code, 201)
        
        resp = client.delete("/api/competencies/2O23/1")
        self.assertEqual(resp.status_code, 204) 
    
    def test_add_competency_element_with_put_and_delete(self, client):
        element = Element(1, "Hello", "Criteria", "2O23")

        resp = client.post('/api/competencies/2O23/elements', json=element.to_json())
        self.assertEqual(resp.status_code, 201)
        
        json = resp.json
        element_id = json['id']
        
        resp = client.delete(f"/api/competencies/2O23/{element_id}")
        self.assertEqual(resp.status_code, 204)
        
        resp = client.delete("/api/competencies/2O23")
        self.assertEqual(resp.status_code, 204)
        
    def test_modify_competency_with_put_and_delete(self, client):
        element = Element(1, "Hello", "Criteria", "2O23")
        
        resp = client.post('/api/competencies', json=element.to_json())
        self.assertEqual(resp.status_code, 201)
        
        element = Element(2, "Hiiiii", "Criteria", "2O23")
        
        resp = client.put('/api/competencies/2O23', json=element.to_json())
        self.assertEqual(resp.status_code, 200)
        
        resp = client.delete("/api/competencies/2O23")
        self.assertEqual(resp.status_code, 204)