import scipy as sc
import numpy as np
from variables import *
from aerodynamic_dist import cl_dist, cd_dist, cm_dist, cl_winglet_dist, cd_winglet_dist, cm_winglet_dist, alpha  # Import interpolated continuous distributions from data


# Variables

# q0 = 100
# q1 = 100
# y=np.linspace(0,10.1,400) #Linear discretization of continuous space, sample size=400

# Force Distributions

def force_span(dist, sample, q, CL=CL_des):  # Input distribution function, sample number, pressure
    y = np.linspace(0, 10.1, sample)  # Linear discretization of continuous space
    chord_y = (ct - cr) / (b / 2) * (y) + 3.44  # Chord distribution
    ddist = dist(y, CL)  # Discretized coefficient distribution
    force_dist = (ddist * q * chord_y)/(np.sqrt(1-mach**2))  # Force distribution
    return force_dist


def moment_span(dist, sample, q, CL=CL_des):  # Input distribution function, sample number, pressure - For moment, chord is squared
    y = np.linspace(0, 10.1, sample)  # Linear discretization of continuous space
    chord_y = (ct - cr) / (b / 2) * (y) + 3.44  # Chord Distribution
    ddist = dist(y, CL)  # Discretized coefficient distribution
    moment_dist = (ddist * q * (chord_y) ** 2)/(np.sqrt(1-mach**2))  # Moment distribution
    return moment_dist


def normal_span(sample, q, CLd=CL_des):  # Input distribution function, sample number, pressure, Wing lift coefficient
    AoA = alpha(CLd)
    normal_dist = np.cos(AoA) * force_span(cl_dist, sample, q, CLd) + np.sin(AoA) * force_span(cd_dist, sample, q, CLd)
    return normal_dist


def force_winglet(dist, sample, q, CLd=CL_des):  # Input distribution function, sample number, pressure
    y = np.linspace(0, wlt_span/2, sample)  # Linear discretization of continuous space
    chord_y = (wlt_ct - wlt_cr) / (wlt_span / 2) * (y) + wlt_cr  # Chord distribution
    # print(chord_y)
    ddist = dist(y+b/2, CLd)  # Discretized coefficient distribution
    # print(ddist)
    force_dist = ddist * q * chord_y  # Force distribution
    force = (np.sum(force_dist) / sample)/(np.sqrt(1-mach**2))
    return force


def moment_winglet(sample, q, CL=CL_des):
    y = np.linspace(0, wlt_span / 2, sample)  # Linear discretization of continuous space
    chord_y = (wlt_ct - wlt_cr) / (wlt_span / 2) * (y) + wlt_cr  # Chord distribution
    # print(chord_y)
    ddist = cm_winglet_dist(y + b / 2, CL_des)  # Discretized coefficient distribution
    # print(ddist)
    moment_dist = ddist * q * chord_y**2  # Moment distribution
    moment = (np.sum(moment_dist) / sample)/(np.sqrt(1-mach**2))
    momenty = moment * np.cos(np.radians(50))  # moment around y-axis (pitch up/down)
    return momenty


def normal_winglet(sample, q, CLd=CL_des):
    AoA = alpha(CLd) * np.cos(np.radians(50))
    normal = np.cos(AoA) * force_winglet(cl_winglet_dist, sample, q, CLd) + np.sin(AoA) * force_winglet(cd_winglet_dist, sample, q, CLd)
    print("Hello :)")
    return normal


def tangential_winglet(sample, q, CLd=CL_des):
    AoA = alpha(CLd) * np.cos(np.radians(50))
    tang = np.sin(AoA) * force_winglet(cl_winglet_dist, sample, q, CLd) + np.cos(AoA) * force_winglet(cd_winglet_dist, sample, q, CLd)
    return tang


# print(tangential_winglet(400, 7000))
# print(force_winglet(cl_winglet_dist, 400, 7000))
# print(force_winglet(cd_winglet_dist, 400, 7000))
# print(moment_winglet(400, 7000))