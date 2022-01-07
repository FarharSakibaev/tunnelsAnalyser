from analyser.analyser import Analyser
from data_type.pathlike_structures_collection import PathlikeStructuresCollection
from data_type.internal_structures_collection import InternalStructuresCollection
from loguru import logger
from params import Params
import os
import sys
import tracemalloc
from typing import Final

DEBUG: Final[str] = '--debug'
LOG_FILE_SIZE: Final[str] = '300 KB'
COMPRESSION_TYPE: Final[str] = 'zip'
DEBUG_LEVEL: Final[str] = 'DEBUG'
LOG_FILE_PATH: Final[str] = 'logs/tunnelsAnalyser.log'
LOG_FILE_FORMAT: Final[str] = '{time} {level} {message}'


def set_logger():
    logger.add(LOG_FILE_PATH, format=LOG_FILE_FORMAT, level=DEBUG_LEVEL, rotation=LOG_FILE_SIZE,
               compression=COMPRESSION_TYPE)
    logger.info('Start program')


def set_params():
    for param in sys.argv:
        if DEBUG in param:
            Params.set_debug(bool(param.split('=')[1]))


def main():
    tracemalloc.start()
    set_params()
    set_logger()

    path = 'test/pathlike'
    files = os.listdir(path)
    tunnels_analyser = Analyser()
    for file in files:
        if 'cavities' in file:
            continue
        InternalStructuresCollection.set_xml_data(f'{path}/{file}')
        tunnels_collection = PathlikeStructuresCollection('Tunnel')
        tunnels_analyser.append_structure_collection(tunnels_collection)
        pores_collection = PathlikeStructuresCollection('Pore')
        tunnels_analyser.append_structure_collection(pores_collection)
    tunnels_analyser.run_analysis()
    logger.info('Current memory usage: %d, Peak memory usage %d' % tracemalloc.get_traced_memory())


if __name__ == '__main__':
    main()
