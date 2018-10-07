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
from scms.gatherer.gather_messages import GatherMessages


def gather_message_count():
    gather_message.get_message_count_in_queues()


def add_message_count_to_db():
    for key, value in gather_message.queues_mess_count_dict.items():
        key_list = key.split('_')
        service_name = key_list[0]
        chain_name = key_list[1]
        queue_message_dao.create_queue_message(service_name, chain_name, value)


def loop_gather_message_count():
    # gathering message count
    t = time.localtime()
    t_start = time.strftime(con.TIME_FORMAT, t)
    print("Start time ", t_start)
    gather_message_count()
    add_message_count_to_db()
    t = time.localtime()
    t_end = time.strftime(con.TIME_FORMAT, t)
    print("Gathering End ", t_end, "Start time is ", t_start)

    Timer(con.GATHER_TIME_INTERVAL, loop_gather_message_count, ()) \
        .start()


gather_message = GatherMessages()
queue_message_dao = QueueMessageDao()
t_gather_start = time.localtime()
t_gather_start = time.strftime(con.TIME_FORMAT, t_gather_start)
print("Start thread of gathering message's count, time : ", t_gather_start)
Timer(3, loop_gather_message_count, ()).start()
