__author__ = 'Maxime'

import logging
from advicegenericscript import AdviceGenericScript, Advice

class InfoScript(AdviceGenericScript):

    scriptname = 'InfoScript'
    version = '1'

    def advice_generator(self, firm):
        answer = Advice
        answer.action = 1
        answer.firm_isin = "FR0000076887"
        answer.module_name = self.scriptname

        return answer

    def run(self):
        print('FDP')


