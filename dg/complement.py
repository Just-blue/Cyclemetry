import numpy as np
from matplotlib import pyplot as plt


# 线性插值函数
def linear_interpolate(x, x0, x1, y0, y1):
    return y0 + ((x - x0) * (y1 - y0) / (x1 - x0))


# 定义一个函数来计算移动平均值
def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size), "valid") / window_size


def liner_fixed(heart_rate_values, threshold, start_index, end_index):
    # 找出非异常值的索引
    valid_indices = [
        i
        for i, hr in enumerate(heart_rate_values)
        if hr >= threshold and i > start_index and i < end_index
    ]

    # 遍历异常值，进行线性插值
    for i in range(len(heart_rate_values)):
        if (
            heart_rate_values[i] < threshold and i > start_index and i < end_index
        ):  # 假设低于100的心率值是异常的
            # 找到异常值前后的非异常值索引
            prev_index = next((j for j in valid_indices if j < i), None)
            next_index = next((j for j in valid_indices if j > i), None)

            if prev_index is not None and next_index is not None:
                # 执行线性插值
                heart_rate_values[i] = linear_interpolate(
                    i,
                    prev_index,
                    next_index,
                    heart_rate_values[prev_index],
                    heart_rate_values[next_index],
                )


def move_avg(heart_rate_values, threshold, start_index, end_index):

    # 计算移动平均的窗口大小，这里我们使用3，意味着每个点将由它自己和前后两个点的平均值来计算
    window_size = 25

    # 计算移动平均值
    averaged_data = moving_average(heart_rate_values, window_size)

    # 由于移动平均会减少数据点的数量，我们需要补全数据列表以匹配原始数据长度
    padded_data = np.pad(heart_rate_values, (window_size - 1, 0), mode="edge")[
        : -window_size + 1
    ]

    # 用移动平均值替换原始数据中的异常值
    for i in range(start_index, end_index):
        if heart_rate_values[i] < threshold:  # 假设低于100的心率值是异常的
            heart_rate_values[i] = round(averaged_data[i])


def fixed(h_data: list):
    threshold = 180
    start_index = 5050
    end_index = 6376

    print(
        f"to fix heartrate {sum(h_data)},threshold:{threshold}, start_index:{start_index}, end_index:{end_index}"
    )
    heart_rate_values = np.array(h_data)
    liner_fixed(heart_rate_values, threshold, start_index, end_index)
    move_avg(heart_rate_values, threshold, start_index, end_index)
    print(f"fixed heartrate {sum(heart_rate_values)}")
    # plt.plot(heart_rate_values)
    return heart_rate_values
