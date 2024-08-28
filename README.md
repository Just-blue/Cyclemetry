## Forked from Original Repository

This project is a fork of [cyclemetry](https://github.com/walkersutton/cyclemetry) by [walkersutton](https://github.com/walkersutton). The original project was designed to generate GPX video overlays。

## Modifications in This Fork

The following changes have been made in this fork:
- Added Shimano di2 Gear display for monitoring gear shifts during rides.
- Adapted grad feature for climbing, including dynamic adjustments based on the gradient.
- Added distance display for tracking total distance covered.
- Modified the input file format to support FIT files.


## Cyclemetry - generate Fit video overlays
![The_Tremola_by Safa_Brian](https://github.com/walkersutton/cyclemetry/assets/25811783/71aa4902-dd29-453f-b4a5-a87ddabd2437)

## Features
* Live course tracking
* Live elevation profile
* Cadence, elevation, gradient, heartrate, power, speed, etc.
* Supports imperial and metric units

## Running
```sh
(venv) $ python main.py <gpx_file> <template_filename>
```

## Templates
(featured image on readme)
* [modified version](templates/temp_4k.json)
* [Safa Brian A](https://github.com/walkersutton/cyclemetry/blob/main/templates/safa_brian_a.json) 

### Designing Templates - UNDER DEVELOPMENT
[Template Designer](https://walkersutton.com/cyclemetry/)

## Dependencies
* [ffmpeg](https://FFmpeg.org/)

## Setup
Tested using Python 3.11.4 and 3.11.6 on MacOS Ventura and MacOS Sonoma

**Not working on Python 3.12.0 (distutils dependency issue)**

```sh
$ git clone https://github.com/walkersutton/cyclemetry.git
$ cd cyclemetry
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

## How to

I need to make Cyclemetry a bit easier to use. [Here's a video](https://youtu.be/gqn5MfcypH4) where I explain how I'm currently using the tool. I plan on writing a more concise user guide in the coming weeks.

## Alternate Tools
* [DashWare](http://www.dashware.net/) (only available on Windows)
* [Garmin VIRB Edit](https://www.garmin.com/en-US/p/573412)
* [GoPro Telemetry Extractor](https://goprotelemetryextractor.com/) ($150/$300? - fuck that)

## Contributors
* All contributions are welcome
* Feel free to [submit your templates](https://github.com/walkersutton/cyclemetry/pulls) for others to use
