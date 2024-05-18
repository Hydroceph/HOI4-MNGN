templateHG="""
division_template = {
	name = "Home Guard"
	regiments = {
		infantry = { x = 0 y = 0 }
		infantry = { x = 0 y = 1 }
		infantry = { x = 1 y = 0 }
		infantry = { x = 1 y = 1 }
	}
}
"""

templateCAV="""
division_template = {
	name = "Cavalry Brigade"
	regiments = {
		cavalry = { x = 0 y = 0 }
		cavalry = { x = 0 y = 1 }
		cavalry = { x = 0 y = 2 }
	}
	priority = 2
}
"""

templateLI="""
division_template = {
	name = "Line Infantry"
	regiments = {
		infantry = { x = 0 y = 0 }
		infantry = { x = 0 y = 1 }
		infantry = { x = 0 y = 2 }
		infantry = { x = 1 y = 0 }
		infantry = { x = 1 y = 1 }
		infantry = { x = 1 y = 2 }
	}
}
"""

division = """
	division = {{
		division_name = {{
			is_name_ordered = yes
			name_order = {od}
		}}
		location = {loc}
		division_template = "{template}"
		start_experience_factor = 0.2
        start_equipment_factor = {eqpt}
	}}
"""



def makeArmy(location:int,numArmies:list[int]) -> str:
    """Make an army following the templates above

    Args:
        location (int): The state to spawn the armies in
        numArmies (list[int]): The number of each of the three base templates to spawn armies in

    Returns:
        str: The string to put into the template file
    """

    def makeBattalion(batType:str, count:int,location:int,eqpt:float=1) -> str:
        retStr = ""
        for bat in range(count):
            retStr += division.format(od=bat+1,loc=location,template=batType,eqpt=eqpt)
        return retStr
    
    hg  = makeBattalion("Home Guard",numArmies[0],location)
    cav = makeBattalion("Cavalry Brigade",numArmies[1],location)
    li  = makeBattalion("Line Infantry",numArmies[2],location,eqpt=0.25)

    return hg + cav + li

#For England:

location = 6103
numArmies = [20,10,20]

army = makeArmy(location,numArmies)

with open("out.txt","w") as f:
    f.write(templateHG)
    f.write(templateCAV)
    f.write(templateLI)
    f.write("units = {")
    f.write(army)
    f.write("}")

