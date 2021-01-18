from django.test import TestCase
from repositories.ProteinRepo import ProteinRepo
from entities.ProteinEntity import ProteinEntity
from entities.OrganismEntity import OrganismEntity
from models_db.Protein import Protein
from models_db.Organism import Organism
from tests.unit.ProteinBuilder import ProteinBuilder
from tests.unit.OrganismBuilder import OrganismBuilder

class TestProteinRepo(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.sequence = "A"
        cls.org_inf = OrganismBuilder().with_infected(True).build()
        cls.org_uninf = OrganismBuilder().with_infected(False).build()

    def setUp(self):
        pass

    def test_get_protein(self):
        # Arrange
        test_protein = Protein.objects.create(sequence=self.sequence, organism=self.org_inf)
        id = test_protein.id
        expected_protein = {'id': id, 'sequence': self.sequence}
        protein_repo = ProteinRepo()

        # Act
        protein = protein_repo.get(id)
        actual_protein = {'id': protein.id, 'sequence': protein.sequence}

        # Assert
        self.assertDictEqual(expected_protein, actual_protein)

    def test_get_protein_not_exist(self):
        # Arrange
        protein_id = 1
        exception = False
        protein_repo = ProteinRepo()

        # Act
        try:
            protein = protein_repo.get(protein_id)
        except:
            exception = True

        # Assert
        self.assertTrue(exception)

    def test_get_infected(self):
        # Arrange
        infected_flag = True
        count = 3
        seq = self.sequence
        protein_repo = ProteinRepo()
        expected_infected_flags = [infected_flag for i in range(count)]
        for i in range(count):
            Protein.objects.create(sequence=seq, organism=self.org_inf)
            seq += "A"

        # Act
        proteins = protein_repo.get_all(infected_flag)
        actual_infected_flags = list(map(lambda x: x.organism.infected, proteins))

        # Assert
        self.assertListEqual(actual_infected_flags, expected_infected_flags)

    def test_get_uninfected(self):
        # Arrange
        infected_flag = False
        count = 4
        seq = self.sequence
        protein_repo = ProteinRepo()
        expected_infected_flags = [infected_flag for i in range(count)]
        for i in range(count):
            Protein.objects.create(sequence=seq, organism=self.org_uninf)
            seq += "A"

        # Act
        proteins = protein_repo.get_all(infected_flag)
        actual_infected_flags = list(map(lambda x: x.organism.infected, proteins))

        # Assert
        self.assertListEqual(actual_infected_flags, expected_infected_flags)

    def test_create_protein(self):
        # Arrange
        infected = False
        sex = "Male"
        org_mnem = "RAT"
        desc = ""
        organismEntity = OrganismEntity(infected=infected, sex=sex, org_mnem=org_mnem, desc=desc)
        proteinEntity = ProteinEntity(sequence=self.sequence, organism=organismEntity)
        protein_repo = ProteinRepo()

        # Act
        protein_repo.create(proteinEntity)
        organism = Organism.objects.all().filter(infected=infected,
                                                 sex=sex,
                                                 organism_mnemonic=org_mnem,
                                                 description=desc).first()

        protein = Protein.objects.all().filter(sequence=self.sequence, organism=organism).first()

        # Assert
        self.assertIsNotNone(protein)
