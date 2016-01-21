from utils import dotdict
import os, yaml

target = os.path.dirname(os.path.realpath(__file__)) + "/config.yaml"
with open(target, 'r') as config_file:
    config_yaml = config_file.read()

c = dotdict(yaml.load(config_yaml))

with open('config.h', 'w') as o:

    o.write("""#ifndef CONFIG_H
#define CONFIG_H

//===================================
// CONFIGURATION CONSTANTS
//===================================

// GENERAL
""")

    for key, value in sorted(c.firmware.iteritems()):
        o.write('#define ')
        o.write(key.upper() + " ")
        o.write(str(value) + '\n')

    o.write("\n// DEVICES\n")
    for key in sorted(c.devices):
        for key2, value in sorted(c.devices[key].iteritems()):
            o.write('#define ')
            o.write(key.upper() + '_')
            o.write(key2.upper() + ' ')
            if isinstance(value, str):
                o.write("'" + value + "'")
            else: o.write(str(value))
            o.write('\n')

    o.write("\n// PACKETS\n")
    for key, value in sorted(c.packet.iteritems()):
        o.write('#define ')
        o.write("PACKET_" + key.upper() + " ")
        o.write(str(value) + '\n')

    o.write("\n// SERIAL ERRORS\n")
    for key, value in sorted(c.serial_errors.iteritems()):
        name = value['name']
        o.write('#define ')
        o.write(name.upper() + "_CODE ")
        o.write("'" + key + "'" + '\n')

    o.write("\n// GENERAL RESPONSES\n")
    for key, value in sorted(c.responses.iteritems()):
        name = value['name']
        o.write('#define ')
        o.write(name.upper() + "_CODE ")
        o.write("'" + key + "'" + '\n')

    o.write("\n#endif")
