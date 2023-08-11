"""
main.py
~~~~~~~

Date: 08/09/2023 23:12
"""
from imports import *
from analyze import analyze



analysis = analyze(REPORT_CODE = "MApTcaJhjxZWQzyr", ANUBARAK_DPS_LOST = 5000, BURROWER_DPS_ADDED = 12000)
analysis.summarize()



x = [-40000 + 1000*i for i in range(81)]    # Anubarak DPS
y = [-40000 + 1000*i for i in range(81)]    # Burrower DPS
_z = [analyze("MApTcaJhjxZWQzyr", x[i], y[i], False, False) for i in track(range(len(x)))]
z = [a.net_change_in_direct_damage_taken_with_LS_on_tanks for a in _z]  # Net change in damage taken by tank (from Anub'arak/Burrowers/LS) and raid (from PC)



fig, ax = plt.subplots()
ax.plot(y, z, marker='o', linestyle='-', linewidth=2, markersize=5)
ax.set_xlabel('Change to Nerubian Burrower DPS')
ax.set_ylabel('Change in Total Damage Taken')
plt.show()

