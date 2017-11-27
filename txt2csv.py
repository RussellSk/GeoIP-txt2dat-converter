import subprocess as bash
import socket, struct
import argparse


def parsearguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="input", default="borderinput.txt", help="Input bgp ip list")
    parser.add_argument("-o", "--output", dest="output", default="outnetworks.txt", help="Output CSV file with aggregated networks")
    return parser.parse_args()


def readbgprulese(args):
    print(" -- Read Border Rules -- ")
    file = open(args.input, 'r')
    network_data = []
    for line in file:
        network_data = network_data + [line]
    file.close()
    aggregate_networks(args.input)
    return network_data


def compose_csv(data):
    print(" -- Compose new CSV dataset --")
    network_range = []
    for line in data:
        command_min = "ipcalc " + line.rstrip() + " | awk 'NR==1{print $2}'"
        command_max = "ipcalc " + line.rstrip() + " | awk 'NR==8{print $2}'"
        hostmin = bash.check_output(['bash', '-c', command_min])
        hostmax = bash.check_output(['bash', '-c', command_max])
        network_range.append({'min' : hostmin.rstrip(), 'max': hostmax.rstrip()})
    return network_range


def write_csv(data, args):
    print("-- Write the newest data --")
    file = open(args.output, 'w')
    for line in data:
        file.writelines('"{0}","{1}","{2}","{3}",{4}\n'.format(
            line['min'].decode("utf-8"),
            line['max'].decode("utf-8"),
            ip2long(line['min']),
            ip2long(line['max']),
            '"UA","Ukraine"'))
    file.close()


def aggregate_networks(file):
    command_aggregate = "aggregate < " + file + " > " + file + ".tmp"
    bash.check_output(['bash', '-c', command_aggregate])
    bash.check_output(['bash', '-c', "cat " + file + ".tmp" + " > " + file])


def ip2long(ip):
    packedIP = socket.inet_aton(ip.decode("utf-8"))
    return struct.unpack("!L", packedIP)[0]


if __name__ == '__main__' :
    args = parsearguments()
    aggregate_networks(args.input)
    write_csv(compose_csv(readbgprulese(args)), args)
