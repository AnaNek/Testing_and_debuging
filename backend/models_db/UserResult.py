from django.db import models
from models_db.ResultSet import ResultSet
from models_db.Profile import Profile

class UserResult(models.Model):
    user = models.ForeignKey(Profile, models.DO_NOTHING, db_column='user')
    result_set = models.ForeignKey(ResultSet, models.DO_NOTHING, db_column='result_set')

    class Meta:
        managed = True
        db_table = 'user_result'
        unique_together = (('user', 'result_set'),)
