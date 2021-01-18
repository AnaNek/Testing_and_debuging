from django.test import TestCase
from unittest.mock import patch, call
from repositories.ResultRepo import ResultRepo
from repositories.ProteinRepo import ProteinRepo
from usecases.ResultUsecase import ResultUsecase
from entities.ResultEntity import ResultEntity
from entities.ProteinPairEntity import ProteinPairEntity
from entities.ProteinEntity import ProteinEntity

class MockResultRepo(ResultRepo):
    def __init__(self):
        self._pair = None
        self._patterns = None
        self._username = None
        self._count_create = 0

    @property
    def pair(self):
        return self._pair

    @property
    def patterns(self):
        return self._patterns

    @property
    def username(self):
        return self._username

    @property
    def count_create(self):
        return self._count_create

    def create(self, pair, patterns, username=None):
        self._count_create += 1
        self._pair = pair
        self._patterns = patterns
        self._username = username

def get(id):
    return ProteinEntity(id=id, sequence="A")

class TestResultUsecase(TestCase):
    @patch.object(ResultRepo, "get_by_proteins")
    def test_get_result(self, mock_repo):
        # Arrange
        protein1_id = 1
        protein2_id = 2
        expected_result = ResultEntity(pair=ProteinPairEntity(id=1))
        mock_repo.get_by_proteins.return_value = expected_result
        usecases = ResultUsecase(mock_repo)

        # Act
        result = usecases.get_result(protein1_id, protein2_id)

        # Assert
        self.assertEqual(result.pair.id, expected_result.pair.id)
        mock_repo.get_by_proteins.assert_called_once_with(protein1_id, protein2_id)

    @patch.object(ProteinRepo, "get")
    @patch("entities.ProteinPairEntity.ProteinPairEntity.compare")
    def test_create_result(self, mock_compare, mock_prot_repo):
        # Arrange
        protein1_id = 1
        protein2_id = 2
        username = None
        patterns = []
        mock_compare.return_value = patterns
        mock_prot_repo.return_value.get.return_value = get
        mock_res_repo = MockResultRepo()
        usecases = ResultUsecase(mock_res_repo)
        expected_calls = [call(protein1_id), call(protein2_id)]

        # Act
        usecases.create_result(protein1_id, protein2_id)

        # Assert
        self.assertEqual(mock_prot_repo.call_count, 2)
        self.assertEqual(mock_compare.call_count, 1)
        self.assertEqual(mock_prot_repo.call_args_list, expected_calls)
        self.assertEqual(mock_res_repo.count_create, 1)
