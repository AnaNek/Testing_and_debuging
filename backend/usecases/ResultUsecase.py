from typing import List
from entities.ResultEntity import ResultEntity
from entities.PatternEntity import PatternEntity
from entities.ProteinPairEntity import ProteinPairEntity
from repositories.ResultRepo import ResultRepo
from repositories.ProteinRepo import ProteinRepo

import logging
logger = logging.getLogger(__name__)

class ResultUsecase:
    def __init__(self, result_repo):
        self.result_repo = result_repo

    def get_result(self, id1, id2) -> ResultEntity:
        result = self.result_repo.get_by_proteins(id1, id2)
        return result

    def create_result(self, id1, id2, username=None):
        protein1 = ProteinRepo.get(id1)
        protein2 = ProteinRepo.get(id2)
        pair = ProteinPairEntity(protein1=protein1, protein2=protein2)
        patterns = pair.compare()

        self.result_repo.create(pair, patterns, username)
