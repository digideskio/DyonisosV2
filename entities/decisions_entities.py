__author__ = 'Maxime'


from sqlobject import SQLObject, StringCol, IntCol, TimestampCol, FloatCol, ForeignKey, MultipleJoin


class system_advices(SQLObject):

    date = TimestampCol()

    actionS = IntCol()
    actionM = IntCol()
    actionL = IntCol()

    firm = ForeignKey('system_firms')
    module = ForeignKey('system_modules')
    order = ForeignKey('system_orders', default=None)



class system_orders(SQLObject):
    forecastType = IntCol() # Short, Medium, Long

    entryQuote = FloatCol()
    exitQuote = FloatCol()

    entryDate = TimestampCol()
    exitDate = TimestampCol()

    amount = FloatCol()

    firm = ForeignKey('system_firms')

    src_advices = MultipleJoin('system_advices')