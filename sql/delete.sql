DROP INDEX org_index;
DROP INDEX pat_index;
DROP INDEX pair_index;
DROP INDEX pr_index;
DROP INDEX res_index;

DROP TRIGGER hash_prot ON Protein;
DROP TRIGGER hash_pat ON Pattern;

DROP FUNCTION hashcodeprot();
DROP FUNCTION hashcodepat();

DROP TABLE User_result;
DROP TABLE Result_set;
DROP TABLE Protein_pair;
DROP TABLE Protein;
DROP TABLE Pattern;
DROP TABLE "User";
DROP TABLE Organism;

DROP DATABASE db_protein;

