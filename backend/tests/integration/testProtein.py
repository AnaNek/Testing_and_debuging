from django.test import TestCase, RequestFactory
from unittest.mock import patch, call
from unittest.mock import Mock
from repositories.ProteinRepo import ProteinRepo
from usecases.ProteinUsecase import ProteinUsecase
from usecases.ProfileUsecase import ProfileUsecase
from entities.ProteinEntity import ProteinEntity
from entities.OrganismEntity import OrganismEntity
from models_db.Protein import Protein
from models_db.Organism import Organism
from tests.unit.OrganismBuilder import OrganismBuilder
from app.views.ProteinView import ProteinView
from app.views.ProteinListView import ProteinListView
from django.contrib.auth.models import User
from entities.SessionEntity import SessionEntity
import json

class TestIntegrationViewUsecaseProtein(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.user = User.objects.create_user(
            username='user', email='', 
            password='secret'
        )

    @patch("repositories.ProteinRepo.ProteinRepo.get")
    def test_get_protein(self, mock_repo):
        # Arrange
        protein_id = 1
        expected_status_code = 200
        expected_protein = ProteinEntity(id=protein_id, sequence="ACG")
        expected_json = {'hash': None, 'sequence': 'ACG', 'organism': None, 'id': 1}
        mock_repo.return_value = expected_protein
        url = '/proteins/' + str(protein_id) + '/'
        request = self.factory.get(url)
        request.user = self.user

        # Act
        response = ProteinView.as_view()(request, protein_id)
        
        # Assert
        self.assertEqual(response.status_code, expected_status_code)
        self.assertDictEqual(response.data, expected_json)
        mock_repo.assert_called_once_with(protein_id)
    
    @patch("repositories.ProteinRepo.ProteinRepo.get_all")
    def test_get_all_proteins(self, mock_repo):
        # Arrange
        protein_id = 1
        expected_proteins = [ProteinEntity(id=protein_id, sequence="ACG")]
        expected_calls = [call(True), call(False)]
        mock_repo.return_value = expected_proteins
        request = self.factory.get('/proteins/')
        request.user = self.user

        # Act
        response = ProteinListView.as_view()(request)
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_repo.call_args_list, expected_calls)
        self.assertEqual(mock_repo.call_count, 2)
    
    @patch("repositories.ProteinRepo.ProteinRepo.create")
    @patch("usecases.ProfileUsecase.ProfileUsecase.verify_token")
    def test_post_protein(self, mock_verify, mock_repo):
        # Arrange
        protein_id = 1
        seq = "ACG"
        expected_proteins = ProteinEntity(id=protein_id, sequence=seq)
        mock_verify.return_value = SessionEntity()
        mock_repo.return_value = expected_proteins
        organism_json = {'infected': True, 'sex': 'Male', 'organism_mnemonic': 'RAT', 
                         'description': '...'}
        form_data = {
            'id': protein_id,
            'sequence': seq,
            'organism': organism_json
        }
        request = self.factory.post('/proteins/', content_type='application/json', data=form_data)
        request.user = self.user
        request.session = {'token': 'sometoken'}

        # Act
        response = ProteinListView.as_view()(request)
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_repo.call_count, 1)

class TestIntegrationRepoUsecaseProtein(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.sequence = "A"
        cls.org_inf = OrganismBuilder().with_infected(True).build()
        cls.org_uninf = OrganismBuilder().with_infected(False).build()
        cls.protein1 = Protein.objects.create(sequence=cls.sequence, organism=cls.org_inf)
        cls.protein2 = Protein.objects.create(sequence=cls.sequence, organism=cls.org_uninf)

    def test_get_protein(self):
        # Arrange
        protein_id = self.protein1.id
        seq = self.protein1.sequence
        expected_protein = {'id': protein_id, 'sequence': seq}
        repo = ProteinRepo()
        usecases = ProteinUsecase(repo)

        # Act
        protein = usecases.get_protein(protein_id)
        actual_protein = {'id': protein.id, 'sequence': protein.sequence}

        # Assert
        self.assertDictEqual(expected_protein, actual_protein)

    def test_create_protein(self):
        # Arrange
        seq = "ACGA"
        infected = True
        sex = "Male"
        org_mn = "SHEEP"
        desc = "some text"
        expected_protein = {'sequence': seq, 'infected': infected,
                            'sex': sex, 'org_mnem': org_mn, 'desc': desc}
        repo = ProteinRepo()
        usecases = ProteinUsecase(repo)

        # Act
        usecases.create_protein(seq, infected, sex, org_mn, desc)
        organism = Organism.objects.all().filter(infected=infected,
                                                 sex=sex,
                                                 organism_mnemonic=org_mn,
                                                 description=desc).first()

        protein = Protein.objects.all().filter(sequence=seq, organism=organism).first()
        actual_protein = {'sequence': protein.sequence, 'infected': protein.organism.infected,
                            'sex': protein.organism.sex, 'org_mnem': protein.organism.organism_mnemonic, 
                            'desc': protein.organism.description}

        # Assert
        self.assertDictEqual(expected_protein, actual_protein)

    def test_get_infected(self):
        # Arrange
        expected_proteins = [{'id': self.protein1.id,
                             'sequence': self.protein1.sequence,
                             'infected': self.protein1.organism.infected}]

        repo = ProteinRepo()
        usecases = ProteinUsecase(repo)

        # Act
        proteins = usecases.get_infected()
        actual_proteins = list(map(lambda x: {'id': x.id,
                                 'sequence': x.sequence, 
                                 'infected': x.organism.infected}, 
                                 proteins))

        # Assert
        self.assertListEqual(expected_proteins, actual_proteins)
    
    def test_get_uninfected(self):
        # Arrange
        expected_proteins = [{'id': self.protein2.id,
                             'sequence': self.protein2.sequence,
                             'infected': self.protein2.organism.infected}]

        repo = ProteinRepo()
        usecases = ProteinUsecase(repo)

        # Act
        proteins = usecases.get_uninfected()
        actual_proteins = list(map(lambda x: {'id': x.id,
                                 'sequence': x.sequence, 
                                 'infected': x.organism.infected}, 
                                 proteins))

        # Assert
        self.assertListEqual(expected_proteins, actual_proteins)
