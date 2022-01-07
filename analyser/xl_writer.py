from pandas import DataFrame, ExcelWriter
from os import path

XL_TYPE = 'xlsx'
replacements = {
    'dimer': 'Димер',
    'monomer': 'Мономер',
    'RELATIONS': 'Связанная структура'
}


def replace_keys(data: dict):
    new_dict = {}
    for key in data:
        if type(data[key]) == dict:
            if key in replacements:
                new_dict[replacements[key]] = replace_keys(data[key])
            else:
                new_dict[key] = data[key]
        elif key in replacements:
            new_dict[replacements[key]] = data[key]
        else:
            new_dict = data
    return new_dict


class XlWriter:

    def __init__(self, protein: str, data: dict, structure_type: str) -> None:
        self.protein: str = protein
        self.data: dict = data
        self.structure_type: str = structure_type
        self.filepath: str = self.get_file_path()

    def write(self) -> None:
        mode = 'a' if path.exists(self.filepath) else 'w'
        self.data = replace_keys(self.data)
        dataframe = DataFrame(data=self.data)
        with ExcelWriter(self.filepath, mode=mode) as writer:
            dataframe.to_excel(writer, sheet_name=self.structure_type)

    @staticmethod
    def write_external_relations(relations: dict) -> None:
        for protein in relations:
            file_path = f'{protein}.{XL_TYPE}'
            for structure in relations[protein]:
                mode = 'a' if path.exists(file_path) else 'w'
                dataframe = DataFrame(data=relations[protein][structure])
                with ExcelWriter(file_path, mode=mode) as writer:
                    dataframe.T.to_excel(writer, sheet_name=f'{protein}_{structure}')

    def get_file_path(self) -> str:
        return f'{self.protein}.{XL_TYPE}'
