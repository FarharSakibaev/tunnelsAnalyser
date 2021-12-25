from analyser.analyser import Analyser
from config.dir_config import DirConfig
from data_type.pathlike_structures_collection import PathlikeStructuresCollection
from data_type.internal_structures_collection import InternalStructuresCollection
from loguru import logger
import os


def set_logger():
    logger.add(DirConfig.LOG_FILE_PATH, format=DirConfig.LOG_FILE_FORMAT, level='DEBUG', rotation='150 KB',
               compression='zip')
    logger.info('Start program')


def main():
    set_logger()

    path = 'test'
    files = os.listdir(path)
    tunnels_analyser = Analyser()
    for file in files:
        InternalStructuresCollection.set_xml_data(f'{path}/{file}')
        tunnels_collection = PathlikeStructuresCollection('Tunnel')
        tunnels_analyser.append_structure_collection(tunnels_collection)
        pores_collection = PathlikeStructuresCollection('Pore')
        tunnels_analyser.append_structure_collection(pores_collection)
    tunnels_analyser.run_analysis()


if __name__ == '__main__':
    main()
