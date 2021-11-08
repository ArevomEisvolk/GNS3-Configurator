import tkinter
import os,sys
import json
import tkinter as tk
from tkinter import filedialog as fd 
from functools import partial

from tkinter import ttk

from tkinter import *
import json
import os
import sys
from typing_extensions import ParamSpecArgs
import uuid


import tkinter as tk
from tkinter import ttk
from typing import Text
class Shema():
    
    json_shema="""
    {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "title": "JSON schema validating a GNS3 appliance",

  "definitions": {
    "dynamips_slot": {
        "enum": ["C2600-MB-2FE", "C2600-MB-1E", "PA-A1", "PA-8E", "C1700-MB-1FE", "PA-8T", "PA-2FE-TX", "PA-FE-TX", "PA-GE", "C2600-MB-2E", "C7200-IO-FE", "NM-4T", "C2600-MB-1FE", "C7200-IO-2FE", "PA-POS-OC3", "PA-4T+", "C1700-MB-WIC1", "NM-16ESW", "C7200-IO-GE-E", "NM-4E", "GT96100-FE", "NM-1FE-TX", "Leopard-2FE", "NM-1E", "PA-4E", ""]
    },

    "dynamips_wic": {
        "enum": ["WIC-1ENET", "WIC-1T", "WIC-2T", ""]
    }
  },

  "properties": {
    "appliance_id": {
      "title": "Appliance ID",
      "type": "string",
      "minLength": 36,
      "maxLength": 36,
      "pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
    },
    "name": {
      "type": "string",
      "title": "Appliance name"
    },
    "category": {
      "enum": [
          "router",
          "multilayer_switch",
          "firewall",
          "guest"
      ],
      "title": "Category of the appliance"
    },
    "description": {
      "type": "string",
      "title": "Description of the appliance. Could be a marketing description"
    },
    "vendor_name": {
      "type": "string",
      "title": "Name of the vendor"
    },
    "vendor_url": {
      "type": "string",
      "format": "uri",
      "title": "Website of the vendor"
    },
    "documentation_url": {
      "type": "string",
      "format": "uri",
      "title": "An optional documentation for using the appliance on vendor website"
    },
    "product_name": {
      "type": "string",
      "title": "Product name"
    },
    "product_url": {
      "type": "string",
      "format": "uri",
      "title": "An optional product url on vendor website"
    },
    "registry_version": {
      "enum": [1, 2, 3, 4, 5],
      "title": "Version of the registry compatible with this appliance"
    },
    "status": {
      "enum": ["stable", "experimental", "broken"],
      "title": "Document if the appliance is working or not"
    },
    "availability": {
      "enum": ["free", "with-registration", "free-to-try", "service-contract"],
      "title": "About image availability"
    },
    "maintainer": {
      "type": "string",
      "title": "Maintainer name"
    },
    "maintainer_email": {
      "type": "string",
      "format": "email",
      "title": "Maintainer email"
    },
    "usage": {
        "type": "string",
        "title": "How to use the appliance"
    },
    "symbol": {
      "type": "string",
      "title": "An optional symbol for the appliance"
    },

    "qemu": {
      "type": "object",
      "title": "Qemu specific options",
      "properties": {
        "adapter_type": {
          "enum": [
              "e1000",
              "i82550",
              "i82551",
              "i82557a",
              "i82557b",
              "i82557c",
              "i82558a",
              "i82558b",
              "i82559a",
              "i82559b",
              "i82559c",
              "i82559er",
              "i82562",
              "i82801",
              "ne2k_pci",
              "pcnet",
              "rtl8139",
              "virtio",
              "virtio-net-pci",
              "vmxnet3"
          ],
          "title": "Type of network adapter"
        },
        "adapters": {
          "type": "integer",
          "title": "Number of adapters"
        },
        "ram": {
          "type": "integer",
          "title": "Ram allocated to the appliance (MB)"
        },
        "cpus": {
          "type": "integer",
          "title": "Number of Virtual CPU"
        },
        "hda_disk_interface": {
            "enum": ["ide", "scsi", "sd", "mtd", "floppy", "pflash", "virtio", "sata"],
            "title": "Disk interface for the installed hda_disk_image"
        },
        "hdb_disk_interface": {
            "enum": ["ide", "scsi", "sd", "mtd", "floppy", "pflash", "virtio", "sata"],
            "title": "Disk interface for the installed hdb_disk_image"
        },
        "hdc_disk_interface": {
            "enum": ["ide", "scsi", "sd", "mtd", "floppy", "pflash", "virtio", "sata"],
            "title": "Disk interface for the installed hdc_disk_image"
        },
        "hdd_disk_interface": {
            "enum": ["ide", "scsi", "sd", "mtd", "floppy", "pflash", "virtio", "sata"],
            "title": "Disk interface for the installed hdd_disk_image"
        },
        "arch": {
          "enum": ["aarch64", "alpha", "arm", "cris", "i386", "lm32", "m68k", "microblaze", "microblazeel", "mips", "mips64", "mips64el", "mipsel", "moxie", "or32", "ppc", "ppc64", "ppcemb", "s390x", "sh4", "sh4eb", "sparc", "sparc64", "tricore", "unicore32", "x86_64", "xtensa", "xtensaeb"],
          "title": "Architecture emulated"
        },
        "console_type": {
          "enum": ["telnet", "vnc", "spice"],
          "title": "Type of console connection for the administration of the appliance"
        },
        "boot_priority": {
            "enum": ["d", "c", "dc", "cd", "n", "nc", "nd", "cn", "dn"],
            "title": "Optional define the disk boot priory. Refer to -boot option in qemu manual for more details."
        },
        "kernel_command_line": {
            "type": "string",
            "title": "Command line parameters send to the kernel"
        },
        "kvm": {
            "title": "KVM requirements",
            "enum": ["require", "allow", "disable"]
        },
        "options": {
            "type": "string",
            "title": "Optional additional qemu command line options"
        }
      },
      "required": [
          "adapter_type",
          "adapters",
          "ram",
          "arch",
          "console_type",
          "kvm"
      ]
    },
    "images": {
      "type": "array",
      "title": "Images for this appliance",
      "items": {
        "type": "object",
        "title": "An image file",
        "properties": {
          "filename": {
            "type": "string",
            "title": "Filename"
          },
          "version": {
            "type": "string",
            "title": "Version of the file"
          },
          "md5sum": {
            "type": "string",
            "title": "md5sum of the file",
            "type": "string",
            "pattern": "^[a-f0-9]{32}$"
          },
          "filesize": {
              "type": "integer",
              "title": "File size in bytes"
          },
          "download_url": {
            "type": "string",
            "format": "uri",
            "title": "Download url where you can download the appliance from a browser"
          },
          "direct_download_url": {
            "type": "string",
            "format": "uri",
            "title": "Optional. Non authenticated url to the image file where you can download the image."
          },
          "compression": {
            "enum": ["bzip2", "gzip", "lzma", "xz", "rar", "zip", "7z"],
            "title": "Optional, compression type of direct download url image."
          }
        },
        "required": [
            "filename",
            "version",
            "md5sum",
            "filesize"
        ]
      }
    },
    "versions": {
      "type": "array",
      "title": "Versions of the appliance",
      "items": {
        "type": "object",
        "title": "A version of the appliance",
        "properties": {
          "name": {
            "type": "string",
            "title": "Name of the version"
          },
          "idlepc": {"type": "string", "pattern": "^0x[0-9a-f]{8}"},
          "images": {
            "type": "object",
            "title": "Images used for this version",
            "properties": {
              "kernel_image": {
                "type": "string",
                "title": "Kernel image"
              },
              "initrd": {
                "type": "string",
                "title": "Initrd disk image"
              },
              "image": {
                "type": "string",
                "title": "OS image"
              },
              "bios_image": {
                "type": "string",
                "title": "Bios image"
              },
              "hda_disk_image": {
                "type": "string",
                "title": "Hda disk image"
              },
              "hdb_disk_image": {
                "type": "string",
                "title": "Hdc disk image"
              },
              "hdc_disk_image": {
                "type": "string",
                "title": "Hdd disk image"
              },
              "hdd_disk_image": {
                "type": "string",
                "title": "Hdd diskimage"
              },
              "cdrom_image": {
                "type": "string",
                "title": "cdrom image"
              }
            }
          }
        },
        "required": [
            "name"
        ]
      }
    }
  },
  "required": [
    "appliance_id",
    "name",
    "category",
    "description",
    "vendor_name",
    "vendor_url",
    "product_name",
    "registry_version",
    "status",
    "maintainer",
    "maintainer_email"
  ]
}

    """

    shema = json.loads(json_shema)

class GUI():
    Keyword = []

    def create_input_frame(self,container,Text):

        frame = ttk.Frame(container)

        # grid layout for the input frame
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(0, weight=3)

        # Find what
        ttk.Label(frame, text=Text).grid(column=0, row=0, sticky=tk.W)
        self.var = StringVar()
        keyword = ttk.Entry(frame, width=30,textvariable = self.var)
        keyword.focus()
        keyword.grid(column=1, row=0, sticky=tk.W)
        

        return frame

    def create_label_frame(self,container,Text):

        frame = ttk.Frame(container)

        ttk.Label(frame, text=Text).grid(column=0, row=0, sticky=tk.W)

        return frame

    def create_file_dialog_frame(self,container,disk):
        
        def filedialog():
            try:
                self.image =  fd.askopenfilename()
            except:
                pass


        self.image = ""
        frame = ttk.Frame(container)

        frame.columnconfigure(0, weight=1)
        
        file = ttk.Button(frame, text=disk ,command=partial(filedialog)).grid(column=0, row=5)
        

        return frame

    def create_dropdown_frame(self,container,option_list):

        frame = ttk.Frame(container)

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(0, weight=3)

        variable = tk.StringVar(frame)
        variable.set(option_list[0])
        
        opt = tk.OptionMenu(frame, variable, *option_list)
        opt.config(width=90, font=('Helvetica', 12))
        opt.pack(side="top")

        labelTest = tk.Label(text="", font=('Helvetica', 12), fg='green')
        labelTest.pack(side="top")
        self.drop = ""
        def callback(*args):
            labelTest.configure(text="The selected item is {}".format(variable.get()))
            self.drop = variable.get()
        
        variable.trace("w", callback)
        
        self.drop = variable.get()
        

        
        return frame


    def destroy_root(self,container):


        frame = ttk.Frame(container)

        frame.columnconfigure(0)
        frame.grid_rowconfigure(0)
        
        ttk.Button(frame, text="weiter" ,command=partial(self.destroy)).grid(column=0, row=5)


        return frame

    def exit_root(self,container):


        frame = ttk.Frame(container)

        frame.columnconfigure(1)
        frame.grid_rowconfigure(1)
        ttk.Button(frame, text="exit" ,command=partial(os._exit,0)).grid(column=2, row=6)


        return frame
        
    def destroy(self): 
        self.root.destroy()

    def restart(self):
        self.__init__()        


class Json_Configurator(GUI,Shema):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Json Configurator")
        self.root.resizable(0, 0)
        #self.root.eval('tk::PlaceWindow . center')
        self.root.geometry("700x200")
        self.destroy_root(self.root).pack(padx=27,pady=5,side="bottom")
        self.exit_root(self.root).pack(padx=28,pady=5,side='bottom')



    def run(self,appliance_name="Standart",opt=False):
        
        self.opt = opt

        
        schema = self.shema

        if os.path.isdir(os.path.join('appliances')):
            pass
        else:
            os.mkdir(os.path.join('appliances'))

        with open(os.path.join('appliances', appliance_name + '.gns3a'), 'w+') as f:
                appliance = {}
                appliance = self.ask_from_schema(schema)
                appliance['qemu'] = self.ask_from_schema(schema['properties']['qemu'])

                
                appliance['images'] = []
                files = []

                
                #image = self.ask_from_schema(schema['properties']['images']['items'])
                #appliance['images'].append(image)
                #files.append(image['filename'])

                appliance['versions'] = []
                
                version = {'images': {}}
                version['name'] = self.ask('Appliance version name')
                for disk in ['hda_disk_image', 'hdb_disk_image', 'hdc_disk_image', 'hdd_disk_image', 'cdrom_image', 'initrd_image', 'kernel_image']:
                    self.ask_file('Image für ' + disk, files, optional=True)
                    if self.image: 
                        version['images'][disk] = self.image
                        self.image = ""

                appliance['versions'].append(version)
                self.root.mainloop()
                

                json.dump(appliance, f, indent=4)

                

   
    def ask_from_schema(self,schema):
            data = {}

            for key, val in schema['properties'].items():
                
                try:
                    self.root.state()
                except:
                    self.restart()
                
                
                
                if key == "appliance_id":
                    # generate an unique ID for the appliance
                    result = str(uuid.uuid4())
                else:
                    optional = not key in schema['required']
                    
                    


                    if 'enum' in val:
                            result = self.ask_multiple(val['title'], val['enum'], optional=optional)
                    elif val['type'] in ('integer', 'string'):
                            result = self.ask(val['title'], type=val['type'], optional=optional)
     
                if result:
                    data[key] = self.val(result)
                elif len(self.val(result)) <= 0:
                    try:
                       
                                if val['type'] in ('integer'):
                                    data[key] = 4
                                else:
                                    data[key] = "Bitte Nachtragen"
                    except:
                        pass
                        
                           
            return data

        

    def ask_multiple(self,question, options, optional=False):
        try:
                self.root.state()
        except:
                self.restart()
        print(options)
        label = self.create_label_frame(self.root,question)
        answer = self.askmulti(options, type='integer', optional=optional)
        
        label.pack()
        answer.pack()
       
        self.root.mainloop()
        
        if answer is None:
            if optional:
                return None

        return self.val(self.drop,optional)

    def ask(self,question, type='string', optional=False):
        try:
            self.root.state()
        except:
            self.restart()
        
        
        if optional:
            frame = self.create_input_frame(self.root,question)
                
        else:
            frame = self.create_input_frame(self.root,question)
        
        frame.pack()  
        self.root.mainloop()

        return self.val(self.var.get(),optional)

    def ask_file(self,disk, type='string', optional=False):
        try:
            self.root.state()
        except:
            self.restart()
        
        
        if optional:
            frame = self.create_file_dialog_frame(self.root,disk)
                
        else:
            frame = self.create_file_dialog_frame(self.root,disk)
        
        frame.pack()  
        self.root.mainloop()

        return self.val(self.image,optional)

    def askmulti(self,question, type='integer', optional=False):
        
        if optional:
            frame = self.create_dropdown_frame(self.root,question)
                
        else:
            frame = self.create_dropdown_frame(self.root,question)
            
        return frame


    def val(self,val,type='string',optional=False):
        
        if optional:
            pass
        try:
            val = int(val)
        except:
            pass
        return val


if __name__ == "__main__":
        Json_Configurator().run()


