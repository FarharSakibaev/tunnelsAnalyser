from loguru import logger


class PathlikeStructure:

    @logger.catch()
    def __init__(self):
        super(PathlikeStructure, self).__init__()
        self.__properties: dict = {}
        self.__profile: list = []
        self.__residues: dict = {}
        self.__relations: list = []
        self.__id: int | str = 0
        self.__protein_level: str = ''

    def set_properties(self, properties: dict) -> None:
        self.__properties = properties

    def set_profile(self, profile: list) -> None:
        self.__profile = profile

    def set_residues(self, residues: dict) -> None:
        self.__residues = residues

    def set_id(self, structure_id: int | str):
        self.__id = structure_id

    def set_protein_level(self, level):
        self.__protein_level = level

    def get_id(self):
        return self.__id

    def get_protein_level(self):
        return self.__protein_level

    def get_residues_number(self):
        return self.__residues.keys()

    def check_relations_empty(self):
        return not self.__relations

    def append_relation(self, relation):
        if relation not in self.__relations:
            self.__relations.append(relation)
