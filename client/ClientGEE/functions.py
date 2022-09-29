from sys import version
from dynaconf import settings
import ee
import urllib3
import json
import requests
from requests import get
from requests import post
from multiprocessing import Pool, cpu_count
from ClientGEE.config import logger


def get_info(in_queue, runnig, ERRORS):
    try:
        RUN_CLASS = settings.CLASS_RUM
        in_queue = get(
            f'{settings.SERVER}/task/get/{settings.VERSION}/{RUN_CLASS}'
        ).json()
        runnig = get(
            f'{settings.SERVER}/task/runnig/{settings.VERSION}/{settings.CLIENT}'
        ).json()
        return in_queue, runnig
    except json.decoder.JSONDecodeError:
        ERRORS.add()
        return in_queue, runnig
    except requests.exceptions.ConnectionError:
        logger.warning('Servidor Fora do ar')
        ERRORS.add()
        return in_queue, runnig


def __check_tasks(args):
    id_, gee_task, new = args
    try:
        state = gee_task[id_]
        if state == 'FAILED':
            state = error_in_task(ee.batch.Task(id_, '', '').status())
    except Exception as e:
        __task = ee.batch.Task(id_, '', '').status()
        state = __task['state']
        if state == 'FAILED':
            state = error_in_task(__task)
        logger.warning(f'state obitdo de forma bruta {id_} {state} {e}')
    data = {
        'id_': new[id_],
        'state': state,
        'task_id': id_,
        'client': settings.CLIENT,
    }
    logger.debug(data)
    post(f'{settings.SERVER}/task/update', json=data)


def check_tasks(runnig, ERRORS):
    tasks_in_queue = [runnig[i] for i in runnig]
    new = {runnig[i]: i for i in runnig}
    try:
        all_task = ee.batch.Task.list()
    except urllib3.exceptions.ProtocolError:
        logger.warning('Error login no GEE na hora de checkar as task')
    gee_task = {i.id: i.state for i in all_task if i.id in tasks_in_queue}
    logger.debug(tasks_in_queue)
    args = [(_id, gee_task, new) for _id in tasks_in_queue]
    for _args in args:
        __check_tasks(_args)


class Error:
    def __init__(self):
        self.error = 0

    def get(self):
        return self.error

    def add(self):
        self.error = self.error + 1


def type_process(type_):
    if type_ in ['READY', 'RUNNING', 'UNSUBMITTED']:
        return 'RUNNING'
    if type_ == 'COMPLETED':
        return 'COMPLETED'
    if type_ == 'ERROR':
        return 'ERROR'
    return 'IN_QUEUE'


def error_in_task(__task):
    errors = [  # Erros que nao poder rodar de novo
        'Image.classify: No valid training data were found.',
        'Image.classify: Expected 2 classes for PROBABILITY, found 1. (Error code: 3)',
        'Image.classify: Expected 2 classes for PROBABILITY, found 1.',
        'Image.sampleRegions: Invalid numInputs: 0.',
    ]
    try:
        if __task['error_message'] in errors:
            logger.log('GEE', f"Erro não iguinorado no script {__task['error_message']}")
            return 'ERROR'
        __task['state']
    except KeyError as e:
        #WARNING
        logger.warnig(f"Erro iguinorado no script {__task['error_message']}")
        return __task['state']


def id_(version, name):
    return f'{version}_{name}'


def login_gee(ee):
    try:
        ee.Initialize()
    except FileNotFoundError as e:
        __login_manual(ee)
    except ee.ee_exception.EEException as e:
        logger.debug('Login fall', e)
        __login_manual(ee)


def __login_manual(ee):
    ee.Authenticate()
    ee.Initialize()
