from loguru import logger
from re import findall



def format_residue(res_name: str, res_number: int, chain: str | None = None) -> str:
    result_chain = ''
    if chain:
        result_chain = f' ({chain})'
    return res_name[0].upper() + res_name[1:].lower() + str(res_number) + result_chain


def sort_res_list(res_list: list):
    def sort_key(res: str):
        return int(findall(r'\d+', res)[0])
    return sorted(res_list, key=sort_key)


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
        self.__type: str = ''
        self.__protein: str = ''

    def set_properties(self, properties: dict) -> None:
        self.__properties = properties

    def set_profile(self, profile: list) -> None:
        self.__profile = profile

    def set_residues(self, residues: dict) -> None:
        self.__residues = residues

    def set_id(self, structure_id: int | str) -> None:
        self.__id = structure_id

    def set_protein_level(self, level: str) -> None:
        self.__protein_level = level

    def set_type(self, structure_type: str) -> None:
        self.__type = structure_type

    def set_protein(self, protein: str) -> None:
        self.__protein = protein

    def get_id(self):
        return self.__id

    def get_protein_level(self):
        return self.__protein_level

    def get_residues_number(self):
        return self.__residues.keys()

    def check_relations_empty(self):
        return not self.__relations

    def get_residues(self, as_str: bool = False, oligomer: bool = False):
        if as_str:
            out_list: list = []
            for res in self.__residues:
                if oligomer:
                    out_list.append(format_residue(self.__residues[res]['NAME'], res, self.__residues[res]['CHAIN']))
                else:
                    out_list.append(format_residue(self.__residues[res]['NAME'], res))
            return ', '.join(sort_res_list(out_list))
        else:
            return self.__residues

    def get_protein(self) -> str:
        return self.__protein

    def get_profile(self) -> list:
        return self.__profile

    def append_relation(self, relation):
        if relation not in self.__relations:
            self.__relations.append(relation)

    def get_relations(self):
        return ', '.join(self.__relations)
