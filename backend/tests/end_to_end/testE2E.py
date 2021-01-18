from django.test import TestCase
from http import HTTPStatus
from django.contrib.auth.models import User
from models_db.Profile import Profile
from models_db.Organism import Organism
from models_db.Protein import Protein
from models_db.Pattern import Pattern
from models_db.ProteinPair import ProteinPair
from models_db.ResultSet import ResultSet
from memory_profiler import *

class TestScenario(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = 'username'
        cls.password = 'password'
        cls.count_passed = 0
        cls.repeats = 1
    
    def tearDown(self):
        print('PASSED:', self.count_passed, '\nRUN ', self.repeats, ' TIMES')

    f=open('memory_profiler_scenario.log','w+')
    @profile(stream=f)
    def _test_scenario(self):
        # Sing up

        # Arrange
        expected_json = {'username': self.username, 'password': self.password}
        form_data = {'username': self.username, 'password': self.password}

        # Act
        response = self.client.post(
            '/api/v1/users/',
            data=form_data)

        # Assert
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data, expected_json)
        self.assertEqual(Profile.objects.all().first().username, form_data['username'])

        # Sing in

        # Arrange
        form_data = {'username': self.username, 'password': self.password}

        # Act
        response = self.client.post('/api/v1/sessions/',
                                   data=form_data)

        # Assert
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data['username'], form_data['username'])

        # Create infected protein 

        # Arrange
        seq = "ACG"
        organism_json = {'infected': True, 'sex': 'Male', 
                        'organism_mnemonic': 'RAT', 
                        'description': '...'}
        form_data = {
            'sequence': seq,
            'organism': organism_json
        }
        
        # Act
        response = self.client.post('/api/v1/proteins/', 
                                    content_type='application/json', 
                                    data=form_data)
        
        organism = Organism.objects.all().filter(infected=organism_json['infected'],
                                                 sex=organism_json['sex'],
                                                 organism_mnemonic=organism_json['organism_mnemonic'],
                                                 description=organism_json['description']).first()

        protein = Protein.objects.all().filter(sequence=form_data['sequence'], organism=organism).first()
        
        organism_db = {'infected': organism.infected, 'sex': organism.sex, 
                        'organism_mnemonic': organism.organism_mnemonic, 
                        'description': organism.description}

        protein_db = {'sequence': protein.sequence, 'organism': organism_db}

        # Assert
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data['sequence'], form_data['sequence'])
        self.assertEqual(protein_db, form_data)

        # Create uninfected protein 

        # Arrange
        seq = "AGG"
        organism_json = {'infected': False, 'sex': 'Male', 
                        'organism_mnemonic': 'RAT', 
                        'description': '...'}
        form_data = {
            'sequence': seq,
            'organism': organism_json
        }
        
        # Act
        response = self.client.post('/api/v1/proteins/', 
                                    content_type='application/json', 
                                    data=form_data)
        
        organism = Organism.objects.all().filter(infected=organism_json['infected'],
                                                 sex=organism_json['sex'],
                                                 organism_mnemonic=organism_json['organism_mnemonic'],
                                                 description=organism_json['description']).first()

        protein = Protein.objects.all().filter(sequence=form_data['sequence'], organism=organism).first()
        
        organism_db = {'infected': organism.infected, 'sex': organism.sex, 
                        'organism_mnemonic': organism.organism_mnemonic, 
                        'description': organism.description}

        protein_db = {'sequence': protein.sequence, 'organism': organism_db}

        # Assert
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data['sequence'], form_data['sequence'])
        self.assertEqual(protein_db, form_data)

        # Get all proteins
        
        # Arrange 
        expected_count_infected = 1
        expected_count_uninfected = 1

        # Act
        response = self.client.get('/api/v1/proteins/')
         
        count_infected = len(response.data['infected'])
        count_uninfected = len(response.data['uninfected'])
        
        # Assert
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(count_infected, expected_count_infected)
        self.assertEqual(count_uninfected, expected_count_uninfected)

        # Compare proteins

        # Arrange
        protein1_id = response.data['infected'][0]['id']
        protein2_id = response.data['uninfected'][0]['id']

        url = '/api/v1/result/' + str(protein1_id) + '/' + str(protein2_id) + '/'

        # Act
        response = self.client.get(url, content_type='application/json')

        protein1 = Protein.objects.all().filter(id=protein1_id).first()
        protein2 = Protein.objects.all().filter(id=protein2_id).first()
        pair = ProteinPair.objects.all().filter(protein1=protein1, protein2=protein2).first()
        
        # Assert
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data['pair']['protein1']['id'], protein1_id)
        self.assertEqual(response.data['pair']['protein2']['id'], protein2_id)
        self.assertIsNotNone(pair)

        # Sign out

        # Arrange
        url = '/api/v1/sessions/' + self.username + '/'

        # Act
        response = self.client.delete(url)

        # Assert
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data['username'], self.username)

        self.count_passed += 1
        self._clean()
    
    def _clean(self):
        ResultSet.objects.all().delete()
        ProteinPair.objects.all().delete()
        Protein.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()

    fp=open('memory_profiler.log','w+')
    @profile(stream=fp)
    def test_scenario(self):  
        self.repeats = int(os.getenv('repeats', 1))
        self.count_passed = 0

        for i in range(self.repeats):
            self._test_scenario()

