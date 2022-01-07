from data_type.pathlike_structures_collection import PathlikeStructuresCollection
from data_type.pathlike_structure import PathlikeStructure
from .xl_writer import XlWriter
from .draw import Draw
from loguru import logger
from typing import Dict

LEVEL = {
    'dimer': 'Димер',
    'monomer': 'Мономер'
}


class Analyser:

    def __init__(self):
        self.structures: dict = {}
        self.errors: list = []
        self.relations: dict = {}
        self.relations_count: int = 0
        self.data_to_write: dict = {}

    def add_error(self, message):
        self.errors.append(message)

    @logger.catch()
    def append_structure_collection(self, collection: PathlikeStructuresCollection):
        structure_type = collection.structure_type
        protein_name = collection.protein_name
        protein_level = collection.protein_level
        if protein_name not in self.structures:
            self.structures[protein_name] = {structure_type: {protein_level: collection}}
        elif structure_type not in self.structures[protein_name]:
            self.structures[protein_name][structure_type] = {protein_level: collection}
        elif protein_level not in self.structures[protein_name][structure_type]:
            self.structures[protein_name][structure_type][protein_level] = collection
        else:
            logger.error(f'{protein_name} {structure_type} {protein_level} is already appended')

    @logger.catch()
    def run_analysis(self):
        logger.info('Run analysis')
        for i, protein in enumerate(self.structures):
            for n, structure_type in enumerate(self.structures[protein]):
                if i + 1 == len(self.structures) and n + 1 == len(self.structures[protein]):
                    write_relations = True
                else:
                    write_relations = False
                self.process_structure_list(self.structures[protein][structure_type], protein, structure_type,
                                            write_relations)
        if not self.errors:
            logger.info('Analysis complete successfully')
        else:
            logger.info('Analysis complete with errors')

    @logger.catch()
    def process_structure_list(self, structure_list: dict, protein: str, structure_type: str, write_relations: bool):
        try:
            structure_collection_primary: Dict[str, PathlikeStructure] = structure_list['dimer'].get_structures()
            if len(structure_collection_primary) == 0:
                structure_collection_primary: Dict[str, PathlikeStructure] = structure_list['monomer'].get_structures()
                structure_collection_minor: dict = {}
            else:
                structure_collection_minor: Dict[str, PathlikeStructure] = structure_list['monomer'].get_structures()
            for structure_primary in structure_collection_primary:
                level = structure_collection_primary[structure_primary].get_protein_level()
                self.prepare_data_to_write(structure_collection_primary[structure_primary], level)
                draw = Draw(structure_collection_primary[structure_primary])
                draw.draw_profile()
                for structure_minor in structure_collection_minor:
                    level = structure_collection_minor[structure_minor].get_protein_level()
                    self.prepare_data_to_write(structure_collection_minor[structure_minor], level)
                    draw = Draw(structure_collection_minor[structure_minor])
                    draw.draw_profile()
                    self.compare_residues_for_collections(structure_collection_primary[structure_primary],
                                                          structure_collection_minor[structure_minor],
                                                          protein, structure_type)
            xl_writer = XlWriter(protein, self.data_to_write, structure_type)
            xl_writer.write()
            if write_relations:
                xl_writer.write_external_relations(self.relations)
            self.data_to_write = {}
        except Exception as exc:
            logger.exception(exc)
            self.add_error(exc)

    @logger.catch()
    def prepare_data_to_write(self, structure: PathlikeStructure, level: str) -> None:
        is_oligomer = True if level != 'monomer' else False
        if level not in self.data_to_write:
            self.data_to_write[level] = {}
        if 'RELATIONS' not in self.data_to_write:
            self.data_to_write['RELATIONS'] = {}
        self.data_to_write[level][structure.get_id()] = structure.get_residues(True, is_oligomer)
        self.data_to_write['RELATIONS'][structure.get_id()] = structure.get_relations()

    @logger.catch()
    def compare_residues_for_collections(self, structure_1: PathlikeStructure,
                                         structure_2: PathlikeStructure,
                                         protein: str, structure_type: str):
        identity_count = 0
        residue_list_1 = structure_1.get_residues_number()
        residue_list_2 = structure_2.get_residues_number()
        protein_level_1 = structure_1.get_protein_level()
        protein_level_2 = structure_2.get_protein_level()
        if protein not in self.relations.keys():
            self.relations[protein] = {
                structure_type: {}
            }
        elif structure_type not in self.relations[protein].keys():
            self.relations[protein][structure_type] = {}
        for residue_1 in residue_list_1:
            for residue_2 in residue_list_2:
                if residue_1 == residue_2:
                    self.set_relations(protein, protein_level_1, protein_level_2, structure_1, structure_2,
                                       structure_type)
                    identity_count += 1
                    if residue_1 \
                            not in self.relations[protein][structure_type][self.relations_count]['RES_LIST_IDENTICAL']:
                        self.relations[protein][structure_type][self.relations_count]['RES_LIST_IDENTICAL'] \
                            .append(residue_1)
        if identity_count > 1:
            identity_percentage = identity_count * 100 / len(residue_list_2)
            self.relations[protein][structure_type][self.relations_count]['IDENTITY'] = identity_percentage
            self.set_nonidentical_res_list(residue_list_1, protein_level_1, protein, structure_type)
            self.set_nonidentical_res_list(residue_list_2, protein_level_2, protein, structure_type)
            self.relations_count += 1

    @logger.catch()
    def set_relations(self, protein, protein_level_1, protein_level_2, structure_1, structure_2, structure_type):
        if protein in self.relations.keys() and \
                self.relations_count not in self.relations[protein][structure_type].keys():
            self.relations[protein][structure_type] = {
                self.relations_count: {
                    protein_level_1: structure_1.get_id(),
                    protein_level_2: structure_2.get_id(),
                    'RES_LIST_IDENTICAL': [],
                    'RES_LIST_NONIDENTICAL': {
                        protein_level_1: [],
                        protein_level_2: [],
                    },
                }
            }

    @logger.catch()
    def set_nonidentical_res_list(self, residue_list, protein_level, protein, structure_type):
        nonidentical_residue_list: list = []
        for res in residue_list:
            if res not in self.relations[protein][structure_type][self.relations_count]['RES_LIST_IDENTICAL']:
                nonidentical_residue_list.append(res)
        self.relations[protein][structure_type][self.relations_count]['RES_LIST_NONIDENTICAL'][
            protein_level] = nonidentical_residue_list
