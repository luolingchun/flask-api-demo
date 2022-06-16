# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2021/5/18 9:27
import time


def job_test(a: int, b: int, job_id: str):
    print(f'test job {job_id}...')
    time.sleep(30)
    return a + b
