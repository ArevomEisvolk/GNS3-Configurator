from pywebio.input import file_upload, input, checkbox ,select , FLOAT, NUMBER, TEXT
from pywebio.output import put_text, put_button
import pywebio

import json
import os
import sys
import uuid

class Schemas():
    appliance_v3="""
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
      "enum": [1, 2, 3],
      "title": "Version of the registry compatible with this appliance"
    },
    "status": {
      "enum": ["stable", "experimental", "broken"],
      "title": "Document if the appliance is working or not"
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
    "first_port_name": {
        "type": "string",
        "title": "Optional name of the first networking port example: eth0"
    },
    "port_name_format": {
        "type": "string",
        "title": "Optional formating of the networking port example: eth{0}"
    },
    "port_segment_size": {
        "type": "integer",
        "title": "Optional port segment size. A port segment is a block of port. For example Ethernet0/0 Ethernet0/1 is the module 0 with a port segment size of 2"
    },
    "linked_base": {
        "type": "boolean",
        "title": "False if you don't want to use a single image for all nodes"
    },

    "docker": {
        "type": "object",
        "title": "Docker specific options",
        "properties": {
            "adapters": {
                "type": "integer",
                "title": "Number of ethernet adapters"
            },
            "image": {
                "type": "string",
                "title": "Docker image in the Docker Hub"
            },
            "start_command": {
                "type": "string",
                "title": "Command executed when the container start. Empty will use the default"
            },
            "environment": {
                "type": "string",
                "title": "One KEY=VAR environment by line"
            },
            "console_type": {
              "enum": ["telnet", "vnc", "http", "https"],
              "title": "Type of console connection for the administration of the appliance"
            },
            "console_http_port": {
                "description": "Internal port in the container of the HTTP server",
                "type": "integer"
            },
            "console_http_path": {
                "description": "Path of the web interface",
                "type": "string"
            }
        },
        "additionalProperties": false,
        "required": [
            "adapters",
            "image"
        ]
    },

    "iou": {
        "type": "object",
        "title": "IOU specific options",
        "properties": {
            "ethernet_adapters": {
                "type": "integer",
                "title": "Number of ethernet adapters"
            },
            "serial_adapters": {
                "type": "integer",
                "title": "Number of serial adapters"
            },
            "nvram": {
                "type": "integer",
                "title": "Host NVRAM"
            },
            "ram": {
                "type": "integer",
                "title": "Host RAM"
            },
            "startup_config": {
                "type": "string",
                "title": "Config loaded at startup"
            }
        },
        "additionalProperties": false,
        "required": [
            "ethernet_adapters",
            "serial_adapters",
            "nvram",
            "ram",
            "startup_config"
        ]
    },

    "dynamips": {
        "type": "object",
        "title": "Dynamips specific options",
        "properties": {
            "chassis": {
                "title": "Chassis type",
                "enum": ["1720", "1721", "1750", "1751", "1760", "2610", "2620", "2610XM", "2620XM", "2650XM", "2621", "2611XM", "2621XM", "2651XM", "3620", "3640", "3660", ""]
            },
            "platform": {
                "title": "Platform type",
                "enum": ["c1700", "c2600", "c2691", "c3725", "c3745", "c3600", "c7200"]
            },
            "ram": {
                "title": "Amount of ram",
                "type": "integer",
                "minimum": 1
            },
            "nvram": {
                "title": "Amount of nvram",
                "type": "integer",
                "minimum": 1
            },
            "startup_config": {
                "type": "string",
                "title": "Config loaded at startup"
            },
            "wic0": { "$ref": "#/definitions/dynamips_wic" },
            "wic1": { "$ref": "#/definitions/dynamips_wic" },
            "wic2": { "$ref": "#/definitions/dynamips_wic" },
            "slot0": { "$ref": "#/definitions/dynamips_slot" },
            "slot1": { "$ref": "#/definitions/dynamips_slot" },
            "slot2": { "$ref": "#/definitions/dynamips_slot" },
            "slot3": { "$ref": "#/definitions/dynamips_slot" },
            "slot4": { "$ref": "#/definitions/dynamips_slot" },
            "slot5": { "$ref": "#/definitions/dynamips_slot" },
            "slot6": { "$ref": "#/definitions/dynamips_slot" },
            "midplane": { "enum": ["std", "vxr"] },
            "npe": { "enum": ["npe-100", "npe-150", "npe-175", "npe-200", "npe-225", "npe-300", "npe-400", "npe-g2"] }
        },
        "additionalProperties": false,
        "required": [
            "platform",
            "ram",
            "nvram"
        ]
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
        "hda_disk_interface": {
            "enum": ["ide", "scsi", "sd", "mtd", "floppy", "pflash", "virtio"],
            "title": "Disk interface for the installed hda_disk_image"
        },
        "hdb_disk_interface": {
            "enum": ["ide", "scsi", "sd", "mtd", "floppy", "pflash", "virtio"],
            "title": "Disk interface for the installed hdb_disk_image"
        },
        "hdc_disk_interface": {
            "enum": ["ide", "scsi", "sd", "mtd", "floppy", "pflash", "virtio"],
            "title": "Disk interface for the installed hdc_disk_image"
        },
        "hdd_disk_interface": {
            "enum": ["ide", "scsi", "sd", "mtd", "floppy", "pflash", "virtio"],
            "title": "Disk interface for the installed hdd_disk_image"
        },
        "arch": {
          "enum": ["aarch64", "alpha", "arm", "cris", "i386", "lm32", "m68k", "microblaze", "microblazeel", "mips", "mips64", "mips64el", "mipsel", "moxie", "or32", "ppc", "ppc64", "ppcemb", "s390x", "sh4", "sh4eb", "sparc", "sparc64", "tricore", "unicore32", "x86_64", "xtensa", "xtensaeb"],
          "title": "Architecture emulated"
        },
        "console_type": {
          "enum": ["telnet", "vnc"],
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
        },
        "cpu_throttling": {
            "type": "number",
            "minimum": 0,
            "maximum": 100,
            "title": "Throttle the CPU"
        },
        "process_priority": {
            "title": "Process priority for QEMU",
            "enum": ["realtime",
                     "very high",
                     "high",
                     "normal",
                     "low",
                     "very low",
                     "null"]
        }
      },
      "additionalProperties": false,
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
        "additionalProperties": false,
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
            },
            "additionalProperties": false
          }
        },
        "required": [
            "name"
        ],
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false,
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
    appliance_v4="""{
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
      "enum": [1, 2, 3, 4],
      "title": "Version of the registry compatible with this appliance"
    },
    "status": {
      "enum": ["stable", "experimental", "broken"],
      "title": "Document if the appliance is working or not"
    },
    "availability": {
      "enum": ["free", "with-registration", "free-to-try", "service-contract"],
      "title": "About image availability: can be downloaded directly; download requires a free registration; paid but a trial version (time or feature limited) is available; not available publicly"
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
    "first_port_name": {
        "type": "string",
        "title": "Optional name of the first networking port example: eth0"
    },
    "port_name_format": {
        "type": "string",
        "title": "Optional formating of the networking port example: eth{0}"
    },
    "port_segment_size": {
        "type": "integer",
        "title": "Optional port segment size. A port segment is a block of port. For example Ethernet0/0 Ethernet0/1 is the module 0 with a port segment size of 2"
    },
    "linked_clone": {
        "type": "boolean",
        "title": "False if you don't want to use a single image for all nodes"
    },

    "docker": {
        "type": "object",
        "title": "Docker specific options",
        "properties": {
            "adapters": {
                "type": "integer",
                "title": "Number of ethernet adapters"
            },
            "image": {
                "type": "string",
                "title": "Docker image in the Docker Hub"
            },
            "start_command": {
                "type": "string",
                "title": "Command executed when the container start. Empty will use the default"
            },
            "environment": {
                "type": "string",
                "title": "One KEY=VAR environment by line"
            },
            "console_type": {
              "enum": ["telnet", "vnc", "http", "https"],
              "title": "Type of console connection for the administration of the appliance"
            },
            "console_http_port": {
                "description": "Internal port in the container of the HTTP server",
                "type": "integer"
            },
            "console_http_path": {
                "description": "Path of the web interface",
                "type": "string"
            }
        },
        "required": [
            "adapters",
            "image"
        ]
    },
    "iou": {
        "type": "object",
        "title": "IOU specific options",
        "properties": {
            "ethernet_adapters": {
                "type": "integer",
                "title": "Number of ethernet adapters"
            },
            "serial_adapters": {
                "type": "integer",
                "title": "Number of serial adapters"
            },
            "nvram": {
                "type": "integer",
                "title": "Host NVRAM"
            },
            "ram": {
                "type": "integer",
                "title": "Host RAM"
            },
            "startup_config": {
                "type": "string",
                "title": "Config loaded at startup"
            }
        },
        "required": [
            "ethernet_adapters",
            "serial_adapters",
            "nvram",
            "ram",
            "startup_config"
        ]
    },
    "dynamips": {
        "type": "object",
        "title": "Dynamips specific options",
        "properties": {
            "chassis": {
                "title": "Chassis type",
                "enum": ["1720", "1721", "1750", "1751", "1760", "2610", "2620", "2610XM", "2620XM", "2650XM", "2621", "2611XM", "2621XM", "2651XM", "3620", "3640", "3660", ""]
            },
            "platform": {
                "title": "Platform type",
                "enum": ["c1700", "c2600", "c2691", "c3725", "c3745", "c3600", "c7200"]
            },
            "ram": {
                "title": "Amount of ram",
                "type": "integer",
                "minimum": 1
            },
            "nvram": {
                "title": "Amount of nvram",
                "type": "integer",
                "minimum": 1
            },
            "startup_config": {
                "type": "string",
                "title": "Config loaded at startup"
            },
            "wic0": { "$ref": "#/definitions/dynamips_wic" },
            "wic1": { "$ref": "#/definitions/dynamips_wic" },
            "wic2": { "$ref": "#/definitions/dynamips_wic" },
            "slot0": { "$ref": "#/definitions/dynamips_slot" },
            "slot1": { "$ref": "#/definitions/dynamips_slot" },
            "slot2": { "$ref": "#/definitions/dynamips_slot" },
            "slot3": { "$ref": "#/definitions/dynamips_slot" },
            "slot4": { "$ref": "#/definitions/dynamips_slot" },
            "slot5": { "$ref": "#/definitions/dynamips_slot" },
            "slot6": { "$ref": "#/definitions/dynamips_slot" },
            "midplane": { "enum": ["std", "vxr"] },
            "npe": { "enum": ["npe-100", "npe-150", "npe-175", "npe-200", "npe-225", "npe-300", "npe-400", "npe-g2"] }
        },
        "required": [
            "platform",
            "ram",
            "nvram"
        ]
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
          "enum": ["telnet", "vnc"],
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
        },
        "cpu_throttling": {
            "type": "number",
            "minimum": 0,
            "maximum": 100,
            "title": "Throttle the CPU"
        },
        "process_priority": {
            "title": "Process priority for QEMU",
            "enum": ["realtime",
                     "very high",
                     "high",
                     "normal",
                     "low",
                     "very low",
                     "null"]
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
    appliance_v5="""{
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
      "title": "About image availability: can be downloaded directly; download requires a free registration; paid but a trial version (time or feature limited) is available; not available publicly"
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
    "first_port_name": {
        "type": "string",
        "title": "Optional name of the first networking port example: eth0"
    },
    "port_name_format": {
        "type": "string",
        "title": "Optional formating of the networking port example: eth{0}"
    },
    "port_segment_size": {
        "type": "integer",
        "title": "Optional port segment size. A port segment is a block of port. For example Ethernet0/0 Ethernet0/1 is the module 0 with a port segment size of 2"
    },
    "linked_clone": {
        "type": "boolean",
        "title": "False if you don't want to use a single image for all nodes"
    },

    "docker": {
        "type": "object",
        "title": "Docker specific options",
        "properties": {
            "adapters": {
                "type": "integer",
                "title": "Number of ethernet adapters"
            },
            "image": {
                "type": "string",
                "title": "Docker image in the Docker Hub"
            },
            "start_command": {
                "type": "string",
                "title": "Command executed when the container start. Empty will use the default"
            },
            "environment": {
                "type": "string",
                "title": "One KEY=VAR environment by line"
            },
            "console_type": {
              "enum": ["telnet", "vnc", "http", "https"],
              "title": "Type of console connection for the administration of the appliance"
            },
            "console_http_port": {
                "description": "Internal port in the container of the HTTP server",
                "type": "integer"
            },
            "console_http_path": {
                "description": "Path of the web interface",
                "type": "string"
            }
        },
        "required": [
            "adapters",
            "image"
        ]
    },
    "iou": {
        "type": "object",
        "title": "IOU specific options",
        "properties": {
            "ethernet_adapters": {
                "type": "integer",
                "title": "Number of ethernet adapters"
            },
            "serial_adapters": {
                "type": "integer",
                "title": "Number of serial adapters"
            },
            "nvram": {
                "type": "integer",
                "title": "Host NVRAM"
            },
            "ram": {
                "type": "integer",
                "title": "Host RAM"
            },
            "startup_config": {
                "type": "string",
                "title": "Config loaded at startup"
            }
        },
        "required": [
            "ethernet_adapters",
            "serial_adapters",
            "nvram",
            "ram",
            "startup_config"
        ]
    },
    "dynamips": {
        "type": "object",
        "title": "Dynamips specific options",
        "properties": {
            "chassis": {
                "title": "Chassis type",
                "enum": ["1720", "1721", "1750", "1751", "1760", "2610", "2620", "2610XM", "2620XM", "2650XM", "2621", "2611XM", "2621XM", "2651XM", "3620", "3640", "3660", ""]
            },
            "platform": {
                "title": "Platform type",
                "enum": ["c1700", "c2600", "c2691", "c3725", "c3745", "c3600", "c7200"]
            },
            "ram": {
                "title": "Amount of ram",
                "type": "integer",
                "minimum": 1
            },
            "nvram": {
                "title": "Amount of nvram",
                "type": "integer",
                "minimum": 1
            },
            "startup_config": {
                "type": "string",
                "title": "Config loaded at startup"
            },
            "wic0": { "$ref": "#/definitions/dynamips_wic" },
            "wic1": { "$ref": "#/definitions/dynamips_wic" },
            "wic2": { "$ref": "#/definitions/dynamips_wic" },
            "slot0": { "$ref": "#/definitions/dynamips_slot" },
            "slot1": { "$ref": "#/definitions/dynamips_slot" },
            "slot2": { "$ref": "#/definitions/dynamips_slot" },
            "slot3": { "$ref": "#/definitions/dynamips_slot" },
            "slot4": { "$ref": "#/definitions/dynamips_slot" },
            "slot5": { "$ref": "#/definitions/dynamips_slot" },
            "slot6": { "$ref": "#/definitions/dynamips_slot" },
            "midplane": { "enum": ["std", "vxr"] },
            "npe": { "enum": ["npe-100", "npe-150", "npe-175", "npe-200", "npe-225", "npe-300", "npe-400", "npe-g2"] }
        },
        "required": [
            "platform",
            "ram",
            "nvram"
        ]
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
        },
        "cpu_throttling": {
            "type": "number",
            "minimum": 0,
            "maximum": 100,
            "title": "Throttle the CPU"
        },
        "process_priority": {
            "title": "Process priority for QEMU",
            "enum": ["realtime",
                     "very high",
                     "high",
                     "normal",
                     "low",
                     "very low",
                     "null"]
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
    appliance_v6="""
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
      "enum": [1, 2, 3, 4, 5, 6],
      "title": "Version of the registry compatible with this appliance"
    },
    "status": {
      "enum": ["stable", "experimental", "broken"],
      "title": "Document if the appliance is working or not"
    },
    "availability": {
      "enum": ["free", "with-registration", "free-to-try", "service-contract"],
      "title": "About image availability: can be downloaded directly; download requires a free registration; paid but a trial version (time or feature limited) is available; not available publicly"
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
    "first_port_name": {
        "type": "string",
        "title": "Optional name of the first networking port example: eth0"
    },
    "port_name_format": {
        "type": "string",
        "title": "Optional formating of the networking port example: eth{0}"
    },
    "port_segment_size": {
        "type": "integer",
        "title": "Optional port segment size. A port segment is a block of port. For example Ethernet0/0 Ethernet0/1 is the module 0 with a port segment size of 2"
    },
    "linked_clone": {
        "type": "boolean",
        "title": "False if you don't want to use a single image for all nodes"
    },

    "docker": {
        "type": "object",
        "title": "Docker specific options",
        "properties": {
            "adapters": {
                "type": "integer",
                "title": "Number of ethernet adapters"
            },
            "image": {
                "type": "string",
                "title": "Docker image in the Docker Hub"
            },
            "start_command": {
                "type": "string",
                "title": "Command executed when the container start. Empty will use the default"
            },
            "environment": {
                "type": "string",
                "title": "One KEY=VAR environment by line"
            },
            "console_type": {
              "enum": ["telnet", "vnc", "http", "https"],
              "title": "Type of console connection for the administration of the appliance"
            },
            "console_http_port": {
                "description": "Internal port in the container of the HTTP server",
                "type": "integer"
            },
            "console_http_path": {
                "description": "Path of the web interface",
                "type": "string"
            }
        },
        "required": [
            "adapters",
            "image"
        ]
    },
    "iou": {
        "type": "object",
        "title": "IOU specific options",
        "properties": {
            "ethernet_adapters": {
                "type": "integer",
                "title": "Number of ethernet adapters"
            },
            "serial_adapters": {
                "type": "integer",
                "title": "Number of serial adapters"
            },
            "nvram": {
                "type": "integer",
                "title": "Host NVRAM"
            },
            "ram": {
                "type": "integer",
                "title": "Host RAM"
            },
            "startup_config": {
                "type": "string",
                "title": "Config loaded at startup"
            }
        },
        "required": [
            "ethernet_adapters",
            "serial_adapters",
            "nvram",
            "ram",
            "startup_config"
        ]
    },
    "dynamips": {
        "type": "object",
        "title": "Dynamips specific options",
        "properties": {
            "chassis": {
                "title": "Chassis type",
                "enum": ["1720", "1721", "1750", "1751", "1760", "2610", "2620", "2610XM", "2620XM", "2650XM", "2621", "2611XM", "2621XM", "2651XM", "3620", "3640", "3660", ""]
            },
            "platform": {
                "title": "Platform type",
                "enum": ["c1700", "c2600", "c2691", "c3725", "c3745", "c3600", "c7200"]
            },
            "ram": {
                "title": "Amount of ram",
                "type": "integer",
                "minimum": 1
            },
            "nvram": {
                "title": "Amount of nvram",
                "type": "integer",
                "minimum": 1
            },
            "startup_config": {
                "type": "string",
                "title": "Config loaded at startup"
            },
            "wic0": { "$ref": "#/definitions/dynamips_wic" },
            "wic1": { "$ref": "#/definitions/dynamips_wic" },
            "wic2": { "$ref": "#/definitions/dynamips_wic" },
            "slot0": { "$ref": "#/definitions/dynamips_slot" },
            "slot1": { "$ref": "#/definitions/dynamips_slot" },
            "slot2": { "$ref": "#/definitions/dynamips_slot" },
            "slot3": { "$ref": "#/definitions/dynamips_slot" },
            "slot4": { "$ref": "#/definitions/dynamips_slot" },
            "slot5": { "$ref": "#/definitions/dynamips_slot" },
            "slot6": { "$ref": "#/definitions/dynamips_slot" },
            "midplane": { "enum": ["std", "vxr"] },
            "npe": { "enum": ["npe-100", "npe-150", "npe-175", "npe-200", "npe-225", "npe-300", "npe-400", "npe-g2"] }
        },
        "required": [
            "platform",
            "ram",
            "nvram"
        ]
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
        "custom_adapters": {
            "type": "array",
            "title": "Custom adapters",
            "items": {
                "type": "object",
                "properties": {
                    "adapter_number": {
                        "title": "Adapter number",
                        "type": "integer"
                    },
                    "port_name": {
                        "title": "Custom port name",
                        "type": "string",
                        "minimum": 1
                    },
                    "adapter_type": {
                        "title": "Custom adapter type",
                        "type": "string",
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
                        ]
                    },
                    "mac_address": {
                        "title": "Custom MAC address",
                        "type": "string",
                        "minimum": 1,
                        "pattern": "^([0-9a-fA-F]{2}[:]){5}([0-9a-fA-F]{2})$"
                    }
                },
                "required": ["adapter_number"]
            }
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
        },
        "cpu_throttling": {
            "type": "number",
            "minimum": 0,
            "maximum": 100,
            "title": "Throttle the CPU"
        },
        "process_priority": {
            "title": "Process priority for QEMU",
            "enum": ["realtime",
                     "very high",
                     "high",
                     "normal",
                     "low",
                     "very low",
                     "null"]
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

class GNS3_GUI(Schemas):

    pywebio.session.set_env(title='GNS3 File Configurator')

    def __init__(self) -> None:

        shema_number = checkbox(label="Bitte gewünschtes Shema auswählen",options=["Eigenes Shema","3","4","5","6"])
        shema_number = "".join(shema_number)
        if shema_number == "Eigenes Shema":
            shema = input(label='Bitte absoluten Pfad zur Json Datei eingeben')
        else:
            if   shema_number == 3:
                shema = self.appliance_v3
            elif shema_number == 4:
                shema = self.appliance_v4
            elif shema_number == 5:
                shema = self.appliance_v5
            elif shema_number == 6:
                shema = self.appliance_v6


        schema = json.loads(shema)

        
        appliance_name = input(label='Appliance filename (example: cisco-asav)')
        if appliance_name == None:
            appliance_name = "Standart"

        # TODO check if file exists
        with open(os.path.join('appliances', appliance_name + '.gns3a'), 'w+') as f:
            appliance = {}
            #appliance = self.ask_from_schema(schema)
            #appliance['qemu'] = self.ask_from_schema(schema['properties']['qemu'])

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
                    img = file_upload(label=f"Image for {disk}", required=False)
                    if img:
                        version['images'][disk] = img.get("filename")

                appliance['versions'].append(version)

            json.dump(appliance, f, indent=4)


    def yesno(self,question):
        while True:
            answer = select(label=question,options=["yes","no"])
            if answer in ['y', 'Y', 'yes']:
                return True
            if answer in ['n', 'N', 'no']:
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
                    result = select(label=val['title'],options=val['enum'],required=required)
                elif val['type'] in ('integer', 'string'):
                    if val['type'] == "integer":
                        result = input(val['title'], required=required, type=NUMBER)
                    else:
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

    def get_shema(self,shema_number):
        
        return f"appliance_v{shema_number}"

if __name__ == "__main__": 
    GNS3_GUI()