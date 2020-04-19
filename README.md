# timenow

A very simple neuron for Kalliope that returns the  date/time after a given delay (requires seconds/minutes/hours) but that can also return the time delay between a given date and now()


## Synopsis

You can ask the current time. It is close to the neuron Systemdate but Systemdate does not provide the second information. 

You can also ask the neuron to give a time delay between the given date/time and the current date/time

The "title" information has no transformation and is not needed. If passed to the neuron, it is just transfered into the output message. This is useful to store this title in the kalliope memory.

The purpose of this neuron is to be used with Nerotimer, to store some information regarding a timer. 
When calling a timer with Neurotimer, you can't get the timer expiration time. 
Then you can't ask kalliope the remaining time before the end of this timer. 
Also for some reason it is not possible to store the minut/seconds/hour info of the timer in Kalliope_Memory. 
Then you can use this neuron instead of forwarded_parameters, because the forwarded parameters can't be forwarded again. This is useful if you want to use a snooze function.

## Installation

  ```
  kalliope install --git-url https://github.com/DuduNord/timenow
  ```


## Options

| parameter                  | required | default | choices | comment                                                                                         |
|----------------------------|----------|---------|---------|-------------------------------------------------------------------------------------------------|
| action                     | yes      |         | create / get-remaining-time   | action to perform                                                         |
| seconds                    | yes      | 0       |         | The seconds delay from now or the seconds time to calculate the delay from now                  |
| minutes                    | yes      | 0       |         | The minutes delay from now or the minutes time to calculate the delay from now                  |
| hours                      | yes      | 0       |         | The hours delay from now or the hours time to calculate the delay from now                      |
| months                     | 'get-remaining-time' only    | 0       |         | The months time to calculate the delay from now                             |
| day_months                 | 'get-remaining-time' only    | 0       |         | The days time to calculate the delay from now                               |
| years                      | 'get-remaining-time' only    | 0       |         | The years time to calculate the delay from now                              |
| title                      | no       |         |         | A title that is just reported on the output to be stored in kalliope memory                     |


## Return Values

| Name             | Description                                                                           | Type     | sample   |
| ---------------- | ------------------------------------------------------------------------------------- | -------- | -------- |
| action           | A copy of the input 'Action' parameter                                                | string   |          |
| timer_hours      | Report the date/time after the input delay (timer = now()+sec/min/hour                | interger |          |
| timer_minutes    |  Report the date/time after the input delay (timer = now()+sec/min/hour               | interger |          |
| timer_seconds    |  Report the date/time after the input delay (timer = now()+sec/min/hour               | interger |          |
| timer_months     |  Report the date/time after the input delay (timer = now()+sec/min/hour               | interger |          |
| timer_day_months |  Report the date/time after the input delay (timer = now()+sec/min/hour               | interger |          |
| timer_years      |  Report the date/time after the input delay (timer = now()+sec/min/hour               | interger |          |
| param_hours      | Same value than the input parameter "hours", to be stored in kalliope memory          | interger |          |
| param_minutes    | Same value than the input parameter "minutes", to be stored in kalliope memory        | interger |          |
| param_seconds    | Same value than the input parameter "seconds", to be stored in kalliope memory        | interger |          |
| param_title      | Same value than the input parameter "title", to be stored in kalliope memory          | string   |          |


## Synapses example

This synapse will calculate the time when the timer will expire
```
---
- name: "simple-timer-heur-and-min-and-sec"     
  signals:
    - order: 
        text: "timer de {{ egg_time_heur }} heure {{ egg_time_min }} minute et {{ egg_time_sec }} seconde"
  neurons:
    - timenow:
        action: "create"
        seconds: "{{ egg_time_sec }}"
        minutes: "{{ egg_time_min }}"
        hours: "{{ egg_time_heur }}"
        kalliope_memory:
          timer_seconds: "{{timer_seconds}}"
          timer_minutes: "{{timer_minutes}}"
          timer_hours: "{{timer_hours}}"
          timer_days: "{{timer_day_months}}"
          timer_months: "{{timer_months}}"
          timer_years: "{{timer_years}}"
          timer_title: "{{param_title}}"
          passed_hours: "{{param_hours}}"
          passed_minutes: "{{param_minutes}}"
          passed_seconds: "{{param_seconds}}"
    - neurotimer:
        seconds: "{{ egg_time_sec }}"
        minutes: "{{ egg_time_min }}"
        hours: "{{ egg_time_heur }}"
        synapse: "notifytimer"
        forwarded_parameters:
          egg_time_sec: "{{ egg_time_sec }}"
          egg_time_min: "{{ egg_time_min }}"
          egg_time_heur: "{{ egg_time_heur }}"
    - say:
        message:
          - "OK, je vous recontacte dans {{ egg_time_heur }} heures {{ egg_time_min }} minutes et {{ egg_time_sec }} secondes"

- name: "notifytimer"
  signals:
     - order: "no-order-for-this-synapse"
  neurons:
    - say:
        file_template : "templates/egg_timer.j2"
```

## Template example

```
le taïmeur de 
{% if kalliope_memory['passed_hours'] != "0" -%}
    {% if kalliope_memory['passed_hours'] == "1" -%}
        une heure
    {% else %}
        {{ kalliope_memory['passed_hours'] }} heure 
    {% endif %}
{% endif %}
{% if kalliope_memory['passed_minutes'] != "0" -%}
    {% if kalliope_memory['passed_minutes'] == "1" -%}
        une minute 
    {% else %}
        {{ kalliope_memory['passed_minutes'] }} minute 
    {% endif %}
{% endif %}
{% if kalliope_memory['passed_seconds'] != "0" -%}
    {% if kalliope_memory['passed_seconds'] == "1" -%}
        une seconde 
    {% else %}
        {{ kalliope_memory['passed_seconds'] }} seconde 
    {% endif %}
{% endif %}
est terminé
```
