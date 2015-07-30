__author__ = 'Maxime'


from sqlobject import SQLObject, StringCol, IntCol, TimestampCol, FloatCol, ForeignKey, MultipleJoin


class system_firms(SQLObject):
    name = StringCol(alternateID = True, unique=True)
    isin = StringCol(alternateID = True, unique=True)
    code = StringCol(alternateID = True, unique=True)

    groupe = StringCol()

    quotations = MultipleJoin('system_firms_quotations')
    advices = MultipleJoin('system_advices')


class system_firms_quotations(SQLObject):
    quote = FloatCol()
    date = TimestampCol()

    firm = ForeignKey('system_firms', dbName='system_firms_id')





