from django.test import TestCase
from tests.unit.OrganismBuilder import OrganismBuilder
from repositories.ResultRepo import ResultRepo
from entities.ResultEntity import ResultEntity
from entities.PatternEntity import PatternEntity
from entities.ProteinPairEntity import ProteinPairEntity
from models_db.ResultSet import ResultSet
from models_db.Protein import Protein
from models_db.ProteinPair import ProteinPair
from models_db.Pattern import Pattern

class TestResultRepo(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.seq1 = "AGCG"
        cls.seq2 = "ACCG"
        cls.org_inf = OrganismBuilder().with_infected(True).build()
        cls.org_uninf = OrganismBuilder().with_infected(False).build()
        cls.protein1 = Protein.objects.create(sequence=cls.seq1, organism=cls.org_inf)
        cls.protein2 = Protein.objects.create(sequence=cls.seq2, organism=cls.org_uninf)

    def setUp(self):
        pass

    def test_get_by_proteins(self):
        # Arrange
        id1 = self.protein1.id
        id2 = self.protein2.id
        result_repo = ResultRepo()
        patterns = ["A", "CG"]
        start_pos = [0, 2]
        end_pos = [0, 3]
        count = 2
        expected_patterns = [{'subsequence': patterns[0],
                              'start_pos': start_pos[0],
                               'end_pos': end_pos[0]},
                            {'subsequence': patterns[1],
                            'start_pos': start_pos[1],
                            'end_pos': end_pos[1]}]

        pair = ProteinPair.objects.create(protein1=self.protein1,
                                          protein2=self.protein2,
                                          similarity=0,
                                          pattern_count=count)
        for i in range(count):
            pattern_db = Pattern.objects.create(subsequence=patterns[i],
                                                start_pos=start_pos[i],
                                                end_pos=end_pos[i])
            result_db = ResultSet.objects.create(protein_pair=pair, pattern=pattern_db)

        # Act
        resultEntity = result_repo.get_by_proteins(id1, id2)
        actual_patterns = list(map(lambda x: {'subsequence': x.subsequence,
                         'start_pos': x.start_pos, 'end_pos': x.end_pos}, resultEntity.patterns))

        # Assert
        self.assertListEqual(actual_patterns, expected_patterns)

    def test_get_by_proteins_not_exist(self):
        # Arrange
        id1 = self.protein1.id
        id2 = self.protein2.id
        result_repo = ResultRepo()

        # Act
        resultEntity = result_repo.get_by_proteins(id1, id2)

        # Assert
        self.assertIsNone(resultEntity)

    def test_create_result(self):
        # Arrange
        count = 2
        result_repo = ResultRepo()
        pattern1 = PatternEntity(subsequence="A", start_pos=0, end_pos=0)
        pattern2 = PatternEntity(subsequence="CG", start_pos=2, end_pos=3)
        patterns = [pattern1, pattern2]
        pair = ProteinPairEntity(protein1=self.protein1,
                                 protein2=self.protein2,
                                 pattern_count=count)

        # Act
        result_repo.create(pair, patterns)
        pairEntity = ProteinPair.objects.all().filter(protein1=self.protein1,
                                                      protein2=self.protein2).first()

        # Assert
        self.assertIsNotNone(pairEntity)
