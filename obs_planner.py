#!/usr/bin/env python

import ephem
import numpy as np
from matplotlib import pyplot as plt
import argparse
from mpl_toolkits.mplot3d import Axes3D
import datetime

parser = argparse.ArgumentParser(description="Observation Planner")
parser.add_argument("--lat",
                    type=str,
                    default="-30:42:47.41",
                    help="Observer Latitude")
parser.add_argument("--long",
                    type=str,
                    default="21:26:38.0",
                    help="Observer Longitude")
parser.add_argument("--elev",
                    type=float,
                    default=1054,
                    help="Observer Elevation")
parser.add_argument("-s",
                    "--start",
                    type=str,
                    default="2017/3/21 08:00:00",
                    help="Observation start time local")
parser.add_argument("-e",
                    "--end",
                    type=str,
                    default="2017/3/21 20:00:00",
                    help="Observation end time local")
parser.add_argument("sources", metavar="src", type=str, nargs="+",
                    help="Sources to plot")

args = parser.parse_args()
meerkat = ephem.Observer()

# Set the observer at the Karoo
meerkat.lat, meerkat.long, meerkat.elevation = args.lat, args.long, args.elev
print "Observer at (lat, long, alt): (%s, %s, %s)" % (meerkat.lat, meerkat.long, meerkat.elevation)
meerkat.epoch = ephem.J2000

scp = ephem.readdb("SCP,f|J,00:00:00.00000,-90:00:00:00000,0.0")

sources = {"Sun": ephem.Sun(),
           "DEEP2": ephem.readdb("DEEP_2,f|J,04:13:26.40,-80.00.00.00000,0.0"),
           "0252-712": ephem.readdb("0252-712,f|J,02:52:46.15,-71.04.35.30,0.0"),
           "0408-65": ephem.readdb("0408-65,f|J,04:08:20:38,-65.45.09.10,0.0"),
           "PKS 1934-638":
           ephem.readdb("custom,f|J,19:39:25:00,-63.42.46.00,0.0"),
           "PKS 1934-638": ephem.readdb("custom,f|J,19:39:25:00,-63.42.46.00,0.0"),
           "3C286": ephem.readdb("custom,f|J,13:31:08.3,30:30:33,0.0"),
           "3C138": ephem.readdb("custom,f|J,05:21:09,16:38:22,0.0"),
           "PKS 1422-29": ephem.readdb("custom,f|J,14:25:30:00,-30.00.00.00,0.0"),
           "alleged ghost": ephem.readdb("custom,f|J,14:25:30:00,30.00.00.00,0.0"),
           "1244-255": ephem.readdb("custom,f|J,12:46:46:80,-25:47:49:3,0.0"),
           "1334-127": ephem.readdb("custom,f|J,13:37:39:78,-12:57:24:7,0.0"),
           "NGC4993_off": ephem.readdb("custom,f|J,13:09:21:00,-23:31:24:0,0.0"),
           "3C283": ephem.readdb("custom,f|J,13:11:40:10,-22:17:04:0,0.0"),
          }
positions = {"Sun": [],
             "DEEP2": [],
             "0252-712": [],
             "0408-65": [],
             "PKS 1934-638": [],
             "3C286": [],
             "3C138": [],
             "PKS 1422-29": [],
             "alleged ghost": [],
             "1244-255": [],
             "1334-127": [],
             "NGC4993_off": [],
             "3C283": []
            }

pi = np.pi
r2d = 180.0/pi
d2r = pi/180.0

r2h = 12.0/pi
h2r = pi/12.0

meerkat.date = args.start
st = meerkat.date
print "Observation start: UTC %s (LST %s = %f)" % (meerkat.date,
                                                   meerkat.sidereal_time(),
                                                   meerkat.sidereal_time()*r2h)
scp.compute(meerkat)
meerkat.date = args.end
et = meerkat.date
print "Observation end: UTC %s (LST %s = %f)" % (meerkat.date,
                                                 meerkat.sidereal_time(),
                                                 meerkat.sidereal_time()*r2h)

scppos = (scp.az, np.pi/2 - scp.alt)
for t in np.linspace(st,et,1500):
    meerkat.date = t
    for k in sources:
        sources[k].compute(meerkat)
        if k == "Sun":
            print sources[k].ra, sources[k].dec
        positions[k].append([float(sources[k].az),
                             float(np.pi * 0.5 - sources[k].alt)])

for k in sources:
    positions[k] = np.rad2deg(np.array(positions[k]))

fig = plt.figure("Observation Planner")
ax = fig.add_subplot(111, projection="3d")
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi/2:10j]
x = np.cos(u)*np.sin(v)
y = np.sin(u)*np.sin(v)
z = np.cos(v)
ax.plot_wireframe(x, y, z, color="0.75")
ax.plot([np.sin(scppos[1])*np.cos(scppos[0])],
        [np.sin(scppos[1])*np.sin(scppos[0])],
        [np.cos(scppos[1])], "k*")

for s in args.sources:
    elv_s = 90 - positions[s][0,1]
    az_s = positions[s][0,0]
    elv_e = 90 - positions[s][-1,1]
    az_e = positions[s][-1,0]

    print "%s: Starting (elevation, azimuth): (%f,%f)" % (s, elv_s, az_s)
    print "%s: Ending (elevation, azimuth): (%f,%f)" % (s, elv_e, az_e)

    ax.plot([np.sin(np.deg2rad(positions[s][0,1]))*np.cos(np.deg2rad(positions[s][0,0]))],
            [np.sin(np.deg2rad(positions[s][0,1]))*np.sin(np.deg2rad(positions[s][0,0]))],
            [np.cos(np.deg2rad(positions[s][0,1]))], "k^")
    ax.plot([np.sin(np.deg2rad(positions[s][-1,1]))*np.cos(np.deg2rad(positions[s][-1,0]))],
            [np.sin(np.deg2rad(positions[s][-1,1]))*np.sin(np.deg2rad(positions[s][-1,0]))],
            [np.cos(np.deg2rad(positions[s][-1,1]))], "kv")
    ax.plot(np.sin(np.deg2rad(positions[s][:,1]))*np.cos(np.deg2rad(positions[s][:,0])),
            np.sin(np.deg2rad(positions[s][:,1]))*np.sin(np.deg2rad(positions[s][:,0])),
            np.cos(np.deg2rad(positions[s][:,1])), label=s)
ax.legend()
ax.grid(False)
ax.set_xlim(-1,1)
ax.set_ylim(-1,1)
ax.set_zlim(-1,1)
plt.show()
