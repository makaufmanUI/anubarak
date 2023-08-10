"""
main.py
~~~~~~~

Date: 08/09/2023 23:12
"""
from imports import *
from analyze import analyze


# DO NOT FORGET TO ADD THE INCLUSION OF LEECHING SWARM DAMAGE ON TANKS IN THEIR DPS_TAKEN VALUES SINCE IT MUST BE HEALED THROUGH


analysis = analyze(REPORT_CODE = "MApTcaJhjxZWQzyr", ANUBARAK_DPS_LOST = 5000, BURROWER_DPS_ADDED = 12000)
analysis.summarize()



x = [-40000 + 1000*i for i in range(81)]    # Anubarak DPS (change from baseline / original)
y = [-40000 + 1000*i for i in range(81)]    # Burrower DPS (change from baseline / original)
_z = [analyze("MApTcaJhjxZWQzyr", x[i], y[i], False, False) for i in track(range(len(x)))]
z = [a.net_change_in_direct_damage_taken for a in _z]  # Net change in damage taken by main tank (from Anub'arak) and raid (from PC)



fig, ax = plt.subplots(figsize=(12, 7))
ax.plot(y, z, marker='o', linestyle='dashed', linewidth=2, markersize=5, label="Burrower DPS vs. Net Δ in direct damage taken")
ax.hlines(0, -40000, 40000, colors='black', linestyles='dashed')
ax.vlines(0, z[0], z[-1], colors='black', linestyles='dashed')
ax.set_xlabel('Change to Nerubian Burrower DPS', fontsize=18)
ax.set_ylabel('Change in Melee + PC Damage Taken', fontsize=18)
ax.grid(True)
plt.show()

