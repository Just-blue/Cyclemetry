import subprocess
import sys
import argparse
import constant
from activity import Activity
from scene import Scene


def get_start_end(scene_conf, activity):
    if "start_time" in scene_conf and "end_time" in scene_conf:
        print(
            f"get start from {scene_conf['start_time']},get end from {scene_conf['end_time']}. "
        )
        start_time, end_time = scene_conf["start_time"], scene_conf["end_time"]
        start, end = activity.sth(start_time, end_time)
    else:
        start, end = scene_conf["start"], scene_conf["end"]

    print(f"start:{start} end:{end}")
    return start, end


def render_overlay(gpx_filename, template_filename):
    activity = Activity(gpx_filename)
    scene = Scene(activity, activity.valid_attributes, template_filename)
    start, end = get_start_end(scene.template["scene"], activity)
    activity.trim(start, end)
    activity.interpolate(scene.fps)
    scene.build_figures()
    scene.render_video(end - start)


def demo_frame(gpx_filename, template_filename, second):
    activity = Activity(gpx_filename)
    scene = Scene(activity, activity.valid_attributes, template_filename)
    start, end = get_start_end(scene.template["scene"], activity)
    activity.trim(start, end)
    activity.interpolate(scene.fps)
    scene.build_figures()
    scene.render_demo(end - start, second)
    print(scene.frames[0].full_path())
    # subprocess.call(["open", scene.frames[0].full_path()])
    return scene


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Render overlay using GPX and JSON template"
    )
    parser.add_argument("--gpx", type=str, required=True, help="Path to the GPX file")
    parser.add_argument(
        "--template", type=str, required=True, help="JSON template filename"
    )
    parser.add_argument("--demo", action="store_true", help="Run in demo mode")
    parser.add_argument(
        "--second", type=int, default=0, help="Second to start demo from"
    )
    args = parser.parse_args()

    if args.demo:
        while True:
            print(
                f"demoing frame using the {args.template} template and {args.gpx} gpx file"
            )
            scene = demo_frame(args.gpx, args.template, args.second)
            input("Enter to re-render:")
            scene.update_configs(args.template)
    else:
        print(
            f"rendering overlay using the {args.template} template and {args.gpx} gpx file"
        )
        render_overlay(args.gpx, args.template)
