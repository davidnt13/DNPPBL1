import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# in mmol/hr now
ss = pd.read_csv('steadystate.csv') *1000
gram = pd.read_csv('1g.csv') *1000
mg = pd.read_csv('100mg.csv') *1000
safe = pd.read_csv('50mg.csv') *1000

'''
THERAPEUTIC INDEX
'''

# plt.figure()

# plt.plot(gram['co5'], 'r', label = '1 gram')
# plt.plot(mg['co5'], 'orange', label = '100mg')
# plt.plot(safe['co5'], 'b', label="50mg")
# plt.plot(ss['co5'], 'g', label='Steady State')
# plt.axhline(1010, linestyle='--', color='gray', label = "Hypercapnia Threshold") # from 65 mmHg Paco2

# plt.title("Effect of DNP Dosage on Venous Carbon Dioxide", fontsize=13)
# plt.xlabel("Time (hr)", fontsize=13)
# plt.ylabel("Molar Flow Rate (mmol/hr)", fontsize=13)
# plt.yscale("log")

# plt.legend()
# plt.savefig('carbondioxide.png')

# plt.figure()

# plt.plot(gram['oxygen5'], 'r', label = '1 gram')
# plt.plot(mg['oxygen5'], 'orange', label = '100mg')
# plt.plot(safe['oxygen5'], 'b', label="50mg")
# plt.plot(ss['oxygen5'], 'g', label='Steady State')
# plt.axhline(1800, linestyle='--', color='gray', label = "Hypoxia Threshold")     # 1800 from 90% of 2 mol/hr which is ss

# plt.title("Effect of DNP Dosage on Venous Oxygen", fontsize=13)
# plt.xlabel("Time (hr)", fontsize=13)
# plt.ylabel("Molar Flow Rate (mmol/hr)", fontsize=13)

# plt.legend(loc='best', bbox_to_anchor=(1,0.75))
# plt.savefig('oxygen.png')

# plt.figure()

# plt.plot(np.abs(gram['dnp5']), 'r', label = '1 gram')
# plt.plot(np.abs(safe['dnp5']), 'orange', label="100mg")
# plt.plot(np.abs(mg['dnp5']), 'b', label = '50mg')
# plt.plot(np.abs(ss['dnp5']), 'g', label='Steady State')

# plt.title("Venous DNP Over Time", fontsize=13)
# plt.xlabel("Time (hr)", fontsize=13)
# plt.ylabel("Molar Flow Rate (mmol/hr)", fontsize=13)

# plt.legend(loc='best', bbox_to_anchor=(1,0.75))
# plt.savefig('dnp.png')

# plt.show()

# plt.figure()

# plt.plot(ss['k5'] / 300, 'g', label='Steady State')
# plt.plot(gram['k5'] / 300, 'r', label = '1 gram')
# plt.plot(mg['k5'] / 300, 'orange', label = '100mg')
# plt.plot(safe['k5'] / 300, 'b', label="50mg")
# plt.axhline(5, linestyle='--', color='gray', label = "Hyperkalemia Threshold")
# plt.title("Effect of DNP Dosage on Venous Potassium Levels")
# plt.ylabel("Concentration (mM)")
# plt.xlabel("Time (hours)")
# plt.legend(bbox_to_anchor=(1, 0.75), loc='upper right')
# plt.savefig('potassiumGraphs')

# plt.show()

'''
CAUSES GRAPH
'''

# fig, ax1 = plt.subplots()

# # Plot the first dataset
# line1, = ax1.plot(gram['co5'], 'b-', label='Carbon Dioxide')
# ax1.set_xlabel('Time (hr)', fontsize=13)
# ax1.set_ylabel('CO2, O2, and K+ Molar Flow Rate (mmol/hr)', fontsize=13)

# line2, = ax1.plot(gram['oxygen5'], 'r-', label='Oxygen')

# line3, = ax1.plot(gram['k5'], color='orange', label="Potassium")

# # Create secondary y-axis
# ax2 = ax1.twinx()

# # Plot the second dataset on the secondary y-axis
# line4, = ax2.plot(gram['dnp5']*1000, 'g-', label='DNP')
# ax2.set_ylabel('DNP Molar Flow Rate (mmol/hr)', fontsize=13)

# # Show legend for all datasets
# lines = [line1, line2, line3, line4]
# labels = [line.get_label() for line in lines]
# ax1.legend(lines, labels, loc='best', bbox_to_anchor=(1,0.8))

# plt.title("Effect of 1g DNP on Venous Carbon Dioxide and Oxygen")
# fig.tight_layout()
# plt.savefig('causes.png')

# plt.show()

'''
RQ
'''
time = np.linspace(0, 1000, 100)
rq = 2.29e-4 * time + 0.746

plt.figure()

plt.plot(time, rq, color='#663A82')

plt.title("Effect of DNP on Baseline RQ", fontsize=13)
plt.xlabel("DNP Dosage (mg)", fontsize=13)
plt.ylabel("Respiratory Quotient", fontsize=13)
plt.ylim(0.7, 1)

plt.savefig('rq.png')
plt.show()