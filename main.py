from jinja2 import Environment, FileSystemLoader
import uuid
import json

def generate_config(data):
    file_loader = FileSystemLoader('templates/')
    env = Environment(loader=file_loader)
    template = env.get_template("panel.j2")
    output = template.render(data=data)
    return output


base = json.loads(open("templates/base.json","r").read())
csv_data = open("interfaces.txt","r").read().split("\n")
for x in csv_data:
    print({"hostname": x.split(",")[0], "interface":x.split(",")[1]})
file_reader = [ {"hostname": x.split(",")[0], "interface":x.split(",")[1]} for x in csv_data]
counter = 0
for x in file_reader:
    x["id"] = counter
    counter = counter + 1
    output = generate_config(x)
    data = json.loads(output)

    base["panels"].append(data)

print(len(base["panels"]))
file_writer = open("output.json","w")
file_writer.write(json.dumps(base))