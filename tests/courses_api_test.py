import flask_unittest
from Application import create_app
from Application.objects.course import Course

class TestCoursesApi(flask_unittest.ClientTestCase):
    app = create_app()
    
    def test_get_courses(self, client):
        resp = client.get('/api/courses/')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)

    def test_get_courses_with_argument(self, client):
        resp = client.get('/api/courses/?id=420-110-DW')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)

    # def test_delete_course(self, client):
    #     resp = client.get('/api/courses/111-111-HI')
    #     self.assertEqual(resp.status_code, 200)
    #     resp = client.delete("/api/courses/111-111-HI")
    #     self.assertEqual(resp.status_code, 204)
    
    def test_add_and_delete_course_with_post(self, client):
        course = Course("111-111-HI", "Hello", 3, 3, 3, "Hi, how are you?", 1, 1)
        url = ""
        domain_url = ""
        resp = client.post('/api/courses/', json=course.to_json(url, domain_url))
        self.assertEqual(resp.status_code, 201)

        # resp = client.delete(f"/api/courses/111-111-HI")
        # self.assertEqual(resp.status_code, 204)
    
    def test_get_course(self, client):
        resp = client.get('/api/courses/420-110-DW')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
    
    # def test_add_course_with_put(self, client):
    #     course = Course("111-111-HI", "Hello", 3, 3, 3, "Hi, how are you?", 1, 1)
    #     url = ""
    #     domain_url = ""
    #     resp = client.put('/api/courses/111-111-HI', json=course.to_json(url, domain_url))
    #     self.assertEqual(resp.status_code, 200)
        
    # def test_modify_course(self, client):
    #     resp = client.get('/api/courses/')
    #     self.assertEqual(resp.status_code, 200)
    #     courses = resp.json
        
    #     course = courses[0]
        
    #     course['title'] = 'A new title'

    #     resp = client.post('/api/courses/', json=course)
    #     self.assertEqual(resp.status_code, 201)