inputString = """108 LAA Angels
109 ARI D-backs
110 BAL Orioles
111 BOS Red Sox
112 CHC Cubs
113 CIN Reds
114 CLE Indians
115 COL Rockies
116 DET Tigers
117 HOU Astros
118 KC Royals
119 LAD Dodgers
120 WSH Nationals
121 NYM Mets
133 OAK Athletics
134 PIT Pirates
135 SD Padres
136 SEA Mariners
137 SF Giants
138 STL Cardinals
139 TB Rays
140 TEX Rangers
141 TOR Blue Jays
142 MIN Twins
143 PHI Phillies
144 ATL Braves
145 CWS White Sox
146 MIA Marlins
147 NYY Yankees
158 MIL Brewers"""

split = inputString.splitlines()
primary = []
secondary = []

for splat in split:
    words = splat.split(" ")
    colors = input(words[2] + " Primary Colors?\n").split(" ")
    primary.append(words[0] + ": Color(" + colors[0] + ", " + colors[1] + ", " + colors[2] + "),")
    
    colors = input(words[2] + " Secondary Colors?\n").split(" ")
    secondary.append(words[0] + ": Color(" + colors[0] + ", " + colors[1] + ", " + colors[2] + "),")
    print("\nPrimary:")
    for p in primary:
        print(p)

    print("\nSeondary:")
    for p in secondary:
        print(p)
