import gurobipy as gp
from gurobipy import Model, GRB, quicksum

# Input data
nfl_teams = {
    0: "Arizona Cardinals",
    1: "Atlanta Falcons",
    2: "Baltimore Ravens",
    3: "Buffalo Bills",
    4: "Carolina Panthers",
    5: "Chicago Bears",
    6: "Cincinnati Bengals",
    7: "Cleveland Browns",
    8: "Dallas Cowboys",
    9: "Denver Broncos",
    10: "Detroit Lions",
    11: "Green Bay Packers",
    12: "Houston Texans",
    13: "Indianapolis Colts",
    14: "Jacksonville Jaguars",
    15: "Kansas City Chiefs",
    16: "Los Angeles Chargers",
    17: "Los Angeles Rams",
    18: "Miami Dolphins",
    19: "Minnesota Vikings",
    20: "New England Patriots",
    21: "New Orleans Saints",
    22: "New York Giants",
    23: "New York Jets",
    24: "Oakland Raiders",
    25: "Philadelphia Eagles",
    26: "Pittsburgh Steelers",
    27: "San Francisco 49ers",
    28: "Seattle Seahawks",
    29: "Tampa Bay Buccaneers",
    30: "Tennessee Titans",
    31: "Washington Commanders"
}

afc_teams = {
    2: "Baltimore Ravens",
    3: "Buffalo Bills",
    6: "Cincinnati Bengals",
    7: "Cleveland Browns",
    9: "Denver Broncos",
    12: "Houston Texans",
    13: "Indianapolis Colts",
    14: "Jacksonville Jaguars",
    15: "Kansas City Chiefs",
    16: "Los Angeles Chargers",
    18: "Miami Dolphins",
    20: "New England Patriots",
    23: "New York Jets",
    24: "Oakland Raiders",
    26: "Pittsburgh Steelers",
    30: "Tennessee Titans"
}

nfc_teams = {
    0: "Arizona Cardinals",
    1: "Atlanta Falcons",
    4: "Carolina Panthers",
    5: "Chicago Bears",
    8: "Dallas Cowboys",
    10: "Detroit Lions",
    11: "Green Bay Packers",
    17: "Los Angeles Rams",
    19: "Minnesota Vikings",
    21: "New Orleans Saints",
    22: "New York Giants",
    25: "Philadelphia Eagles",
    27: "San Francisco 49ers",
    28: "Seattle Seahawks",
    29: "Tampa Bay Buccaneers",
    31: "Washington Commanders"
}

weeks = list(range(18)) 
num_games_total = 17   


# Distance matrix 
distances_matrix = [
[0,1868,2366,2274,2107,1819,1876,2085,1077,904,2074,2017,1188,1764,2072,1360,2390,1805,2700,1687,1548,2481,2481,742,2420,2136,1517,358,750,1513,2184,2362],
[1868,0,679,910,238,717,476,726,792,1403,735,927,800,531,344,801,661,1129,1074,248,473,869,869,2468,782,676,549,2166,2618,2705,455,636],
[2366,679,0,370,441,708,521,377,1399,1690,532,918,1470,600,763,1087,1109,1121,392,707,1142,192,192,2820,104,246,841,2724,2840,2775,960,38],
[2274,910,370,0,695,545,442,197,1393,1546,277,753,1513,508,1080,995,1425,958,455,706,1254,400,400,2661,414,217,749,2632,2677,2612,1276,384],
[2107,238,441,695,0,761,476,520,1031,1559,675,994,1041,575,385,956,730,1173,835,426,713,631,631,2725,543,438,704,2405,2759,2827,581,397],
[1819,717,708,545,761,0,302,346,936,1015,283,208,1108,184,1065,532,1382,409,985,472,935,797,797,2132,768,467,294,2105,2146,2062,1176,701],
[1876,476,521,442,476,302,0,253,958,1200,261,506,1079,116,803,597,1141,714,841,274,820,636,636,2385,576,292,350,2234,2407,2368,935,517],
[2085,726,377,197,520,346,253,0,1208,1347,171,553,1328,319,904,806,1254,760,639,521,1070,466,466,2462,437,136,560,2437,2478,2413,1101,370],
[1077,792,1399,1393,1031,936,958,1208,0,887,1218,1149,241,913,1049,554,1367,999,1755,667,525,1589,1589,1725,1501,1246,635,1375,1827,2208,1161,1362],
[904,1403,1690,1546,1559,1015,1200,1347,887,0,1284,1105,1127,1088,1751,603,2069,924,1987,1162,1409,1799,1799,1266,1744,1460,855,1092,1271,1329,1862,1686],
[2074,735,532,277,675,283,261,171,1218,1284,0,490,1338,318,1060,795,1401,697,707,535,1079,622,622,2398,592,292,549,2373,2415,2350,1194,526],
[2017,927,918,753,994,208,506,553,1149,1105,490,0,1390,393,1273,626,1594,280,1192,680,1135,998,998,2229,968,669,497,2181,2236,1939,1384,906],
[1188,800,1470,1513,1041,1108,1079,1328,241,1127,1338,1390,0,1033,884,795,1201,1240,1835,859,360,1660,1660,1921,1572,1366,863,1487,1938,2444,945,1433],
[1764,531,600,508,575,184,116,319,913,1088,318,393,1033,0,879,485,1196,596,950,288,826,715,715,2275,655,370,239,2122,2290,2249,990,596],
[2072,344,763,1080,385,1065,803,904,1049,1751,1060,1273,884,879,0,1148,345,1477,1142,594,556,953,953,2792,866,822,896,2370,2822,3052,196,720],
[1360,801,1087,995,956,532,597,806,554,603,795,626,795,485,1148,0,1466,441,1434,558,932,1202,1202,1803,1141,857,252,1695,1814,1872,1259,1083],
[2390,661,1109,1425,730,1382,1141,1250,1367,2069,1401,1594,1201,1196,345,1466,0,1794,1492,915,874,1299,1299,3113,1211,1167,1214,2688,3140,3370,274,1065],
[1805,1129,1121,958,1173,409,714,760,999,924,697,280,1240,596,1477,441,1794,0,1392,870,1337,1211,1211,2042,1181,881,621,2014,2055,1654,1588,111],
[2700,1074,392,455,835,985,841,639,1755,1987,707,1192,1835,950,1142,1434,1492,1392,0,1090,1510,204,204,3111,295,572,1193,3062,3117,3051,1367,432],
[1687,248,707,706,426,472,274,521,667,1162,535,680,859,288,594,558,915,870,1090,0,534,890,890,2300,809,560,309,2028,2311,2405,705,676],
[1548,473,1142,1254,713,935,820,1070,525,1409,1079,1135,360,826,556,932,874,1337,1510,534,0,1332,1332,2268,1245,1108,690,1846,2298,2731,668,1106],
[2481,869,192,400,631,797,636,466,1589,1799,622,998,1660,715,953,1202,1299,1211,204,890,1332,0,0,2908,91,367,956,2839,2929,2864,1150,228],
[2481,869,192,400,631,797,636,466,1589,1799,622,998,1660,715,953,1202,1299,1211,204,890,1332,0,0,2908,91,367,956,2839,2929,2864,1150,228],
[742,2468,2820,2661,2725,2132,2385,2462,1725,1266,2398,2229,1921,2275,2792,1803,3113,2042,3111,2300,2268,2908,2908,0,2877,2578,2056,492,12,804,2902,281],
[2420,782,104,414,543,768,576,437,1501,1744,592,968,1572,655,866,1141,1211,1181,295,809,1245,91,91,2877,0,306,895,2779,2900,2835,1062,140],
[2136,676,246,217,438,467,292,136,1246,1460,292,669,1366,370,822,857,1167,881,572,560,1108,367,367,2578,306,0,611,2494,2599,2534,1019,240],
[1517,549,849,749,704,294,350,560,635,855,549,497,863,239,896,252,1214,621,1193,309,690,956,956,2056,895,611,0,1875,2066,2125,1008,837],
[358,2166,2724,2632,2405,2105,2234,2437,1375,1092,2373,2181,1487,2122,2370,1695,2688,2014,3062,2028,1846,2839,2839,492,2779,2494,1875,0,508,1271,2481,2720],
[750,2618,2840,2677,2759,2146,2407,2478,1827,1271,2415,2236,1938,2290,2822,1814,3140,2055,3117,2311,2298,2929,2929,12,2900,2599,2066,508,0,816,2933,2834],
[1513,2705,2775,2612,2827,2062,2368,2413,2208,1329,2350,1939,2449,2249,3052,1872,3370,1654,3051,2405,2731,2864,2864,804,2835,2534,2125,1271,816,0,3164,2769],
[2184,455,960,1276,581,1176,935,1101,1161,1862,1194,1384,995,990,196,1259,274,1588,1367,705,668,1150,1150,2902,1062,1019,1008,2481,2933,3164,0,916],
[2362,636,38,384,397,701,517,370,1362,1686,526,906,1433,596,720,1083,1065,1115,432,676,1106,228,228,2815,140,240,837,2720,2834,2769,916,0]
]


model = Model("CO 370 Final Project")

# Decision Variables
x = model.addVars(nfl_teams, nfl_teams, weeks, vtype=GRB.BINARY, name = "x")  

# Objective: Minimize total distance traveled
model.setObjective(
    quicksum(2 * distances_matrix[i][j] * x[i, j, w] for i in nfl_teams for j in nfl_teams if i != j for w in weeks), GRB.MINIMIZE
)

# Constraints
# Each team plays exactly 17 games (either 9 at home 8 away or vice versa)
for i in nfl_teams:
    model.addConstr(quicksum(x[i, j, w] for j in nfl_teams if i != j for w in weeks) <= 9, name = f"HomeGames_{i}")  
    model.addConstr(quicksum(x[j, i, w] for j in nfl_teams if i != j for w in weeks) <= 9, name = f"AwayGames_{i}")  
    model.addConstr(
        quicksum(x[i, j, w] + x[j, i, w] for j in nfl_teams if j != i for w in weeks) == 17, name = f"TotalGames_{i}")  

# Each team plays at most one game per day
for i in nfl_teams:
    for w in weeks:
        model.addConstr(
            quicksum(x[i, j, w] + x[j, i, w] for j in nfl_teams if j != i) <= 1, name = f"OneGamePerWeek_{i}_{w}")

# No duplicate games (team i cannot play team j more than once on the same day)
for i in nfl_teams:
    for j in nfl_teams:
        if i != j:
            for w in weeks:
                model.addConstr(x[i, j, w] + x[j, i, w] <= 1, name = f"NoDuplicate_{i}_{j}_{w}")
                
# Equal distribution between home and away games in each matchup pair     
for i in nfl_teams:
    for j in nfl_teams:
        if i != j:
            model.addConstr(quicksum(x[i, j, w] for w in weeks) - quicksum(x[j, i, w] for w in weeks) <= 1, name = f"HomeandAwaySplit_{i}_{j}")
            
# Each pair of teams in the same conference plays at most 3 games against eachother (2 or 3)
for i in nfl_teams:
    for j in nfl_teams:
        if i != j:
            model.addConstr(quicksum(x[i, j, w] + x[j, i, w] for w in weeks) <= 3, name = f"MaxMatchups_{i}_{j}")

# Teams in opposite conferences play at most once during the season
for i in afc_teams:
    for j in nfc_teams:
        model.addConstr(quicksum(x[i, j, w] + x[j, i, w] for w in weeks) <= 1, name = f"InterconferenceGames_{i}_{j}")
        
# Avoid back-to-back games against the same opponent
for i in nfl_teams:
    for j in nfl_teams:
       if i != j:
            for w in range(len(weeks) - 1):
                model.addConstr(x[i, j, w] + x[i, j, w+1] + x[j, i, w] + x[j, i, w+1] <= 1, name = f"NoBackToBack_{i}_{j}_{w}")


# Optimize and output schedule line by line
model.optimize()

if model.status == GRB.OPTIMAL:
    print("Optimal schedule found!")
    for i, j, w in x.keys():
        if x[i, j, w].x == 1: 
            print(f"Week {w + 1}: {nfl_teams[i]} at {nfl_teams[j]}")
else:
    print("No feasible schedule found.")








