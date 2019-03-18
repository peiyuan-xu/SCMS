#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuangxu
@email: zhuangxu0@gmail.com
@time: 2019/1/7 11:16
@desc:
"""
from enum import Enum
from threading import Timer
import time

import numpy as np

from scms.common import constants as con
from scms.db.api import ImageDAO
from scms.db.api import InstanceDAO
from scms.db.api import QueueMessageDao
from scms.db import common
from scms.scheduler.gather_messages import GatherMessages
from scms.zun_gw.zun_handle import ZunHandle


class ScalingStatus(Enum):
    Rise = 0
    Decline = 1
    Stable = 2


# 指数平滑公式
def exponential_smoothing(alpha, s):
    s2 = np.zeros(s.shape)
    s2[0] = s[0]
    for i in range(1, len(s2)):
        s2[i] = alpha*s[i]+(1-alpha)*s2[i-1]
    return s2


def forecast(raw_data_list):
    np_data_list = np.array(raw_data_list)
    alpha = 0.70
    s_single = exponential_smoothing(alpha, np_data_list)  # 计算一次指数平滑
    s_double = exponential_smoothing(alpha, s_single)  # 计算二次指数平滑

    a_double = 2 * s_single - s_double  # 计算二次指数平滑的a
    b_double = (alpha / (1 - alpha)) * (s_single - s_double)  # 计算二次指数平滑的b
    # print("一次平滑: " + str(a_double))
    # print("二次平滑：" + str(b_double))

    pre_next_one = a_double[-1] + b_double[-1] * 1  # 预测下一年
    pre_next_two = a_double[-1] + b_double[-1] * 2  # 预测下两年
    pre_mean = (pre_next_one + pre_next_two)/2
    # print("预测值：" + str(pre_next_one) + ", " + str(pre_next_two) + " -> " + str(pre_mean))

    if raw_data_list[-1] == 0:
        return ScalingStatus.Decline
    elif pre_mean > 0 and pre_mean >= raw_data_list[-1]:
        return ScalingStatus.Rise
    else:
        return ScalingStatus.Stable


def auto_add_container(chain_name, service_name):
    image_dao = ImageDAO()
    # image is not null
    image = image_dao.get_last_image_by_service(service_name)
    zun_handle = ZunHandle()
    name = chain_name + service_name + common.generate_uuid()
    image_name = image['image_name']
    command = image['command']

    # command = 'python SCMSServiceDemo/books.py -s 192.168.1.220 -c chain1'
    rabbitMQ_server = '192.168.1.220'
    comm_list = command.split()
    comm_tail = ['-s', rabbitMQ_server, '-c', chain_name]
    comm_list.extend(comm_tail)

    # print('\n Add a new container name: ' + name)
    t_s = int(time.time()*1000)
    res = zun_handle.create_and_start_container(name=name,
                                                image=image_name,
                                                command=comm_list)
    # print(res)
    t_e = int(time.time()*1000)
    p_dict = {'tag': 'add', 'chain': chain_name, 'service': service_name, 'start_t': t_s, 'end_t': t_e}
    print(str(p_dict) + ',')
    # add a instance
    instance_dao = InstanceDAO()
    instance = instance_dao.create_instance(service_name, image['id'], chain_name, res['uuid'])
    # print(instance)


def auto_delete_container(chain_name, service_name):
    # delete a container
    instance_dao = InstanceDAO()
    container_runing = instance_dao.list_instance_by_service_and_chain(service_name, chain_name)
    zun_handle = ZunHandle()
    if container_runing:
        delete_uuid = container_runing[0]['container_id']

        t_s = int(time.time() * 1000)
        zun_handle.stop_and_delete_container(delete_uuid)
        t_e = int(time.time() * 1000)
        p_dict = {'tag': 'delete', 'chain': chain_name, 'service': service_name, 'start_t': t_s, 'end_t': t_e}
        print(str(p_dict) + ',')
        # print('Delete a Container success, uuid: ' + delete_uuid)
        instance_dao.delete_instance_by_instanceid(container_runing[0]['container_id'])


def loop_auto_scaling_container():
    # auto scaling
    MAX_INSTANCE_NUM_OF_EACH_SERVICE = 6
    page_size = 10
    queue_length_dict = gather_message.get_message_count_in_queues()
    for key, value in queue_length_dict.items():
        # auto scaling every type of service
        key_list = key.split('_')
        chain_name = key_list[0]
        service_name = key_list[1]
        if service_name == 'gw':
            continue

        queue_length_list = queue_message_dao.list_message_by_chain_and_service(
            service_name, chain_name, page_size)
        if queue_length_list:
            queue_length_data_list = [queue.message_number for queue in queue_length_list]
            queue_length_data_list.reverse()
            scaling_status = forecast(queue_length_data_list)
            # print('chain: ' + chain_name + '  service: ' + service_name + '  queue length')
            # print(queue_length_data_list)
            if scaling_status == ScalingStatus.Rise:
                instance_dao = InstanceDAO()
                achieve_max_num = instance_dao.get_instance_num_by_service(service_name)
                if achieve_max_num == MAX_INSTANCE_NUM_OF_EACH_SERVICE:
                    pass
                else:
                    #print('---Add a container---')
                    # call zun gateway to add new container
                    auto_add_container(chain_name, service_name)
            elif scaling_status == ScalingStatus.Decline:
                # delete a container
                #print('---Delete a container---')
                auto_delete_container(chain_name, service_name)

    Timer(con.SCALING_TIME_INTERVAL, loop_auto_scaling_container, ()) \
        .start()


gather_message = GatherMessages()
queue_message_dao = QueueMessageDao()
t_auto_start = time.localtime()
t_gather_start = time.strftime(con.TIME_FORMAT, t_auto_start)
print("Start auto scaling, time : ", t_gather_start)
Timer(con.SCALING_TIME_INTERVAL, loop_auto_scaling_container, ()).start()
