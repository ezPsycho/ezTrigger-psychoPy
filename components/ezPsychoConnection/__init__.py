from os import path
from .._base import BaseComponent, Param, getInitVals, _translate

__author__ = 'Losses Don'

# abs path to the folder containing this path
thisFolder = path.abspath(path.dirname(__file__))
iconFile = path.join(thisFolder, 'ezPsychoConnection.png')
tooltip = _translate('ezTrigger Connection: Connecting to a ezTrigger system server.')

connectionScript = open(path.join(thisFolder, 'connectionScript.py'), 'r').read()

# only use _localized values for label values, nothing functional:
_localized = {'serverIp': _translate('Server address'),
              'serverPort': _translate("Server port"),
              'ClientType': _translate("Client type"),
              'ClientId': _translate("Client ID")}


class ezTriggerConnectionComponent(BaseComponent):
    categories = ['ezTrigger System']

    def __init__(self, exp, parentName, name='ezTriggerConnection',
                 serverIp='', serverPort='233333', clientType='PPY', clientId=''):
        super(ezTriggerConnectionComponent, self).__init__(exp, parentName, name)

        self.type = 'ezTriggerConnection'
        self.targets = ['PsychoPy']
        self.url = "https://github.com/ezPsycho"
        # params
        # want a copy, else codeParamNames list gets mutated

        msg = _translate(
            "The address of the server - an IP address or an domain.")
        self.params['serverIp'] = Param(
            serverIp, valType='str', allowedTypes=[],
            hint=msg,
            label=_localized["serverIp"])

        
        msg = _translate(
            "The port of the server - a number between 1 and 65535.")
        self.params['serverPort'] = Param(
            serverPort, valType='num', allowedTypes=[],
            hint=msg,
            label=_localized["serverPort"])

        msg = _translate(
            "The type of this client - fill 'PPY' if you dont know what does it means.")
        self.params['clientType'] = Param(
            clientType, valType='str', allowedTypes=[],
            hint=msg,
            label=_localized["ClientType"])

        msg = _translate(
            "The ID of this client - to distinguish this device from other devices, you can set an IP for each one.")
        self.params['clientId'] = Param(
            clientId, valType='str', allowedTypes=[],
            hint=msg,
            label=_localized["ClientId"])

        for p in ('startType', 'startVal', 'startEstim', 'stopVal',
                  'stopType', 'durationEstim'):
            del self.params[p]


    def writeInitCode(self, buff):
        buff.writeIndentedLines(connectionScript + '\n')

        inits = getInitVals(self.params, 'PsychoPy')
        code = ("%(name)s = PDESClient(%(serverIp)s , %(serverPort)s, %(ClientType)s, %(ClientId)s)"
                "%(name)s.start()")

        buff.writeIndentedLines(code % inits + '\n')

    def writeExperimentEndCode(self, buff):
        inits = getInitVals(self.params, 'PsychoPy')
        code = ("%(name)s.close()")

        buff.writeIndentedLines(code % inits + '\n')
