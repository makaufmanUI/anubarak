"""
analyze.py
~~~~~~~~~~

Date: 08/09/2023 21:14
"""
from imports import *
from wcl import (
    get_fight,
    get_damage_done_data,
    get_damage_taken_data,
    get_enemy_healing_done_data,
    get_friendly_healing_done_data,
    get_fights_and_participants_info,
)

ANUBARAK_HP_P3 = 8_157_825



class _dps_taken:
    def __init__(self, dps_taken_ot: float, dps_taken_mt: float, dps_taken_raid_ls: float, dps_taken_raid_pc: float) -> None:
        self._dps_taken_ot = dps_taken_ot
        self._dps_taken_mt = dps_taken_mt
        self._dps_taken_raid_ls = dps_taken_raid_ls
        self._dps_taken_raid_pc = dps_taken_raid_pc

    @property
    def off_tanks(self) -> float:
        """
        ---\n
        Total damage taken by the (2) off tanks in the `t₀ + Δt` phase 3 time span.\n
        ---\n
        𝐷𝑢𝑒 𝑡𝑜   →   `𝑀𝑒𝑙𝑒𝑒`\n
        𝐹𝑟𝑜𝑚     →   `𝑁𝑒𝑟𝑢𝑏𝑖𝑎𝑛 𝐵𝑢𝑟𝑟𝑜𝑤𝑒𝑟`\n
        ---\n
        """
        return self._dps_taken_ot
    @off_tanks.setter
    def off_tanks(self, value: float) -> None:
        self._dps_taken_ot = value

    @property
    def main_tank(self) -> float:
        """
        ---\n
        Total damage taken by the main tank in the `t₀ + Δt` phase 3 time span.\n
        ---\n
        𝐷𝑢𝑒 𝑡𝑜   →   `𝑀𝑒𝑙𝑒𝑒`  /  `𝐹𝑟𝑒𝑒𝑧𝑖𝑛𝑔 𝑆𝑙𝑎𝑠ℎ`\n
        𝐹𝑟𝑜𝑚     →   `𝐴𝑛𝑢𝑏'𝑎𝑟𝑎𝑘`\n
        ---\n
        """
        return self._dps_taken_mt
    @main_tank.setter
    def main_tank(self, value: float) -> None:
        self._dps_taken_mt = value

    @property
    def raid_LS(self) -> float:
        """
        ---\n
        Damage taken by the entire raid in the `t₀ + Δt` phase 3 time span.\n
        ---\n
        𝐷𝑢𝑒 𝑡𝑜   →   `𝐿𝑒𝑒𝑐ℎ𝑖𝑛𝑔 𝑆𝑤𝑎𝑟𝑚`\n
        𝐹𝑟𝑜𝑚     →   `𝐴𝑛𝑢𝑏'𝑎𝑟𝑎𝑘`\n
        ---\n
        """
        return self._dps_taken_raid_ls
    @raid_LS.setter
    def raid_LS(self, value: float) -> None:
        self._dps_taken_raid_ls = value

    @property
    def raid_PC(self) -> float:
        """
        ---\n
        Damage taken by the entire raid in the `t₀ + Δt` phase 3 time span.\n
        ---\n
        𝐷𝑢𝑒 𝑡𝑜   →   `𝑃𝑒𝑛𝑒𝑡𝑟𝑎𝑡𝑖𝑛𝑔 𝐶𝑜𝑙𝑑`\n
        𝐹𝑟𝑜𝑚     →   `𝐴𝑛𝑢𝑏'𝑎𝑟𝑎𝑘`\n
        ---\n
        """
        return self._dps_taken_raid_pc
    @raid_PC.setter
    def raid_PC(self, value: float) -> None:
        self._dps_taken_raid_pc = value

    @property
    def raid(self) -> float:
        """
        ---\n
        Total damage taken by the entire raid in the `t₀ + Δt` phase 3 time span.\n
        ---\n
        𝐷𝑢𝑒 𝑡𝑜   →   `𝐿𝑒𝑒𝑐ℎ𝑖𝑛𝑔 𝑆𝑤𝑎𝑟𝑚`  /  `𝑃𝑒𝑛𝑒𝑡𝑟𝑎𝑡𝑖𝑛𝑔 𝐶𝑜𝑙𝑑`\n
        𝐹𝑟𝑜𝑚     →   `𝐴𝑛𝑢𝑏'𝑎𝑟𝑎𝑘`\n
        ---\n
        """
        return self._raid_dps_taken_ls + self._raid_dps_taken_pc
    @raid.setter
    def raid(self, value: float) -> None:
        self._raid_dps_taken_ls = value
        self._raid_dps_taken_pc = value

    @property
    def total(self) -> float:
        """
        ---\n
        Entirety of DPS taken from all sources in the `t₀ + Δt` phase 3 time span.\n
        ---\n
        𝐷𝑢𝑒 𝑡𝑜   →   `𝑀𝑒𝑙𝑒𝑒 (1)`  /  `𝑀𝑒𝑙𝑒𝑒 (2)`  /  `𝐹𝑟𝑒𝑒𝑧𝑖𝑛𝑔 𝑆𝑙𝑎𝑠ℎ (2)`  /  `𝐿𝑒𝑒𝑐ℎ𝑖𝑛𝑔 𝑆𝑤𝑎𝑟𝑚 (2)`  /  `𝑃𝑒𝑛𝑒𝑡𝑟𝑎𝑡𝑖𝑛𝑔 𝐶𝑜𝑙𝑑 (2)`\n
        𝐹𝑟𝑜𝑚     →   `𝑁𝑒𝑟𝑢𝑏𝑖𝑎𝑛 𝐵𝑢𝑟𝑟𝑜𝑤𝑒𝑟 (1)`  /  `𝐴𝑛𝑢𝑏'𝑎𝑟𝑎𝑘 (2)`\n
        ---\n
        """
        return self._raid_dps_taken_ls + self._raid_dps_taken_pc + self._dps_taken_mt + self._dps_taken_ot
    @total.setter
    def total(self, value: float) -> None:
        self._raid_dps_taken_ls = value
        self._raid_dps_taken_pc = value
        self._dps_taken_mt = value
        self._dps_taken_ot = value





class _hps_taken:
    def __init__(self, anub_hps_taken_ls, raid_hps_taken_jol) -> None:
        self._anub_hps_taken_ls = anub_hps_taken_ls
        self._raid_hps_taken_jol = raid_hps_taken_jol

    @property
    def anubarak(self) -> float:
        """
        ---\n
        Healing taken by Anub'arak in the `t₀ + Δt` phase 3 time span.\n
        ---\n
        𝐷𝑢𝑒 𝑡𝑜   →   `𝐿𝑒𝑒𝑐ℎ𝑖𝑛𝑔 𝑆𝑤𝑎𝑟𝑚`\n
        𝐹𝑟𝑜𝑚     →   `𝐴𝑛𝑢𝑏'𝑎𝑟𝑎𝑘`\n
        ---\n
        """
        return self._anub_hps_taken_ls
    @anubarak.setter
    def anubarak(self, value: float) -> None:
        self._anub_hps_taken_ls = value

    @property
    def raid(self) -> float:
        """
        ---\n
        Healing taken by the entire raid in the `t₀ + Δt` phase 3 time span.\n
        ---\n
        𝐷𝑢𝑒 𝑡𝑜   →   `𝐽𝑢𝑑𝑔𝑒𝑚𝑒𝑛𝑡 𝑜𝑓 𝐿𝑖𝑔ℎ𝑡`\n
        𝐹𝑟𝑜𝑚     →   `𝑃𝑙𝑎𝑦𝑒𝑟𝑠`\n
        ---\n
        """
        return self._raid_hps_taken_jol
    @raid.setter
    def raid(self, value: float) -> None:
        self._raid_hps_taken_jol = value

    @property
    def total(self) -> float:
        """
        ---\n
        Entirety of healing taken from all sources in the `t₀ + Δt` phase 3 time span.\n
        ---\n
        𝐷𝑢𝑒 𝑡𝑜   →   `𝐽𝑢𝑑𝑔𝑒𝑚𝑒𝑛𝑡 𝑜𝑓 𝐿𝑖𝑔ℎ𝑡 (1)`  /  `𝐿𝑒𝑒𝑐ℎ𝑖𝑛𝑔 𝑆𝑤𝑎𝑟𝑚 (2)`\n
        𝐹𝑟𝑜𝑚     →   `𝑃𝑙𝑎𝑦𝑒𝑟𝑠 (1)`  /  `𝐴𝑛𝑢𝑏'𝑎𝑟𝑎𝑘 (2)`\n
        ---\n
        """
        return self._anub_hps_taken_ls + self._raid_hps_taken_jol
    @total.setter
    def total(self, value: float) -> None:
        self._anub_hps_taken_ls = value
        self._raid_hps_taken_jol = value





class _dps_done:
    def __init__(self, raid_dps_done, new_raid_dps, raid_dps_pct_change) -> None:
        self._raid_dps_done = raid_dps_done
        self._new_raid_dps = new_raid_dps
        self._raid_dps_pct_change = raid_dps_pct_change

    @property
    def raid1(self) -> float:
        """
        ---\n
        Damage done by the entire raid in the `t₀` phase 3 time span.\n
        ---\n
        𝐷𝑢𝑒 𝑡𝑜   →   `𝑀𝑒𝑙𝑒𝑒`  /  `𝑆𝑝𝑒𝑙𝑙𝑠`\n
        𝐹𝑟𝑜𝑚     →   `𝑃𝑙𝑎𝑦𝑒𝑟𝑠`\n
        𝑇𝑎𝑟𝑔𝑒𝑡   →   `𝐴𝑛𝑢𝑏'𝑎𝑟𝑎𝑘`\n
        ---\n
        """
        return self._raid_dps_done
    @raid1.setter
    def raid1(self, value: float) -> None:
        self._raid_dps_done = value

    @property
    def raid2(self) -> float:
        """
        ---\n
        Damage done by the entire raid in the `t₀ + Δt` phase 3 time span.\n
        ---\n
        𝐷𝑢𝑒 𝑡𝑜   →   `𝑀𝑒𝑙𝑒𝑒`  /  `𝑆𝑝𝑒𝑙𝑙𝑠`\n
        𝐹𝑟𝑜𝑚     →   `𝑃𝑙𝑎𝑦𝑒𝑟𝑠`\n
        𝑇𝑎𝑟𝑔𝑒𝑡   →   `𝐴𝑛𝑢𝑏'𝑎𝑟𝑎𝑘`\n
        ---\n
        """
        return self._new_raid_dps
    @raid2.setter
    def raid2(self, value: float) -> None:
        self._new_raid_dps = value

    @property
    def raid_pct_change(self) -> float:
        """
        ---\n
        Percentage change in damage done by the raid in the `t₀` and `t₀ + Δt` phase 3 time spans.\n
        Note that negative values indicate a loss in raid dps, leading to an increase in phase 3 duration.\n
        ---\n
        𝐷𝑢𝑒 𝑡𝑜   →   `𝑀𝑒𝑙𝑒𝑒`  /  `𝑆𝑝𝑒𝑙𝑙𝑠`\n
        𝐹𝑟𝑜𝑚     →   `𝑃𝑙𝑎𝑦𝑒𝑟𝑠`\n
        𝑇𝑎𝑟𝑔𝑒𝑡   →   `𝐴𝑛𝑢𝑏'𝑎𝑟𝑎𝑘`\n
        ---\n
        """
        return self._raid_dps_pct_change
    @raid_pct_change.setter
    def raid_pct_change(self, value: float) -> None:
        self._raid_dps_pct_change = value





class Analysis:
    """
    ---\n
    Class for storing and accessing the results of the Nerubian Burrower / Anub'arak damage exchange analysis.\n
    ---\n

    Properties
    ----------
    - `anubarak_dps_lost` - 
    - `burrower_dps_added` - 
    - `dps_done` - 
        - `raid1`
        - `raid2`
        - `raid_pct_change`
    - `dps_taken`
        - `main_tank`
        - `off_tanks`
        - `raid`
        - `raid_LS`
        - `raid_PC`
        - `total`
    - `hps_taken`
        - `anubarak`
        - `raid`
        - `total`
    - `net_change_in_direct_damage_taken`
    - `net_change_in_passive_damage_taken`
    - `net_damage_added_raid_LS`
    - `time_added_to_phase3`
    - `time_added_to_phase3_pct_change`
    
    - `time_spent_in_phase3_initial`
    - `time_spent_in_phase3_final`
    
    - `total_damage_added_mt`
    - `total_damage_added_raid_LS`
    - `total_damage_added_raid_PC`
    - `total_damage_saved_ot`
    """
    def __init__(self, 
                    dps_taken_ot: float,
                    dps_taken_mt: float,
                    raid_dps_taken_ls: float,
                    raid_dps_taken_pc: float,
                    raid_dps_done: float,
                    anub_hps_taken_ls: float,
                    raid_hps_taken_jol: float,
                    burrower_dps_added: float,
                    anubarak_dps_lost: float,
                    new_raid_dps: float,
                    raid_dps_pct_change: float,
                    time_added_to_phase3: float,
                    time_added_pct_change: float,
                    total_ot_damage_saved: float,
                    total_mt_damage_added: float,
                    total_pc_damage_added: float,
                    net_ls_damage_added: float,
                    gross_ls_damage_added: float,
                    net_increase_decrease_in_passive_damage_taken: float,
                    net_increase_decrease_in_immediate_damage_taken: float,
                    time_spent_in_phase3_initial: float,    # NEW
                    time_spent_in_phase3_final: float,      # NEW
                    ) -> None:
        self._dps_taken_ot = dps_taken_ot
        self._dps_taken_mt = dps_taken_mt
        self._raid_dps_taken_ls = raid_dps_taken_ls
        self._raid_dps_taken_pc = raid_dps_taken_pc
        self._raid_dps_done = raid_dps_done
        self._anub_hps_taken_ls = anub_hps_taken_ls
        self._raid_hps_taken_jol = raid_hps_taken_jol
        self._burrower_dps_added = burrower_dps_added
        self._anubarak_dps_lost = anubarak_dps_lost
        self._new_raid_dps = new_raid_dps
        self._raid_dps_pct_change = raid_dps_pct_change
        self._time_added_to_phase3 = time_added_to_phase3
        self._time_added_pct_change = time_added_pct_change
        self._total_ot_damage_saved = total_ot_damage_saved
        self._total_mt_damage_added = total_mt_damage_added
        self._total_pc_damage_added = total_pc_damage_added
        self._net_ls_damage_added = net_ls_damage_added
        self._gross_ls_damage_added = gross_ls_damage_added
        self._net_increase_decrease_in_passive_damage_taken = net_increase_decrease_in_passive_damage_taken
        self._net_increase_decrease_in_immediate_damage_taken = net_increase_decrease_in_immediate_damage_taken

        self._time_spent_in_phase3_initial = time_spent_in_phase3_initial    # NEW
        self._time_spent_in_phase3_final = time_spent_in_phase3_final        # NEW

        self._dps_taken = _dps_taken(self._dps_taken_ot, self._dps_taken_mt, self._raid_dps_taken_ls, self._raid_dps_taken_pc)
        self._hps_taken = _hps_taken(self._anub_hps_taken_ls, self._raid_hps_taken_jol)
        self._dps_done = _dps_done(self._raid_dps_done, self._new_raid_dps, self._raid_dps_pct_change)


    @property    # NEW
    def time_spent_in_phase3_initial(self) -> float:
        """
        ---\n
        The time spent in phase 3 of the encounter, in the `t₀` time span, prior to any DPS reallocation.\n
        ---\n
        """
        return self._time_spent_in_phase3_initial
    @time_spent_in_phase3_initial.setter
    def time_spent_in_phase3_initial(self, value: float) -> None:
        self._time_spent_in_phase3_initial = value

    @property    # NEW
    def time_spent_in_phase3_final(self) -> float:
        """
        ---\n
        The time spent in phase 3 of the encounter, in the `t₀ + Δt` time span, after reallocation of DPS from Anub'arak to Nerubian Burrowers.\n
        ---\n
        """
        return self._time_spent_in_phase3_final
    @time_spent_in_phase3_final.setter
    def time_spent_in_phase3_final(self, value: float) -> None:
        self._time_spent_in_phase3_final = value

    @property
    def dps_taken(self) -> "_dps_taken":
        """
        ---\n
        Information about DPS taken by:\n
        - Main Tank
        - Off Tanks
        - Raid (total)
        - Raid (from `Leeching Swarm`)
        - Raid (from `Penetrating Cold`)
        - Total (Main Tank + Off Tanks + Raid)
        ---\n
        𝐷𝑢𝑒 𝑡𝑜   →   `𝑀𝑒𝑙𝑒𝑒 (1)`  /  `𝑀𝑒𝑙𝑒𝑒 (2)`  /  `𝐹𝑟𝑒𝑒𝑧𝑖𝑛𝑔 𝑆𝑙𝑎𝑠ℎ (2)`  /  `𝐿𝑒𝑒𝑐ℎ𝑖𝑛𝑔 𝑆𝑤𝑎𝑟𝑚 (2)`  /  `𝑃𝑒𝑛𝑒𝑡𝑟𝑎𝑡𝑖𝑛𝑔 𝐶𝑜𝑙𝑑 (2)`\n
        𝐹𝑟𝑜𝑚     →   `𝑁𝑒𝑟𝑢𝑏𝑖𝑎𝑛 𝐵𝑢𝑟𝑟𝑜𝑤𝑒𝑟 (1)`  /  `𝐴𝑛𝑢𝑏'𝑎𝑟𝑎𝑘 (2)`\n
        ---\n
        """
        return self._dps_taken
    @dps_taken.setter
    def dps_taken(self, value: "_dps_taken") -> None:
        self._dps_taken = value

    @property
    def hps_taken(self) -> "_hps_taken":
        """
        ---\n
        Information about HPS taken by:\n
        - Anub'arak (from `Leeching Swarm`)
        - Raid (from `Judgement of Light`)
        - Total (Anub'arak + Raid)
        ---\n
        𝐷𝑢𝑒 𝑡𝑜   →   `𝐿𝑒𝑒𝑐ℎ𝑖𝑛𝑔 𝑆𝑤𝑎𝑟𝑚 (1)`  /  `𝐽𝑢𝑑𝑔𝑒𝑚𝑒𝑛𝑡 𝑜𝑓 𝐿𝑖𝑔ℎ𝑡 (2)`\n
        𝐹𝑟𝑜𝑚     →   `𝐴𝑛𝑢𝑏'𝑎𝑟𝑎𝑘 (1)`  /  `𝑃𝑙𝑎𝑦𝑒𝑟𝑠 (2)`\n
        ---\n
        """
        return self._hps_taken
    @hps_taken.setter
    def hps_taken(self, value: "_hps_taken") -> None:
        self._hps_taken = value

    @property
    def dps_done(self) -> "_dps_done":
        """
        ---\n
        Information about DPS done:\n
        - By the raid to Anub'arak (original)
        - By the raid to Anub'arak (after reallocation)
        - Percentage change in raid DPS to Anub'arak
        ---\n
        𝐷𝑢𝑒 𝑡𝑜   →   `𝑀𝑒𝑙𝑒𝑒`  /  `𝑆𝑝𝑒𝑙𝑙𝑠`\n
        𝐹𝑟𝑜𝑚     →   `𝑃𝑙𝑎𝑦𝑒𝑟𝑠`\n
        𝑇𝑎𝑟𝑔𝑒𝑡   →   `𝐴𝑛𝑢𝑏'𝑎𝑟𝑎𝑘`\n
        ---\n
        """
        return self._dps_done
    @dps_done.setter
    def dps_done(self, value: "_dps_done") -> None:
        self._dps_done = value
    
    @property
    def burrower_dps_added(self) -> float:
        """
        ---\n
        The dps gained by removing dps on Anub'arak.\n
        ---\n
        𝐷𝑢𝑒 𝑡𝑜   →   `𝑀𝑒𝑙𝑒𝑒`  /  `𝑆𝑝𝑒𝑙𝑙𝑠`\n
        𝐹𝑟𝑜𝑚     →   `𝑃𝑙𝑎𝑦𝑒𝑟`\n
        𝑇𝑎𝑟𝑔𝑒𝑡   →   `𝑁𝑒𝑟𝑢𝑏𝑖𝑎𝑛 𝐵𝑢𝑟𝑟𝑜𝑤𝑒𝑟`\n
        ---\n
        """
        return self._burrower_dps_added
    @burrower_dps_added.setter
    def burrower_dps_added(self, value: float) -> None:
        self._burrower_dps_added = value

    @property
    def anubarak_dps_lost(self) -> float:
        """
        ---\n
        The dps lost by redirecting damage from Anub'arak to Nerubian Burrowers.\n
        ---\n
        𝐷𝑢𝑒 𝑡𝑜   →   `𝑀𝑒𝑙𝑒𝑒`  /  `𝑆𝑝𝑒𝑙𝑙𝑠`\n
        𝐹𝑟𝑜𝑚     →   `𝑃𝑙𝑎𝑦𝑒𝑟`\n
        𝑇𝑎𝑟𝑔𝑒𝑡   →   `𝐴𝑛𝑢𝑏'𝑎𝑟𝑎𝑘`\n
        ---\n
        """
        return self._anubarak_dps_lost
    @anubarak_dps_lost.setter
    def anubarak_dps_lost(self, value: float) -> None:
        self._anubarak_dps_lost = value

    @property
    def time_added_to_phase3(self) -> float:
        """
        ---\n
        The amount of time added to Phase 3 by redirecting damage from Anub'arak to Nerubian Burrowers.\n
        ---\n
        𝐷𝑢𝑒 𝑡𝑜   →   `𝑀𝑒𝑙𝑒𝑒`  /  `𝑆𝑝𝑒𝑙𝑙𝑠`\n
        𝐹𝑟𝑜𝑚     →   `𝑃𝑙𝑎𝑦𝑒𝑟`\n
        𝑇𝑎𝑟𝑔𝑒𝑡   →   `𝐴𝑛𝑢𝑏'𝑎𝑟𝑎𝑘`\n
        ---\n
        """
        return self._time_added_to_phase3
    @time_added_to_phase3.setter
    def time_added_to_phase3(self, value: float) -> None:
        self._time_added_to_phase3 = value

    @property
    def time_added_to_phase3_pct_change(self) -> float:
        """
        ---\n
        The percent change in the duration of phase 3, caused by redirecting damage from Anub'arak to Nerubian Burrowers.\n
        Note a positive value indicates an increase in the duration of phase 3.\n
        ---\n
        𝐷𝑢𝑒 𝑡𝑜   →   `𝑀𝑒𝑙𝑒𝑒`  /  `𝑆𝑝𝑒𝑙𝑙𝑠`\n
        𝐹𝑟𝑜𝑚     →   `𝑃𝑙𝑎𝑦𝑒𝑟`\n
        𝑇𝑎𝑟𝑔𝑒𝑡   →   `𝐴𝑛𝑢𝑏'𝑎𝑟𝑎𝑘`\n
        ---\n
        """
        return self._time_added_pct_change
    @time_added_to_phase3_pct_change.setter
    def time_added_to_phase3_pct_change(self, value: float) -> None:
        self._time_added_pct_change = value

    @property
    def total_damage_saved_ot(self) -> float:
        """
        ---\n
        The total damage saved on the (2) off tanks by redirecting damage from Anub'arak to Nerubian Burrowers.\n
        ---\n
        𝐷𝑢𝑒 𝑡𝑜   →   `𝑀𝑒𝑙𝑒𝑒`  /  `𝑆𝑝𝑒𝑙𝑙𝑠`\n
        𝐹𝑟𝑜𝑚     →   `𝑃𝑙𝑎𝑦𝑒𝑟`\n
        𝑇𝑎𝑟𝑔𝑒𝑡   →   `𝑁𝑒𝑟𝑢𝑏𝑖𝑎𝑛 𝐵𝑢𝑟𝑟𝑜𝑤𝑒𝑟`\n
        ---\n
        """
        return self._total_ot_damage_saved
    @total_damage_saved_ot.setter
    def total_damage_saved_ot(self, value: float) -> None:
        self._total_ot_damage_saved = value

    @property
    def total_damage_added_mt(self) -> float:
        """
        ---\n
        The total damage added to the main tank by redirecting damage from Anub'arak to Nerubian Burrowers.\n
        ---\n
        𝐷𝑢𝑒 𝑡𝑜   →   `𝑀𝑒𝑙𝑒𝑒`  /  `𝐹𝑟𝑒𝑒𝑧𝑖𝑛𝑔 𝑆𝑙𝑎𝑠ℎ`\n
        𝐹𝑟𝑜𝑚     →   `𝐴𝑛𝑢𝑏'𝑎𝑟𝑎𝑘`\n
        𝑇𝑎𝑟𝑔𝑒𝑡   →   `𝑁𝑒𝑟𝑢𝑏𝑖𝑎𝑛 𝐵𝑢𝑟𝑟𝑜𝑤𝑒𝑟`\n
        ---\n
        """
        return self._total_mt_damage_added
    @total_damage_added_mt.setter
    def total_damage_added_mt(self, value: float) -> None:
        self._total_mt_damage_added = value

    @property
    def total_damage_added_raid_PC(self) -> float:
        """
        ---\n
        The total damage added to the entire raid by redirecting damage from Anub'arak to Nerubian Burrowers.\n
        ---\n
        𝐷𝑢𝑒 𝑡𝑜   →   `𝑃𝑒𝑛𝑒𝑡𝑟𝑎𝑡𝑖𝑛𝑔 𝐶𝑜𝑙𝑑`\n
        𝐹𝑟𝑜𝑚     →   `𝐴𝑛𝑢𝑏'𝑎𝑟𝑎𝑘`\n
        𝑇𝑎𝑟𝑔𝑒𝑡   →   `𝑃𝑙𝑎𝑦𝑒𝑟𝑠`\n
        ---\n
        """
        return self._total_pc_damage_added
    @total_damage_added_raid_PC.setter
    def total_damage_added_raid_PC(self, value: float) -> None:
        self._total_pc_damage_added = value

    @property
    def total_damage_added_raid_LS(self) -> float:
        """
        ---\n
        The total damage added to the entire raid by redirecting damage from Anub'arak to Nerubian Burrowers.\n
        ---\n
        𝐷𝑢𝑒 𝑡𝑜   →   `𝐿𝑒𝑒𝑐ℎ𝑖𝑛𝑔 𝑆𝑤𝑎𝑟𝑚`\n
        𝐹𝑟𝑜𝑚     →   `𝐴𝑛𝑢𝑏'𝑎𝑟𝑎𝑘`\n
        𝑇𝑎𝑟𝑔𝑒𝑡   →   `𝑃𝑙𝑎𝑦𝑒𝑟𝑠`\n
        ---\n
        """
        return self._gross_ls_damage_added
    @total_damage_added_raid_LS.setter
    def total_damage_added_raid_LS(self, value: float) -> None:
        self._gross_ls_damage_added = value

    @property
    def net_damage_added_raid_LS(self) -> float:
        """
        ---\n
        The net damage added to the entire raid by redirecting damage from Anub'arak to Nerubian Burrowers, after healing from `Judgement of Light`.\n
        ---\n
        𝐷𝑢𝑒 𝑡𝑜   →   `𝐿𝑒𝑒𝑐ℎ𝑖𝑛𝑔 𝑆𝑤𝑎𝑟𝑚 (1)`  /  `𝐽𝑢𝑑𝑔𝑒𝑚𝑒𝑛𝑡 𝑜𝑓 𝐿𝑖𝑔ℎ𝑡 (2)`\n
        𝐹𝑟𝑜𝑚     →   `𝐴𝑛𝑢𝑏'𝑎𝑟𝑎𝑘 (1)`  /  `𝑃𝑎𝑙𝑎𝑑𝑖𝑛𝑠 (2)`\n
        𝑇𝑎𝑟𝑔𝑒𝑡   →   `𝑃𝑙𝑎𝑦𝑒𝑟𝑠`\n
        ---\n
        """
        return self._net_ls_damage_added
    @net_damage_added_raid_LS.setter
    def net_damage_added_raid_LS(self, value: float) -> None:
        self._net_ls_damage_added = value

    @property
    def net_change_in_passive_damage_taken(self) -> float:
        """
        ---\n
        The net change in passive damage taken by the entire raid, after redirecting damage from Anub'arak to Nerubian Burrowers.\n
        ---\n
        𝐷𝑢𝑒 𝑡𝑜   →   `𝐿𝑒𝑒𝑐ℎ𝑖𝑛𝑔 𝑆𝑤𝑎𝑟𝑚`\n
        𝐹𝑟𝑜𝑚     →   `𝐴𝑛𝑢𝑏'𝑎𝑟𝑎𝑘`\n
        𝑇𝑎𝑟𝑔𝑒𝑡   →   `𝑃𝑙𝑎𝑦𝑒𝑟𝑠`\n
        ---\n
        """
        return self._net_increase_decrease_in_passive_damage_taken
    @net_change_in_passive_damage_taken.setter
    def net_change_in_passive_damage_taken(self, value: float) -> None:
        self._net_increase_decrease_in_passive_damage_taken = value

    @property
    def net_change_in_direct_damage_taken(self) -> float:
        """
        ---\n
        The net change in direct damage taken by the entire raid, after redirecting damage from Anub'arak to Nerubian Burrowers.\n
        ---\n
        𝐷𝑢𝑒 𝑡𝑜   →   `𝑀𝑒𝑙𝑒𝑒 (1)`  /  `𝑀𝑒𝑙𝑒𝑒 (2)`  /  `𝐹𝑟𝑒𝑒𝑧𝑖𝑛𝑔 𝑆𝑙𝑎𝑠ℎ (2)`  /  `𝑃𝑒𝑛𝑒𝑡𝑟𝑎𝑡𝑖𝑛𝑔 𝐶𝑜𝑙𝑑 (2)`\n
        𝐹𝑟𝑜𝑚     →   `𝑁𝑒𝑟𝑢𝑏𝑖𝑎𝑛 𝐵𝑢𝑟𝑟𝑜𝑤𝑒𝑟 (1)`  /  `𝐴𝑛𝑢𝑏'𝑎𝑟𝑎𝑘 (2)`\n
        𝑇𝑎𝑟𝑔𝑒𝑡   →   `𝑃𝑙𝑎𝑦𝑒𝑟𝑠`\n
        ---\n
        """
        return self._net_increase_decrease_in_immediate_damage_taken
    @net_change_in_direct_damage_taken.setter
    def net_change_in_direct_damage_taken(self, value: float) -> None:
        self._net_increase_decrease_in_immediate_damage_taken = value
    

    def summarize(self) -> None:
        """
        Prints a summary of the analysis.
        """
        richprint("                                  [magenta]PHASE3 MAIN ABILITIES OVERVIEW  --  AVGERAGED VALUES[/magenta]    ")
        print("                              ------------------------------------------------------------")
        rprints(30, f"OT DPS Taken (Burrower Melee): [white]........[/white] {self.dps_taken.off_tanks:,.3f} dps")
        rprints(30, f"MT DPS Taken (Anub Melee + FS): [white].......[/white] {self.dps_taken.main_tank:,.3f} dps\n")
        rprints(30, f"Raid DPS Taken (Leeching Swarm): [white]......[/white] {self.dps_taken.raid_LS:,.2f} dps")
        rprints(30, f"Raid DPS Taken (Penetrating Cold): [white]....[/white] {self.dps_taken.raid_PC:,.3f} dps\n")
        rprints(30, f"Raid DPS Done (Anub'arak Only): [white].......[/white] {self.dps_done.raid1:,.1f} dps")
        rprints(30, f"Anub HPS Taken (Leeching Swarm): [white]......[/white] {self.hps_taken.anubarak:,.2f} hps")
        rprints(30, f"Raid HPS Taken (Judgement of Light): [white]..[/white] {self.hps_taken.raid:,.3f} hps")
        print("                              ------------------------------------------------------------\n\n\n\n")

        richprint("                                         [magenta]PARAMETERS AFFECTING DAMAGE DONE/TAKEN[/magenta]    ")
        print("                                     ----------------------------------------------")
        rprints(37, f"Burrower DPS Added: [white].......[/white] {self.burrower_dps_added:,.1f} dps")
        rprints(37, f"Anub'arak DPS Lost: [white].......[/white] {self.anubarak_dps_lost:,.1f} dps\n")
        rprints(37, f"New Raid DPS (Anub): [white]......[/white] {self.dps_done.raid2:,.0f} dps")
        rprints(37, f"Raid DPS (% change): [white]......[/white] {self.dps_done.raid_pct_change:,.4f} pct\n")
        rprints(37, f"Time Added to Phase3: [white].....[/white] {self.time_added_to_phase3:,.5f} sec")
        rprints(37, f"Time Added (% change): [white]....[/white] {self.time_added_to_phase3_pct_change:,.5f} pct")
        print("                                     ----------------------------------------------\n\n\n\n")

        richprint("                                          [magenta]OVERALL EFFECT ON DAMAGE SAVED/ADDED[/magenta]  ")
        print("                                   ---------------------------------------------------")
        rprints(35, f"Total OT Damage Saved: [white].......[/white] {self.total_damage_saved_ot:,.2f} dps\n")
        rprints(35, f"Total MT Damage Added: [white].......[/white] {self.total_damage_added_mt:,.2f} dps")
        rprints(35, f"Total PC Damage Added: [white].......[/white] {self.total_damage_added_raid_PC:,.2f} dps\n")
        rprints(35, f"Net LS Damage Added: [white].........[/white] {self.net_damage_added_raid_LS:,.1f} dps")
        rprints(35, f"Gross LS Damage Added: [white].......[/white] {self.total_damage_added_raid_LS:,.1f} dps")
        print("                                   ---------------------------------------------------\n\n\n\n")

        rprint(f"Net Increase/Decrease In Passive Damage [bold]Taken[/bold] (LS damage gained - JoL damage saved): [white]........[/white] {'[bold red]+ [/bold red]' if self.net_change_in_passive_damage_taken >= 0 else '[bold green]- [/bold green]'}{self.net_change_in_passive_damage_taken:,.2f} damage")
        rprint(f"Net Increase/Decrease In Immediate Damage [bold]Taken[/bold] (MT & PC damage gained - OT damage saved): [white]..[/white] {'[bold red]+  [/bold red]' if self.net_change_in_direct_damage_taken >= 0 else '[bold green]-  [/bold green]'}{self.net_change_in_direct_damage_taken:,.2f} damage\n")










def analyze(REPORT_CODE: str, ANUBARAK_DPS_LOST: float, BURROWER_DPS_ADDED: float, print_report: bool = False, log: bool = False) -> "Analysis":
    """
    For the pull resulting in a kill of Anub'arak in the given `REPORT_CODE`, determines the effect of:\n
    Adding `BURROWER_DPS_ADDED` DPS to Nerubian Burrowers in exchange for `ANUBARAK_DPS_LOST` less DPS to Anub'arak.
    """
    fights_and_participants = get_fights_and_participants_info(REPORT_CODE)
    anubarak_kill = get_fight(fights_and_participants, boss_name="Anub'arak")
    # friendly_damage_taken = get_damage_taken_data(REPORT_CODE, anubarak_kill, enemy=anubarak_kill.get_enemy_by_name("Nerubian Burrower"), ability=1)  # Melee
    leeching_swarm_damage_taken = get_damage_taken_data(REPORT_CODE, anubarak_kill, enemy=anubarak_kill.get_enemy_by_name("Anub'arak"), ability=66240)   # Leeching Swarm
    leeching_swarm_healing_done = get_enemy_healing_done_data(REPORT_CODE, anubarak_kill, enemy=anubarak_kill.get_enemy_by_name("Anub'arak"), ability=66125)   # Leeching Swarm
    
    p3_start_time_seconds = leeching_swarm_healing_done.series[0].timestamps_adjusted[[i for i in range(len(leeching_swarm_healing_done.series[0].values)) if leeching_swarm_healing_done.series[0].values[i] > 0][0]] / 1000
    p3_start_timestamp = leeching_swarm_healing_done.series[0].timestamps[[i for i in range(len(leeching_swarm_healing_done.series[0].values)) if leeching_swarm_healing_done.series[0].values[i] > 0][0]]
    p3_end_time_seconds = leeching_swarm_healing_done.series[0].timestamps_adjusted[-1] / 1000
    # p3_end_timestamp = leeching_swarm_healing_done.series[0].timestamps[-1]
    
    p3_duration_seconds = p3_end_time_seconds - p3_start_time_seconds

    burrower_melee_damage_taken = get_damage_taken_data(REPORT_CODE, anubarak_kill, enemy=anubarak_kill.get_enemy_by_name("Nerubian Burrower"), ability=1, start_time=int(p3_start_timestamp))
    burrower_melee_damage_taken_series = []
    for s in burrower_melee_damage_taken.series:
        if s.name != "Total": burrower_melee_damage_taken_series.append(s)
    burrower_melee_damage_taken_series = sorted(burrower_melee_damage_taken_series, key=lambda s: s.total, reverse=True)
    off_tank_damage_series = burrower_melee_damage_taken_series[:2]

    DPS_taken_OT = off_tank_damage_series[0].total/p3_duration_seconds + off_tank_damage_series[1].total/p3_duration_seconds

    leeching_swarm_damage_taken_series = leeching_swarm_damage_taken.series[:-1]
    total_leeching_swarm_damage = sum([s.total for s in leeching_swarm_damage_taken_series])
    total_leeching_swarm_dps = total_leeching_swarm_damage / p3_duration_seconds
    leeching_swarm_healing_done_series = leeching_swarm_healing_done.series[:-1]
    # total_leeching_swarm_healing = sum([s.total for s in leeching_swarm_healing_done_series])
    total_leeching_swarm_hps = sum([s.total for s in leeching_swarm_healing_done_series]) / p3_duration_seconds

    DPS_taken_LS = total_leeching_swarm_dps

    raid_damage_done_to_boss = get_damage_done_data(REPORT_CODE, anubarak_kill, start_time=int(p3_start_timestamp), enemy=anubarak_kill.get_enemy_by_name("Anub'arak"))
    raid_damage_done_to_boss_series = raid_damage_done_to_boss.series[:-1]
    raid_damage_done_to_boss = sum([s.total for s in raid_damage_done_to_boss_series])

    raid_damage_done_to_boss_dps = raid_damage_done_to_boss / p3_duration_seconds

    penetrating_cold_damage_taken = get_damage_taken_data(REPORT_CODE, anubarak_kill, start_time=int(p3_start_timestamp), enemy=anubarak_kill.get_enemy_by_name("Anub'arak"), ability=66013)   # Penetrating Cold
    penetrating_cold_damage_taken_series = penetrating_cold_damage_taken.series[:-1]
    # total_penetrating_cold_damage_taken = sum([s.total for s in penetrating_cold_damage_taken_series])
    total_penetrating_cold_dps = sum([s.total for s in penetrating_cold_damage_taken_series]) / p3_duration_seconds

    DPS_taken_PC = total_penetrating_cold_dps

    anub_melee_damage_taken = get_damage_taken_data(REPORT_CODE, anubarak_kill, start_time=int(p3_start_timestamp), enemy=anubarak_kill.get_enemy_by_name("Anub'arak"), ability=1)  # Melee
    anub_melee_damage_taken_series = []
    for s in anub_melee_damage_taken.series:
        if s.name != "Total": anub_melee_damage_taken_series.append(s)
    anub_melee_damage_taken_series = sorted(anub_melee_damage_taken_series, key=lambda s: s.total, reverse=True)
    main_tank_anub_melee_damage_taken_series = anub_melee_damage_taken_series[0]
    # total_damage_taken_MT_melee = main_tank_anub_melee_damage_taken_series.total
    DPS_taken_MT_melee = main_tank_anub_melee_damage_taken_series.total/p3_duration_seconds
    anub_freezing_slash_damage_taken = get_damage_taken_data(REPORT_CODE, anubarak_kill, start_time=int(p3_start_timestamp), enemy=anubarak_kill.get_enemy_by_name("Anub'arak"), ability=66012)  # Melee
    anub_freezing_slash_damage_taken_series = []
    for s in anub_freezing_slash_damage_taken.series:
        if s.name != "Total": anub_freezing_slash_damage_taken_series.append(s)
    anub_freezing_slash_damage_taken_series = sorted(anub_freezing_slash_damage_taken_series, key=lambda s: s.total, reverse=True)
    main_tank_anub_freezing_slash_damage_taken_series = anub_freezing_slash_damage_taken_series[0]
    # total_damage_taken_MT_freezing_slash = main_tank_anub_freezing_slash_damage_taken_series.total
    DPS_taken_MT_freezing_slash = main_tank_anub_freezing_slash_damage_taken_series.total/p3_duration_seconds

    DPS_taken_MT = DPS_taken_MT_melee + DPS_taken_MT_freezing_slash

    judgement_healing_done = get_friendly_healing_done_data(REPORT_CODE, anubarak_kill, start_time=int(p3_start_timestamp), ability=20267, anubarak=True)   # Judgement of Light
    judgement_healing_done_series = judgement_healing_done.series[:-1]
    total_judgement_healing = sum([s.total for s in judgement_healing_done_series])
    total_judgement_hps = total_judgement_healing / p3_duration_seconds

    HPS_taken_JoL = total_judgement_hps

    T_P3 = -8_157_825 / (total_leeching_swarm_hps - raid_damage_done_to_boss_dps)
    T_P3_2 = -8_157_825 / (total_leeching_swarm_hps - (raid_damage_done_to_boss_dps-ANUBARAK_DPS_LOST))
    DELTA_T_P3 = T_P3_2 - T_P3

    DAMAGE_SAVED_OT = DPS_taken_OT * (  DELTA_T_P3  +  30*( 1 - (97000/(97000+BURROWER_DPS_ADDED)) )  )
    DAMAGE_GAINED_MT = DPS_taken_MT * DELTA_T_P3
    DAMAGE_GAINED_PC = DPS_taken_PC * DELTA_T_P3
    DAMAGE_GAINED_LS = DPS_taken_LS * DELTA_T_P3
    NET_DAMAGE_GAINED_LS = DAMAGE_GAINED_LS - (HPS_taken_JoL * DELTA_T_P3)
    TOTAL_IMMEDIATE_DAMAGE_GAINED = DAMAGE_GAINED_MT + DAMAGE_GAINED_PC - DAMAGE_SAVED_OT
    TOTAL_LS_DAMAGE_NOT_HEALED = NET_DAMAGE_GAINED_LS

        
    if print_report:
        rprint(f"P3 Start: [white].....[/white] {p3_start_time_seconds:.2f} seconds  ({p3_start_timestamp:.0f})")
        rprint(f"P3 End: [white].......[/white] {p3_end_time_seconds:.2f} seconds  ({p3_end_timestamp:.0f})")
        rprint(f"P3 Duration: [white]..[/white] {p3_duration_seconds:.2f} seconds  ( {p3_end_timestamp - p3_start_timestamp:.0f} )\n\n\n\n")

        richprint("                                  [magenta]PHASE3 MAIN ABILITIES OVERVIEW  --  AVGERAGED VALUES[/magenta]    ")
        print("                              ------------------------------------------------------------")
        rprints(30, f"OT DPS Taken (Burrower Melee): [white]........[/white] {DPS_taken_OT:,.3f} dps")
        rprints(30, f"MT DPS Taken (Anub Melee + FS): [white].......[/white] {DPS_taken_MT:,.3f} dps\n")
        rprints(30, f"Raid DPS Taken (Leeching Swarm): [white]......[/white] {DPS_taken_LS:,.2f} dps")
        rprints(30, f"Raid DPS Taken (Penetrating Cold): [white]....[/white] {DPS_taken_PC:,.3f} dps\n")
        rprints(30, f"Raid DPS Done (Anub'arak Only): [white].......[/white] {raid_damage_done_to_boss_dps:,.1f} dps")
        rprints(30, f"Anub HPS Taken (Leeching Swarm): [white]......[/white] {total_leeching_swarm_hps:,.2f} hps")
        rprints(30, f"Raid HPS Taken (Judgement of Light): [white]..[/white] {total_judgement_hps:,.3f} hps")
        print("                              ------------------------------------------------------------\n\n\n\n")

        richprint("                                         [magenta]PARAMETERS AFFECTING DAMAGE DONE/TAKEN[/magenta]    ")
        print("                                     ----------------------------------------------")
        rprints(37, f"Burrower DPS Added: [white].......[/white] {BURROWER_DPS_ADDED:,.1f} dps")
        rprints(37, f"Anub'arak DPS Lost: [white].......[/white] {ANUBARAK_DPS_LOST:,.1f} dps\n")
        rprints(37, f"New Raid DPS (Anub): [white]......[/white] {raid_damage_done_to_boss_dps-ANUBARAK_DPS_LOST:,.0f} dps")
        rprints(37, f"Raid DPS (% change): [white]......[/white] {(((raid_damage_done_to_boss_dps-ANUBARAK_DPS_LOST)-raid_damage_done_to_boss_dps)/raid_damage_done_to_boss_dps)*100:,.4f} pct\n")
        rprints(37, f"Time Added to Phase3: [white].....[/white] {DELTA_T_P3:,.5f} sec")
        rprints(37, f"Time Added (% change): [white]....[/white] {(DELTA_T_P3/T_P3)*100:,.5f} pct")
        print("                                     ----------------------------------------------\n\n\n\n")

        richprint("                                          [magenta]OVERALL EFFECT ON DAMAGE SAVED/ADDED[/magenta]  ")
        print("                                   ---------------------------------------------------")
        rprints(35, f"Total OT Damage Saved: [white].......[/white] {DAMAGE_SAVED_OT:,.2f} dps\n")
        rprints(35, f"Total MT Damage Added: [white].......[/white] {DAMAGE_GAINED_MT:,.2f} dps")
        rprints(35, f"Total PC Damage Added: [white].......[/white] {DAMAGE_GAINED_PC:,.2f} dps\n")
        rprints(35, f"Net LS Damage Added: [white].........[/white] {NET_DAMAGE_GAINED_LS:,.1f} dps")
        rprints(35, f"Gross LS Damage Added: [white].......[/white] {DAMAGE_GAINED_LS:,.1f} dps")
        print("                                   ---------------------------------------------------\n\n\n\n")

        rprint(f"Net Increase/Decrease In Passive Damage [bold]Taken[/bold] (LS damage gained - JoL damage saved): [white]........[/white] {'[bold red]+ [/bold red]' if TOTAL_LS_DAMAGE_NOT_HEALED >= 0 else '[bold green]- [/bold green]'}{TOTAL_LS_DAMAGE_NOT_HEALED:,.2f} damage")
        rprint(f"Net Increase/Decrease In Immediate Damage [bold]Taken[/bold] (MT & PC damage gained - OT damage saved): [white]..[/white] {'[bold red]+  [/bold red]' if TOTAL_IMMEDIATE_DAMAGE_GAINED >= 0 else '[bold green]-  [/bold green]'}{TOTAL_IMMEDIATE_DAMAGE_GAINED:,.2f} damage\n")

    if log:
        with open(f"logs/{ANUBARAK_DPS_LOST}_{BURROWER_DPS_ADDED}.txt", "w", encoding="utf-8") as f:
            f.write("Anub'arak DPS Lost: " + str(ANUBARAK_DPS_LOST) + "\n")
            f.write("Burrower DPS Added: " + str(BURROWER_DPS_ADDED) + "\n\n")
            f.write("OT DPS Taken (Burrower Melee): " + str(DPS_taken_OT) + "\n")
            f.write("MT DPS Taken (Anub Melee + FS): " + str(DPS_taken_MT) + "\n\n")
            f.write("Raid DPS Taken (Leeching Swarm): " + str(DPS_taken_LS) + "\n")
            f.write("Raid DPS Taken (Penetrating Cold): " + str(DPS_taken_PC) + "\n\n")
            f.write("Raid DPS Done (Anub'arak Only): " + str(raid_damage_done_to_boss_dps) + "\n")
            f.write("Anub HPS Taken (Leeching Swarm): " + str(total_leeching_swarm_hps) + "\n")
            f.write("Raid HPS Taken (Judgement of Light): " + str(total_judgement_hps) + "\n\n\n\n")
            f.write("Burrower DPS Added: " + str(BURROWER_DPS_ADDED) + "\n")
            f.write("Anub'arak DPS Lost: " + str(ANUBARAK_DPS_LOST) + "\n\n")
            f.write("New Raid DPS (Anub): " + str(raid_damage_done_to_boss_dps-ANUBARAK_DPS_LOST) + "\n")
            f.write("Raid DPS (% change): " + str((((raid_damage_done_to_boss_dps-ANUBARAK_DPS_LOST)-raid_damage_done_to_boss_dps)/raid_damage_done_to_boss_dps)*100) + "\n\n")
            f.write("Time Added to Phase3: " + str(DELTA_T_P3) + "\n")
            f.write("Time Added (% change): " + str((DELTA_T_P3/T_P3)*100) + "\n\n\n\n")
            f.write("Total OT Damage Saved: " + str(DAMAGE_SAVED_OT) + "\n\n")
            f.write("Total MT Damage Added: " + str(DAMAGE_GAINED_MT) + "\n")
            f.write("Total PC Damage Added: " + str(DAMAGE_GAINED_PC) + "\n\n")
            f.write("Net LS Damage Added: " + str(NET_DAMAGE_GAINED_LS) + "\n")
            f.write("Gross LS Damage Added: " + str(DAMAGE_GAINED_LS) + "\n\n\n\n")
            f.write("Net Increase/Decrease In Passive Damage Taken (LS damage gained - JoL damage saved): " + ('+ ' if TOTAL_LS_DAMAGE_NOT_HEALED >= 0 else '- ') + str(TOTAL_LS_DAMAGE_NOT_HEALED) + " damage\n")
            f.write("Net Increase/Decrease In Immediate Damage Taken (MT & PC damage gained - OT damage saved): " + ('+  ' if TOTAL_IMMEDIATE_DAMAGE_GAINED >= 0 else '-  ') + str(TOTAL_IMMEDIATE_DAMAGE_GAINED) + " damage\n\n\n\n")

    
    return Analysis(
        DPS_taken_OT, 
        DPS_taken_MT, 
        DPS_taken_LS, 
        DPS_taken_PC, 
        raid_damage_done_to_boss_dps, 
        total_leeching_swarm_hps, 
        total_judgement_hps, 
        BURROWER_DPS_ADDED, 
        ANUBARAK_DPS_LOST, 
        raid_damage_done_to_boss_dps-ANUBARAK_DPS_LOST, 
        (((raid_damage_done_to_boss_dps-ANUBARAK_DPS_LOST)-raid_damage_done_to_boss_dps)/raid_damage_done_to_boss_dps)*100, 
        DELTA_T_P3, 
        (DELTA_T_P3/T_P3)*100, 
        DAMAGE_SAVED_OT, 
        DAMAGE_GAINED_MT, 
        DAMAGE_GAINED_PC, 
        NET_DAMAGE_GAINED_LS, 
        DAMAGE_GAINED_LS, 
        TOTAL_LS_DAMAGE_NOT_HEALED, 
        TOTAL_IMMEDIATE_DAMAGE_GAINED,
        T_P3,                                # NEW
        T_P3 + DELTA_T_P3,                   # NEW
    )
    
