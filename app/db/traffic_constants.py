"""
Constants for the Traffic class.

:Author:     Maded Batara III
:Version:    v1.0 (2016-03-29)
"""

# Root of traffic API website
TRAFFIC_ROOT = "http://trapik.acacialabs.com/api/traffic"

# Traffic density -> corresponding edge weight
WEIGHTS = {
    "LIGHT TRAFFIC": 1,
    "MODERATE TRAFFIC": 2,
    "HEAVY TRAFFIC": 3
}

# !!!!!NOTE!!!!
# This dictionary is a remnant fron v1.0. As the database is 1-based instead
# of 0-based, the node list and the place ID need to be ++ed in order for
# it to be usable.
#
# (List of nodes along path) -> (line, place, direction)
# NOTE: Edge list not necessarily contiguous, but below thing is a
# guarantee:
# Algorithm should generate edge pairs (x, y) where (x, y) is in the graph
# and x comes before y in the edge list. This will then be the key with the
# value equal to the 3-tuples (AREA_ID, LINE_INDEX, DIRECTION) below:
PLACES = {
    # EDSA:
    (199, 187, 3705, 3704, 3702): (1, 0, "south_bound"),                      # Balintawak
    (3702, 3701, 3700, 295, 294): (1, 1, "south_bound"),                      # Kaingin Road
    (294, 293, 292, 296, 298, 299): (1, 2, "south_bound"),                    # Muñoz
    (299, 300, 301): (1, 3, "south_bound"),                                   # Bansalangin
    (301, 302, 318, 320): (1, 4, "south_bound"),                              # North Ave.
    (320, 321, 322, 3547, 3548): (1, 5, "south_bound"),                       # Trinoma
    (3548, 3549, 3550, 3553, 3554, 3555): (1, 6, "south_bound"),              # Quezon Ave.
    (3555, 3556, 3557, 3558, 3559): (1, 7, "south_bound"),                    # NIA Road
    (3559, 1262, 3560): (1, 8, "south_bound"),                                # Timog
    (3560, 3561, 3562): (1, 9, "south_bound"),                                # Kamuning
    (3562, 3564, 3565): (1, 10, "south_bound"),                               # New York - Nepa Q-Mart
    (3565, 3805, 1239): (1, 11, "south_bound"),                               # Monte De Piedad
    (1239, 3566, 3567): (1, 12, "south_bound"),                               # Aurora Blvd.
    (3567, 3568): (1, 13, "south_bound"),                                     # Mc Arthur - Farmers
    (3568, 3569, 3570): (1, 14, "south_bound"),                               # P. Tuazon
    (3570, 3571, 1311): (1, 15, "south_bound"),                               # Main Ave.
    (1311, 3572, 3574, 3774, 3575, 3576): (1, 16, "south_bound"),             # Santolan
    (3576, 3784, 3577, 3578, 3579): (1, 17, "south_bound"),                   # White Plains - Connecticut
    (3579, 3580, 3581, 3583, 3584, 3585, 3586): (1, 18, "south_bound"),       # Ortigas Ave.
    (3586, 3587, 3588, 3589): (1, 19, "south_bound"),                         # SM Megamall
    (3589, 1194, 1195): (1, 20, "south_bound"),                               # Shaw Blvd.
    (1195, 1196): (1, 21, "south_bound"),                                     # Reliance
    (1196, 3835, 1197, 3834): (1, 22, "south_bound"),                         # Pioneer - Boni
    (3834, 3833, 1123, 2388, 1122): (1, 23, "south_bound"),                   # Guadalupe
    (1122, 1121, 1119): (1, 24, "south_bound"),                               # Orense
    (1119, 1118, 1117): (1, 25, "south_bound"),                               # Kalayaan - Estrella
    (1117, 1114, 3597, 3596): (1, 26, "south_bound"),                         # Buendia
    (3596, 1111, 3595): (1, 27, "south_bound"),                               # Ayala Ave.
    (3595, 3594, 3592, 3591): (1, 28, "south_bound"),                         # Arnaiz - Pasay Road
    (3591, 3590, 1080, 1079, 1078): (1, 29, "south_bound"),                   # Magallanes
    (1078, 1076): (1, 30, "south_bound"),                                     # Malibay
    (1076, 869): (1, 31, "south_bound"),                                      # Tramo
    (869, 848, 1498, 841): (1, 32, "south_bound"),                            # Taft Ave.
    (): (1, 33, "south_bound"),                                               # F.B. Harrison
    (841, 842, 843): (1, 34, "south_bound"),                                  # Roxas Boulevard
    (843, 844): (1, 35, "south_bound"),                                       # Macapagal Ave.
    (844, 846, 847): (1, 36, "south_bound"),                                  # Mall of Asia
    # Commonwealth:
    (4798, 4797, 4796, 4803, 4804): (7, 0, "south_bound"),                    # Batasan
    (4804, 4805, 4806): (7, 1, "south_bound"),                                # St. Peter's Church
    (4806, 4807): (7, 2, "south_bound"),                                      # Ever Gotesco
    (4807, 4808): (7, 3, "south_bound"),                                      # Diliman Preparatory School
    (4808, 4809, 4810, 4811): (7, 4, "south_bound"),                          # Zuzuarregi
    (4811, 34, 35): (7, 5, "south_bound"),                                    # General Malvar Hospital
    (35, 36): (7, 6, "south_bound"),                                          # Tandang Sora Eastside
    (36, 37): (7, 7, "south_bound"),                                          # Tandang Sora Westside
    (37, 38, 39): (7, 8, "south_bound"),                                      # Central Ave
    (39, 40, 41): (7, 9, "south_bound"),                                      # Magsaysay Ave
    (41, 42, 43): (7, 10, "south_bound"),                                     # University Ave
    (43, 44, 45): (7, 11, "south_bound"),                                     # Philcoa
    # Quezon Ave.:
    (1406, 46, 47, 48, 49, 477, 476, 475): (2, 0, "south_bound"),             # Elliptical Road
    (475, 474, 471): (2, 1, "south_bound"),                                   # Agham Road
    (471, 470): (2, 2, "south_bound"),                                        # Bantayog Road
    (470, 469): (2, 3, "south_bound"),                                        # Edsa
    (469, 468): (2, 4, "south_bound"),                                        # SGT. Esguera
    (468, 467): (2, 5, "south_bound"),                                        # Scout Albano
    (467, 466, 465, 464): (2, 6, "south_bound"),                              # Scout Borromeo
    (464, 455): (2, 7, "south_bound"),                                        # Scout Santiago
    (455, 454): (2, 8, "south_bound"),                                        # Timog
    (454, 453): (2, 9, "south_bound"),                                        # Scout Reyes
    (453, 452): (2, 10, "south_bound"),                                       # Scout Magbanua
    (452, 440): (2, 11, "south_bound"),                                       # Roces Avenue
    (440, 438): (2, 12, "south_bound"),                                       # Roosevelt Avenue
    (438, 437, 436): (2, 13, "south_bound"),                                  # Dr. Garcia Sr.
    (436, 435): (2, 14, "south_bound"),                                       # Scout Chuatoco
    (435, 434): (2, 15, "south_bound"),                                       # G. Araneta Ave.
    (434, 433): (2, 16, "south_bound"),                                       # Sto. Domingo
    (433, 432): (2, 17, "south_bound"),                                       # Biak na Bato
    (432, 431): (2, 18, "south_bound"),                                       # Banawe
    (431, 430): (2, 19, "south_bound"),                                       # Cordillera
    (430, 400): (2, 20, "south_bound"),                                       # D. Tuazon
    (): (2, 21, "south_bound"),                                               # Speaker Perez
    (400, 397): (2, 22, "south_bound"),                                       # Apo Avenue
    (): (2, 23, "south_bound"),                                               # Kanlaon
    (397, 575): (2, 24, "south_bound"),                                       # Mayon
    # España:
    (575, 578): (3, 0, "south_bound"),                                        # Welcome Rotunda
    (578, 581): (3, 1, "south_bound"),                                        # Bluementritt
    (): (3, 2, "south_bound"),                                                # A. Maceda
    (581, 582): (3, 3, "south_bound"),                                        # Antipolo
    (582, 583): (3, 4, "south_bound"),                                        # Vicente Cruz
    (583, 600, 599): (3, 5, "south_bound"),                                   # Gov. Forbes - Lacson
    (599, 598): (3, 6, "south_bound"),                                        # P.Noval
    (598, 604): (3, 7, "south_bound"),                                        # Lerma
    # C5: (ang messed up ng pathiness niya)
    (75, 1420): (4, 0, "south_bound"),                                        # Tandang Sora
    (1420, 1422, 1423, 1424, 1425, 3723): (4, 1, "south_bound"),              # Capitol Hills
    (1425, 3723, 1426, 3725, 3722, 3726, 3721): (4, 2, "south_bound"),        # University of the Philippines
    (3726, 3721, 3727, 3720, 3728, 3719): (4, 3, "south_bound"),              # C.P. Garcia
    (3719, 3729, 3718): (4, 4, "south_bound"),                                # Miriam College
    (3718, 3717, 3716, 3730, 3731): (4, 5, "south_bound"),                    # Ateneo De Manila University
    (3716, 3731, 3715): (4, 6, "south_bound"),                                # Xavierville
    (3715, 1365): (4, 7, "south_bound"),                                      # Aurora Boulevard
    (): (4, 8, "south_bound"),                                                # P. Tuazon
    (3790, 3796, 3791, 3795, 3792): (4, 9, "south_bound"),                    # Bonny Serrano
    (3795, 3792, 3794, 3203, 3205, 3206, 3209): (4, 10, "south_bound"),       # Libis Flyover
    (3209, 3210, 3211): (4, 11, "south_bound"),                               # Eastwood
    (3211, 3212, 3213, 3214, 3216, 3217): (4, 12, "south_bound"),             # Green Meadows
    (3217, 3218, 3219, 3220): (4, 13, "south_bound"),                         # Ortigas Ave.
    (3220, 2473, 2472): (4, 14, "south_bound"),                               # J. Vargas
    (2472, 2471, 3221, 3222, 3223): (4, 15, "south_bound"),                   # Lanuza
    (3223, 3224, 3225, 2438, 2442, 3227, 3228): (4, 16, "south_bound"),       # Bagong Ilog
    (3228, 2322, 2321, 2319): (4, 17, "south_bound"),                         # Kalayaan
    (2319, 2318, 2317, 2316): (4, 18, "south_bound"),                         # Market! Market!
    # Ortigas:
    (1295, 1296): (8, 0, "south_bound"),                                      # Santolan
    (1296, 1297): (8, 1, "south_bound"),                                      # Madison
    (1297, 1298): (8, 2, "south_bound"),                                      # Roosevelt
    (1298, 1300): (8, 3, "south_bound"),                                      # Club Filipino
    (1300, 1301): (8, 4, "south_bound"),                                      # Wilson
    (1301, 1302): (8, 5, "south_bound"),                                      # Connecticut
    (1302, 1303): (8, 6, "south_bound"),                                      # La Salle Greenhills
    (1303, 1304): (8, 7, "south_bound"),                                      # POEA
    (1304, 1305): (8, 8, "south_bound"),                                      # EDSA Shrine
    (1305, 2455): (8, 9, "south_bound"),                                      # San Miguel Ave
    (2455, 2454): (8, 10, "south_bound"),                                     # Meralco Ave
    (2454, 2552, 2553): (8, 11, "south_bound"),                               # Medical City
    (2553, 2554): (8, 12, "south_bound"),                                     # Lanuza Ave
    (2554, 2462): (8, 13, "south_bound"),                                     # Greenmeadows Ave.
    (2462, 2465, 2466): (8, 14, "south_bound"),                               # C5 Flyover
    # Marcos Highway:
    (3014, 3013, 3012, 3011): (9, 0, "south_bound"),                          # SM City Marikina
    (3011, 3010, 3009): (9, 1, "south_bound"),                                # LRT-2 Station
    (3009, 3008, 3007): (9, 2, "south_bound"),                                # Dona Juana
    (3007, 3006): (9, 3, "south_bound"),                                      # Amang Rodriguez
    (3006, 3005): (9, 4, "south_bound"),                                      # F. Mariano Ave
    (3005, 3003, 3002): (9, 5, "south_bound"),                                # Robinson's Metro East
    (3002, 3001): (9, 6, "south_bound"),                                      # San Benildo School
    # Roxas Blvd.:
    (3773, 721, 722): (5, 0, "south_bound"),                                  # Anda Circle
    (722, 724, 732): (5, 1, "south_bound"),                                   # Finance Road
    (): (5, 2, "south_bound"),                                                # U.N. Avenue
    (): (5, 3, "south_bound"),                                                # Pedro Gil
    (): (5, 4, "south_bound"),                                                # Rajah Sulayman
    (3614, 3616): (5, 5, "south_bound"),                                      # Quirino
    (3616, 806, 3617, 3618): (5, 6, "south_bound"),                           # Pablo Ocampo
    (3618, 876, 3619, 3620, 3621): (5, 7, "south_bound"),                     # Buendia
    (3621, 3622, 1468): (5, 8, "south_bound"),                                # Edsa Extension
    (1468, 1469): (5, 9, "south_bound"),                                      # Baclaran
    (1469, 1470, 1471, 1472, 1473, 1474): (5, 10, "south_bound"),             # Airport Road
    (1474, 1475, 1476, 1478, 1479): (5, 11, "south_bound"),                   # Coastal Road
    # SLEX:
    (1082, 1080, 2147, 2146, 2145, 2144): (6, 0, "south_bound"),              # Magallanes
    (2144, 2142, 2141, 2140): (6, 1, "south_bound"),                          # Nichols
    (2140, 2139, 2138): (6, 3, "south_bound"),                                # Merville Exit
    (2138, 2137, 2127, 2126, 2124, 2125): (6, 2, "south_bound"),              # C5 On-ramp
    (2125, 2123, 2122, 2119, 2118, 2117, 2116, 2115): (6, 4, "south_bound"),  # Bicutan Exit
    (2115, 2114, 2113, 2112, 1571, 1814, 1815, 1816): (6, 5, "south_bound"),  # Sucat Exit
    (1816, 1817, 1818, 1819, 1820, 1822, 1823, 1824): (6, 6, "south_bound"),  # Alabang Exit
    # NLEX: (WALANG MAP VIEW!!! smh)
    (): (10, 0, "south_bound"),               # Sta. Ines
    (): (10, 1, "south_bound"),               # Dau
    (): (10, 2, "south_bound"),               # Angeles
    (): (10, 3, "south_bound"),               # Merville Exit
    (): (10, 4, "south_bound"),               # San Fernando
    (): (10, 5, "south_bound"),               # San Simon
    (): (10, 6, "south_bound"),               # Pulilan
    (): (10, 7, "south_bound"),               # Sta. Rita
    (): (10, 8, "south_bound"),               # Balagtas
    (): (10, 9, "south_bound"),               # Tabang
    (): (10, 10, "south_bound"),              # Bocaue
    (): (10, 11, "south_bound"),              # Marilao
    (): (10, 12, "south_bound"),              # Meycauayan
    (): (10, 13, "south_bound"),              # Valenzuela
    (): (10, 14, "south_bound"),              # Mindanao Avenue
    (): (10, 15, "south_bound")               # Balintawak
}

# Area numbers (as per API docs) -> names
AREAS = {
    1: "EDSA",
    2: "Quezon Ave.",
    3: "España",
    4: "C5",
    5: "Roxas Blvd.",
    6: "SLEX",
    7: "Commonwealth",
    8: "Ortigas",
    9: "Marcos Highway",
    10: "NLEX"
}
