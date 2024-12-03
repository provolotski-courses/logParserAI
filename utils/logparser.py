import logging
import datefinder
from utils.config import LOG_DIR, LOG_FILE, LOG_LEVEL

logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s %(name)-30s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.FileHandler(LOG_DIR + LOG_FILE), logging.StreamHandler()])
logger = logging.getLogger(__name__)


def parsMultistring(file):
    logger.debug(f'Обработка мультистрингового лога')
    if file is None:
        logger.error('Пустой файл')
    else:
        logger.info('файл получен')
        logger.info(f'Размер файла {len(file)}')
        row_list = file.split(b'\n')
        item_str =''
        for row in row_list:
            date = datefinder.find_dates(row)

            if
            print(row.decode('utf-8'))

