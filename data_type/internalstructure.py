

class InternalStructure:

    def __init__(self):
        self.structure_type: str = ''
        self.protein_name: str = ''

    def _set_protein_level(self, file_path) -> None:
        protein_level = file_path.split('_')[1]
        if '.' in protein_level:
            protein_level = protein_level.split('.')[0]
        self.protein_level = protein_level
