#!/usr/bin/env python

import ephem
import numpy as np
from matplotlib import pyplot as plt
import argparse
from mpl_toolkits.mplot3d import Axes3D
import datetime
import matplotlib.dates as mdates

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
parser.add_argument("--elev-cutoff",
                    type=float,
                    default=-90,
                    help="Elevation cutoff")
parser.add_argument("sources", metavar="src", type=str, nargs="+",
                    help="Sources to plot")
parser.add_argument("--solar-separation",
                    type=float,
                    default=15,
                    help="Minimum solar separation")

parser.add_argument("--lunar-separation",
                    type=float,
                    default=0.75,
                    help="Minimum lunar separation")

parser.add_argument("--plot-styles",
                    type=str,
                    default=["k*-", "k^-", "kv-", "kx-", "k<-", "k>-", "kD-",
                             "k|-", "k_-", "kp-"],
                    nargs="+",
                    help="Plot style")
parser.add_argument("--marker-size",
                    type=float,
                    default="6.0",
                    help="Marker size")

args = parser.parse_args()
if len(args.plot_styles) < len(args.sources):
    raise ValueError("Not enough plot styles defined for the number of sources to be plotted")
meerkat = ephem.Observer()

# Set the observer at the Karoo
meerkat.lat, meerkat.long, meerkat.elevation = args.lat, args.long, args.elev
print "Observer at (lat, long, alt): (%s, %s, %s)" % (meerkat.lat, meerkat.long, meerkat.elevation)
meerkat.epoch = ephem.J2000
 
scp = ephem.readdb("SCP,f|J,00:00:00.00000,-90:00:00:00000,0.0")

sources = {"Sun": ephem.Sun(),
           "Moon": ephem.Moon(),
           "DEEP2": ephem.readdb("DEEP_2,f|J,04:13:26.40,-80.00.00.00000,0.0"),
           "0252-712": ephem.readdb("0252-712,f|J,02:52:46.15,-71.04.35.30,0.0"),
           "0408-65": ephem.readdb("0408-65,f|J,04:08:20:38,-65.45.09.10,0.0"),
           "PKS 0407-65": ephem.readdb("0408-65,f|J,04:08:20:38,-65.45.09.10,0.0"),
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
           "A781": ephem.readdb("custom,f|J,09:20:25:00,+30:30:11:0,0.0"),
           "RXCJ 1638.2-6420":ephem.readdb("custom,f|J,16:38:18:00,-64:21:07:0,0.0"),
           "RXCJ 1631.6-7507":ephem.readdb("custom,f|J,16:31:24:00,-75:07:01:0,0.0"),
           "PSZ1G 018.75+23.5":ephem.readdb("custom,f|J,17:02:22:00,-01:00:16:0,0.0"),
           "A1300":ephem.readdb("custom,f|J,11:31:54,-19:55:42,0.0"),
           "1854-663":ephem.readdb("custom,f|J,18:59:57:00,-66:15:03:0,0.0"),
           "1607-841":ephem.readdb("custom,f|J,16:19:33:00,-84:18:19:0,0.0"),
           "1722-554":ephem.readdb("custom,f|J,17:26:49:00,-55:29:38:0,0.0"),
           "2210-016":ephem.readdb("custom,f|J,22:12:38,+01:37:05:0,0.0"),
           "1548+056":ephem.readdb("custom,f|J,15:50:35,+05:27:11:0,0.0"),
           "CTD93":ephem.readdb("custom,f|J,16:09:13:00,+26:41:29:0,0.0"),
           "1139-285":ephem.readdb("custom,f|J,11:41:35,-28:50:52:00,0.0"),
           "MACSJ 1931-2635":ephem.readdb("custom,f|J,19:31:49,-26:34:34,0.0"),
           "1948-277":ephem.readdb("custom,f|J,19:51:23:00,-27:37:20:00,0.0"),
           "1936-155":ephem.readdb("custom,f|J,19:39:26.657740,-15:25:43.058320,0.0"),
           "0408+085":ephem.readdb("custom,f|J,04:11:33.8575,+08:48:11.408,0.0"),
           "0000+177":ephem.readdb("custom,f|J,00:03:21.10,-17:27:11.78,0.0"),
           "PSZ2G277.76-51.74":ephem.readdb("custom,f|J,02:54:17.5,-58:57:10.8,0.0"),
           "PSZ2G254.08-58.45":ephem.readdb("custom,f|J,03:04:16.8,-44:01:51.6,0.0"),
           "PSZ2G255.60-46.18":ephem.readdb("custom,f|J,04:11:15.5,-48:19:19.2,0.0")
          }
positions = {k: [] for k in sources}
pa = {k: [] for k in sources}

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
time = np.linspace(st,et,1500)
times_above = {k: [] for k in sources}
times_interference = {k: [] for k in sources}
positions_interference = {k: [] for k in sources}
pa_interference = {k: [] for k in sources}
sidereals = {k: [] for k in sources}

for t in time:
    meerkat.date = t
    for k in sources:
        sources["Sun"].compute(meerkat)
        sun_coord = np.asarray([sources["Sun"].az, sources["Sun"].alt],
                               dtype=np.float64)
        sources["Moon"].compute(meerkat)
        moon_coord = np.asarray([sources["Moon"].az, sources["Moon"].alt],
                               dtype=np.float64)

        sources[k].compute(meerkat)
        src_coord = np.asarray([sources[k].az, sources[k].alt],
                               dtype=np.float64)
        dot_src_sun = np.arccos(np.dot(sun_coord, src_coord) /
                                np.sqrt(np.sum(sun_coord**2)) /
                                np.sqrt(np.sum(src_coord**2)))
        dot_src_moon = np.arccos(np.dot(moon_coord, src_coord) /
                                 np.sqrt(np.sum(moon_coord**2)) /
                                 np.sqrt(np.sum(src_coord**2)))

        if sources[k].alt > np.deg2rad(args.elev_cutoff) and \
           dot_src_sun > np.deg2rad(args.solar_separation) and \
           dot_src_moon > np.deg2rad(args.lunar_separation):
            positions[k].append([float(sources[k].az),
                                 float(np.pi * 0.5 - sources[k].alt)])
            pa[k].append(sources[k].parallactic_angle())
            times_above[k].append(t)
            sidereals[k].append(meerkat.sidereal_time())

        else:
            if dot_src_sun <= np.deg2rad(args.solar_separation) and k in args.sources and sources[k].alt > np.deg2rad(args.elev_cutoff):
                print "WARNING: {0:s} experiences solar interference at {1:s}".format(k, str(ephem.Date(t).datetime()))
                times_interference[k].append(t)
                pa_interference[k].append(sources[k].parallactic_angle())
                positions_interference[k].append([float(sources[k].az),
                                                  float(np.pi * 0.5 - sources[k].alt)])

            if dot_src_moon <= np.deg2rad(args.lunar_separation) and k in args.sources and sources[k].alt > np.deg2rad(args.elev_cutoff):
                print "WARNING: {0:s} is behind the moon lunar at {1:s}".format(k, str(ephem.Date(t).datetime()))
                times_interference[k].append(t)
                pa_interference[k].append(sources[k].parallactic_angle())
                positions_interference[k].append([float(sources[k].az),
                                                  float(np.pi * 0.5 - sources[k].alt)])


            times_above[k].append(np.nan)
            positions[k].append([np.nan, np.nan])
            pa[k].append(np.nan)
            sidereals[k].append(np.nan)

for k in sources:
    positions[k] = np.rad2deg(np.array(positions[k]))
    positions_interference[k] = np.rad2deg(np.array(positions_interference[k]))

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

for si, s in enumerate(args.sources):
    elv_s = 90 - positions[s][0,1]
    az_s = positions[s][0,0]
    elv_e = 90 - positions[s][-1,1]
    az_e = positions[s][-1,0]

    if len(np.where(np.logical_not(np.isnan(positions[s][:,0])))[0]) == 0:
        print "{0:s} is never above elevation limit!".format(s)
        continue
    else:
        print "%s: Starting (elevation, azimuth): (%f,%f)" % (s, elv_s, az_s)
        print "%s: Ending (elevation, azimuth): (%f,%f)" % (s, elv_e, az_e)
        print "%s: Minimum (elevation, azimuth): (%f, %f)" % (s,
                                                              90 - np.nanmax(positions[s][:,1]),
                                                              np.nanmin(positions[s][:,0]))
        print "%s: Maximum (elevation, azimuth): (%f, %f)" % (s,
                                                              90 - np.nanmin(positions[s][:,1]),
                                                              np.nanmax(positions[s][:,0]))
        lst_start = np.nanmin(sidereals[s])
        lst_end = np.nanmax(sidereals[s])
        print "Observable times LST %02.0f:%02.0f to %02.0f:%02.0f" % (np.floor(lst_start),
                                                 np.floor((lst_start - np.floor(lst_start))*60),
                                                 np.floor(lst_end),
                                                 np.floor((lst_end - np.floor(lst_end))*60))



    start_time = np.deg2rad(positions[s][np.where(np.logical_not(np.isnan(positions[s][:,0])))[0][0],:])
    end_time = np.deg2rad(positions[s][np.where(np.logical_not(np.isnan(positions[s][:,0])))[0][-1],:])
    ax.plot([np.sin(start_time[1])*np.cos(start_time[0])],
            [np.sin(start_time[1])*np.sin(start_time[0])],
            [np.cos(start_time[1])], "k^")
    ax.plot([np.sin(end_time[1])*np.cos(end_time[0])],
            [np.sin(end_time[1])*np.sin(end_time[0])],
            [np.cos(end_time[1])], "kv")

    ax.plot(np.sin(np.deg2rad(positions[s][:,1]))*np.cos(np.deg2rad(positions[s][:,0])),
            np.sin(np.deg2rad(positions[s][:,1]))*np.sin(np.deg2rad(positions[s][:,0])),
            np.cos(np.deg2rad(positions[s][:,1])), args.plot_styles[si],
            label=s, markersize=args.marker_size, markevery=25)
    ax.plot(np.sin(np.deg2rad(positions_interference[s][:,1]))*np.cos(np.deg2rad(positions_interference[s][:,0])),
            np.sin(np.deg2rad(positions_interference[s][:,1]))*np.sin(np.deg2rad(positions_interference[s][:,0])),
            np.cos(np.deg2rad(positions_interference[s][:,1])), "r.",
            markersize=args.marker_size/6.0)

ax.legend()
ax.grid(False)
ax.set_xlim(-1,1)
ax.set_ylim(-1,1)
ax.set_zlim(-1,1)

fig = plt.figure("Elevation v Time")
ax = fig.add_subplot(111)
for si, s in enumerate(args.sources):
    elv_s = 90 - positions[s][0,1]
    az_s = positions[s][0,0]
    elv_e = 90 - positions[s][-1,1]
    az_e = positions[s][-1,0]

    time = [ephem.Date(t).datetime() if not np.isnan(t) else datetime.datetime.now() for t in
            times_above[s]]
    ax.plot(time, 90 - positions[s][:,1], args.plot_styles[si], label=s,
            markersize = args.marker_size, markevery=25)
    time = [ephem.Date(t).datetime() if not np.isnan(t) else datetime.datetime.now() for t in
            times_interference[s]]
    ax.plot(time, 90 - positions_interference[s][:,1], "r.",
            markersize = args.marker_size/6.0)
hfmt = mdates.DateFormatter('%H:%M')

ax.xaxis.set_major_formatter(hfmt)
plt.xlabel("Time (%s) UTC" % str(args.start))
plt.ylabel("Elevation angle")
plt.grid(True)
plt.legend()

fig = plt.figure("PA v Time")
ax = fig.add_subplot(111)
for si, s in enumerate(args.sources):
    time = [ephem.Date(t).datetime() if not np.isnan(t) else datetime.datetime.now() for t in
            times_above[s]]
    ax.plot(time, pa[s][:], args.plot_styles[si], label=s,
            markersize=args.marker_size, markevery=25)
    time = [ephem.Date(t).datetime() if not np.isnan(t) else datetime.datetime.now() for t in
            times_interference[s]]
    ax.plot(time, pa_interference[s][:], "r.", markersize=args.marker_size/6.0)

hfmt = mdates.DateFormatter('%H:%M')

ax.xaxis.set_major_formatter(hfmt)
plt.xlabel("Time (%s) UTC" % str(args.start))
plt.ylabel("Parallactic angle")
plt.grid(True)
plt.legend()
plt.show()
