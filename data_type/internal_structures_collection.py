import xml.etree.ElementTree as ElementTree
from loguru import logger


class InternalStructuresCollection:
    data = {}
    file_path = ''

    def __init__(self):
        self.structure_type: str = ''
        self.protein_name: str = ''

    def _set_type(self, structure_type: str | list) -> None:
        """
        Устанавливает тип внутренней структуры

        :type structure_type: str | list
        """
        self.structure_type = structure_type


    @staticmethod
    def set_xml_data(file_path: str) -> None:
        """
        Устанавливает дерево элементов из xml-файла

        :param file_path: str
        :return:
        """
        InternalStructuresCollection.file_path = file_path
        tree = ElementTree.parse(file_path)
        InternalStructuresCollection.data['XML_ROOT'] = tree.getroot()
        logger.info(f'xml data for {file_path} has been set')

    def _set_protein_name(self) -> None:
        protein_name = InternalStructuresCollection.file_path.split('_')[0]
        if '/' in protein_name:
            protein_name = protein_name.split('/')[-1]
        elif '\\' in protein_name:
            protein_name = protein_name.split('\\')[-1]
        self.protein_name = protein_name

    def _set_protein_level(self) -> None:
        protein_level = InternalStructuresCollection.file_path.split('_')[1]
        if '.' in protein_level:
            protein_level = protein_level.split('.')[0]
        self.protein_level = protein_level

    @staticmethod
    def _get_elements_from_xml_tree(elements_name: str, node=None) -> list[ElementTree.Element]:
        """
        Возвращает все элементы по заданному имени

        :param elements_name:
        :return:
        """
        elements: list = []
        if node is None:
            node = InternalStructuresCollection.data['XML_ROOT']
        for element in node.iter(elements_name):
            elements.append(element)
        return elements
