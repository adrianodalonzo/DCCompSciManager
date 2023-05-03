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
        resp = client.get('/api/domains')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)

    def test_get_domains_with_argument(self, client):
        resp = client.get('/api/domains?id=1')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
    
    def test_add_domain_with_post_and_delete(self, client):
        domain = Domain("New Domain", "Hello")

        resp = client.post('/api/domains', json=domain.to_json("", ""))
        self.assertEqual(resp.status_code, 201)
        
        url = resp.headers['Location']
        
        resp = client.delete(f"{url}")
        self.assertEqual(resp.status_code, 204)   
        
    def test_modify_domain_with_put_and_delete(self, client):
        domain = Domain("New Domain", "Hello")
       
        resp = client.post('/api/domains', json=domain.to_json("", ""))
        self.assertEqual(resp.status_code, 201)
        
        url = resp.headers['Location']
        
        domain = Domain("New Domain", "Hiiiiiiiii")
        
        resp = client.put(f'{url}', json=domain.to_json("", ""))
        self.assertEqual(resp.status_code, 200)
        
        resp = client.delete(f"{url}")
        self.assertEqual(resp.status_code, 204)