import flask_unittest
from Application import create_app
from Application.objects.domain import Domain

class TestDomainsApi(flask_unittest.ClientTestCase):
    app = create_app()
    
    def test_get_domain(self, client):
        resp = client.get('/api/domains/1')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
    
    def test_get_domains(self, client):
        resp = client.get('/api/domains/')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)

    def test_get_domains_with_argument(self, client):
        resp = client.get('/api/domains/?id=1')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
    
    def test_delete(self, client):
        domain = Domain("New Domain", "Hello")
        resp = client.delete(f"/api/domains/{domain.id}")
        self.assertEqual(resp.status_code, 204) 

    # def test_add_domain_with_post_and_delete(self, client):
    #     domain = Domain("New Domain", "Hello")

    #     resp = client.post('/api/domains/', json=domain.to_json("", ""))
    #     self.assertEqual(resp.status_code, 201)
        
    #     resp = client.delete(f"/api/domains/{domain.id}")
    #     self.assertEqual(resp.status_code, 204)   
    
    # def test_add_domain_with_put_and_delete(self, client):
    #     domain = Domain("New Domain", "Hello")

    #     resp = client.put('/api/domains/1', json=domain.to_json("", ""))
    #     self.assertEqual(resp.status_code, 201)
        
    #     resp = client.delete(f"/api/domains/{domain.id}")
    #     self.assertEqual(resp.status_code, 204)
        
    # def test_modify_domain_and_delete(self, client):
    #     domain = Domain("New Domain", "Hello")
       
    #     resp = client.post('/api/domains/', json=domain.to_json("", ""))
    #     self.assertEqual(resp.status_code, 201)
        
    #     domain = Domain("New Domain", "Hello")
        
    #     resp = client.put(f'/api/domains/{domain.id}', json=domain.to_json("", ""))
    #     self.assertEqual(resp.status_code, 200)
        
    #     resp = client.delete(f"/api/domains/{domain.id}")
    #     self.assertEqual(resp.status_code, 204)