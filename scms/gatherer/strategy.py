#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhuangxu
@email: zhuangxu0@gmail.com
@time: 2019/1/7 11:16
@desc:
"""
from threading import Timer
import time

import numpy as np

from scms.common import constants as con
from scms.db.api import QueueMessageDao
from scms.gatherer.gather_messages import GatherMessages
from scms.zun_gw.zun_handle import ZunHandle

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

    return pre_mean > raw_data_list[-1]


def loop_auto_scaling_container():
    # auto scaling
    page_size = 10
    queue_length_dict = gather_message.get_message_count_in_queues()
    for key, value in queue_length_dict.items():
        # auto scaling every type of service
        key_list = key.split('_')
        service_name = key_list[0]
        chain_name = key_list[1]
        queue_length_list = queue_message_dao.list_message_by_chain_and_service(
            service_name, chain_name, page_size)
        if queue_length_list:
            need_scaling = forecast(queue_length_list)
            if need_scaling:
                # call zun gateway to add new container
                pass



    Timer(con.SCALING_TIME_INTERVAL, loop_auto_scaling_container, ()) \
        .start()


gather_message = GatherMessages()
queue_message_dao = QueueMessageDao()

# if __name__ == '__main__':
#     raw_data_list = [1,2,6,8,10,9,7]
#     forecast(raw_data_list)