__author__ = 'Maxime'

import logging
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from sqlobject import *
from entities.configuration_entities import system_configuration
from entities.decisions_entities import system_advices, system_orders
from entities.firms_entities import system_firms, system_firms_quotations
from entities.modules_entities import system_modules, system_modules_markers, system_modules_marks

# Advice Scripts return now nothing: they write themselfe in the DB
# We have to populate a system_advices object in advice_generator
#
class AdviceGenericScript:

    script_name = None
    version = '1'
    DataM = None
    answer = []

    conf = []

    def __init__(self):
        self.script_name = self.__class__.__name__



    def run(self):
        pass


    def logexec(self):
        logging.info(self.script_name + ' run.')

