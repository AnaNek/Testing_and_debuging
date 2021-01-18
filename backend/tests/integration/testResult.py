from django.test import TestCase, RequestFactory
from unittest.mock import patch, call
from repositories.ResultRepo import ResultRepo
from repositories.ProteinRepo import ProteinRepo
from usecases.ResultUsecase import ResultUsecase
from entities.ResultEntity import ResultEntity
from entities.ProteinPairEntity import ProteinPairEntity
from entities.ProteinEntity import ProteinEntity
from entities.OrganismEntity import OrganismEntity
from tests.unit.OrganismBuilder import OrganismBuilder
from repositories.ResultRepo import ResultRepo
from models_db.Protein import Protein
from models_db.ProteinPair import ProteinPair
from models_db.Pattern import Pattern
from models_db.ResultSet import ResultSet
from django.contrib.auth.models import User
from app.views.ResultView import ResultView

class TestIntegrationViewUsecaseResult(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.user = User.objects.create_user(
            username='user', email='', 
            password='secret'
        )

    @patch("repositories.ResultRepo.ResultRepo.get_by_proteins")
    def test_get_result(self, mock_repo):
        # Arrange
        protein1_id = 1
        protein2_id = 2
        expected_result = ResultEntity(pair=ProteinPairEntity(
                                       protein1=ProteinEntity(id=protein1_id),
                                       protein2=ProteinEntity(id=protein2_id)))
        mock_repo.return_value = expected_result
        expected_status_code = 200
        url = '/result/' + str(protein1_id) + '/' + str(protein2_id) + '/'
        request = self.factory.get(url, content_type='application/json')
        request.user = self.user

        # Act
        response = ResultView.as_view()(request, protein1_id, protein2_id)

        # Assert
        self.assertEqual(response.status_code, expected_status_code)
        mock_repo.assert_called_once_with(protein1_id, protein2_id)

class TestIntegrationRepoUsecaseResult(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.seq1 = "AGCG"
        cls.seq2 = "ACCG"
        cls.org_inf = OrganismBuilder().with_infected(True).build()
        cls.org_uninf = OrganismBuilder().with_infected(False).build()
        cls.protein1 = Protein.objects.create(sequence=cls.seq1, organism=cls.org_inf)
        cls.protein2 = Protein.objects.create(sequence=cls.seq1, organism=cls.org_uninf)
        cls.protein3 = Protein.objects.create(sequence=cls.seq2, organism=cls.org_uninf)
        cls.pair = ProteinPair.objects.create(protein1=cls.protein1, protein2=cls.protein2, 
                                              pattern_count=1, similarity=100)
        cls.pattern = Pattern.objects.create(subsequence=cls.seq1, start_pos=0,
                                             end_pos=3)
        cls.result = ResultSet.objects.create(protein_pair=cls.pair, pattern=cls.pattern)

    def test_get_result(self):
        # Arrange
        protein1_id = self.protein1.id
        protein2_id = self.protein2.id
        expected_result = {'pattern_count': self.pair.pattern_count, 
                          'similarity': self.pair.similarity,
                          'patterns': [{'sequence': self.pattern.subsequence, 
                                        'start_pos': self.pattern.start_pos,
                                        'end_pos': self.pattern.end_pos}]}
        repo = ResultRepo()
        usecases = ResultUsecase(repo)

        # Act
        result = usecases.get_result(protein1_id, protein2_id)
        patterns = list(map(lambda x: {'sequence': x.subsequence,
                                       'start_pos': x.start_pos, 
                                       'end_pos': x.end_pos}, 
                                        result.patterns))
        actual_result = {'pattern_count': result.pair.pattern_count, 
                         'similarity': result.pair.similarity,
                         'patterns': patterns}
        # Assert
        self.assertDictEqual(actual_result, expected_result)

    def test_create_result(self):
        # Arrange
        protein1_id = self.protein1.id
        protein2_id = self.protein3.id
        username = None
        expected_result = {'pattern_count': 2, 
                          'similarity': 75,
                          'patterns': [{'sequence': 'A', 
                                        'start_pos': 0,
                                        'end_pos': 0},
                                        {'sequence': 'CG', 
                                        'start_pos': 2,
                                        'end_pos': 3}]}
        repo = ResultRepo()
        usecases = ResultUsecase(repo)

        # Act
        usecases.create_result(protein1_id, protein2_id)
        pair = ProteinPair.objects.all().filter(protein1=self.protein1, 
                                                protein2=self.protein3).first()
        result = ResultSet.objects.all().filter(protein_pair=pair)
        patterns = list(map(lambda x: {'sequence': x.pattern.subsequence,
                                       'start_pos': x.pattern.start_pos, 
                                       'end_pos': x.pattern.end_pos}, 
                                        result))
        actual_result = {'pattern_count': pair.pattern_count, 
                         'similarity': pair.similarity,
                         'patterns': patterns}

        # Assert
        self.assertDictEqual(actual_result, expected_result)
