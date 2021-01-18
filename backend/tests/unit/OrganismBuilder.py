from models_db.Organism import Organism

class OrganismBuilder:
    def __init__(self):
        self.infected = False
        self.organism_mnemonic = ""
        self.sex = ""
        self.description = ""
        self.organism = Organism.objects.create(infected=self.infected,
                                organism_mnemonic=self.organism_mnemonic,
                                sex=self.sex,
                                description=self.description)
        
    def with_infected(self, infected):
        self.organism.infected = infected
        self.organism.save()
        return self
        
    def with_org_mnem(self, org_mnem):
        self.organism.organism_mnemonic = org_mnem
        self.organism.save()
        return self
       
    def with_sex(self, sex):
        self.organism.sex = sex
        self.organism.save()
        return self
        
    def with_description(self, description):
        self.organism.description = description
        self.organism.save()
        return self
        
    def build(self):
        return self.organism
        
        
      
