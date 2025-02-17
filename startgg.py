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

def MakeRequest(API_KEY, EVENT_QUERY, variables):
    headers = {
            'Authorization': 'Bearer ' + API_KEY,
            'Content-Type': 'application/json'
    }

    response = requests.post(
        "https://api.smash.gg/gql/alpha",
        headers=headers,
        json={'query': EVENT_QUERY, 'variables': variables}
    )

    return response.json()

def GetTop8(tourneySlug: str, eventSlug: str):
    EVENT_QUERY = """query ($tourneySlug: String!, $eventSlug: String!){
    tournament(slug: $tourneySlug){
        events(filter: {slug: $eventSlug}){
            entrants (query: {page: 1}) {
                nodes {
                    participants {
                        player {
                            id
                            prefix
                            gamerTag
                            user {
                                id
                                images {
                                    url
                                }
                            }
                        }
                    }
                    seeds {
                        seedNum
                    }
                    standing {
                        placement
                    }
                }
            }
        }
    }
    }"""

    variables = {
        "tourneySlug": tourneySlug,
        "eventSlug": eventSlug,
    }

    API_KEY = os.getenv("API_KEY")
    return MakeRequest(API_KEY, EVENT_QUERY, variables)

results = GetTop8("leeds-legacy-rivals-pixel-4", "rivals-2-singles")

top_8_players = []

for event in results["data"]["tournament"]["events"]:
    for entrant in event["entrants"]["nodes"]:
        if int(entrant["standing"]["placement"]) < 9:
            for participant in entrant["participants"]:
                player_data = participant["player"]
                name = player_data["gamerTag"]
                prefix = player_data["prefix"] if player_data["prefix"] else ""
                
                # Get the first image URL if available, or use a default
                pfp_url = "No profile picture available"
                if player_data["user"] and player_data["user"]["images"]:
                    for image in player_data["user"]["images"]:
                        pfp_url = image["url"]
                        break  # first image

            # seed information
            seed = None
            for seed_info in entrant["seeds"]:
                seed = seed_info["seedNum"]
                break
            
            placement = entrant["standing"]["placement"]

            top_8_players.append(Player(name, prefix, seed, placement, pfp_url))
        
for player in top_8_players:
    player.PrintInformation()