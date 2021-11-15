from pywebio.input import input, checkbox, select, NUMBER, TEXT
from pywebio.output import put_text, put_button
import pywebio

import json
import os
import uuid
import sys

class GNS3_GUI():

    pywebio.session.set_env(title='GNS3 File Configurator')

    def __init__(self) -> None:
        
        schema_urls = ["https://raw.githubusercontent.com/GNS3/gns3-registry/master/schemas/appliance_v3.json","https://raw.githubusercontent.com/GNS3/gns3-registry/master/schemas/appliance_v4.json","https://raw.githubusercontent.com/GNS3/gns3-registry/master/schemas/appliance_v5.json","https://raw.githubusercontent.com/GNS3/gns3-registry/master/schemas/appliance_v6.json"]
        if os.path.isdir('schemas') == False:
            os.mkdir(os.path.join('schemas'))
            put_button("Download Schema Files", onclick=lambda: [os.popen(f"wget --directory-prefix=schemas {url}") for url in schema_urls], color='success', outline=True)

        shema_number = "".join(checkbox(label="Bitte gewünschtes Shema auswählen",options=["Eigenes Shema","3","4","5","6"]))

        if shema_number == "Eigenes Shema":
            shema = input(label='Bitte absoluten Pfad zur Json Datei eingeben')
        else:
            shema = os.path.dirname(os.path.abspath(__file__)) + "/" + os.path.join('schemas',f"appliance_v{shema_number}.json")
        
        with open(shema) as f:
          schema = json.load(f)

        
        appliance_name = input(label='Appliance filename (example: cisco-asav)')
        if len(appliance_name) == 0:
          appliance_name = "Standart"

        if os.path.isdir('appliances') == False:
          os.mkdir(os.path.join('appliances'))

        with open(os.path.join('appliances', f'{appliance_name}.gns3a'), 'w+') as f:
            appliance = {}
            appliance = self.ask_from_schema(schema)
            appliance['qemu'] = self.ask_from_schema(schema['properties']['qemu'])

            appliance['images'] = []
            files = []
            if self.yesno('Add image?'):
                image = self.ask_from_schema(schema['properties']['images']['items'])
                appliance['images'].append(image)
                files.append(image['filename'])

            appliance['versions'] = []
            if self.yesno('Add appliance version?'):
                version = {'images': {}}
                version['name'] = input('Appliance version name')
                for disk in ['hda_disk_image', 'hdb_disk_image', 'hdc_disk_image', 'hdd_disk_image', 'cdrom_image', 'initrd_image', 'kernel_image']:
                    img = input(label=f"Image for {disk}", required=False)
                    if img:
                        version['images'][disk] = img.get("filename")

                appliance['versions'].append(version)

            json.dump(appliance, f, indent=4)
            sys.exit()


    def yesno(self,question):
        while True:
            answer = select(label=question,options=["yes","no"])
            if answer in ['yes']:
                return True
            if answer in ['no']:
                return False

    def ask_from_schema(self,schema):
        data = {}
        for key, val in schema['properties'].items():

            if key == "appliance_id":
                # generate an unique ID for the appliance
                result = str(uuid.uuid4())
            else:
                optional = not key in schema['required']
                if optional == True:
                    required = False
                else:
                    required = True

                if 'enum' in val:
                    result = select(label=val['title'],options=val['enum']+["None"],required=required)
                    if result == "None":
                        result = None
                elif "user_input" in val:
                    if val['user_input'] != "ignore":
                        result = val['user_input']

                elif val['type'] == "integer":
                    result = input(val['title'], required=required, type=NUMBER)

                elif val['type'] == "string":
                    result = input(val['title'], required=required, type=TEXT)

            if result:
                data[key] = self.val(result)

        return data

    def val(self,value):
        
        try:
            val = int(value)
        except ValueError:
            val = str(value)

        return val


if __name__ == "__main__": 
    GNS3_GUI()
