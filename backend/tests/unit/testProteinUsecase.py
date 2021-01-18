from django.test import TestCase
from unittest.mock import patch
from repositories.ProteinRepo import ProteinRepo
from usecases.ProteinUsecase import ProteinUsecase
from entities.ProteinEntity import ProteinEntity
from entities.OrganismEntity import OrganismEntity

class TestProteinUsecase(TestCase):
    @patch.object(ProteinRepo, "get")
    def test_get_protein(self, mock_repo):
        # Arrange
        protein_id = 1
        expected_protein = ProteinEntity(id=protein_id, sequence="ACG")
        mock_repo.get.return_value = expected_protein
        usecases = ProteinUsecase(mock_repo)

        # Act
        protein = usecases.get_protein(protein_id)

        # Assert
        self.assertEqual(expected_protein.id, protein.id)
        mock_repo.get.assert_called_once_with(protein_id)

    @patch.object(ProteinRepo, "get_all")
    def test_get_infected(self, mock_repo):
        # Arrange
        infected_flag = True
        expected_proteins = [ProteinEntity(id=1),
                            ProteinEntity(id=2)]

        mock_repo.get_all.return_value = expected_proteins
        usecases = ProteinUsecase(mock_repo)

        # Act
        proteins = usecases.get_infected()

        # Assert
        self.assertListEqual(expected_proteins, proteins)

        mock_repo.get_all.assert_called_once_with(infected_flag)

    @patch.object(ProteinRepo, "get_all")
    def test_get_uninfected(self, mock_repo):
        # Arrange
        infected_flag = False
        expected_proteins = [ProteinEntity(id=1),
                            ProteinEntity(id=2)]

        mock_repo.get_all.return_value = expected_proteins
        usecases = ProteinUsecase(mock_repo)

        # Act
        proteins = usecases.get_uninfected()

        # Assert
        self.assertListEqual(expected_proteins, proteins)

        mock_repo.get_all.assert_called_once_with(infected_flag)

    @patch.object(ProteinRepo, "create")
    def test_create_protein(self, mock_repo):
        # Arrange
        seq = "ACGA"
        infected = True
        sex = "Male"
        org_mn = "SHEEP"
        desc = "some text"
        usecases = ProteinUsecase(mock_repo)

        # Act
        usecases.create_protein(seq, infected, sex, org_mn, desc)

        # Assert
        self.assertEqual(mock_repo.create.call_count, 1)
