__author__ = 'Maxime'


from sqlobject import SQLObject, StringCol, IntCol, TimestampCol, FloatCol, ForeignKey, MultipleJoin, AND

from entities.configuration_entities import system_configuration
from entities.decisions_entities import system_advices, system_orders
from entities.modules_entities import system_modules, system_modules_markers, system_modules_marks

import datetime


class system_firms(SQLObject):
    name = StringCol(alternateID = True, unique=True)
    isin = StringCol(alternateID = True, unique=True)
    code = StringCol(alternateID = True, unique=True)

    groupe = StringCol()

    quotations = MultipleJoin('system_firms_quotations')
    advices = MultipleJoin('system_advices')



    def _get_rates(self):
        advices = system_advices.select(AND(system_advices.q.firmID == self.q.id, system_advices.q.date > datetime.datetime.now() - datetime.timedelta(days=30)))
        print list(advices)
        advices = list(advices)

        rates = {'rateshort': 0.00, 'ratemedium': 0.00, 'ratelong': 0.00}

        for advice in advices:
            if advice.date > datetime.datetime.now() - datetime.timedelta(days=3):
                rates['rateshort'] += advice.actionS * advice.module.rateshort
            if advice.date > datetime.datetime.now() - datetime.timedelta(days=10):
                rates['ratemedium'] += advice.actionM * advice.module.ratemedium
            if advice.date > datetime.datetime.now() - datetime.timedelta(days=30):
                rates['ratelong'] += advice.actionL * advice.module.ratelong

        return rates



class system_firms_quotations(SQLObject):
    quote = FloatCol()
    date = TimestampCol()

    firm = ForeignKey('system_firms', dbName='system_firms_id')





