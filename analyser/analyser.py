from data_type.pathlike_structures_collection import PathlikeStructuresCollection
from data_type.pathlike_structure import PathlikeStructure
from loguru import logger


class Analyser:

    def __init__(self):
        self.structures: dict = {}
        self.errors: list = []
        self.relations: dict = {}
        self.relations_count: int = 0

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
        for protein in self.structures:
            for structure_type in self.structures[protein]:
                self.compare_residues(self.structures[protein][structure_type], protein)
        if not self.errors:
            logger.info('Analysis complete successful')
        else:
            logger.info('Analysis complete with errors')

    @logger.catch()
    def compare_residues(self, structure_list: dict, protein: str):
        try:
            structure_collection_1 = structure_list['dimer'].get_structures()
            structure_collection_2 = structure_list['monomer'].get_structures()
            for structure_1 in structure_collection_1:
                for structure_2 in structure_collection_2:
                    self.compare_residues_for_collections(structure_collection_1[structure_1],
                                                          structure_collection_2[structure_2],
                                                          protein)
        except Exception as exc:
            logger.exception(exc)
            self.add_error(exc)

    @logger.catch()
    def compare_residues_for_collections(self, structure_1: PathlikeStructure,
                                         structure_2: PathlikeStructure,
                                         protein: str):
        identity_count = 0
        residue_list_1 = structure_1.get_residues_number()
        residue_list_2 = structure_2.get_residues_number()
        protein_level_1 = structure_1.get_protein_level()
        protein_level_2 = structure_2.get_protein_level()
        if protein not in self.relations.keys():
            self.relations[protein] = {}
        for residue_1 in residue_list_1:
            for residue_2 in residue_list_2:
                if residue_1 == residue_2:
                    self.set_relations(protein, protein_level_1, protein_level_2, structure_1, structure_2)
                    identity_count += 1
                    if residue_1 not in self.relations[protein][self.relations_count]['RES_LIST_IDENTICAL']:
                        self.relations[protein][self.relations_count]['RES_LIST_IDENTICAL'].append(residue_1)
        if identity_count > 1:
            identity_percentage = identity_count * 100 / len(residue_list_2)
            self.relations[protein][self.relations_count]['IDENTITY'] = identity_percentage
            self.set_nonidentical_res_list(residue_list_1, protein_level_1, protein)
            self.set_nonidentical_res_list(residue_list_2, protein_level_2, protein)
            self.relations_count += 1

    @logger.catch()
    def set_relations(self, protein, protein_level_1, protein_level_2, structure_1, structure_2):
        if protein in self.relations.keys() and self.relations_count not in self.relations[protein].keys():
            self.relations[protein] = {
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
    def set_nonidentical_res_list(self, residue_list, protein_level, protein):
        nonidentical_residue_list: list = []
        for res in residue_list:
            if res not in self.relations[protein][self.relations_count]['RES_LIST_IDENTICAL']:
                nonidentical_residue_list.append(res)
        self.relations[protein][self.relations_count]['RES_LIST_NONIDENTICAL'][
            protein_level] = nonidentical_residue_list
