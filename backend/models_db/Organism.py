from django.db import models

class Organism(models.Model):
    infected = models.BooleanField(default=False)
    organism_mnemonic = models.CharField(max_length=80)
    sex = models.CharField(max_length=15)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'organism'
        unique_together = (('infected', 'organism_mnemonic', 'sex', 'description'),)
