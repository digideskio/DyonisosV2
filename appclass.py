__author__ = 'Maxime'

import logging

import threading
import sys, os
import time, datetime

# import DB Entities

from sqlobject import *
import YahouAPI.YahouApi as Yp

from entities.configuration_entities import system_configuration
from entities.decisions_entities import system_advices, system_orders
from entities.firms_entities import system_firms, system_firms_quotations
from entities.modules_entities import system_modules, system_modules_markers, system_modules_marks

from sqlobject import sqlhub, connectionForURI




class appclass():
    var = None

    firms = None  # A list of system_firms object
    instantiatedModules = None  # List of list => [[module SQL Object, instance of the script]]

    connection = None # db connection used for manual insertion or query

    def __init__(self):


        logging.basicConfig(filename='Data/dyonisos.log', format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p', filemode='a', level=logging.DEBUG)

        logging.info("================= Dyonisos ======================")

        logging.info("================= DB Connection =================")
        self.connection = connectionForURI('mysql://root@localhost:3306/dyonisos')
        sqlhub.processConnection = self.connection

        logging.info("==========Check if table are existing ===========")
        system_configuration.createTable(True)
        system_advices.createTable(True)
        system_orders.createTable(True)
        system_firms_quotations.createTable(True)
        system_firms.createTable(True)
        system_modules_markers.createTable(True)
        system_modules_marks.createTable(True)
        system_modules.createTable(True)

        #mod = system_modules(name='InfoScript', active=1, type='Gatherer', version=1.1)

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

        #system_firms(name='AB', isin='FFF', code='AB', groupe='1')



    def get_last_quote_info(self):
        codes = []
        for f in self.firms:
            codes.append(f.code)

        Request = Yp.RequestQuoteFirms(codes)
        data = Request.getall()

        query = 'INSERT INTO system_firms_quotations (quote, date, system_firms_id) VALUES'

        print Request.data
        for d, f in zip(data, self.firms):
            print d
            query = query + ' (' + str(d["LastTradePriceOnly"]) + ',' + str(time.time()) + ',' + str(f.id) + '),'

        print query
        query = query.rstrip(',')
        print query
        self.connection.query("INSERT INTO system_firms_quotations (quote, date, system_firms_id) VALUES (83.78,1438440200.77,1), (83.78,1438440200.77,1)")




    def run_gatherer(self):

        threadpool = []

        for m in self.instantiatedModules:
            mod = m[0]
            instance = m[1]
            if str(mod.type) == 'Gatherer':
                try:
                    t = threading.Thread(target=instance.run)
                    t.start()
                    # Add new thread in the threadlist
                    threadpool.append(t)

                except SystemError as error:
                    logging.warning(error[0])

        # Wait for all thread are finished
        for thread in threadpool:
            thread.join()

    def run_mathsanalysis(self):

        threadpool = []

        for m in self.instantiatedModules:
            mod = m[0]
            instance = m[1]
            if str(mod.type) == 'Mathsanalysis':
                try:
                    t = threading.Thread(target=instance.run)
                    t.start()
                    # Add new thread in the threadlist
                    threadpool.append(t)

                except SystemError as error:
                    logging.warning(error[0])

        # Wait for all thread are finished
        for thread in threadpool:
            thread.join()


    def run(self):
        self.get_last_quote_info()
        self.run_gatherer()
