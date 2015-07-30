__author__ = 'Maxime'

import logging
import sys, os
import time, datetime

# import DB Entities

from sqlobject import *

from entities.configuration_entities import system_configuration
from entities.decisions_entities import system_advices, system_orders
from entities.firms_entities import system_firms, system_firms_quotations
from entities.modules_entities import system_modules, system_modules_markers, system_modules_marks

from sqlobject import sqlhub, connectionForURI


class appclass():
    var = None

    firms = None  # A list of system_firms object
    instantiatedModules = None  # List of list => [[module SQL Object, instance]]

    def __init__(self):
        logging.basicConfig(filename='Data/dyonisos.log', format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p', filemode='a', level=logging.DEBUG)

        logging.info("================= Dyonisos ======================")

        logging.info("================= DB Connection =================")
        sqlhub.processConnection = connectionForURI('sqlite:/:memory:')

        logging.info("==========Check if table are existing ===========")
        system_configuration.createTable(True)
        system_advices.createTable(True)
        system_orders.createTable(True)
        system_firms_quotations.createTable(True)
        system_firms.createTable(True)
        system_modules_markers.createTable(True)
        system_modules_marks.createTable(True)
        system_modules.createTable(True)

        logging.info("========== Load Firms ===========")
        self.firms = system_firms.select()

        logging.info("========== Load Modules ===========")
        self.modules = system_modules.selectBy(active=1)

        logging.info("========== Import Modules ===========")

        self.instantiatedModules = []

        for m in self.modules:
            try:
                scriptmodule = __import__(str(m.type) + '.' + str(m.name), globals(), locals(), [str(m.name)], -1)
                modscript = getattr(scriptmodule, str(m.name))

                self.instantiatedModules.append([m, modscript()])
            except ImportError:
                logging.warning(str(m.type) + "." + str(m.name) + ": Echec.")

        logging.info("========== End of init ===========")


        mod = system_modules(name='InfoScript', active=1, type='Gatherer', version=1.1)
        system_modules_marks(actionS = 50, actionL = 50, actionM = 50, date= datetime.datetime(2001, 5, 3), module=mod)
        mod._get_rate()


    def run_gatherer(self):
        for m in self.instantiatedModules:

            mod = m[0]
            instance = m[1]
            if str(mod.type) == 'Gatherer':
                try:
                    instance.run(self.firms)
                except SystemError as error:
                    logging.warning(error[0])


    def run(self):
        self.run_gatherer()
