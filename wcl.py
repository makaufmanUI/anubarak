"""
wcl.py
~~~~~~

Date: 08/09/2023 05:11
"""
from imports import *
from stuff import view

ANUBARAK_HP_P3 = 8_157_825



def request(url: str) -> dict:
    """
    Makes a `GET` request to the specified URL and returns a `dict` / JSON object.
    """
    report_code = [x for x in url.split('/') if len(x) == 16 and not x.islower()][0]
    headers = {
        "referer": f"https://classic.warcraftlogs.com/reports/{report_code}", "authority": "classic.warcraftlogs.com", 
        "cookie": "usprivacy=1---; ad_clicker=false;", "accept-language": "en-US,en;q=0.9", "x-requested-with": "XMLHttpRequest",
        "accept": "application/json, text/javascript, */*; q=0.01", "sec-ch-ua-platform": "\"Windows\"", "sec-ch-ua-mobile": "?0",
        "sec-ch-ua": "\"Not/A", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        rprint(f"\n\nError:\n{response.status_code}\n\n")
        return {}
    return json.loads(response.text)



def get_fights_and_participants_info(report_code: str) -> dict:
    """
    """
    return request(f"https://classic.warcraftlogs.com/reports/fights-and-participants/{report_code}/1")



def get_fight(fights_and_participants_info: dict, fight_id: int = None, boss_name: str = None) -> NamedTuple:
    """
    """
    if fight_id is None and boss_name is None:
        raise ValueError("Either `fight_id` or `boss_name` must be specified.")
    from stuff import view
    enemies = fights_and_participants_info['enemies']
    Enemy = namedtuple(
        "Enemy",
        ["name", "report_id", "guid", "type", "fight_ids", "instance_counts", "instance_group_counts", "boss_ids", "view", "to_dict", "attributes"]
    )
    FightInfo = namedtuple(
        "FightInfo",
        ["fight_id", "boss_id", "start_time", "end_time", "boss_name", "zone_id", "zone_name", "raid_size", "was_kill", "enemies", "view", "to_dict", "attributes", "get_enemy_by_name"]
    )
    if fight_id is not None:
        matches = [x for x in fights_and_participants_info['fights'] if int(x['id']) == fight_id]
        if len(matches) == 0:
            raise ValueError(f"No fight with ID '{fight_id}' found in fights.")
        elif len(matches) == 1:
            fight_info = matches[0]
            enemies = [e for e in enemies if str(fight_id) in e['fights'].split('.') and int(e['guid']) != 34660]
            for e in enemies:
                e['fights'] = [int(x) for x in e['fights'].split('.') if x != '']
                e['bosses'] = [int(x) for x in e['bosses'].split('.') if x != '']
            enemies = [Enemy(e['name'], e['id'], e['guid'], e['type'], e['fights'], e['instanceCounts'], None if 'instanceGroupCounts' not in e else e['instanceGroupCounts'], e['bosses'], lambda _=0: view({'name': e['name'], 'id': e['id'], 'guid': e['guid'], 'type': e['type'], 'fights': e['fights'], 'instanceCounts': e['instanceCounts'], 'instanceGroupCounts': None if 'instanceGroupCounts' not in e else e['instanceGroupCounts'], 'bosses': e['bosses']}), lambda _=0: {'name': e['name'], 'id': e['id'], 'guid': e['guid'], 'type': e['type'], 'fights': e['fights'], 'instanceCounts': e['instanceCounts'], 'instanceGroupCounts': None if 'instanceGroupCounts' not in e else e['instanceGroupCounts'], 'bosses': e['bosses']}, ["name", "report_id", "guid", "type", "fight_ids", "instance_counts", "instance_group_counts", "boss_ids", "view", "to_dict", "attributes"]) for e in enemies]
            d = {'fight_id': fight_info['id'], 'boss_id': fight_info['boss'], 'start_time': fight_info['start_time'], 'end_time': fight_info['end_time'], 'boss_name': fight_info['name'], 'zone_id': fight_info['zoneID'], 'zone_name': fight_info['zoneName'], 'raid_size': fight_info['size'], 'was_kill': fight_info['kill']==1, 'enemies': [e.to_dict() for e in enemies]}
            return FightInfo(fight_info['id'], fight_info['boss'], fight_info['start_time'], fight_info['end_time'], fight_info['name'], fight_info['zoneID'], fight_info['zoneName'], fight_info['size'], fight_info['kill']==1, enemies, lambda _=0: view(d), lambda _=0: d, ["fight_id", "boss_id", "start_time", "end_time", "boss_name", "zone_id", "zone_name", "raid_size", "was_kill", "enemies", "view", "to_dict", "attributes", "get_enemy_by_name"], lambda name: [e for e in enemies if e.name.lower() == name.lower()][0])
        else:
            raise ValueError(f"Multiple fights with ID '{fight_id}' found in fights.")
    elif boss_name is not None:
        matches = [x for x in fights_and_participants_info['fights'] if x['name'].lower() == boss_name.lower()]
        if len(matches) == 0:
            raise ValueError(f"No boss named '{boss_name}' found in fights.")
        elif len(matches) == 1:
            fight_info = matches[0]
            fight_id = fight_info['id']
            enemies = [e for e in enemies if str(fight_id) in e['fights'].split('.') and int(e['guid']) != 34660]
            for e in enemies:
                e['fights'] = [int(x) for x in e['fights'].split('.') if x != '']
                e['bosses'] = [int(x) for x in e['bosses'].split('.') if x != '']
            enemies = [Enemy(e['name'], e['id'], e['guid'], e['type'], e['fights'], e['instanceCounts'], None if 'instanceGroupCounts' not in e else e['instanceGroupCounts'], e['bosses'], lambda _=0: view({'name': e['name'], 'id': e['id'], 'guid': e['guid'], 'type': e['type'], 'fights': e['fights'], 'instanceCounts': e['instanceCounts'], 'instanceGroupCounts': None if 'instanceGroupCounts' not in e else e['instanceGroupCounts'], 'bosses': e['bosses']}), lambda _=0: {'name': e['name'], 'id': e['id'], 'guid': e['guid'], 'type': e['type'], 'fights': e['fights'], 'instanceCounts': e['instanceCounts'], 'instanceGroupCounts': None if 'instanceGroupCounts' not in e else e['instanceGroupCounts'], 'bosses': e['bosses']}, ["name", "report_id", "guid", "type", "fight_ids", "instance_counts", "instance_group_counts", "boss_ids", "view", "to_dict", "attributes"]) for e in enemies]
            d = {'fight_id': fight_info['id'], 'boss_id': fight_info['boss'], 'start_time': fight_info['start_time'], 'end_time': fight_info['end_time'], 'boss_name': fight_info['name'], 'zone_id': fight_info['zoneID'], 'zone_name': fight_info['zoneName'], 'raid_size': fight_info['size'], 'was_kill': fight_info['kill']==1, 'enemies': [e.to_dict() for e in enemies]}
            return FightInfo(fight_info['id'], fight_info['boss'], fight_info['start_time'], fight_info['end_time'], fight_info['name'], fight_info['zoneID'], fight_info['zoneName'], fight_info['size'], fight_info['kill']==1, enemies, lambda _=0: view(d), lambda _=0: d, ["fight_id", "boss_id", "start_time", "end_time", "boss_name", "zone_id", "zone_name", "raid_size", "was_kill", "enemies", "view", "to_dict", "attributes", "get_enemy_by_name"], lambda name: [e for e in enemies if e.name.lower() == name.lower()][0])
        else:
            for match in matches:
                if match['kill'] == 1:
                    fight_info = match
                    fight_id = fight_info['id']
                    enemies = [e for e in enemies if str(fight_id) in e['fights'].split('.') and int(e['guid']) != 34660]
                    for e in enemies:
                        e['fights'] = [int(x) for x in e['fights'].split('.') if x != '']
                        e['bosses'] = [int(x) for x in e['bosses'].split('.') if x != '']
                    enemies = [Enemy(e['name'], e['id'], e['guid'], e['type'], e['fights'], e['instanceCounts'], None if 'instanceGroupCounts' not in e else e['instanceGroupCounts'], e['bosses'], lambda _=0: view({'name': e['name'], 'id': e['id'], 'guid': e['guid'], 'type': e['type'], 'fights': e['fights'], 'instanceCounts': e['instanceCounts'], 'instanceGroupCounts': None if 'instanceGroupCounts' not in e else e['instanceGroupCounts'], 'bosses': e['bosses']}), lambda _=0: {'name': e['name'], 'id': e['id'], 'guid': e['guid'], 'type': e['type'], 'fights': e['fights'], 'instanceCounts': e['instanceCounts'], 'instanceGroupCounts': None if 'instanceGroupCounts' not in e else e['instanceGroupCounts'], 'bosses': e['bosses']}, ["name", "report_id", "guid", "type", "fight_ids", "instance_counts", "instance_group_counts", "boss_ids", "view", "to_dict", "attributes"]) for e in enemies]
                    d = {'fight_id': fight_info['id'], 'boss_id': fight_info['boss'], 'start_time': fight_info['start_time'], 'end_time': fight_info['end_time'], 'boss_name': fight_info['name'], 'zone_id': fight_info['zoneID'], 'zone_name': fight_info['zoneName'], 'raid_size': fight_info['size'], 'was_kill': fight_info['kill']==1, 'enemies': [e.to_dict() for e in enemies]}
                    return FightInfo(fight_info['id'], fight_info['boss'], fight_info['start_time'], fight_info['end_time'], fight_info['name'], fight_info['zoneID'], fight_info['zoneName'], fight_info['size'], fight_info['kill']==1, enemies, lambda _=0: view(d), lambda _=0: d, ["fight_id", "boss_id", "start_time", "end_time", "boss_name", "zone_id", "zone_name", "raid_size", "was_kill", "enemies", "view", "to_dict", "attributes", "get_enemy_by_name"], lambda name: [e for e in enemies if e.name.lower() == name.lower()][0])
            fight_info = matches[0]
            fight_id = fight_info['id']
            enemies = [e for e in enemies if str(fight_id) in e['fights'].split('.') and int(e['guid']) != 34660]
            for e in enemies:
                e['fights'] = [int(x) for x in e['fights'].split('.') if x != '']
                e['bosses'] = [int(x) for x in e['bosses'].split('.') if x != '']
            enemies = [Enemy(e['name'], e['id'], e['guid'], e['type'], e['fights'], e['instanceCounts'], None if 'instanceGroupCounts' not in e else e['instanceGroupCounts'], e['bosses'], lambda _=0: view({'name': e['name'], 'id': e['id'], 'guid': e['guid'], 'type': e['type'], 'fights': e['fights'], 'instanceCounts': e['instanceCounts'], 'instanceGroupCounts': None if 'instanceGroupCounts' not in e else e['instanceGroupCounts'], 'bosses': e['bosses']}), lambda _=0: {'name': e['name'], 'id': e['id'], 'guid': e['guid'], 'type': e['type'], 'fights': e['fights'], 'instanceCounts': e['instanceCounts'], 'instanceGroupCounts': None if 'instanceGroupCounts' not in e else e['instanceGroupCounts'], 'bosses': e['bosses']}, ["name", "report_id", "guid", "type", "fight_ids", "instance_counts", "instance_group_counts", "boss_ids", "view", "to_dict", "attributes"]) for e in enemies]
            d = {'fight_id': fight_info['id'], 'boss_id': fight_info['boss'], 'start_time': fight_info['start_time'], 'end_time': fight_info['end_time'], 'boss_name': fight_info['name'], 'zone_id': fight_info['zoneID'], 'zone_name': fight_info['zoneName'], 'raid_size': fight_info['size'], 'was_kill': fight_info['kill']==1, 'enemies': [e.to_dict() for e in enemies]}
            return FightInfo(fight_info['id'], fight_info['boss'], fight_info['start_time'], fight_info['end_time'], fight_info['name'], fight_info['zoneID'], fight_info['zoneName'], fight_info['size'], fight_info['kill']==1, enemies, lambda _=0: view(d), lambda _=0: d, ["fight_id", "boss_id", "start_time", "end_time", "boss_name", "zone_id", "zone_name", "raid_size", "was_kill", "enemies", "view", "to_dict", "attributes", "get_enemy_by_name"], lambda name: [e for e in enemies if e.name.lower() == name.lower()][0])



def get_damage_taken_data(report_code: str, fight: NamedTuple, start_time: int = None, enemy: NamedTuple = None, ability: int = 0) -> NamedTuple:
    """
    """
    if start_time is None:
        start_time = fight.start_time
    url = f"https://classic.warcraftlogs.com/reports/graph/damage-taken/{report_code}/{fight.fight_id}/{start_time}/{fight.end_time}" + \
          f"/source/0/0/{enemy.report_id if enemy is not None else 0}/0/0/{ability}/-1.0.-1.-1/0/Any/Any/2/0"
    r = request(url)
    Data = namedtuple("Data", ["start_time", "end_time", "series", "view", "to_dict", "attributes"])
    Series = namedtuple("Series", ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"])
    return Data(
        r['startTime'], r['endTime'],
        [Series(
            s['name'], s['id'], None if 'guid' not in s else int(s['guid']), s['type'], int(s['pointStart']), float(s['pointInterval']), None if 'total' not in s else float(s['total']), [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], [float(s['pointInterval']*i) for i in range(len(s['data']))], [float(s['data'][i]) for i in range(len(s['data']))],
            lambda _=0: view({'name': s['name'], 'id': s['id'], 'guid': None if 'guid' not in s else s['guid'], 'type': s['type'], 'start_time': s['pointStart'], 'interval': s['pointInterval'], 'total': None if 'total' not in s else s['total'], 'timestamps': [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], 'timestamps_adjusted': [float(s['pointInterval']*i) for i in range(len(s['data']))], 'values': [float(s['data'][i]) for i in range(len(s['data']))], 'attributes': ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]}),
            lambda _=0: {'name': s['name'], 'id': s['id'], 'guid': None if 'guid' not in s else s['guid'], 'type': s['type'], 'start_time': s['pointStart'], 'interval': s['pointInterval'], 'total': None if 'total' not in s else s['total'], 'timestamps': [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], 'timestamps_adjusted': [float(s['pointInterval']*i) for i in range(len(s['data']))], 'values': [float(s['data'][i]) for i in range(len(s['data']))], 'attributes': ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]},
            ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]
        ) for s in r['series']],
        lambda _=0: view({'start_time': r['startTime'], 'end_time': r['endTime'], 'series': [Series(
            s['name'], s['id'], None if 'guid' not in s else int(s['guid']), s['type'], int(s['pointStart']), float(s['pointInterval']), None if 'total' not in s else float(s['total']), [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], [float(s['pointInterval']*i) for i in range(len(s['data']))], [float(s['data'][i]) for i in range(len(s['data']))],
            lambda _=0: view({'name': s['name'], 'id': s['id'], 'guid': None if 'guid' not in s else s['guid'], 'type': s['type'], 'start_time': s['pointStart'], 'interval': s['pointInterval'], 'total': None if 'total' not in s else s['total'], 'timestamps': [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], 'timestamps_adjusted': [float(s['pointInterval']*i) for i in range(len(s['data']))], 'values': [float(s['data'][i]) for i in range(len(s['data']))], 'attributes': ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]}),
            lambda _=0: {'name': s['name'], 'id': s['id'], 'guid': None if 'guid' not in s else s['guid'], 'type': s['type'], 'start_time': s['pointStart'], 'interval': s['pointInterval'], 'total': None if 'total' not in s else s['total'], 'timestamps': [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], 'timestamps_adjusted': [float(s['pointInterval']*i) for i in range(len(s['data']))], 'values': [float(s['data'][i]) for i in range(len(s['data']))], 'attributes': ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]},
            ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]
        ).to_dict() for s in r['series']], 'attributes': ["start_time", "end_time", "series", "view", "to_dict", "attributes"]}),
        lambda _=0: {'start_time': r['startTime'], 'end_time': r['endTime'], 'series': [Series(
            s['name'], s['id'], None if 'guid' not in s else int(s['guid']), s['type'], int(s['pointStart']), float(s['pointInterval']), None if 'total' not in s else float(s['total']), [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], [float(s['pointInterval']*i) for i in range(len(s['data']))], [float(s['data'][i]) for i in range(len(s['data']))],
            lambda _=0: view({'name': s['name'], 'id': s['id'], 'guid': None if 'guid' not in s else s['guid'], 'type': s['type'], 'start_time': s['pointStart'], 'interval': s['pointInterval'], 'total': None if 'total' not in s else s['total'], 'timestamps': [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], 'timestamps_adjusted': [float(s['pointInterval']*i) for i in range(len(s['data']))], 'values': [float(s['data'][i]) for i in range(len(s['data']))], 'attributes': ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]}),
            lambda _=0: {'name': s['name'], 'id': s['id'], 'guid': None if 'guid' not in s else s['guid'], 'type': s['type'], 'start_time': s['pointStart'], 'interval': s['pointInterval'], 'total': None if 'total' not in s else s['total'], 'timestamps': [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], 'timestamps_adjusted': [float(s['pointInterval']*i) for i in range(len(s['data']))], 'values': [float(s['data'][i]) for i in range(len(s['data']))], 'attributes': ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]},
            ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]
        ).to_dict() for s in r['series']], 'attributes': ["start_time", "end_time", "series", "view", "to_dict", "attributes"]},
        ["start_time", "end_time", "series", "view", "to_dict", "attributes"]
    )



def get_enemy_healing_done_data(report_code: str, fight: NamedTuple, start_time: int = None, enemy: NamedTuple = None, ability: int = 0) -> NamedTuple:
    """
    """
    if start_time is None:
        start_time = fight.start_time
    url = f"https://classic.warcraftlogs.com/reports/graph/healing/{report_code}/{fight.fight_id}/{start_time}/{fight.end_time}" + \
          f"/source/1/0/{enemy.report_id if enemy is not None else 0}/0/0/{ability}/-1.0.-1.-1/0/Any/Any/0/0"
    r = request(url)
    Data = namedtuple("Data", ["start_time", "end_time", "series", "view", "to_dict", "attributes"])
    Series = namedtuple("Series", ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"])
    return Data(
        r['startTime'], r['endTime'],
        [Series(
            s['name'], s['id'], None if 'guid' not in s else int(s['guid']), s['type'], int(s['pointStart']), float(s['pointInterval']), None if 'total' not in s else float(s['total']), [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], [float(s['pointInterval']*i) for i in range(len(s['data']))], [float(s['data'][i]) for i in range(len(s['data']))],
            lambda _=0: view({'name': s['name'], 'id': s['id'], 'guid': None if 'guid' not in s else s['guid'], 'type': s['type'], 'start_time': s['pointStart'], 'interval': s['pointInterval'], 'total': None if 'total' not in s else s['total'], 'timestamps': [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], 'timestamps_adjusted': [float(s['pointInterval']*i) for i in range(len(s['data']))], 'values': [float(s['data'][i]) for i in range(len(s['data']))], 'attributes': ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]}),
            lambda _=0: {'name': s['name'], 'id': s['id'], 'guid': None if 'guid' not in s else s['guid'], 'type': s['type'], 'start_time': s['pointStart'], 'interval': s['pointInterval'], 'total': None if 'total' not in s else s['total'], 'timestamps': [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], 'timestamps_adjusted': [float(s['pointInterval']*i) for i in range(len(s['data']))], 'values': [float(s['data'][i]) for i in range(len(s['data']))], 'attributes': ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]},
            ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]
        ) for s in r['series']],
        lambda _=0: view({'start_time': r['startTime'], 'end_time': r['endTime'], 'series': [Series(
            s['name'], s['id'], None if 'guid' not in s else int(s['guid']), s['type'], int(s['pointStart']), float(s['pointInterval']), None if 'total' not in s else float(s['total']), [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], [float(s['pointInterval']*i) for i in range(len(s['data']))], [float(s['data'][i]) for i in range(len(s['data']))],
            lambda _=0: view({'name': s['name'], 'id': s['id'], 'guid': None if 'guid' not in s else s['guid'], 'type': s['type'], 'start_time': s['pointStart'], 'interval': s['pointInterval'], 'total': None if 'total' not in s else s['total'], 'timestamps': [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], 'timestamps_adjusted': [float(s['pointInterval']*i) for i in range(len(s['data']))], 'values': [float(s['data'][i]) for i in range(len(s['data']))], 'attributes': ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]}),
            lambda _=0: {'name': s['name'], 'id': s['id'], 'guid': None if 'guid' not in s else s['guid'], 'type': s['type'], 'start_time': s['pointStart'], 'interval': s['pointInterval'], 'total': None if 'total' not in s else s['total'], 'timestamps': [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], 'timestamps_adjusted': [float(s['pointInterval']*i) for i in range(len(s['data']))], 'values': [float(s['data'][i]) for i in range(len(s['data']))], 'attributes': ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]},
            ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]
        ).to_dict() for s in r['series']], 'attributes': ["start_time", "end_time", "series", "view", "to_dict", "attributes"]}),
        lambda _=0: {'start_time': r['startTime'], 'end_time': r['endTime'], 'series': [Series(
            s['name'], s['id'], None if 'guid' not in s else int(s['guid']), s['type'], int(s['pointStart']), float(s['pointInterval']), None if 'total' not in s else float(s['total']), [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], [float(s['pointInterval']*i) for i in range(len(s['data']))], [float(s['data'][i]) for i in range(len(s['data']))],
            lambda _=0: view({'name': s['name'], 'id': s['id'], 'guid': None if 'guid' not in s else s['guid'], 'type': s['type'], 'start_time': s['pointStart'], 'interval': s['pointInterval'], 'total': None if 'total' not in s else s['total'], 'timestamps': [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], 'timestamps_adjusted': [float(s['pointInterval']*i) for i in range(len(s['data']))], 'values': [float(s['data'][i]) for i in range(len(s['data']))], 'attributes': ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]}),
            lambda _=0: {'name': s['name'], 'id': s['id'], 'guid': None if 'guid' not in s else s['guid'], 'type': s['type'], 'start_time': s['pointStart'], 'interval': s['pointInterval'], 'total': None if 'total' not in s else s['total'], 'timestamps': [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], 'timestamps_adjusted': [float(s['pointInterval']*i) for i in range(len(s['data']))], 'values': [float(s['data'][i]) for i in range(len(s['data']))], 'attributes': ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]},
            ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]
        ).to_dict() for s in r['series']], 'attributes': ["start_time", "end_time", "series", "view", "to_dict", "attributes"]},
        ["start_time", "end_time", "series", "view", "to_dict", "attributes"]
    )



def get_friendly_healing_done_data(report_code: str, fight: NamedTuple, start_time: int = None, enemy: NamedTuple = None, ability: int = 0, anubarak: bool = False) -> NamedTuple:
    """
    """
    if start_time is None:
        start_time = fight.start_time
    url = f"https://classic.warcraftlogs.com/reports/graph/healing/{report_code}/{fight.fight_id}/{start_time}/{fight.end_time}" + \
          f"/source/0/0/{enemy.report_id if enemy is not None else 0}/0/0/{ability}/-1.0.-1.-1/0/Any/Any/{8192 if anubarak else 0}/0"
    r = request(url)
    Data = namedtuple("Data", ["start_time", "end_time", "series", "view", "to_dict", "attributes"])
    Series = namedtuple("Series", ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"])
    return Data(
        r['startTime'], r['endTime'],
        [Series(
            s['name'], s['id'], None if 'guid' not in s else int(s['guid']), s['type'], int(s['pointStart']), float(s['pointInterval']), None if 'total' not in s else float(s['total']), [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], [float(s['pointInterval']*i) for i in range(len(s['data']))], [float(s['data'][i]) for i in range(len(s['data']))],
            lambda _=0: view({'name': s['name'], 'id': s['id'], 'guid': None if 'guid' not in s else s['guid'], 'type': s['type'], 'start_time': s['pointStart'], 'interval': s['pointInterval'], 'total': None if 'total' not in s else s['total'], 'timestamps': [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], 'timestamps_adjusted': [float(s['pointInterval']*i) for i in range(len(s['data']))], 'values': [float(s['data'][i]) for i in range(len(s['data']))], 'attributes': ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]}),
            lambda _=0: {'name': s['name'], 'id': s['id'], 'guid': None if 'guid' not in s else s['guid'], 'type': s['type'], 'start_time': s['pointStart'], 'interval': s['pointInterval'], 'total': None if 'total' not in s else s['total'], 'timestamps': [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], 'timestamps_adjusted': [float(s['pointInterval']*i) for i in range(len(s['data']))], 'values': [float(s['data'][i]) for i in range(len(s['data']))], 'attributes': ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]},
            ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]
        ) for s in r['series']],
        lambda _=0: view({'start_time': r['startTime'], 'end_time': r['endTime'], 'series': [Series(
            s['name'], s['id'], None if 'guid' not in s else int(s['guid']), s['type'], int(s['pointStart']), float(s['pointInterval']), None if 'total' not in s else float(s['total']), [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], [float(s['pointInterval']*i) for i in range(len(s['data']))], [float(s['data'][i]) for i in range(len(s['data']))],
            lambda _=0: view({'name': s['name'], 'id': s['id'], 'guid': None if 'guid' not in s else s['guid'], 'type': s['type'], 'start_time': s['pointStart'], 'interval': s['pointInterval'], 'total': None if 'total' not in s else s['total'], 'timestamps': [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], 'timestamps_adjusted': [float(s['pointInterval']*i) for i in range(len(s['data']))], 'values': [float(s['data'][i]) for i in range(len(s['data']))], 'attributes': ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]}),
            lambda _=0: {'name': s['name'], 'id': s['id'], 'guid': None if 'guid' not in s else s['guid'], 'type': s['type'], 'start_time': s['pointStart'], 'interval': s['pointInterval'], 'total': None if 'total' not in s else s['total'], 'timestamps': [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], 'timestamps_adjusted': [float(s['pointInterval']*i) for i in range(len(s['data']))], 'values': [float(s['data'][i]) for i in range(len(s['data']))], 'attributes': ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]},
            ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]
        ).to_dict() for s in r['series']], 'attributes': ["start_time", "end_time", "series", "view", "to_dict", "attributes"]}),
        lambda _=0: {'start_time': r['startTime'], 'end_time': r['endTime'], 'series': [Series(
            s['name'], s['id'], None if 'guid' not in s else int(s['guid']), s['type'], int(s['pointStart']), float(s['pointInterval']), None if 'total' not in s else float(s['total']), [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], [float(s['pointInterval']*i) for i in range(len(s['data']))], [float(s['data'][i]) for i in range(len(s['data']))],
            lambda _=0: view({'name': s['name'], 'id': s['id'], 'guid': None if 'guid' not in s else s['guid'], 'type': s['type'], 'start_time': s['pointStart'], 'interval': s['pointInterval'], 'total': None if 'total' not in s else s['total'], 'timestamps': [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], 'timestamps_adjusted': [float(s['pointInterval']*i) for i in range(len(s['data']))], 'values': [float(s['data'][i]) for i in range(len(s['data']))], 'attributes': ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]}),
            lambda _=0: {'name': s['name'], 'id': s['id'], 'guid': None if 'guid' not in s else s['guid'], 'type': s['type'], 'start_time': s['pointStart'], 'interval': s['pointInterval'], 'total': None if 'total' not in s else s['total'], 'timestamps': [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], 'timestamps_adjusted': [float(s['pointInterval']*i) for i in range(len(s['data']))], 'values': [float(s['data'][i]) for i in range(len(s['data']))], 'attributes': ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]},
            ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]
        ).to_dict() for s in r['series']], 'attributes': ["start_time", "end_time", "series", "view", "to_dict", "attributes"]},
        ["start_time", "end_time", "series", "view", "to_dict", "attributes"]
    )



def get_damage_done_data(report_code: str, fight: NamedTuple, start_time: int = None, friendly_id: int = None, enemy: NamedTuple = None, ability: int = 0, anub_arak: bool = False) -> NamedTuple:
    """
    """
    if start_time is None:
        start_time = fight.start_time
    if anub_arak:
        second_last_flag = 8192
    else:
        second_last_flag = 0
    url = f"https://classic.warcraftlogs.com/reports/graph/damage-done/{report_code}/{fight.fight_id}/{start_time}/{fight.end_time}" + \
          f"/source/0/{friendly_id if friendly_id is not None else 0}/{enemy.report_id if enemy is not None else 0}/0/0/{ability}/-1.0.-1.-1/0/Any/Any/{second_last_flag}/0"
    r = request(url)
    Data = namedtuple("Data", ["start_time", "end_time", "series", "view", "to_dict", "attributes"])
    Series = namedtuple("Series", ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"])
    return Data(
        r['startTime'], r['endTime'],
        [Series(
            s['name'], s['id'], None if 'guid' not in s else int(s['guid']), s['type'], int(s['pointStart']), float(s['pointInterval']), None if 'total' not in s else float(s['total']), [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], [float(s['pointInterval']*i) for i in range(len(s['data']))], [float(s['data'][i]) for i in range(len(s['data']))],
            lambda _=0: view({'name': s['name'], 'id': s['id'], 'guid': None if 'guid' not in s else s['guid'], 'type': s['type'], 'start_time': s['pointStart'], 'interval': s['pointInterval'], 'total': None if 'total' not in s else s['total'], 'timestamps': [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], 'timestamps_adjusted': [float(s['pointInterval']*i) for i in range(len(s['data']))], 'values': [float(s['data'][i]) for i in range(len(s['data']))], 'attributes': ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]}),
            lambda _=0: {'name': s['name'], 'id': s['id'], 'guid': None if 'guid' not in s else s['guid'], 'type': s['type'], 'start_time': s['pointStart'], 'interval': s['pointInterval'], 'total': None if 'total' not in s else s['total'], 'timestamps': [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], 'timestamps_adjusted': [float(s['pointInterval']*i) for i in range(len(s['data']))], 'values': [float(s['data'][i]) for i in range(len(s['data']))], 'attributes': ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]},
            ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]
        ) for s in r['series']],
        lambda _=0: view({'start_time': r['startTime'], 'end_time': r['endTime'], 'series': [Series(
            s['name'], s['id'], None if 'guid' not in s else int(s['guid']), s['type'], int(s['pointStart']), float(s['pointInterval']), None if 'total' not in s else float(s['total']), [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], [float(s['pointInterval']*i) for i in range(len(s['data']))], [float(s['data'][i]) for i in range(len(s['data']))],
            lambda _=0: view({'name': s['name'], 'id': s['id'], 'guid': None if 'guid' not in s else s['guid'], 'type': s['type'], 'start_time': s['pointStart'], 'interval': s['pointInterval'], 'total': None if 'total' not in s else s['total'], 'timestamps': [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], 'timestamps_adjusted': [float(s['pointInterval']*i) for i in range(len(s['data']))], 'values': [float(s['data'][i]) for i in range(len(s['data']))], 'attributes': ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]}),
            lambda _=0: {'name': s['name'], 'id': s['id'], 'guid': None if 'guid' not in s else s['guid'], 'type': s['type'], 'start_time': s['pointStart'], 'interval': s['pointInterval'], 'total': None if 'total' not in s else s['total'], 'timestamps': [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], 'timestamps_adjusted': [float(s['pointInterval']*i) for i in range(len(s['data']))], 'values': [float(s['data'][i]) for i in range(len(s['data']))], 'attributes': ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]},
            ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]
        ).to_dict() for s in r['series']], 'attributes': ["start_time", "end_time", "series", "view", "to_dict", "attributes"]}),
        lambda _=0: {'start_time': r['startTime'], 'end_time': r['endTime'], 'series': [Series(
            s['name'], s['id'], None if 'guid' not in s else int(s['guid']), s['type'], int(s['pointStart']), float(s['pointInterval']), None if 'total' not in s else float(s['total']), [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], [float(s['pointInterval']*i) for i in range(len(s['data']))], [float(s['data'][i]) for i in range(len(s['data']))],
            lambda _=0: view({'name': s['name'], 'id': s['id'], 'guid': None if 'guid' not in s else s['guid'], 'type': s['type'], 'start_time': s['pointStart'], 'interval': s['pointInterval'], 'total': None if 'total' not in s else s['total'], 'timestamps': [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], 'timestamps_adjusted': [float(s['pointInterval']*i) for i in range(len(s['data']))], 'values': [float(s['data'][i]) for i in range(len(s['data']))], 'attributes': ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]}),
            lambda _=0: {'name': s['name'], 'id': s['id'], 'guid': None if 'guid' not in s else s['guid'], 'type': s['type'], 'start_time': s['pointStart'], 'interval': s['pointInterval'], 'total': None if 'total' not in s else s['total'], 'timestamps': [float(s['pointStart']) + float(s['pointInterval'])*i for i in range(len(s['data']))], 'timestamps_adjusted': [float(s['pointInterval']*i) for i in range(len(s['data']))], 'values': [float(s['data'][i]) for i in range(len(s['data']))], 'attributes': ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]},
            ["name", "id", "guid", "type", "start_time", "interval", "total", "timestamps", "timestamps_adjusted", "values", "view", "to_dict", "attributes"]
        ).to_dict() for s in r['series']], 'attributes': ["start_time", "end_time", "series", "view", "to_dict", "attributes"]},
        ["start_time", "end_time", "series", "view", "to_dict", "attributes"]
    )
