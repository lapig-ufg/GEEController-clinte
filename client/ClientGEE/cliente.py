from ClientGEE.functions import get_info, check_tasks, Error
from ClientGEE.scripty import get_Exports


from requests import get
from time import sleep
import json
from sys import exit
import requests
from random import choice


from os.path import isfile
import ee
from ClientGEE.functions import __login_manual, login_gee


from requests import get
from sys import exit
from dynaconf import settings
from ClientGEE.config import logger






def main():

    if str(settings.LOGIN_FORCE) == '1':
        logger.debug('Please login a user on Google Earth Engine!')
        __login_manual(ee)

    if not isfile('.env'):
        import uuid

        with open('.env', 'w') as the_file:
            the_file.write(f"DYNACONF_CLIENT = '{uuid.uuid4().hex}'\n")
        login_gee(ee)

    logger.debug(f'This customer already has a user logged in')
    logger.debug(
        f'The client id is {settings.CLIENT} and is configured to process {settings.QUANTITY_ALLOWED_IN_QUEUE} task at the same time'
    )
    logger.debug(f'This client works with a class {settings.CLASS_RUM}')

    try:
        data = get(
            f'{settings.SERVER}/coder/get/{settings.VERSION}'
        ).json()
        with open('ClientGEE/scripty.py', 'w') as f1:
            f1.write(data['coder'])
        logger.warning(f" {data['date']}")

    except:
        exit(1)
    version = settings.VERSION
    client = settings.CLIENT
    ERRORS = Error()
    MAXRUN = settings.QUANTITY_ALLOWED_IN_QUEUE
    try:
        RUN_CLASS = settings.CLASS_RUM

        in_queue = get(
            f'{settings.SERVER}/task/get/{version}/{RUN_CLASS}'
        ).json()
        runnig = get(
            f'{settings.SERVER}/task/runnig/{version}/{client}'
        ).json()

    except json.decoder.JSONDecodeError:
        logger.warning('Servido não esta respondendo de forma correta')
        exit()
    except requests.exceptions.ConnectionError:
        logger.warning('Servidor Fora do ar')
        exit(1)

    while len(in_queue) + len(runnig) > 0:

        check_tasks(runnig, ERRORS)
        in_queue, runnig = get_info(in_queue, runnig, ERRORS)
        if len(runnig) < MAXRUN and len(in_queue) > 0:
            element = choice(in_queue)
            try:
                id_ = element['id_']
                name = element['name']
                num = element['num']
                task_id, res = get_Exports(version, num, name)
                runnig[id_] = task_id
                logger.info(f'add task ID:{id_} gee_id:{task_id}')
            except Exception as e:
                logger.exception(
                    f'element:{element}, tamanho:len(in_queue), error:{e}'
                )

        sleep(1)
        try:
            completed = get(
                f'{settings.SERVER}/task/completed/{version}'
            ).json()
            c_len = completed[0]['completed']
            falta = completed[0]['falta']
            len_errors = completed[0]['errors']
            logger.info(
                f'Foi completado {c_len} task, falta {falta} task, falhou {len_errors} task'
            )
        except Exception as e:
            logger.warning(f'{e}')
        logger.info(f'Estamos processando {len(runnig)}')
        logger.info(f'Errors = {ERRORS.get()}')
        if ERRORS.get() >= 25:
            exit(1)

    logger.info('Finalizado')
