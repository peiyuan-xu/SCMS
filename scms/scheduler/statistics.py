#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuangxu
@email: zhuangxu0@gmail.com
@time: 2018/10/7 11:43
@desc:
"""

from threading import Timer
import time

from scms.common import constants as con
from scms.db.api import QueueMessageDao
from scms.scheduler.gather_messages import GatherMessages


def gather_message_count():
    gather_message.get_message_count_in_queues()


def add_message_count_to_db(queue_length_dict={}):
    for key, value in queue_length_dict.items():
        key_list = key.split('_')
        chain_name = key_list[0]
        service_name = key_list[1]
        queue_message_dao.create_queue_message(service_name, chain_name, value)


old_all_zero_stage = True


def loop_gather_message_count():
    # gathering message queues length
    queue_length_dict = gather_message.get_message_count_in_queues()

    # get the time
    new_all_zero_stage = True
    for key, value in queue_length_dict.items():
        if value > 0:
            new_all_zero_stage = False

    global old_all_zero_stage
    if old_all_zero_stage != new_all_zero_stage:
        old_all_zero_stage = new_all_zero_stage
        t = time.localtime()
        t_start = time.strftime(con.TIME_FORMAT, t)
        if new_all_zero_stage:
            print("No message, time: ", t_start)
        else:
            print("Have message, time: ", t_start)

    # add queue length to db
    add_message_count_to_db(queue_length_dict)
    t = time.localtime()
    t_end = time.strftime(con.TIME_FORMAT, t)
    # print("Gathering End ", t_end, "Start time is ", t_start)

    Timer(con.GATHER_TIME_INTERVAL, loop_gather_message_count, ()) \
        .start()


gather_message = GatherMessages()
queue_message_dao = QueueMessageDao()
t_gather_start = time.localtime()
t_gather_start = time.strftime(con.TIME_FORMAT, t_gather_start)
print("Start thread of gathering message's count, time : ", t_gather_start)
Timer(con.SCALING_TIME_INTERVAL, loop_gather_message_count, ()).start()
