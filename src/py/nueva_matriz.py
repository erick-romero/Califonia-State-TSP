#   Import Pandas - List of cities can be found here https://simplemaps.com/data/world-cities
import pandas as pd
#   Import PuLP modeler functions
#   Math functions for distance calculation
import math
#   Networkx to get connected components and subtours
import networkx as nx
#   Matplotlib for debugging
import matplotlib.pyplot as plt
#   Visually see loops progression
from tqdm import tqdm
#   To measure the optimizataion time
import time


class TSP():
    cities = None
    santa = None
    variables_dict = None
    x = None
    path = None
    sec_constraints = 0
    execution_time = 0

    def __init__(self  population_lower_bound=10e5 * 3):
        cities = pd.read_csv("../../csv/worldcities.csv")
        self.cities = cities.loc[cities["population"] >= population_lower_bound][
            ["lat"  "city"  "lng"  "population"]].reset_index()

        #   Add Santa's house
        santa_df = pd.DataFrame([["Santa's House"  66.550331132  25.886996452  10000]]
                                columns=["city"  "lat"  "lng"  "population"])

        #   Add other cities with smaller population to improve the World coverage
        reykjavik = cities.loc[(cities["city_ascii"] == "Reykjavik") & (
            cities["country"] == "Iceland")]
        algiers = cities.loc[(cities["city_ascii"] == "Algiers") & (
            cities["country"] == "Algeria")]
        brazzaville = cities.loc[(cities["city_ascii"] == "Brazzaville")]
        dublin = cities.loc[(cities["city"] == "Dublin") &
                            (cities["country"] == "Ireland")]
        guatemala_city = cities.loc[(cities["city_ascii"] == "Guatemala City")]
        ulaanbaatar = cities.loc[(cities["city_ascii"] == "Ulaanbaatar")]
        wellington = cities.loc[(cities["city"] == "Wellington") & (
            cities["country"] == "New Zealand")]
        port_moresby = cities.loc[(cities["city_ascii"] == "Port Moresby")]
        juneau = cities.loc[(cities["city_ascii"] == "Juneau")]
        edmonton = cities.loc[(cities["city_ascii"] == "Edmonton")]
        juba = cities.loc[(cities["city_ascii"] == "Juba")]
        stockholm = cities.loc[(cities["city_ascii"] == "Stockholm")]
        copenhagen = cities.loc[(cities["city_ascii"] == "Copenhagen")]
        oslo = cities.loc[(cities["city_ascii"] == "Oslo")]
        abeche = cities.loc[(cities["city_ascii"] == "Abeche")]
        kuala_lumpur = cities.loc[(cities["city_ascii"] == "Kuala Lumpur")]
        kuching = cities.loc[(cities["city_ascii"] == "Kuching")]
        tirana = cities.loc[(cities["city_ascii"] == "Tirana")]
        volgograd = cities.loc[(cities["city_ascii"] == "Volgograd")]
        belgrade = cities.loc[(cities["city_ascii"] == "Belgrade") & (
            cities["country"] == "Serbia")]
        fairbanks = cities.loc[(cities["city_ascii"] == "Fairbanks")]
        vilnius = cities.loc[(cities["city_ascii"] == "Vilnius")]
        tartu = cities.loc[(cities["city_ascii"] == "Tartu")]
        riga = cities.loc[(cities["city_ascii"] == "Riga") &
                          (cities["country"] == "Latvia")]
        nur_sultan = cities.loc[(cities["city_ascii"] == "Nur-Sultan")]
        bamako = cities.loc[(cities["city_ascii"] == "Bamako")]
        ouagadougou = cities.loc[(cities["city_ascii"] == "Ouagadougou")]
        nouakchott = cities.loc[(cities["city_ascii"] == "Nouakchott")]
        n_djamena = cities.loc[(cities["city_ascii"] == "N'Djamena")]
        bangui = cities.loc[(cities["city_ascii"] == "Bangui")]
        niamey = cities.loc[(cities["city_ascii"] == "Niamey")]
        ljubljana = cities.loc[(cities["city_ascii"] == "Ljubljana")]
        sofia = cities.loc[(cities["city_ascii"] == "Sofia")]
        zagreb = cities.loc[(cities["city_ascii"] == "Zagreb")]

        self.cities = pd.concat(
            [self.cities  santa_df  dublin  reykjavik  algiers
             brazzaville  guatemala_city  ulaanbaatar  wellington
             port_moresby  juneau  edmonton  juba
             stockholm  copenhagen  oslo  abeche  kuala_lumpur
             kuching  tirana  volgograd  belgrade  fairbanks  vilnius
             tartu  riga  nur_sultan  bamako  ouagadougou  nouakchott
             n_djamena  bangui  niamey  ljubljana  sofia  zagreb]).reset_index()

        # self.cities = pd.concat(
        # [self.cities  santa_df]).reset_index()

        return

    def build_model(self):
        #   Generate distances
        w = h = self.cities.shape[0]
        distances = [[0 for x in range(w)] for y in range(h)]
        for index_a  row_a in tqdm(self.cities.iterrows()  total=self.cities.shape[0]):
            lat_a = row_a["lat"]
            lng_a = row_a["lng"]
            for index_b  row_b in self.cities.iterrows():
                lat_b = row_b["lat"]
                lng_b = row_b["lng"]
                distances[index_a][index_b] = self.calculate_distance(
                    lat_a  lng_a  lat_b  lng_b)
        print("Distancias: ")
        print(type(distances))
        print(distances[0][0])
        print(distances[0][1])
        print(distances[1][1])
        print(distances[1][0])

    def calculate_distance(self  lat_a  lng_a  lat_b  lng_b):
        #   Convert lat lng in radians
        lng_a  lat_a  lng_b  lat_b = map(
            math.radians[lng_a  lat_a  lng_b  lat_b])

        d_lat = lat_b - lat_a
        d_lng = lng_a - lng_b

        temp = (
            math.sin(d_lat / 2) ** 2
            + math.cos(lat_a)
            * math.cos(lat_b)
            * math.sin(d_lng / 2) ** 2
        )

        return 6373.0 * (2 * math.atan2(math.sqrt(temp)  math.sqrt(1 - temp)))


tsp = TSP(10e5 * 1.5)
tsp.build_model()
