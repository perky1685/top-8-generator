import challonge
import os
import requests
from dotenv import load_dotenv
load_dotenv()

class Player:
    def __init__(self, name: str, prefix: str, seed: int, placement: int, pfp_url: str):
        self.name = name
        self.prefix = prefix if prefix else ""
        self.seed = seed
        self.placement = placement
        self.pfp_url = pfp_url

    def PrintInformation(self):
        if self.prefix:
            print(f"{self.prefix} | {self.name} placed {self.placement}")
        else:
            print(f"{self.name} placed {self.placement}")
        print(self.pfp_url)

challonge.set_credentials("phoebie", os.getenv("CHALLONGE_API_KEY"))

# TOURNAMENT ID IS IN CDATA "tournament_id: XXX"
people = challonge.participants.index("TWTOT98")

top_8_players = []

for person in people:
    #print(person["name"])
    name = person["name"]
    prefix = ""
    #print(person["seed"])
    seed = person["seed"]
    #print(person["final_rank"])
    placement = person["final_rank"]
    #print(person["attached_participatable_portrait_url"])
    pfp_url = person["attached_participatable_portrait_url"]

    top_8_players.append(Player(name, prefix, seed, placement, pfp_url))

for player in top_8_players:
    player.PrintInformation()