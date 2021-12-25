import re
from data_type.internal_structures_collection import InternalStructuresCollection
from data_type.pathlike_structure import PathlikeStructure
from typing import Dict
from loguru import logger


class PathlikeStructuresCollection(InternalStructuresCollection):
    """
    Туннели и поры
    """

    @logger.catch()
    def __init__(self, structure_type: str):
        super(PathlikeStructuresCollection, self).__init__()
        self.structures: Dict[PathlikeStructure] = {}

        self._set_type(structure_type)
        self._set_protein_name()
        self._set_protein_level()
        self.__set_structures()
        self._set_structures_internal_relations()
        logger.info(f'{self.structure_type} collection for {self.protein_name} {self.protein_level} has been created')

    @logger.catch()
    def __set_structures(self) -> None:
        structures_data_collection: list = self.__get_structures_from_xml_tree()
        for structure_data in structures_data_collection:
            structure = PathlikeStructure()
            structure_id = structure_data.attrib['Id']

            structure.set_id(int(structure_id))
            structure.set_properties(self.__get_properties_from_xml_tree(structure_data))
            structure.set_profile(self.__get_profile_nodes(structure_data))
            structure.set_residues(self.__get_residues(structure_data))
            structure.set_protein_level(self.protein_level)

            self.structures[structure_id] = structure

    @logger.catch()
    def __get_structures_from_xml_tree(self):
        return self._get_elements_from_xml_tree(self.structure_type)

    @logger.catch()
    def __get_properties_from_xml_tree(self, structure) -> dict:
        properties: list = self._get_elements_from_xml_tree('Properties', structure)
        return {
            'CHARGE': properties[0].attrib['Charge'],
            'NUM_POSITIVES': properties[0].attrib['NumPositives'],
            'NUM_NEGATIVES': properties[0].attrib['NumNegatives'],
            'HYDROPHOBICITY': properties[0].attrib['Hydrophobicity'],
            'HYDROPATHY': properties[0].attrib['Hydropathy'],
            'POLARITY': properties[0].attrib['Polarity'],
            'MUTABILITY': properties[0].attrib['Mutability']
        }

    @logger.catch()
    def __get_profile_nodes(self, structure) -> list:
        profile = self._get_elements_from_xml_tree('Profile', structure)
        nodes: list = []
        for node in profile[0].iter('Node'):
            nodes.append(self.__get_node_properties(node))
        return nodes

    @staticmethod
    def __get_node_properties(node) -> dict:
        return {
            'RADIUS': node.attrib['Radius'],
            'T': node.attrib['T'],
            'DISTANCE': node.attrib['Distance'],
            'X': node.attrib['X'],
            'Y': node.attrib['Y'],
            'Z': node.attrib['Z'],
        }

    @logger.catch()
    def __get_residues(self, structure) -> dict:
        residue_flow = self._get_elements_from_xml_tree('ResidueFlow', structure)[0].text.split(',')
        residues: dict = {}
        for residue in residue_flow:
            residue_id = re.findall(r'\d{1,3}', residue)[0]
            residues[residue_id] = {}
            residues[residue_id]['NAME'] = re.findall(r'[A-Za-z]{3}', residue)[0]
            result = re.findall(r'[A-Za-z]{4,}', residue)
            if len(result) > 0:
                residues[residue_id]['IN_STRUCTURE'] = result[0]
                index = len(result[0])+2
                residues[residue_id]['CHAIN'] = residue[-index]
            else:
                residues[residue_id]['CHAIN'] = residue[-1]
        return residues

    @logger.catch()
    def _set_structures_internal_relations(self) -> None:
        for structure_1 in self.structures:
            for structure_2 in self.structures:
                if structure_2 == structure_1:
                    continue
                for residue_1 in self.structures[structure_1].get_residues_number():
                    for residue_2 in self.structures[structure_2].get_residues_number():
                        if residue_1 == residue_2:
                            self.structures[structure_1].append_relation(structure_2)

    def get_type(self) -> str:
        return self.structure_type

    def get_structures(self) -> dict:
        return self.structures
