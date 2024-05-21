import io
from pathlib import Path

import matplotlib.axes as ax
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from constant import FONTS_DIR
from utils import printc


def build_gear(
    config,
    front_gear,
    rear_gear,
):

    fig, ax = plt.subplots()
    if "width" and "height" in config.keys():
        padding = 200
        fig, ax = plt.subplots(
            figsize=(
                (config["width"] + padding) / config["dpi"],
                (config["height"] + padding) / config["dpi"],
            )
        )
    plt.rcParams["lines.linewidth"] = config["line_width"]
    plt.axis("off")

    # 计算柱状图的宽度以增加间隙

    bar_width = config["r_bar_width"]  # 减小这个值可以增加间隙
    bar_gap = (1 - bar_width) / 2  # 计算间隙的大小

    # 从左到右绘制齿比的柱状图
    for i, ratio in enumerate(rear_gear):
        # 添加间隙：通过调整x位置和减小宽度来实现
        rect = plt.Rectangle(
            (i + bar_gap, (max(rear_gear) - ratio) / 2),
            bar_width,
            ratio,
            linewidth=1,
            edgecolor="black",
            facecolor=config["color"],
            zorder=2,
        )
        rect.tag = "rear"
        ax.add_patch(rect)

    # 绘制牙盘的齿比水平放置在图的顶部
    bar_width = config["f_bar_width"]
    bar_gap = bar_width / 2  # 计算间隙的大小
    y_lim = max(rear_gear) + bar_width * 2 + bar_gap + config["interval"]

    zoom = config["f_zoom"]
    for i, ratio in enumerate(front_gear):
        rect = plt.Rectangle(
            (
                (max(front_gear) - ratio) / zoom / 2,
                y_lim - (i + 1) * bar_width - bar_gap * i,
            ),  # 将牙盘齿比放置在图的顶部
            ratio / zoom,
            bar_width,
            linewidth=1,
            edgecolor="black",
            facecolor=config["color"],
            zorder=2,
        )
        rect.tag = "front"
        ax.add_patch(rect)

    # 隐藏坐标轴
    ax.axis("off")

    # 设置图形的范围，考虑到间隙，可能需要适当调整
    ax.set_xlim(0, len(rear_gear))
    ax.set_ylim(0, y_lim)

    if "reverse" in config and config["reverse"] is True:
        # 反转x轴
        plt.gca().invert_xaxis()

    if "margin" in config.keys():
        ax = plt.gca()
        ax.set_xmargin(config["margin"])
        ax.set_ymargin(config["margin"])

    return fig


def build_figure(config, x, y, ref=None):
    fig = plt.figure()
    if "width" and "height" in config.keys():
        padding = 200
        fig = plt.figure(
            figsize=(
                (config["width"] + padding) / config["dpi"],
                (config["height"] + padding) / config["dpi"],
            )
        )
    plt.rcParams["lines.linewidth"] = config["line_width"]
    plt.axis("off")

    plt.plot(
        x,
        y,
        color=config["color"],
    )

    if "reverse" in config and config["reverse"] is True:
        # 反转x轴
        plt.gca().invert_xaxis()

    if "margin" in config.keys():
        ax = plt.gca()
        ax.set_xmargin(config["margin"])
        ax.set_ymargin(config["margin"])
    if "axis" in config.keys():
        try:
            plt.axis(config["axis"])
        except ValueError as e:
            printc(f"Invalid axis value: {e}", "red")
    if "slope_area" in config.keys() and ref is not None:
        grades = np.array(ref)
        min_threshold = min(y) * 0.99
        y = np.array(y)

        # 根据坡度值填充颜色
        for item in config["slope_area"]:
            plt.fill_between(
                x,
                y,
                min_threshold,
                where=(grades >= item["start"]) & (grades < item["end"]),
                facecolor=config["color"],
                alpha=item["fill_opacity"],
                label=f"{item['start']}% - { item['end']}% Grade",
                linewidth=0,
            )

    return fig


def build_gear_image(fig, config, front_gear, rear_gear, text=""):
    plt.figure(fig.number)
    for rect in fig.axes[0].patches:
        if (rect.tag == "rear" and rect.get_height() == rear_gear) or (
            rect.tag == "front" and rect.get_width() == front_gear / config["f_zoom"]
        ):
            rect.set_facecolor(config["cover_color"])
        else:
            rect.set_facecolor(config["color"])

    # for some reason, faster to create buffer here than to pass as param - also prevents figure duplication issue
    buffer = io.BytesIO()
    plt.savefig(
        buffer,
        bbox_inches=config["bbox"] if "bbox" in config.keys() else None,
        transparent=True,
        dpi=config["dpi"],
    )
    img = Image.open(buffer)

    return img, buffer


def build_image(fig, config, x, y, text=""):
    plt.figure(fig.number)
    fig, points = draw_points(fig, config, x, y)
    fig, labels = draw_labels(fig, config, x, y, text)

    # for some reason, faster to create buffer here than to pass as param - also prevents figure duplication issue
    buffer = io.BytesIO()
    plt.savefig(
        buffer,
        bbox_inches=config["bbox"] if "bbox" in config.keys() else None,
        transparent=True,
        dpi=config["dpi"],
    )
    img = Image.open(buffer)

    # TODO this is significantly faster than the above - need to get alpha channel working
    # fig.canvas.draw()
    # buffer = fig.canvas.tostring_argb()
    # img = Image.frombytes('RGBA', fig.canvas.get_width_height(), buffer)

    for point in points:
        point.remove()
    for label in labels:
        label.remove()
    return img, buffer


def draw_points(fig, config, x, y):
    plt.figure(fig.number)
    points = []
    points.append(
        plt.scatter(  # assuming every profile and course includes point_weight - might want to make this a child property
            x=x,
            y=y,
            color=config["color"],
            s=config["point_weight"],
            zorder=3,
        )
    )
    if "sub_point" in config.keys():
        points.append(
            plt.scatter(
                x=x,
                y=y,
                color=config["sub_point"]["color"],
                s=config["sub_point"]["point_weight"],
                zorder=2,
                alpha=config["sub_point"]["opacity"],
                edgecolor="none",
            )
        )
    return fig, points


def draw_labels(
    fig, config, x, y, text
):  # probably want to make text a list? and iterate through labels?
    plt.figure(fig.number)
    labels = []
    if "point_label" in config.keys():  # rename - label
        labels.append(
            plt.text(
                x + config["point_label"]["x_offset"],
                y + config["point_label"]["y_offset"],
                text,
                fontsize=config["point_label"]["font_size"],
                color=config["point_label"]["color"],
                font=Path(
                    f'{FONTS_DIR}{config["point_label"]["font"]}'
                ),  # TODO - support system fonts? not sure how pyplot deals with this
            )
        )
    return fig, labels
