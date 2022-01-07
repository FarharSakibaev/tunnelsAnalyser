import matplotlib.pyplot as plt
from data_type.pathlike_structure import PathlikeStructure

X_LABEL = 'Расстояние'
Y_LABEL = 'Радиус'
FONT_SIZE = 15
DPI = 350
PRIMARY_FORMAT = 'tif'
MINOR_FORMAT = 'png'


class Draw:

    def __init__(self, structure: PathlikeStructure):
        self.structure: PathlikeStructure = structure
        self.path: str = self.get_path()
        self.coordinates: list = prepare_data_to_draw(structure)

    def draw_profile(self):
        ax = plt.subplots()[1]
        ax.set_xlabel(X_LABEL, fontsize=FONT_SIZE)
        ax.set_ylabel(Y_LABEL, fontsize=FONT_SIZE)
        ax.plot(*self.coordinates)
        plt.grid(True)
        plt.savefig(f'{self.path}.{MINOR_FORMAT}')
        plt.savefig(f'{self.path}.{PRIMARY_FORMAT}', dpi=350)
        plt.close()

    def get_path(self) -> str:
        protein = self.structure.get_protein()
        protein_level = self.structure.get_protein_level()
        structure_id = self.structure.get_id()
        return f'{protein}_{protein_level}_{structure_id}'


def prepare_data_to_draw(structure: PathlikeStructure):
    output_profile = [[], []]
    structure_profile = structure.get_profile()
    for data in structure_profile:
        output_profile[0].append(float(data['T']))
        output_profile[1].append(float(data['RADIUS']))
    return output_profile
