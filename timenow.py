import logging
import datetime

from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException
from datetime import timedelta

logging.basicConfig()
logger = logging.getLogger("kalliope")

class Timenow(NeuronModule):
    """
    Advanced timer kalliope neuron
    Launch timers and store in Kalliope_memory the date/time of the lauch to be able to know the remaing time
    """
    def __init__(self, **kwargs):
        super(Timenow, self).__init__(**kwargs)

        self.action = kwargs.get('action', None)
        self.seconds = kwargs.get('seconds', "0")
        self.minutes = kwargs.get('minutes', "0")
        self.hours = kwargs.get('hours', "0")
        self.months = kwargs.get('months', "0")
        self.day_months = kwargs.get('day_months', "0")
        self.years = kwargs.get('years', "0"),
        self.title = kwargs.get('title', None)

        if self._is_parameters_ok():
            if self.action == 'create':
                self.seconds = self.get_integer_time_parameter(self.seconds)
                self.minutes = self.get_integer_time_parameter(self.minutes)
                self.hours = self.get_integer_time_parameter(self.hours)
                timertime = datetime.datetime.now() + datetime.timedelta(hours=self.hours, minutes=self.minutes, seconds=self.seconds)
                logger.debug("[timenow] timer at : " + str(timertime))
                # local time and date
                second = timertime.strftime("%S")        # Second as a decimal number [00,59].
                minute = timertime.strftime("%M")        # Minute as a decimal number [00,59].
                hour = timertime.strftime("%H")          # Hour (24-hour clock) as a decimal number [00,23].
                day_month = timertime.strftime("%d")     # Day of the month as a decimal number [01,31].
                month = timertime.strftime("%m")         # Month as a decimal number [01,12].
                year = timertime.strftime("%Y")          # Year with century as a decimal number. E.g: 2016
                self.message = {
                    "action": self.action,
                    "timer_hours": hour,
                    "timer_minutes": minute,
                    "timer_seconds": second,
                    "timer_months": month,
                    "timer_day_months": day_month,
                    "timer_years": year,
                    "param_hours": str(self.hours),
                    "param_minutes": str(self.minutes),
                    "param_seconds": str(self.seconds),
                    "param_title": self.title
                }
            elif self.action == 'get-remaining-time':
                passed_date = datetime.datetime(self.years,self.months,self.day_months,self.hours,self.minutes,self.seconds)
                logger.debug("[timenow] cmd: " + self.action + ": date to compare: " + str(passed_date))
                if passed_date >=  datetime.datetime.now():
                    time_delay =  passed_date - datetime.datetime.now()
                else:
                    time_delay =  datetime.datetime.now() - passed_date
                time_delay_total_seconds = round(time_delay.total_seconds())
                logger.debug("[timenow] cmd: " + self.action + ": difference: " + str(time_delay)+" ou "+str(time_delay_total_seconds)+"sec")
                reporting_days = time_delay_total_seconds // (3600*24)
                time_delay_total_seconds = time_delay_total_seconds % (3600*24)
                reporting_hours = time_delay_total_seconds // 3600
                time_delay_total_seconds = time_delay_total_seconds % 3600
                reporting_minutes = time_delay_total_seconds // 60
                reporting_seconds = time_delay_total_seconds % 60
                self.message = {
                    "action": self.action,
                    "hours": str(reporting_hours),
                    "minutes": str(reporting_minutes),
                    "seconds": str(reporting_seconds),
                    "months": "0",
                    "day_months": str(reporting_days),
                    "years": "0"
                    # "hours": time_delay.datetime.strftime("%H"),
                    # "minutes": time_delay.datetime.strftime("%M"),
                    # "seconds": time_delay.datetime.strftime("%S"),
                    # "months": time_delay.datetime.strftime("%m"),
                    # "day_months": time_delay.datetime.strftime("%d"),
                    # "years": time_delay.datetime.strftime("%y")
                }
            else:
                self.message = "no message"
            self.say(self.message)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron.
        :return: True if parameters are ok, raise an exception otherwise.
        .. raises:: MissingParameterException
        """
        if self.action != 'create' and self.action != 'get-remaining-time':
            raise InvalidParameterException("AdvancedTime need a valid command : create or get-remaining-time")
        if self.action == 'create':
            if self.seconds is None or self.minutes is None or self.hours is None:
                raise MissingParameterException("AdvancedTime must have all time information : seconds, minutes, hours")
        if self.action == 'get-remaining-time':
            if self.seconds is None or self.minutes is None or self.hours is None or self.months is None or self.day_months is None or self.years is None:
                raise MissingParameterException("AdvancedTime must have all time information : seconds, minutes, hours, day_months, months, years")
        return True

    @staticmethod
    def get_integer_time_parameter(time_parameter):
        """
        Check if a given time parameter is a valid integer:
        - must be > 0
        - if type no an integer, must be convertible to integer
        :param time_parameter: string or integer
        :return: integer
        """
        if time_parameter is not None:
            if not isinstance(time_parameter, int):
                # try to convert into integer
                try:
                    time_parameter = int(time_parameter)
                except ValueError:
                    raise InvalidParameterException("[AdvancedTime] %s is not a valid integer" % time_parameter)
            # check if positive
            if time_parameter < 0:
                raise InvalidParameterException("[AdvancedTime] %s must be > 0" % time_parameter)
        return time_parameter
