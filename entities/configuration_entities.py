__author__ = 'Maxime'

from sqlobject import SQLObject, StringCol, IntCol, TimestampCol, FloatCol, ForeignKey, MultipleJoin, BoolCol

class system_configuration(SQLObject):

    key = StringCol(alternateID=True, unique=True)
    val = StringCol()

    type = StringCol()
