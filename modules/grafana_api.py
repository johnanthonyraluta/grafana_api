from jinja2 import Environment, FileSystemLoader
from starlette.responses import FileResponse
import json
import os

file_path_windows = "C:\\Users\\raluta\\nso_parser\\grafana_api\\output_"
file_path_linux = "/mnt/c/Users/jraluta/nso_parser/grafana_api/output_"

def generate_config(data):
    file_loader = FileSystemLoader('templates/')
    env = Environment(loader=file_loader)
    template = env.get_template("panel.j2")
    output = template.render(data=data)
    return output

def template(unique_id):
    if os.path.exists(file_path_linux + unique_id +'.json'):
        my_json= FileResponse(file_path_linux+ unique_id +'.json', media_type='application/octet-stream',\
                              filename='output_'+unique_id +'.json')
        return my_json
    return {'error' : 'File ' + unique_id +'.json' + ' not found!'}

def grafana_json(unique_id,uuid4):
    base = json.loads(open("./templates/base.json", "r").read())
    try:
        filesize = os.path.getsize("./interfaces_"+ unique_id + ".txt")
    except:
        return {"error": "./interfaces_"+ unique_id + ".txt" + ' not found'}
    if filesize ==0:
        return {'error':'No services found, check your uploaded file!'}
    if filesize !=0:
        csv_data = open("./interfaces_"+ unique_id + ".txt", "r").read().split("\n")
        # for x in csv_data:
        #     #print({"hostname": x.split(",")[0], "interface":x.split(",")[1]})
        #     if x != '':
        #         file_reader = {"hostname": x.split(",")[0], "interface": x.split(",")[1]}
        #     else:
        #         break
        file_reader = [{"hostname": x.split(",")[0], "interface":x.split(",")[1]} for x in csv_data]
        counter = 0
        posy_even = 1
        posy_odd = 1
        # for x in file_reader:
        #     x["id"] = counter
        #     counter = counter + 1
        #     output = generate_config(x)
        #     data = json.loads(output)
        #     base["panels"].append(data)
        for i,x in enumerate(file_reader):
            if (i % 2) == 0:
                x["x"] = 0
                x["y"] = posy_even
                posy_even = posy_even + 9
            if (i % 2) !=0:
                x["x"] = 12
                x["y"] = posy_odd
                posy_odd = posy_odd + 9
            x["id"] = counter
            counter = counter + 1
            output = generate_config(x)
            data = json.loads(output)
            base["panels"].append(data)
        print(len(base["panels"]))
        base["title"] = unique_id
        base["uid"] = uuid4
        file_writer = open("./output_" + unique_id + ".json", "w")
        file_writer.write(json.dumps(base))
    return(200)
