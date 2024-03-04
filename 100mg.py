import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''
FUNCTIONS (BOXES ON OUR DIAGRAM)
'''
# 1 + 2 + 5 = 3 + 4
def intake(oxygen1, co1, k1, dnp1, oxygen2, co2, k2, dnp2, oxygen3, co3, k3, dnp3, oxygen5, co5, k5, dnp5):
    oxygen4 = oxygen1 + oxygen2 + oxygen5 - oxygen3
    co4 = co1 + co2 + co5 - co3
    k4 = k1 + k2 + k5 - k3
    dnp4 = dnpFrac*dnp1 + dnp2 + dnp5 - dnp3
    
    return oxygen4, co4, k4, dnp4

# splits arterial blood into 3 streams
def arterial(oxygen4, co4, k4, dnp4):
    oxygen6 = adiposeFrac * oxygen4
    co6 = adiposeFrac * co4
    k6 = adiposeFrac * k4
    dnp6 = adiposeFrac * dnp4

    oxygen7 = skmcFrac * oxygen4
    co7 = skmcFrac * co4
    k7 = skmcFrac * k4
    dnp7 = skmcFrac * dnp4

    oxygen8 = robFrac * oxygen4
    co8 = robFrac * co4
    k8 = robFrac * k4
    dnp8 = robFrac * dnp4
    
    return oxygen6, co6, k6, dnp6, oxygen7, co7, k7, dnp7, oxygen8, co8, k8, dnp8

def adipose(oxygen6, co6, k6, dnp6):
    oxygen9 = oxygen6 * (1-rq)
    if oxygen6 < 2*adiposeFrac * oxygen5init:
        co9 = co6 + adiposeFrac * oxygenAvail * rq * 6
    else:
        co9 = co6 + oxygen6 * rq
    k9 = k6
    dnp9 = dnp6
    return oxygen9, co9, k9, dnp9

def skmc(oxygen7, co7, k7, dnp7):
    oxygen10 = oxygen7 * (1-rq)
    if oxygen7 < 2*skmcFrac * oxygen5init:
        co10 = co7 + skmcFrac * oxygenAvail * rq * 6 / 0.75
    else:
        co10 = co7 + oxygen7 * rq / 0.75
    k10 = k7
    dnp10 = dnp7
    return oxygen10, co10, k10, dnp10

def rob(oxygen8, co8, k8, dnp8):
    oxygen11 = oxygen8 * (1-rq)
    if oxygen8 < 2*robFrac * oxygen5init:
        co11 = co8 + robFrac * oxygenAvail * rq * 6
    else:
        co11 = co8 + oxygen8 * rq
    k11 = k8
    dnp11 = dnp8 - 6.593e-4
    return oxygen11, co11, k11, dnp11, oxygen12, co12, k12, dnp12

# 9 + 10 + 11 = 5
def venous(oxygen9, co9, k9, dnp9, oxygen10, co10, k10, dnp10, oxygen11, co11, k11, dnp11, i, out):
    oxygen5 = oxygen9 + oxygen10 + oxygen11
    co5 = co9 + co10 + co11
    co5 = co5 - (bicarb * (co5 - co5const))
    k5 = k9 + k10 + k11
    dnp5 = dnp9 + dnp10 + dnp11
    dnp5 = out[i-1] * dnp5
    
    return oxygen5, co5, k5, dnp5

# calculates dnp fractions
def f(i):
    if i == 1:
        return np.exp(-0.0673)
    else:
        return f(i-1) + np.exp(-0.0673 * i)

'''
ACTUAL CODE
'''

colnames = []
compounds = ["oxygen", "co", "k", "dnp"]
for i in range (1, 13):
    for compound in compounds:
        colnames.append(f"{compound}{i}")

data = pd.DataFrame(columns=colnames, index=range(25))

# initialize everything as 0, conditions/ICs below
zeros = [0] * 48
oxygen1, co1, k1, dnp1, oxygen2, co2, k2, dnp2, oxygen3, co3, k3, dnp3, oxygen4, co4, k4, dnp4, oxygen5, co5, k5, dnp5, \
    oxygen6, co6, k6, dnp6, oxygen7, co7, k7, dnp7, oxygen8, co8, k8, dnp8, oxygen9, co9, k9, dnp9, oxygen10, co10, k10, dnp10, \
    oxygen11, co11, k11, dnp11, oxygen12, co12, k12, dnp12 = zeros
    
# constants/initial conditions here (MOLES/HR)
airVol = 600 # liters of air per hour
molesPerHour = airVol / 0.08206 / 310.15   # n = PV/RT

# breathing in
oxygen1 = molesPerHour * 0.21 * 0.9
co1 = molesPerHour * 0.0004 * 0.9
dnp1 = 5.43e-4

# eating
k2 = 0.00321

# breathing out
oxygen3 = molesPerHour * 0.164
co3 = molesPerHour * 0.036

# initial conditions in blood
oxygen5 = 2.036
co5 = 0.8203
#k5 = 1.32
k5 = 300 * (((0.001393 * 184.106) * dnp1) + 0.0044)

# initial/steady states for reference
oxygenAvail = oxygen1 - oxygen3
oxygen5init = 2.036
co5const = 0.8203

# arterial fractions
adiposeFrac = 0.04
skmcFrac = 0.14
robFrac = 1 - adiposeFrac - skmcFrac

# reaction rates
# rq = 0.7 * 0.35
rq = -0.596*np.exp(-665.9*dnp1) + 0.744
bicarb = 0.08356 * np.log(40.23)

# dnp absorption fraction
dnpFrac = 0.31

# urine potassium leaving
urinek = 0.00321

# fill into row 0 of data
data.iloc[0] = [oxygen1, co1, k1, dnp1, oxygen2, co2, k2, dnp2, oxygen3, co3, k3, dnp3, oxygen4, co4, k4, dnp4, \
    oxygen5, co5, k5, dnp5, oxygen6, co6, k6, dnp6, oxygen7, co7, k7, dnp7, oxygen8, co8, k8, dnp8, \
    oxygen9, co9, k9, dnp9, oxygen10, co10, k10, dnp10, oxygen11, co11, k11, dnp11, oxygen12, co12, k12, dnp12]

out = np.zeros(24)
for i in range(1, 25):
    out[i-1] = f(i) / i

for i in range(1, 25):
    oxygen4, co4, k4, dnp4 = intake(oxygen1, co1, k1, dnp1, oxygen2, co2, k2, dnp2, oxygen3, co3, k3, dnp3, oxygen5, co5, k5, dnp5)
    oxygen6, co6, k6, dnp6, oxygen7, co7, k7, dnp7, oxygen8, co8, k8, dnp8 = arterial(oxygen4, co4, k4, dnp4)
    oxygen9, co9, k9, dnp9 = adipose(oxygen6, co6, k6, dnp6)
    oxygen10, co10, k10, dnp10 = skmc(oxygen7, co7, k7, dnp7)
    oxygen11, co11, k11, dnp11, oxygen12, co12, k12, dnp12 = rob(oxygen8, co8, k8, dnp8)
    oxygen5, co5, k5, dnp5 = venous(oxygen9, co9, k9, dnp9, oxygen10, co10, k10, dnp10, oxygen11, co11, k11, dnp11, i, out)
    
    data.iloc[i] = [oxygen1, co1, k1, dnp1, oxygen2, co2, k2, dnp2, oxygen3, co3, k3, dnp3, oxygen4, co4, k4, dnp4, \
        oxygen5, co5, k5, dnp5, oxygen6, co6, k6, dnp6, oxygen7, co7, k7, dnp7, oxygen8, co8, k8, dnp8, \
        oxygen9, co9, k9, dnp9, oxygen10, co10, k10, dnp10, oxygen11, co11, k11, dnp11, oxygen12, co12, k12, dnp12]
    
data.to_csv("100mg.csv")

# stream = 5
    
# # plt.figure()
# # plt.plot(data[f'oxygen{stream}'])
# # plt.title('Venous Oxygen Over Time (100mg DNP)')
# # plt.xlabel('Time (hr)')
# # plt.ylabel('Molar Flow Rate (moles/hr)')
# # plt.grid(True)
# # plt.savefig(f"100mg-oxygen{stream}.png")

# # plt.figure()
# # plt.plot(data[f'co{stream}'])
# # plt.title('Venous Carbon Dioxide Over Time (100mg DNP)')
# # plt.xlabel('Time (hr)')
# # plt.ylabel('Molar Flow Rate (moles/hr)')
# # plt.grid(True)
# # plt.savefig(f"100mg-co{stream}.png")

# # plt.figure()
# # plt.plot(data[f'k{stream}'])
# # plt.title('Venous Potassium Over Time (100mg DNP)')
# # plt.xlabel('Time (hr)')
# # plt.ylabel('Molar Flow Rate (moles/hr)')
# # plt.grid(True)
# # plt.savefig(f"100mg-k{stream}.png")

# # plt.figure()
# # plt.plot(data[f'dnp{stream}'])
# # plt.title('Venous DNP Over Time (100mg DNP)')
# # plt.xlabel('Time (hr)')
# # plt.ylabel('Molar Flow Rate (moles/hr)')
# # plt.grid(True)
# # plt.savefig(f"100mg-dnp{stream}.png")

# fig, axes = plt.subplots(2, 2, figsize=(15, 8))

# ax = axes[0,0]
# ax.plot(data[f'oxygen{stream}'])
# ax.set_title('Venous Oxygen Over Time (100mg DNP)')
# ax.set_xlabel('Time (hr)')
# ax.set_ylabel('Molar Flow Rate (moles/hr)')
# ax.grid(True)

# ax = axes[0,1]
# ax.plot(data[f'co{stream}'])
# ax.set_title('Venous Carbon Dioxide Over Time (100mg DNP)')
# ax.set_xlabel('Time (hr)')
# ax.set_ylabel('Molar Flow Rate (moles/hr)')
# ax.grid(True)

# ax = axes[1,0]
# ax.plot(data[f'k{stream}'])
# ax.set_title('Venous Potassium Over Time (100mg DNP)')
# ax.set_xlabel('Time (hr)')
# ax.set_ylabel('Molar Flow Rate (moles/hr)')
# ax.grid(True)

# ax = axes[1,1]
# ax.plot(data[f'dnp{stream}'])
# ax.set_title('Venous DNP Over Time (100mg DNP)')
# ax.set_xlabel('Time (hr)')
# ax.set_ylabel('Molar Flow Rate (moles/hr)')
# ax.grid(True)
    
# fig.tight_layout()

# plt.savefig('100mg.png')
# plt.show()
