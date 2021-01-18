from django.db import models

class Pattern(models.Model):
    hash = models.CharField(max_length=200, blank=True, null=True)
    subsequence = models.CharField(max_length=4500)
    start_pos = models.IntegerField()
    end_pos = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'pattern'
        unique_together = (('hash', 'start_pos', 'end_pos'),)

