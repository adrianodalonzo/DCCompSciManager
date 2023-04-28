import flask_unittest
from Application import create_app
from Application.objects.competency import Competency

class TestCompetenciesApi(flask_unittest.ClientTestCase):
    app = create_app()