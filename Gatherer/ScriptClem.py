__author__ = 'Maxime'


import logging
from advicegenericscript import AdviceGenericScript, Advice

class ScriptClem(AdviceGenericScript):

    scriptname = 'ScriptClem'
    version = '1'

    def advice_generator(self, firm):
        # firm = (name, isin, code)

        #
        #
        #
        # ....

        conseil = Advice

        conseil.Source = scriptname
        conseil.action = action
        conseil.firm_isin = firm[1]


        return conseil





