from django.test import TestCase
from entities.ProteinPairEntity import ProteinPairEntity
from entities.ProteinEntity import ProteinEntity
from entities.PatternEntity import PatternEntity

class TestPairEntity(TestCase):

    def test_compare_no_patterns(self):
        # Arrange
        protein1 = ProteinEntity(sequence="AGC")
        protein2 = ProteinEntity(sequence="CAG")
        expected_patterns = []
        pair = ProteinPairEntity(protein1=protein1, protein2=protein2)

        # Act
        patterns = pair.compare()

        # Assert
        self.assertListEqual(patterns, expected_patterns)

    def test_compare_multiple_patterns(self):
        # Arrange
        protein1 = ProteinEntity(sequence="AGCG")
        protein2 = ProteinEntity(sequence="AACG")
        expected_count = 2
        expected_patterns = [PatternEntity(subsequence="A", start_pos=0, end_pos=0),
                             PatternEntity(subsequence="CG", start_pos=2, end_pos=3)]
        expected_patterns_dict = list(map(lambda x: x.__dict__, expected_patterns))
        pair = ProteinPairEntity(protein1=protein1, protein2=protein2)

        # Act
        patterns = pair.compare()
        patterns_dict = list(map(lambda x: x.__dict__, patterns))

        # Assert
        self.assertListEqual(patterns_dict, expected_patterns_dict)

    def test_compare_full_equal(self):
        # Arrange
        protein1 = ProteinEntity(sequence="AGCG")
        protein2 = ProteinEntity(sequence="AGCG")
        expected_count = 1
        expected_patterns = [PatternEntity(subsequence="AGCG", start_pos=0, end_pos=3)]
        expected_patterns_dict = list(map(lambda x: x.__dict__, expected_patterns))
        pair = ProteinPairEntity(protein1=protein1, protein2=protein2)

        # Act
        patterns = pair.compare()
        patterns_dict = list(map(lambda x: x.__dict__, patterns))

        # Assert
        self.assertListEqual(patterns_dict, expected_patterns_dict)
