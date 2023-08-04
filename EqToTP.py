
#
# Read an EQ specification output by AutoEq and convert it to a TrackPlug 6 EQ preset
#

"""
Output of AutoEq python script:

Preamp: -6.2 dB
Filter 1: ON LSC Fc 105 Hz Gain 6.3 dB Q 0.70
Filter 2: ON HSC Fc 10000 Hz Gain -6.2 dB Q 0.70
Filter 3: ON PK Fc 3517 Hz Gain -6.9 dB Q 2.12
Filter 4: ON PK Fc 7125 Hz Gain 5.0 dB Q 1.08
Filter 5: ON PK Fc 141 Hz Gain -2.4 dB Q 0.36
Filter 6: ON PK Fc 2047 Hz Gain 3.5 dB Q 1.80
Filter 7: ON PK Fc 493 Hz Gain 1.8 dB Q 0.91
Filter 8: ON PK Fc 4484 Hz Gain -2.1 dB Q 1.57
Filter 9: ON PK Fc 58 Hz Gain 1.7 dB Q 3.88
Filter 10: ON PK Fc 41 Hz Gain 0.7 dB Q 1.82

Corresponding TP6 EQ preset, with HS filter at end

preset name = "SennHD600", plug = TrackPlug 6 EQ, version = 617, numparam = 50
2 1 105 1 6.3 2
0 3520 0.674 -6.9 2 0
7120 1.292 5 2 0 141
3.265 -2.4 2 0 2050 0.792
3.5 2 0 493 1.515 1.8
2 0 4480 0.904 -2.1 2
0 58 0.37 1.7 2 0
41 0.783 0.700001 2 2 10000
1 -6.2
"""

import math
from array import array
import sys

# evaluate table defined by x_arr and y_arr at point x.
# x_arr must be monotonically increasing.
def tab_eval(x_arr, y_arr, x):
    if len(x_arr) != len(y_arr):
        raise ValueError
    n = len(x_arr)

    if x <= x_arr[0]:
        return y_arr[0]
    if x >= x_arr[n-1]:
        return y_arr[n-1]
    # binary search
    lo = 0
    hi = n - 1
    while hi > lo + 1:
        i = math.floor((hi + lo) / 2)
        if x_arr[i] > x:
            hi = i
        else:
            lo = i
    # now hi = lo + 1
    y = y_arr[lo] + (x - x_arr[lo]) * (y_arr[hi] - y_arr[lo]) / (x_arr[hi] - x_arr[lo])
    return y


# convert width in octaves to Q factor
def width2q(W):
    Q = 1 / (2**(W/2) - 2**(-W/2))
    return Q

# convert Q factor to width in octaves
def q2width(Q):
    # build table
    maxw = 4
    minw = 0.01
    dw = 0.01
    nw = int(1 + (maxw - minw) / dw)
    x_arr = [0] * nw
    y_arr = [0] * nw
    for i in range(0, nw):
        W = minw + i * dw
        y_arr[nw - i - 1] = W
        x_arr[nw - i - 1] = width2q(W)

    W = tab_eval(x_arr, y_arr, Q)
    return W

# read autoEQ spec and return as list of dicts, one per EQ
def parseAutoEq(fileName):
    eqs = []
    with open(fileName) as file:
        while line := file.readline():
            s = line.split()
            if len(s) > 0 and s[0] == "Filter":
                eq = { "type" : s[3], "fc" : s[5], "gain" : s[8], "Q" : s[11] }
                eqs.append(eq)
    return eqs

# convert autoEq dicts to TP values, with integer type and width
def autoEqToTpEq(autoEq):
    tp_eqs = []
    type_map = { "PK" : 0, "LSC" : 1, "HSC" : 2 }
    for i in range(0, len(autoEq)):
        eq = autoEq[i]
        eq["tp_type"] = type_map[eq["type"]]
        eq["width"] = q2width(float(eq["Q"]))
        tp_eqs.append(eq)
    return tp_eqs

# return 5 float param list for eq dict
# enable type fc gain width
def tpEqParams(eq):
    return [2, float(eq["tp_type"]), float(eq["fc"]), float(eq["width"]), float(eq["gain"])]

# write legacy (v4/v5/v6) WA preset
def writePreset(fileName, presetName, plugName, version, preset):
    n = len(preset)
    file = open(fileName, "w")
    file.write(f"preset name = \"{presetName}\", plug = \"{plugName}\", version = {version}, numparam = {n}\n")
    for i in range(0,n):
        file.write(f"{preset[i]}")
        if (i + 1) % 6 == 0:
            file.write("\n")
        else:
            file.write(" ")
    file.write("\n")
    file.close()

# convert tpEq (list of dicts) to trackplug preset
def tpEqToPreset(tpEq):
    # make preset
    preset = [0] * 50
    n = len(tpEq)
    for i in range(0,n):
        params = tpEqParams(tpEq[i])
        for j in range(0,5):
            preset[i * 5 + j] = params[j]
    return preset

# convert an autoEQ spec to a TP6 preset file
def convert(autoEqFileName, tpEqPresetFileName, presetName):
    autoEq = parseAutoEq(autoEqFileName)
    tpEq = autoEqToTpEq(autoEq)
    preset = tpEqToPreset(tpEq)
    writePreset(tpEqPresetFileName, presetName, "TrackPlug 6 EQ", 617, preset)

# Usage: python EqToTp.py autoEqFileName tpEqPresetFileName presetName
if len(sys.argv) != 4:
    print("Usage: python EqToTp.py autoEqFileName tpEqPresetFileName presetName")
    raise ValueError

convert(sys.argv[1], sys.argv[2], sys.argv[3])
