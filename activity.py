import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from collections import defaultdict

import constant
from gradient import smooth_gradients
from fitparse import FitFile
import datetime


class Activity:
    def __init__(self, filename):
        self.fitfile = FitFile(filename)
        self.valid_attributes = set()
        self.set_valid_attributes()
        self.parse_data()

    def set_valid_attributes(self):
        records = []

        # 遍历FIT文件中的所有记录
        for record in self.fitfile.get_messages("record"):
            record_data = {}
            for data in record:
                record_data[data.name] = data.value
            records.append(record_data)

        # 创建DataFrame
        df = pd.DataFrame(records)

        # 选择需要的列并设置索引
        df = df[
            [
                "timestamp",
                "power",
                "altitude",
                "position_lat",
                "position_long",
                "cadence",
                "temperature",
                "grade",
                "speed",
                "heart_rate",
            ]
        ]
        df["timestamp"] = (
            pd.to_datetime(df["timestamp"])
            .dt.tz_localize("UTC")
            .dt.tz_convert("Asia/Shanghai")
            .dt.tz_localize(None)
        )

        df.set_index("timestamp", inplace=True, drop=False)

        # # 对每列缺失的数据进行补数
        df["power"] = df["power"].interpolate(method="linear")
        df["cadence"] = df["cadence"].interpolate(method="linear")
        df["temperature"] = df["temperature"].interpolate(method="linear")
        df["speed"] = df["speed"].interpolate(method="linear")
        df["heart_rate"] = df["heart_rate"].interpolate(method="linear")
        df.fillna(method="ffill", inplace=True)  # 前向填充
        df.fillna(method="bfill", inplace=True)  # 后向填充
        df["course"] = list(zip(df["position_lat"], df["position_long"]))
        df.rename(
            columns={
                "altitude": constant.ATTR_ELEVATION,
                "grade": constant.ATTR_GRADIENT,
                "heart_rate": constant.ATTR_HEARTRATE,
                "timestamp": constant.ATTR_TIME,
            },
            inplace=True,
        )
        self.df = df

    def parse_data(self):
        data = defaultdict(list)
        for attribute in self.df.columns:
            match attribute:
                case (
                    constant.ATTR_CADENCE
                    | constant.ATTR_HEARTRATE
                    | constant.ATTR_POWER
                    | constant.ATTR_TEMPERATURE
                    | constant.ATTR_GRADIENT
                    | constant.ATTR_SPEED
                    | constant.ATTR_ELEVATION
                    | constant.ATTR_COURSE
                    | constant.ATTR_TIME
                ):
                    data[attribute] = self.df[attribute].tolist()
                    self.valid_attributes.add(attribute)

        for attribute in self.valid_attributes:
            if attribute == constant.ATTR_GRADIENT:
                data[attribute] = smooth_gradients(data[attribute])
            setattr(self, attribute, data[attribute])

    def interpolate(self, fps: int):
        def helper(data):
            data.append(2 * data[-1] - data[-2])
            x = np.arange(len(data))
            interp_func = interp1d(x, data)
            new_x = np.arange(x[0], x[-1], 1 / fps)
            return interp_func(new_x).tolist()

        for attribute in self.valid_attributes:
            if attribute in constant.NO_INTERPOLATE_ATTRIBUTES:
                continue
            data = getattr(self, attribute)
            if attribute == constant.ATTR_COURSE:
                new_lat = helper([ele[0] for ele in data])
                new_lon = helper([ele[1] for ele in data])
                new_data = list(zip(new_lat, new_lon))
            else:
                new_data = helper(data)
            setattr(self, attribute, new_data)

    def trim(self, start, end):
        for attribute in self.valid_attributes:
            data = getattr(self, attribute)
            if start > len(data):
                print(
                    f"invalid scene start value in config. Value should be less than {len(data)}. Current value is {start}"
                )
                exit(1)
            if end > len(data) or end < start:
                print(
                    f"invalid scene end value in config. Value should be less than {len(data)} and greater than {start}. Current value is {end}"
                )
                exit(1)
            setattr(self, attribute, data[start:end])

    def sth(self, start_time, end_time):
        """_summary_

        Args:
            start_time (_type_): _description_  2024-05-15 07:12:37
            end_time (_type_): _description_  2024-05-15 07:26:04

        Returns:
            _type_: _description_
        """

        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

        start = self.time.index(start_time)
        end = self.time.index(end_time)
        return start, end
