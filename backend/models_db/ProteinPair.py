from django.db import models
from models_db.Protein import Protein

class ProteinPair(models.Model):
    protein1 = models.ForeignKey(Protein, models.DO_NOTHING, db_column='protein1', related_name='protein_1')
    protein2 = models.ForeignKey(Protein, models.DO_NOTHING, db_column='protein2', related_name='protein_2')
    pattern_count = models.IntegerField()
    similarity = models.FloatField()

    class Meta:
        managed = True
        db_table = 'protein_pair'
