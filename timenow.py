import logging

from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException

logging.basicConfig()
logger = logging.getLogger("kalliope")

class timenow(NeuronModule):
    """
    Advanced timer kalliope neuron
    Launch timers and store in Kalliope_memory the date/time of the lauch to be able to know the remaing time
    """
    def __init__(self, **kwargs):
        # super(timenow, self).__init__(**kwargs)

        self.configuration = {
            'action': kwargs.get('action', None)
        }

        self.say(self.action)
