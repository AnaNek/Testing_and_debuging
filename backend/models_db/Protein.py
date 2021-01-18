from django.db import models
from models_db.Organism import Organism

class Protein(models.Model):
    hash = models.CharField(max_length=200, blank=True, null=True)
    sequence = models.CharField(max_length=4500)
    organism = models.ForeignKey(Organism, models.DO_NOTHING, db_column='organism', default=0)

    class Meta:
        managed = True
        db_table = 'protein'
        unique_together = (('hash', 'organism'),)
