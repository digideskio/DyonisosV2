from sqlobject import SQLObject, StringCol, IntCol, TimestampCol, FloatCol, ForeignKey, MultipleJoin, BoolCol, Col, AND
import datetime
import time

class system_modules(SQLObject):
    name = StringCol(alternateID=True, unique=True)
    type = StringCol() # It's the old block column: Gatherer, MathsAnalysis ...

    version = FloatCol()

    active = BoolCol()

    advices = MultipleJoin('system_advices')
    marks = MultipleJoin('system_modules_marks')

    def _get_rates(self):
        actions = system_modules_marks.select(AND(system_modules_marks.q.moduleID == self.q.id, system_modules_marks.q.date > datetime.datetime.now() - datetime.timedelta(3600*24)))

        rates = {'rateshort': 0.00, 'ratemedium': 0.00, 'ratelong': 0.00}
        actions = list(actions)
        for action in actions:
            rates['rateshort'] += action.actionS
            rates['ratemedium'] += action.actionM
            rates['ratelong'] += action.actionL

        if rates['rateshort'] <= 0:
            rates['rateshort'] = 0
        if rates['ratemedium'] <= 0:
            rates['ratemedium'] = 0
        if rates['ratelong'] <= 0:
            rates['ratelong'] = 0


        rates['rateshort'] = rates['rateshort'] / len(actions)
        rates['ratemedium'] = rates['ratemedium'] / len(actions)
        rates['ratelong'] = rates['ratelong'] / len(actions)

        return rates

    def _get_rateshort(self):
        rates = self._get_rates()
        return rates['rateshort']

    def _get_ratemedium(self):
        rates = self._get_rates()
        return rates['ratemedium']

    def _get_ratelong(self):
        rates = self._get_rates()
        return rates['ratelong']


class system_modules_marks(SQLObject):
    actionS = IntCol()
    actionM = IntCol()
    actionL = IntCol()

    date = TimestampCol()

    advice = ForeignKey('system_advices', default=None) # Give the advice on which the mark is based
    Source = ForeignKey('system_modules_markers', default=None) # Give the notation Script
    module = ForeignKey('system_modules', default=None)


class system_modules_markers(SQLObject):
    name = StringCol(alternateID=True, unique=True)



