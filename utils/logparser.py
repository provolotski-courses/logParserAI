import logging
import re
from DAO.connection import load_log,load_event
from dateutil.parser import parse
from utils.config import LOG_DIR, LOG_FILE, LOG_LEVEL
import utils.cacheVariables as cacheVariables

logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s %(name)-30s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.FileHandler(LOG_DIR + LOG_FILE), logging.StreamHandler()])
logger = logging.getLogger(__name__)


def findDateInRow(row):
    try:
        date = parse(row, fuzzy=True)
        return True, date
    except (ValueError, OverflowError):
        return False, None


def findErrorinRow(row):
    pattern = r'\b(' + '|'.join(re.escape(element) for element in cacheVariables.ErrorTemplates) + r')\b'
    return bool(re.search(pattern, row))


def parsMultistring(file,filename):
    logger.debug(f'Обработка мультистрингового лога')
    if file is None:
        logger.error('Пустой файл')
    else:
        logger.info('файл получен')
        log_id = load_log(filename)
        logger.info(f'Размер файла {len(file)}')
        row_list = file.split(b'\n')
        item_str = ''
        for row in row_list:
            try:
                item_row = str(row, encoding='utf-8')
            except UnicodeDecodeError:
                # try:
                item_row = str(row, encoding='windows-1251')
                # except:
                #     item_row = str(row)

            flag, date = findDateInRow(item_row)
            if flag:
                if item_str != '':
                    if findErrorinRow(item_str):
                        load_event(date,item_str,2,log_id)
                    else:
                        load_event(date,item_str,1,log_id)
                    item_str = item_row
            else:
                try:
                    item_str += ' '
                    item_str += item_row
                except OverflowError:
                    logger.error(item_str)
                    logger.error(item_row)
                    item_str = item_row
