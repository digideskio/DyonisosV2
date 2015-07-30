from sqlobject import SQLObject, StringCol, IntCol, TimestampCol, FloatCol, ForeignKey, MultipleJoin, BoolCol, Col, AND
import time

class system_modules(SQLObject):
    name = StringCol(alternateID=True, unique=True)
    type = StringCol() # It's the old block column: Gatherer, MathsAnalysis ...

    version = FloatCol()

    active = BoolCol()

    advices = MultipleJoin('system_advices')
    marks = MultipleJoin('system_modules_marks')

    def _get_rate(self):
        actions = system_modules_marks.select(AND(system_modules_marks.q.moduleID == self.q.id, system_modules_marks.q.date > time.time() - (3600*24)))

        for a in list(actions):




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



