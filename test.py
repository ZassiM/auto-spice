import json

param = {}

with open("config.json", 'r') as file:
    config = json.load(file)

    xbar = config["crossbar_params"]

    xbar=list(xbar.items())

    if(len(xbar) > 13):
        for i in range(13, len(xbar)):
            param[xbar[i][0]] = xbar[i][1]
        
    print(param)


