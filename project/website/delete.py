import json
# bu = []
# t = []
# fro = []
# if 1==1:
#         f = open("user_bus_dict.json")
#         user_bus_dict = json.load(f)
#         f.close()
#         x = user_bus_dict[0]
#         y = x["2"]
#         print(y)
#         for l in y:
#             bus = (l["Bus_num"])
#             from_loc = (l["from_loc"])
#             to_loc = (l["to"])
#             bu.append(bus)
#             t.append(to_loc)
#             fro.append(from_loc)
            
# print(bu)  
try:
    user_bus_dict = {}
    f = open("user_bus_dict.json")
    user_bus_dict = json.load(f)
    f.close()
    emp = user_bus_dict["9"]

    bu=[]
    t=  []
    fro=[]
    for x in emp:
        bus = (x["Bus_num"])
        bu.append(bus)
        too = (x["to"])
        t.append(too)
        from_loc = (x["from_loc"])
        fro.append(from_loc)
    
except KeyError:
    print("KeyError")
    
except json.decoder.JSONDecodeError:
    print("JSONDecodeError")  


        
