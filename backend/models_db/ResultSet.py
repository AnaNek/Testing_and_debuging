from django.db import models
from models_db.ProteinPair import ProteinPair
from models_db.Pattern import Pattern

class ResultSet(models.Model):
    protein_pair = models.ForeignKey(ProteinPair, models.DO_NOTHING, db_column='protein_pair')
    pattern = models.ForeignKey(Pattern, models.DO_NOTHING, db_column='pattern')

    class Meta:
        managed = True
        db_table = 'result_set'
        
