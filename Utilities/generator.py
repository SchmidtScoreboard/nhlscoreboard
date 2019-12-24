import json
from collections import namedtuple
Color = namedtuple('Color', 'red green blue')

inputString = """108 LAA Angels Los Angeles
109 ARI D-backs Arizona
110 BAL Orioles Baltimore
111 BOS Red Sox Boston
112 CHC Cubs Cubs
113 CIN Reds Cincinnati
114 CLE Indians Cleveland
115 COL Rockies Colorado
116 DET Tigers Detroit
117 HOU Astros Houston
118 KC Royals Kansas City
119 LAD Dodgers Los Angeles
120 WSH Nationals Washington
121 NYM Mets New York
133 OAK Athletics Oakland
134 PIT Pirates Pittsburgh
135 SD Padres San Diego
136 SEA Mariners Seattle
137 SF Giants San Francisco
138 STL Cardinals St. Louis
139 TB Rays Tampa Bay
140 TEX Rangers Texas
141 TOR Blue Jays Toronto
142 MIN Twins Minnesota
143 PHI Phillies Philadelphia
144 ATL Braves Atlanta
145 CWS White Sox Chicago
146 MIA Marlins Miami
147 NYY Yankees New York
158 MIL Brewers Milkwaukee
159 NL NL All Stars
160 AL AL All Stars"""


primaryColorMap = {
    108: Color(186, 0, 33),
    109: Color(167, 25, 48),
    110: Color(223, 70, 1),
    111: Color(198, 1, 31),
    112: Color(14, 51, 134),
    113: Color(198, 1, 31),
    114: Color(227, 25, 55),
    115: Color(51, 0, 111),
    116: Color(12, 35, 64),
    117: Color(0, 45, 98),
    118: Color(0, 70, 135),
    119: Color(0, 90, 156),
    120: Color(171, 0, 3),
    121: Color(0, 45, 114),
    133: Color(0, 56, 49),
    134: Color(253, 184, 39),
    135: Color(0, 45, 98),
    136: Color(0, 92, 92),
    137: Color(39, 37, 31),
    138: Color(196, 30, 58),
    139: Color(214, 90, 36),
    140: Color(0, 50, 120),
    141: Color(19, 74, 142),
    142: Color(0, 43, 92),
    143: Color(232, 24, 40),
    144: Color(19, 39, 79),
    145: Color(39, 37, 31),
    146: Color(0, 0, 0),
    147: Color(12, 35, 64),
    158: Color(19, 41, 75),
    159: Color(255, 0, 0),
    160: Color(0, 0, 255),
}


secondaryColorMap = {
    108: Color(196, 206, 212),
    109: Color(227, 212, 173),
    110: Color(39, 37, 31),
    111: Color(255, 255, 255),
    112: Color(204, 52, 51),
    113: Color(0, 0, 0),
    114: Color(12, 35, 64),
    115: Color(196, 206, 212),
    116: Color(250, 70, 22),
    117: Color(244, 145, 30),
    118: Color(189, 155, 96),
    119: Color(239, 62, 66),
    120: Color(20, 34, 90),
    121: Color(252, 89, 16),
    133: Color(239, 178, 30),
    134: Color(39, 37, 31),
    135: Color(162, 170, 173),
    136: Color(196, 206, 212),
    137: Color(253, 90, 30),
    138: Color(12, 35, 64),
    139: Color(255, 255, 255),
    140: Color(192, 17, 31),
    141: Color(177, 179, 179),
    142: Color(211, 17, 69),
    143: Color(0, 45, 114),
    144: Color(206, 17, 65),
    145: Color(196, 206, 212),
    146: Color(0, 163, 224),
    147: Color(255, 255, 255),
    158: Color(182, 146, 46),
    159: Color(255, 255, 255),
    160: Color(255, 255, 255)
}
nhlPrimaryColorMap = {
    # todo fill in color map
    1: Color(200, 16, 46),
    2: Color(0, 48, 135),
    3: Color(0, 51, 160),
    4: Color(250, 70, 22),
    5: Color(255, 184, 28),
    6: Color(252, 181, 20),
    7: Color(0, 38, 84),
    8: Color(166, 25, 46),
    9: Color(200, 16, 46),
    10: Color(0, 32, 91),
    12: Color(204, 0, 0),
    13: Color(200, 16, 46),
    14: Color(0, 32, 91),
    15: Color(4, 30, 66),
    16: Color(206, 17, 38),
    17: Color(200, 16, 46),
    18: Color(255, 184, 28),
    19: Color(0, 47, 135),
    20: Color(206, 17, 38),
    21: Color(35, 97, 146),
    22: Color(252, 76, 2),
    23: Color(0, 136, 82),
    24: Color(181, 152, 90),
    25: Color(0, 99, 65),
    26: Color(162, 170, 173),
    28: Color(0, 98, 114),
    29: Color(4, 30, 66),
    30: Color(21, 71, 52),
    52: Color(4, 30, 66),
    53: Color(140, 38, 51),
    54: Color(185, 151, 91)}

nhlSecondaryColorMap = {
    # todo fill in color map
    1: Color(0, 0, 0),
    2: Color(252, 76, 2),
    3: Color(200, 16, 46),
    4: Color(0, 0, 0),
    5: Color(0, 0, 0),
    6: Color(0, 0, 0),
    7: Color(252, 181, 20),
    8: Color(0, 30, 98),
    9: Color(198, 146, 20),
    10: Color(255, 255, 255),
    12: Color(162, 169, 175),
    13: Color(185, 151, 91),
    14: Color(255, 255, 255),
    15: Color(200, 16, 46),
    16: Color(204, 138, 0),
    17: Color(255, 255, 255),
    18: Color(4, 30, 66),
    19: Color(255, 184, 28),
    20: Color(243, 188, 82),
    21: Color(111, 38, 61),
    22: Color(4, 30, 66),
    23: Color(0, 32, 91),
    24: Color(249, 86, 2),
    25: Color(162, 170, 173),
    26: Color(0, 0, 0),
    28: Color(229, 114, 0),
    29: Color(200, 16, 46),
    30: Color(166, 25, 46),
    52: Color(162, 170, 173),
    53: Color(226, 214, 181),
    54: Color(0, 0, 0)}

nhlJson = """{
  "teams" : [ {
    "id" : 1,
    "name" : "New Jersey Devils",
    "link" : "/api/v1/teams/1",
    "venue" : {
      "name" : "Prudential Center",
      "link" : "/api/v1/venues/null",
      "city" : "Newark",
      "timeZone" : {
        "id" : "America/New_York",
        "offset" : -4,
        "tz" : "EDT"
      }
    },
    "abbreviation" : "NJD",
    "teamName" : "Devils",
    "locationName" : "New Jersey",
    "firstYearOfPlay" : "1982",
    "division" : {
      "id" : 18,
      "name" : "Metropolitan",
      "nameShort" : "Metro",
      "link" : "/api/v1/divisions/18",
      "abbreviation" : "M"
    },
    "conference" : {
      "id" : 6,
      "name" : "Eastern",
      "link" : "/api/v1/conferences/6"
    },
    "franchise" : {
      "franchiseId" : 23,
      "teamName" : "Devils",
      "link" : "/api/v1/franchises/23"
    },
    "shortName" : "New Jersey",
    "officialSiteUrl" : "http://www.newjerseydevils.com/",
    "franchiseId" : 23,
    "active" : true
  }, {
    "id" : 2,
    "name" : "New York Islanders",
    "link" : "/api/v1/teams/2",
    "venue" : {
      "id" : 5026,
      "name" : "Barclays Center",
      "link" : "/api/v1/venues/5026",
      "city" : "Brooklyn",
      "timeZone" : {
        "id" : "America/New_York",
        "offset" : -4,
        "tz" : "EDT"
      }
    },
    "abbreviation" : "NYI",
    "teamName" : "Islanders",
    "locationName" : "New York",
    "firstYearOfPlay" : "1972",
    "division" : {
      "id" : 18,
      "name" : "Metropolitan",
      "nameShort" : "Metro",
      "link" : "/api/v1/divisions/18",
      "abbreviation" : "M"
    },
    "conference" : {
      "id" : 6,
      "name" : "Eastern",
      "link" : "/api/v1/conferences/6"
    },
    "franchise" : {
      "franchiseId" : 22,
      "teamName" : "Islanders",
      "link" : "/api/v1/franchises/22"
    },
    "shortName" : "NY Islanders",
    "officialSiteUrl" : "http://www.newyorkislanders.com/",
    "franchiseId" : 22,
    "active" : true
  }, {
    "id" : 3,
    "name" : "New York Rangers",
    "link" : "/api/v1/teams/3",
    "venue" : {
      "id" : 5054,
      "name" : "Madison Square Garden",
      "link" : "/api/v1/venues/5054",
      "city" : "New York",
      "timeZone" : {
        "id" : "America/New_York",
        "offset" : -4,
        "tz" : "EDT"
      }
    },
    "abbreviation" : "NYR",
    "teamName" : "Rangers",
    "locationName" : "New York",
    "firstYearOfPlay" : "1926",
    "division" : {
      "id" : 18,
      "name" : "Metropolitan",
      "nameShort" : "Metro",
      "link" : "/api/v1/divisions/18",
      "abbreviation" : "M"
    },
    "conference" : {
      "id" : 6,
      "name" : "Eastern",
      "link" : "/api/v1/conferences/6"
    },
    "franchise" : {
      "franchiseId" : 10,
      "teamName" : "Rangers",
      "link" : "/api/v1/franchises/10"
    },
    "shortName" : "NY Rangers",
    "officialSiteUrl" : "http://www.newyorkrangers.com/",
    "franchiseId" : 10,
    "active" : true
  }, {
    "id" : 4,
    "name" : "Philadelphia Flyers",
    "link" : "/api/v1/teams/4",
    "venue" : {
      "id" : 5096,
      "name" : "Wells Fargo Center",
      "link" : "/api/v1/venues/5096",
      "city" : "Philadelphia",
      "timeZone" : {
        "id" : "America/New_York",
        "offset" : -4,
        "tz" : "EDT"
      }
    },
    "abbreviation" : "PHI",
    "teamName" : "Flyers",
    "locationName" : "Philadelphia",
    "firstYearOfPlay" : "1967",
    "division" : {
      "id" : 18,
      "name" : "Metropolitan",
      "nameShort" : "Metro",
      "link" : "/api/v1/divisions/18",
      "abbreviation" : "M"
    },
    "conference" : {
      "id" : 6,
      "name" : "Eastern",
      "link" : "/api/v1/conferences/6"
    },
    "franchise" : {
      "franchiseId" : 16,
      "teamName" : "Flyers",
      "link" : "/api/v1/franchises/16"
    },
    "shortName" : "Philadelphia",
    "officialSiteUrl" : "http://www.philadelphiaflyers.com/",
    "franchiseId" : 16,
    "active" : true
  }, {
    "id" : 5,
    "name" : "Pittsburgh Penguins",
    "link" : "/api/v1/teams/5",
    "venue" : {
      "id" : 5034,
      "name" : "PPG Paints Arena",
      "link" : "/api/v1/venues/5034",
      "city" : "Pittsburgh",
      "timeZone" : {
        "id" : "America/New_York",
        "offset" : -4,
        "tz" : "EDT"
      }
    },
    "abbreviation" : "PIT",
    "teamName" : "Penguins",
    "locationName" : "Pittsburgh",
    "firstYearOfPlay" : "1967",
    "division" : {
      "id" : 18,
      "name" : "Metropolitan",
      "nameShort" : "Metro",
      "link" : "/api/v1/divisions/18",
      "abbreviation" : "M"
    },
    "conference" : {
      "id" : 6,
      "name" : "Eastern",
      "link" : "/api/v1/conferences/6"
    },
    "franchise" : {
      "franchiseId" : 17,
      "teamName" : "Penguins",
      "link" : "/api/v1/franchises/17"
    },
    "shortName" : "Pittsburgh",
    "officialSiteUrl" : "http://pittsburghpenguins.com/",
    "franchiseId" : 17,
    "active" : true
  }, {
    "id" : 6,
    "name" : "Boston Bruins",
    "link" : "/api/v1/teams/6",
    "venue" : {
      "id" : 5085,
      "name" : "TD Garden",
      "link" : "/api/v1/venues/5085",
      "city" : "Boston",
      "timeZone" : {
        "id" : "America/New_York",
        "offset" : -4,
        "tz" : "EDT"
      }
    },
    "abbreviation" : "BOS",
    "teamName" : "Bruins",
    "locationName" : "Boston",
    "firstYearOfPlay" : "1924",
    "division" : {
      "id" : 17,
      "name" : "Atlantic",
      "nameShort" : "ATL",
      "link" : "/api/v1/divisions/17",
      "abbreviation" : "A"
    },
    "conference" : {
      "id" : 6,
      "name" : "Eastern",
      "link" : "/api/v1/conferences/6"
    },
    "franchise" : {
      "franchiseId" : 6,
      "teamName" : "Bruins",
      "link" : "/api/v1/franchises/6"
    },
    "shortName" : "Boston",
    "officialSiteUrl" : "http://www.bostonbruins.com/",
    "franchiseId" : 6,
    "active" : true
  }, {
    "id" : 7,
    "name" : "Buffalo Sabres",
    "link" : "/api/v1/teams/7",
    "venue" : {
      "id" : 5039,
      "name" : "KeyBank Center",
      "link" : "/api/v1/venues/5039",
      "city" : "Buffalo",
      "timeZone" : {
        "id" : "America/New_York",
        "offset" : -4,
        "tz" : "EDT"
      }
    },
    "abbreviation" : "BUF",
    "teamName" : "Sabres",
    "locationName" : "Buffalo",
    "firstYearOfPlay" : "1970",
    "division" : {
      "id" : 17,
      "name" : "Atlantic",
      "nameShort" : "ATL",
      "link" : "/api/v1/divisions/17",
      "abbreviation" : "A"
    },
    "conference" : {
      "id" : 6,
      "name" : "Eastern",
      "link" : "/api/v1/conferences/6"
    },
    "franchise" : {
      "franchiseId" : 19,
      "teamName" : "Sabres",
      "link" : "/api/v1/franchises/19"
    },
    "shortName" : "Buffalo",
    "officialSiteUrl" : "http://www.sabres.com/",
    "franchiseId" : 19,
    "active" : true
  }, {
    "id" : 8,
    "name" : "Montréal Canadiens",
    "link" : "/api/v1/teams/8",
    "venue" : {
      "id" : 5028,
      "name" : "Bell Centre",
      "link" : "/api/v1/venues/5028",
      "city" : "Montréal",
      "timeZone" : {
        "id" : "America/Montreal",
        "offset" : -4,
        "tz" : "EDT"
      }
    },
    "abbreviation" : "MTL",
    "teamName" : "Canadiens",
    "locationName" : "Montréal",
    "firstYearOfPlay" : "1909",
    "division" : {
      "id" : 17,
      "name" : "Atlantic",
      "nameShort" : "ATL",
      "link" : "/api/v1/divisions/17",
      "abbreviation" : "A"
    },
    "conference" : {
      "id" : 6,
      "name" : "Eastern",
      "link" : "/api/v1/conferences/6"
    },
    "franchise" : {
      "franchiseId" : 1,
      "teamName" : "Canadiens",
      "link" : "/api/v1/franchises/1"
    },
    "shortName" : "Montréal",
    "officialSiteUrl" : "http://www.canadiens.com/",
    "franchiseId" : 1,
    "active" : true
  }, {
    "id" : 9,
    "name" : "Ottawa Senators",
    "link" : "/api/v1/teams/9",
    "venue" : {
      "id" : 5031,
      "name" : "Canadian Tire Centre",
      "link" : "/api/v1/venues/5031",
      "city" : "Ottawa",
      "timeZone" : {
        "id" : "America/New_York",
        "offset" : -4,
        "tz" : "EDT"
      }
    },
    "abbreviation" : "OTT",
    "teamName" : "Senators",
    "locationName" : "Ottawa",
    "firstYearOfPlay" : "1990",
    "division" : {
      "id" : 17,
      "name" : "Atlantic",
      "nameShort" : "ATL",
      "link" : "/api/v1/divisions/17",
      "abbreviation" : "A"
    },
    "conference" : {
      "id" : 6,
      "name" : "Eastern",
      "link" : "/api/v1/conferences/6"
    },
    "franchise" : {
      "franchiseId" : 30,
      "teamName" : "Senators",
      "link" : "/api/v1/franchises/30"
    },
    "shortName" : "Ottawa",
    "officialSiteUrl" : "http://www.ottawasenators.com/",
    "franchiseId" : 30,
    "active" : true
  }, {
    "id" : 10,
    "name" : "Toronto Maple Leafs",
    "link" : "/api/v1/teams/10",
    "venue" : {
      "name" : "Scotiabank Arena",
      "link" : "/api/v1/venues/null",
      "city" : "Toronto",
      "timeZone" : {
        "id" : "America/Toronto",
        "offset" : -4,
        "tz" : "EDT"
      }
    },
    "abbreviation" : "TOR",
    "teamName" : "Maple Leafs",
    "locationName" : "Toronto",
    "firstYearOfPlay" : "1917",
    "division" : {
      "id" : 17,
      "name" : "Atlantic",
      "nameShort" : "ATL",
      "link" : "/api/v1/divisions/17",
      "abbreviation" : "A"
    },
    "conference" : {
      "id" : 6,
      "name" : "Eastern",
      "link" : "/api/v1/conferences/6"
    },
    "franchise" : {
      "franchiseId" : 5,
      "teamName" : "Maple Leafs",
      "link" : "/api/v1/franchises/5"
    },
    "shortName" : "Toronto",
    "officialSiteUrl" : "http://www.mapleleafs.com/",
    "franchiseId" : 5,
    "active" : true
  }, {
    "id" : 12,
    "name" : "Carolina Hurricanes",
    "link" : "/api/v1/teams/12",
    "venue" : {
      "id" : 5066,
      "name" : "PNC Arena",
      "link" : "/api/v1/venues/5066",
      "city" : "Raleigh",
      "timeZone" : {
        "id" : "America/New_York",
        "offset" : -4,
        "tz" : "EDT"
      }
    },
    "abbreviation" : "CAR",
    "teamName" : "Hurricanes",
    "locationName" : "Carolina",
    "firstYearOfPlay" : "1979",
    "division" : {
      "id" : 18,
      "name" : "Metropolitan",
      "nameShort" : "Metro",
      "link" : "/api/v1/divisions/18",
      "abbreviation" : "M"
    },
    "conference" : {
      "id" : 6,
      "name" : "Eastern",
      "link" : "/api/v1/conferences/6"
    },
    "franchise" : {
      "franchiseId" : 26,
      "teamName" : "Hurricanes",
      "link" : "/api/v1/franchises/26"
    },
    "shortName" : "Carolina",
    "officialSiteUrl" : "http://www.carolinahurricanes.com/",
    "franchiseId" : 26,
    "active" : true
  }, {
    "id" : 13,
    "name" : "Florida Panthers",
    "link" : "/api/v1/teams/13",
    "venue" : {
      "id" : 5027,
      "name" : "BB&T Center",
      "link" : "/api/v1/venues/5027",
      "city" : "Sunrise",
      "timeZone" : {
        "id" : "America/New_York",
        "offset" : -4,
        "tz" : "EDT"
      }
    },
    "abbreviation" : "FLA",
    "teamName" : "Panthers",
    "locationName" : "Florida",
    "firstYearOfPlay" : "1993",
    "division" : {
      "id" : 17,
      "name" : "Atlantic",
      "nameShort" : "ATL",
      "link" : "/api/v1/divisions/17",
      "abbreviation" : "A"
    },
    "conference" : {
      "id" : 6,
      "name" : "Eastern",
      "link" : "/api/v1/conferences/6"
    },
    "franchise" : {
      "franchiseId" : 33,
      "teamName" : "Panthers",
      "link" : "/api/v1/franchises/33"
    },
    "shortName" : "Florida",
    "officialSiteUrl" : "http://www.floridapanthers.com/",
    "franchiseId" : 33,
    "active" : true
  }, {
    "id" : 14,
    "name" : "Tampa Bay Lightning",
    "link" : "/api/v1/teams/14",
    "venue" : {
      "id" : 5017,
      "name" : "Amalie Arena",
      "link" : "/api/v1/venues/5017",
      "city" : "Tampa",
      "timeZone" : {
        "id" : "America/New_York",
        "offset" : -4,
        "tz" : "EDT"
      }
    },
    "abbreviation" : "TBL",
    "teamName" : "Lightning",
    "locationName" : "Tampa Bay",
    "firstYearOfPlay" : "1991",
    "division" : {
      "id" : 17,
      "name" : "Atlantic",
      "nameShort" : "ATL",
      "link" : "/api/v1/divisions/17",
      "abbreviation" : "A"
    },
    "conference" : {
      "id" : 6,
      "name" : "Eastern",
      "link" : "/api/v1/conferences/6"
    },
    "franchise" : {
      "franchiseId" : 31,
      "teamName" : "Lightning",
      "link" : "/api/v1/franchises/31"
    },
    "shortName" : "Tampa Bay",
    "officialSiteUrl" : "http://www.tampabaylightning.com/",
    "franchiseId" : 31,
    "active" : true
  }, {
    "id" : 15,
    "name" : "Washington Capitals",
    "link" : "/api/v1/teams/15",
    "venue" : {
      "id" : 5094,
      "name" : "Capital One Arena",
      "link" : "/api/v1/venues/5094",
      "city" : "Washington",
      "timeZone" : {
        "id" : "America/New_York",
        "offset" : -4,
        "tz" : "EDT"
      }
    },
    "abbreviation" : "WSH",
    "teamName" : "Capitals",
    "locationName" : "Washington",
    "firstYearOfPlay" : "1974",
    "division" : {
      "id" : 18,
      "name" : "Metropolitan",
      "nameShort" : "Metro",
      "link" : "/api/v1/divisions/18",
      "abbreviation" : "M"
    },
    "conference" : {
      "id" : 6,
      "name" : "Eastern",
      "link" : "/api/v1/conferences/6"
    },
    "franchise" : {
      "franchiseId" : 24,
      "teamName" : "Capitals",
      "link" : "/api/v1/franchises/24"
    },
    "shortName" : "Washington",
    "officialSiteUrl" : "http://www.washingtoncapitals.com/",
    "franchiseId" : 24,
    "active" : true
  }, {
    "id" : 16,
    "name" : "Chicago Blackhawks",
    "link" : "/api/v1/teams/16",
    "venue" : {
      "id" : 5092,
      "name" : "United Center",
      "link" : "/api/v1/venues/5092",
      "city" : "Chicago",
      "timeZone" : {
        "id" : "America/Chicago",
        "offset" : -5,
        "tz" : "CDT"
      }
    },
    "abbreviation" : "CHI",
    "teamName" : "Blackhawks",
    "locationName" : "Chicago",
    "firstYearOfPlay" : "1926",
    "division" : {
      "id" : 16,
      "name" : "Central",
      "nameShort" : "CEN",
      "link" : "/api/v1/divisions/16",
      "abbreviation" : "C"
    },
    "conference" : {
      "id" : 5,
      "name" : "Western",
      "link" : "/api/v1/conferences/5"
    },
    "franchise" : {
      "franchiseId" : 11,
      "teamName" : "Blackhawks",
      "link" : "/api/v1/franchises/11"
    },
    "shortName" : "Chicago",
    "officialSiteUrl" : "http://www.chicagoblackhawks.com/",
    "franchiseId" : 11,
    "active" : true
  }, {
    "id" : 17,
    "name" : "Detroit Red Wings",
    "link" : "/api/v1/teams/17",
    "venue" : {
      "id" : 5145,
      "name" : "Little Caesars Arena",
      "link" : "/api/v1/venues/5145",
      "city" : "Detroit",
      "timeZone" : {
        "id" : "America/Detroit",
        "offset" : -4,
        "tz" : "EDT"
      }
    },
    "abbreviation" : "DET",
    "teamName" : "Red Wings",
    "locationName" : "Detroit",
    "firstYearOfPlay" : "1926",
    "division" : {
      "id" : 17,
      "name" : "Atlantic",
      "nameShort" : "ATL",
      "link" : "/api/v1/divisions/17",
      "abbreviation" : "A"
    },
    "conference" : {
      "id" : 6,
      "name" : "Eastern",
      "link" : "/api/v1/conferences/6"
    },
    "franchise" : {
      "franchiseId" : 12,
      "teamName" : "Red Wings",
      "link" : "/api/v1/franchises/12"
    },
    "shortName" : "Detroit",
    "officialSiteUrl" : "http://www.detroitredwings.com/",
    "franchiseId" : 12,
    "active" : true
  }, {
    "id" : 18,
    "name" : "Nashville Predators",
    "link" : "/api/v1/teams/18",
    "venue" : {
      "id" : 5030,
      "name" : "Bridgestone Arena",
      "link" : "/api/v1/venues/5030",
      "city" : "Nashville",
      "timeZone" : {
        "id" : "America/Chicago",
        "offset" : -5,
        "tz" : "CDT"
      }
    },
    "abbreviation" : "NSH",
    "teamName" : "Predators",
    "locationName" : "Nashville",
    "firstYearOfPlay" : "1997",
    "division" : {
      "id" : 16,
      "name" : "Central",
      "nameShort" : "CEN",
      "link" : "/api/v1/divisions/16",
      "abbreviation" : "C"
    },
    "conference" : {
      "id" : 5,
      "name" : "Western",
      "link" : "/api/v1/conferences/5"
    },
    "franchise" : {
      "franchiseId" : 34,
      "teamName" : "Predators",
      "link" : "/api/v1/franchises/34"
    },
    "shortName" : "Nashville",
    "officialSiteUrl" : "http://www.nashvillepredators.com/",
    "franchiseId" : 34,
    "active" : true
  }, {
    "id" : 19,
    "name" : "St. Louis Blues",
    "link" : "/api/v1/teams/19",
    "venue" : {
      "id" : 5076,
      "name" : "Enterprise Center",
      "link" : "/api/v1/venues/5076",
      "city" : "St. Louis",
      "timeZone" : {
        "id" : "America/Chicago",
        "offset" : -5,
        "tz" : "CDT"
      }
    },
    "abbreviation" : "STL",
    "teamName" : "Blues",
    "locationName" : "St. Louis",
    "firstYearOfPlay" : "1967",
    "division" : {
      "id" : 16,
      "name" : "Central",
      "nameShort" : "CEN",
      "link" : "/api/v1/divisions/16",
      "abbreviation" : "C"
    },
    "conference" : {
      "id" : 5,
      "name" : "Western",
      "link" : "/api/v1/conferences/5"
    },
    "franchise" : {
      "franchiseId" : 18,
      "teamName" : "Blues",
      "link" : "/api/v1/franchises/18"
    },
    "shortName" : "St Louis",
    "officialSiteUrl" : "http://www.stlouisblues.com/",
    "franchiseId" : 18,
    "active" : true
  }, {
    "id" : 20,
    "name" : "Calgary Flames",
    "link" : "/api/v1/teams/20",
    "venue" : {
      "id" : 5075,
      "name" : "Scotiabank Saddledome",
      "link" : "/api/v1/venues/5075",
      "city" : "Calgary",
      "timeZone" : {
        "id" : "America/Denver",
        "offset" : -6,
        "tz" : "MDT"
      }
    },
    "abbreviation" : "CGY",
    "teamName" : "Flames",
    "locationName" : "Calgary",
    "firstYearOfPlay" : "1980",
    "division" : {
      "id" : 15,
      "name" : "Pacific",
      "nameShort" : "PAC",
      "link" : "/api/v1/divisions/15",
      "abbreviation" : "P"
    },
    "conference" : {
      "id" : 5,
      "name" : "Western",
      "link" : "/api/v1/conferences/5"
    },
    "franchise" : {
      "franchiseId" : 21,
      "teamName" : "Flames",
      "link" : "/api/v1/franchises/21"
    },
    "shortName" : "Calgary",
    "officialSiteUrl" : "http://www.calgaryflames.com/",
    "franchiseId" : 21,
    "active" : true
  }, {
    "id" : 21,
    "name" : "Colorado Avalanche",
    "link" : "/api/v1/teams/21",
    "venue" : {
      "id" : 5064,
      "name" : "Pepsi Center",
      "link" : "/api/v1/venues/5064",
      "city" : "Denver",
      "timeZone" : {
        "id" : "America/Denver",
        "offset" : -6,
        "tz" : "MDT"
      }
    },
    "abbreviation" : "COL",
    "teamName" : "Avalanche",
    "locationName" : "Colorado",
    "firstYearOfPlay" : "1979",
    "division" : {
      "id" : 16,
      "name" : "Central",
      "nameShort" : "CEN",
      "link" : "/api/v1/divisions/16",
      "abbreviation" : "C"
    },
    "conference" : {
      "id" : 5,
      "name" : "Western",
      "link" : "/api/v1/conferences/5"
    },
    "franchise" : {
      "franchiseId" : 27,
      "teamName" : "Avalanche",
      "link" : "/api/v1/franchises/27"
    },
    "shortName" : "Colorado",
    "officialSiteUrl" : "http://www.coloradoavalanche.com/",
    "franchiseId" : 27,
    "active" : true
  }, {
    "id" : 22,
    "name" : "Edmonton Oilers",
    "link" : "/api/v1/teams/22",
    "venue" : {
      "id" : 5100,
      "name" : "Rogers Place",
      "link" : "/api/v1/venues/5100",
      "city" : "Edmonton",
      "timeZone" : {
        "id" : "America/Edmonton",
        "offset" : -6,
        "tz" : "MDT"
      }
    },
    "abbreviation" : "EDM",
    "teamName" : "Oilers",
    "locationName" : "Edmonton",
    "firstYearOfPlay" : "1979",
    "division" : {
      "id" : 15,
      "name" : "Pacific",
      "nameShort" : "PAC",
      "link" : "/api/v1/divisions/15",
      "abbreviation" : "P"
    },
    "conference" : {
      "id" : 5,
      "name" : "Western",
      "link" : "/api/v1/conferences/5"
    },
    "franchise" : {
      "franchiseId" : 25,
      "teamName" : "Oilers",
      "link" : "/api/v1/franchises/25"
    },
    "shortName" : "Edmonton",
    "officialSiteUrl" : "http://www.edmontonoilers.com/",
    "franchiseId" : 25,
    "active" : true
  }, {
    "id" : 23,
    "name" : "Vancouver Canucks",
    "link" : "/api/v1/teams/23",
    "venue" : {
      "id" : 5073,
      "name" : "Rogers Arena",
      "link" : "/api/v1/venues/5073",
      "city" : "Vancouver",
      "timeZone" : {
        "id" : "America/Vancouver",
        "offset" : -7,
        "tz" : "PDT"
      }
    },
    "abbreviation" : "VAN",
    "teamName" : "Canucks",
    "locationName" : "Vancouver",
    "firstYearOfPlay" : "1970",
    "division" : {
      "id" : 15,
      "name" : "Pacific",
      "nameShort" : "PAC",
      "link" : "/api/v1/divisions/15",
      "abbreviation" : "P"
    },
    "conference" : {
      "id" : 5,
      "name" : "Western",
      "link" : "/api/v1/conferences/5"
    },
    "franchise" : {
      "franchiseId" : 20,
      "teamName" : "Canucks",
      "link" : "/api/v1/franchises/20"
    },
    "shortName" : "Vancouver",
    "officialSiteUrl" : "http://www.canucks.com/",
    "franchiseId" : 20,
    "active" : true
  }, {
    "id" : 24,
    "name" : "Anaheim Ducks",
    "link" : "/api/v1/teams/24",
    "venue" : {
      "id" : 5046,
      "name" : "Honda Center",
      "link" : "/api/v1/venues/5046",
      "city" : "Anaheim",
      "timeZone" : {
        "id" : "America/Los_Angeles",
        "offset" : -7,
        "tz" : "PDT"
      }
    },
    "abbreviation" : "ANA",
    "teamName" : "Ducks",
    "locationName" : "Anaheim",
    "firstYearOfPlay" : "1993",
    "division" : {
      "id" : 15,
      "name" : "Pacific",
      "nameShort" : "PAC",
      "link" : "/api/v1/divisions/15",
      "abbreviation" : "P"
    },
    "conference" : {
      "id" : 5,
      "name" : "Western",
      "link" : "/api/v1/conferences/5"
    },
    "franchise" : {
      "franchiseId" : 32,
      "teamName" : "Ducks",
      "link" : "/api/v1/franchises/32"
    },
    "shortName" : "Anaheim",
    "officialSiteUrl" : "http://www.anaheimducks.com/",
    "franchiseId" : 32,
    "active" : true
  }, {
    "id" : 25,
    "name" : "Dallas Stars",
    "link" : "/api/v1/teams/25",
    "venue" : {
      "id" : 5019,
      "name" : "American Airlines Center",
      "link" : "/api/v1/venues/5019",
      "city" : "Dallas",
      "timeZone" : {
        "id" : "America/Chicago",
        "offset" : -5,
        "tz" : "CDT"
      }
    },
    "abbreviation" : "DAL",
    "teamName" : "Stars",
    "locationName" : "Dallas",
    "firstYearOfPlay" : "1967",
    "division" : {
      "id" : 16,
      "name" : "Central",
      "nameShort" : "CEN",
      "link" : "/api/v1/divisions/16",
      "abbreviation" : "C"
    },
    "conference" : {
      "id" : 5,
      "name" : "Western",
      "link" : "/api/v1/conferences/5"
    },
    "franchise" : {
      "franchiseId" : 15,
      "teamName" : "Stars",
      "link" : "/api/v1/franchises/15"
    },
    "shortName" : "Dallas",
    "officialSiteUrl" : "http://www.dallasstars.com/",
    "franchiseId" : 15,
    "active" : true
  }, {
    "id" : 26,
    "name" : "Los Angeles Kings",
    "link" : "/api/v1/teams/26",
    "venue" : {
      "id" : 5081,
      "name" : "STAPLES Center",
      "link" : "/api/v1/venues/5081",
      "city" : "Los Angeles",
      "timeZone" : {
        "id" : "America/Los_Angeles",
        "offset" : -7,
        "tz" : "PDT"
      }
    },
    "abbreviation" : "LAK",
    "teamName" : "Kings",
    "locationName" : "Los Angeles",
    "firstYearOfPlay" : "1967",
    "division" : {
      "id" : 15,
      "name" : "Pacific",
      "nameShort" : "PAC",
      "link" : "/api/v1/divisions/15",
      "abbreviation" : "P"
    },
    "conference" : {
      "id" : 5,
      "name" : "Western",
      "link" : "/api/v1/conferences/5"
    },
    "franchise" : {
      "franchiseId" : 14,
      "teamName" : "Kings",
      "link" : "/api/v1/franchises/14"
    },
    "shortName" : "Los Angeles",
    "officialSiteUrl" : "http://www.lakings.com/",
    "franchiseId" : 14,
    "active" : true
  }, {
    "id" : 28,
    "name" : "San Jose Sharks",
    "link" : "/api/v1/teams/28",
    "venue" : {
      "name" : "SAP Center at San Jose",
      "link" : "/api/v1/venues/null",
      "city" : "San Jose",
      "timeZone" : {
        "id" : "America/Los_Angeles",
        "offset" : -7,
        "tz" : "PDT"
      }
    },
    "abbreviation" : "SJS",
    "teamName" : "Sharks",
    "locationName" : "San Jose",
    "firstYearOfPlay" : "1990",
    "division" : {
      "id" : 15,
      "name" : "Pacific",
      "nameShort" : "PAC",
      "link" : "/api/v1/divisions/15",
      "abbreviation" : "P"
    },
    "conference" : {
      "id" : 5,
      "name" : "Western",
      "link" : "/api/v1/conferences/5"
    },
    "franchise" : {
      "franchiseId" : 29,
      "teamName" : "Sharks",
      "link" : "/api/v1/franchises/29"
    },
    "shortName" : "San Jose",
    "officialSiteUrl" : "http://www.sjsharks.com/",
    "franchiseId" : 29,
    "active" : true
  }, {
    "id" : 29,
    "name" : "Columbus Blue Jackets",
    "link" : "/api/v1/teams/29",
    "venue" : {
      "id" : 5059,
      "name" : "Nationwide Arena",
      "link" : "/api/v1/venues/5059",
      "city" : "Columbus",
      "timeZone" : {
        "id" : "America/New_York",
        "offset" : -4,
        "tz" : "EDT"
      }
    },
    "abbreviation" : "CBJ",
    "teamName" : "Blue Jackets",
    "locationName" : "Columbus",
    "firstYearOfPlay" : "1997",
    "division" : {
      "id" : 18,
      "name" : "Metropolitan",
      "nameShort" : "Metro",
      "link" : "/api/v1/divisions/18",
      "abbreviation" : "M"
    },
    "conference" : {
      "id" : 6,
      "name" : "Eastern",
      "link" : "/api/v1/conferences/6"
    },
    "franchise" : {
      "franchiseId" : 36,
      "teamName" : "Blue Jackets",
      "link" : "/api/v1/franchises/36"
    },
    "shortName" : "Columbus",
    "officialSiteUrl" : "http://www.bluejackets.com/",
    "franchiseId" : 36,
    "active" : true
  }, {
    "id" : 30,
    "name" : "Minnesota Wild",
    "link" : "/api/v1/teams/30",
    "venue" : {
      "id" : 5098,
      "name" : "Xcel Energy Center",
      "link" : "/api/v1/venues/5098",
      "city" : "St. Paul",
      "timeZone" : {
        "id" : "America/Chicago",
        "offset" : -5,
        "tz" : "CDT"
      }
    },
    "abbreviation" : "MIN",
    "teamName" : "Wild",
    "locationName" : "Minnesota",
    "firstYearOfPlay" : "1997",
    "division" : {
      "id" : 16,
      "name" : "Central",
      "nameShort" : "CEN",
      "link" : "/api/v1/divisions/16",
      "abbreviation" : "C"
    },
    "conference" : {
      "id" : 5,
      "name" : "Western",
      "link" : "/api/v1/conferences/5"
    },
    "franchise" : {
      "franchiseId" : 37,
      "teamName" : "Wild",
      "link" : "/api/v1/franchises/37"
    },
    "shortName" : "Minnesota",
    "officialSiteUrl" : "http://www.wild.com/",
    "franchiseId" : 37,
    "active" : true
  }, {
    "id" : 52,
    "name" : "Winnipeg Jets",
    "link" : "/api/v1/teams/52",
    "venue" : {
      "id" : 5058,
      "name" : "Bell MTS Place",
      "link" : "/api/v1/venues/5058",
      "city" : "Winnipeg",
      "timeZone" : {
        "id" : "America/Winnipeg",
        "offset" : -5,
        "tz" : "CDT"
      }
    },
    "abbreviation" : "WPG",
    "teamName" : "Jets",
    "locationName" : "Winnipeg",
    "firstYearOfPlay" : "2011",
    "division" : {
      "id" : 16,
      "name" : "Central",
      "nameShort" : "CEN",
      "link" : "/api/v1/divisions/16",
      "abbreviation" : "C"
    },
    "conference" : {
      "id" : 5,
      "name" : "Western",
      "link" : "/api/v1/conferences/5"
    },
    "franchise" : {
      "franchiseId" : 35,
      "teamName" : "Jets",
      "link" : "/api/v1/franchises/35"
    },
    "shortName" : "Winnipeg",
    "officialSiteUrl" : "http://winnipegjets.com/",
    "franchiseId" : 35,
    "active" : true
  }, {
    "id" : 53,
    "name" : "Arizona Coyotes",
    "link" : "/api/v1/teams/53",
    "venue" : {
      "id" : 5043,
      "name" : "Gila River Arena",
      "link" : "/api/v1/venues/5043",
      "city" : "Glendale",
      "timeZone" : {
        "id" : "America/Phoenix",
        "offset" : -7,
        "tz" : "MST"
      }
    },
    "abbreviation" : "ARI",
    "teamName" : "Coyotes",
    "locationName" : "Arizona",
    "firstYearOfPlay" : "1979",
    "division" : {
      "id" : 15,
      "name" : "Pacific",
      "nameShort" : "PAC",
      "link" : "/api/v1/divisions/15",
      "abbreviation" : "P"
    },
    "conference" : {
      "id" : 5,
      "name" : "Western",
      "link" : "/api/v1/conferences/5"
    },
    "franchise" : {
      "franchiseId" : 28,
      "teamName" : "Coyotes",
      "link" : "/api/v1/franchises/28"
    },
    "shortName" : "Arizona",
    "officialSiteUrl" : "http://www.arizonacoyotes.com/",
    "franchiseId" : 28,
    "active" : true
  }, {
    "id" : 54,
    "name" : "Vegas Golden Knights",
    "link" : "/api/v1/teams/54",
    "venue" : {
      "id" : 5178,
      "name" : "T-Mobile Arena",
      "link" : "/api/v1/venues/5178",
      "city" : "Las Vegas",
      "timeZone" : {
        "id" : "America/Los_Angeles",
        "offset" : -7,
        "tz" : "PDT"
      }
    },
    "abbreviation" : "VGK",
    "teamName" : "Golden Knights",
    "locationName" : "Vegas",
    "firstYearOfPlay" : "2016",
    "division" : {
      "id" : 15,
      "name" : "Pacific",
      "nameShort" : "PAC",
      "link" : "/api/v1/divisions/15",
      "abbreviation" : "P"
    },
    "conference" : {
      "id" : 5,
      "name" : "Western",
      "link" : "/api/v1/conferences/5"
    },
    "franchise" : {
      "franchiseId" : 38,
      "teamName" : "Golden Knights",
      "link" : "/api/v1/franchises/38"
    },
    "shortName" : "Vegas",
    "officialSiteUrl" : "http://www.vegasgoldenknights.com/",
    "franchiseId" : 38,
    "active" : true
  } ]
}"""
nhl = json.loads(nhlJson)
teams = nhl["teams"]

# for team in teams:
#     primaryColor = nhlPrimaryColorMap[int(team["id"])]
#     secondaryColor = nhlSecondaryColorMap[int(team["id"])]
#     print("""{} : Team("{}", "{}", "{}", Color.fromRGBO({}, {}, {}, 1.0), Color.fromRGBO({}, {}, {}, 1.0)),"""
#        .format(team["id"], team["locationName"], team["teamName"], team["abbreviation"],
#        primaryColor.red, primaryColor.green, primaryColor.blue,
#        secondaryColor.red, secondaryColor.green, secondaryColor.blue))


def color_to_hex(color):
    return "{:02x}{:02x}{:02x}".format(color.red, color.green, color.blue)


for team in teams:
    primaryColor = nhlPrimaryColorMap[int(team["id"])]
    secondaryColor = nhlSecondaryColorMap[int(team["id"])]
    print("""{}: {{id: {}, city: "{}", name: "{}", display_name: "{}", abbreviation: "{}", primary_color: "{}", secondary_color: "{}"}},""".format(
        team["id"], team["id"], team["locationName"], team["teamName"], team["teamName"], team["abbreviation"], color_to_hex(primaryColor), color_to_hex(secondaryColor)))


# split = inputString.splitlines()

# for splat in split:
#     words = splat.split(" ")
#     primaryColor = primaryColorMap[int(words[0])]
#     secondaryColor = secondaryColorMap[int(words[0])]
#     print("""{} : Team("{}", "{}", "{}", Color.fromRGBO({}, {}, {}, 1.0), Color.fromRGBO({}, {}, {}, 1.0),"""
#        .format(words[0], words[3], words[2], words[1],
#        primaryColor.red, primaryColor.green, primaryColor.blue,
#        secondaryColor.red, secondaryColor.green, secondaryColor.blue))
# primary = []
# secondary = []

# for splat in split:
#     words = splat.split(" ")
#     colors = input(words[2] + " Primary Colors?\n").split(" ")
#     primary.append(words[0] + ": Color(" + colors[0] + ", " + colors[1] + ", " + colors[2] + "),")

#     colors = input(words[2] + " Secondary Colors?\n").split(" ")
#     secondary.append(words[0] + ": Color(" + colors[0] + ", " + colors[1] + ", " + colors[2] + "),")
#     print("\nPrimary:")
#     for p in primary:
#         print(p)

#     print("\nSeondary:")
#     for p in secondary:
#         print(p)
