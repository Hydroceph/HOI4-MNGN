# note - to run python from PS on windows, you need to cal `py` rather than `python`
import json
from loguru import logger
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import BaseModel


# lookup for ship shorthand
BOATS={
    #capital
    "BB" :"Battleship",
    "BC" :"Battlecruiser",
    "CA" :"Heavy Cruiser",
    "CV" :"Carrier",
    #screen
    "DD" :"Destroyer",
    "CL" :"Light Cruiser",
    #submersable
    "SS" :"Submarine"
}

BOATS_DEFINITIONS={
    #capital
    "BB" :"battleship",
    "BC" :"battle_cruiser",
    "CA" :"heavy_cruiser",
    "CV" :"carrier",
    #screen
    "DD" :"destroyer",
    "CL" :"light_ruiser",
    #submersable
    "SS" :"submarine"
}

HULLS={
        #capital
    "BB" :"ship_hull_heavy_1",
    "BC" :"ship_hull_heavy_1",
    "CA" :"ship_hull_cruiser_1",
    "CV" :"ship_hull_carrier_conversion_bb",
    #screen
    "DD" :"ship_hull_light_1",
    "CL" :"ship_hull_cruiser_1",
    #submersable
    "SS" :"ship_hull_submarine_1"
}

# custom class definitions for making fleet OOBs. Extends from pydantic basemodel for type checking
class Ship(BaseModel):
    name:str
    definition:str
    hull:str
    version_name:str

class TaskForce(BaseModel):
    name:str
    ships:list[Ship]

class Fleet(BaseModel):
    name:str
    location:int
    tf:TaskForce
    owner:str



logger.debug("Reading in navy template file")
with open("scripts/navy_replacement.json", mode="r") as f:
    customisation = json.load(f)
logger.debug(f"cust: {customisation}")

players = customisation.get("players")
fleet_designs = customisation.get("fleet_designs")

logger.debug("Reading in OOB template file")
env = Environment(
    loader = FileSystemLoader("scripts/templates/jinja_templates"),
    autoescape=select_autoescape()
)
template = env.get_template("fleet.jinja")

base_dir = os.curdir
logger.debug(f"cwd: {base_dir}")
# for each major country
for country in players[0]:
    print(country)

    # remove existing navy OOB
    oob = country.get("oob_path")
    logger.debug(f"Testing if path to oob exists: {oob}")
    logger.debug(os.path.exists(oob))
    if os.path.exists(oob):
        logger.warning("not removing while in dev - writing to temp file first.")
        pass
        #os.remove(oob)
        #logger.debug("File removed.")
    else:
        logger.warning("oob file not found.")
    
    # read in custom navy names from `navy_replacement.json`

    # hold all the fleets
    fleets = []
    # keep track of how many of each boat we have, for when we run out of named boats
    counters:dict = {x:1 for x in BOATS.keys()}

    ship_names:list[str] = country.get("list_of_names")

    fleet_iter = {
        "strike_force":country.get("sf_names"),
        "detection":country.get("dt_names"),
        "wolfpack":country.get("wp_names")}


    for fleet_type, fleet_names in fleet_iter.items():
    # make the strike force fleets
        sf_design:dict = fleet_designs.get(fleet_type)
        for fleet_name in fleet_names:
            ships = []
            # make all the capital ships
            if sf_design.get("capital") is not None:
                for ship_type in sf_design.get("capital").keys():
                    for s in range(sf_design.get("capital").get(ship_type)):
                        if ship_names:
                            name = ship_names.pop()
                        else:
                            count = counters.get(ship_type)
                            name = f"{BOATS.get(ship_type)} {count}"
                            counters[ship_type] = counters[ship_type] + 1

                        ships.append(Ship(
                            name=name,
                            definition=BOATS_DEFINITIONS.get(ship_type).lower(),
                            hull = HULLS.get(ship_type),
                            version_name=f"Standard {BOATS.get(ship_type)}"
                        ))

            # make all the screens
            if sf_design.get("screen") is not None:
                for ship_type in sf_design.get("screen").keys():
                    for s in range(sf_design.get("screen").get(ship_type)):
                        count = counters.get(ship_type)
                        name = f"{BOATS.get(ship_type)} {count}"
                        counters[ship_type] = counters[ship_type] + 1

                        ships.append(Ship(
                            name=name,
                            definition=BOATS_DEFINITIONS.get(ship_type).lower(),
                            hull = HULLS.get(ship_type),
                            version_name=f"Standard {BOATS.get(ship_type)}"
                        ))

            # make all the subs
            if sf_design.get("wolfpack") is not None:
                for ship_type in sf_design.get("wolfpack").keys():
                    for s in range(sf_design.get("wolfpack").get(ship_type)):

                        count = counters.get(ship_type)
                        name = f"{BOATS.get(ship_type)} {count}"
                        counters[ship_type] = counters[ship_type] + 1

                        ships.append(Ship(
                            name=name,
                            definition=BOATS.get(ship_type).lower(),
                            hull = HULLS.get(ship_type),
                            version_name=f"Standard {BOATS.get(ship_type)}"
                        ))

            # make the task force to hold them
            tf = TaskForce(
                name=fleet_name,
                ships = ships
            )
            ft = Fleet(
                name = fleet_name,
                location = country.get("main_location"),
                tf = tf,
                owner = country.get("country")
            )
            fleets.append(ft)

    packed = template.render(fleets=fleets)
    print(packed)

    with open("exampleOOB.txt", "w") as f:
        #TODO do something smart here to remove the whiteline only lines
        f.write(packed)


    # create replacement navy in correct location