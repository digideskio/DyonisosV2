__author__ = 'Maxime'

import logging
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

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


    def advice_generator(self, firm):
        raise SystemError('You have to overwrite advicegenerator()')

    def build_answer_generator(self, firms):
        for f in firms:
            self.advice_generator(f)

    def run(self, firms):
        self.build_answer_generator(firms)


    def logexec(self):
        logging.info(self.script_name + ' run.')

