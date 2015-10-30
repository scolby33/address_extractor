#!/usr/bin/env python3
import argparse
import collections
import os
import re
import sys

import usaddress

def parsed_address_to_human(address):
    a = collections.defaultdict(str, address[0])
    return (
        '"' + ' '.join((a['Recipient'], a['BuildingName'])) + '"',
        '"' + ' '.join((a['AddressNumberPrefix'], a['AddressNumber'], a['AddressNumberSuffix'], a['StreetNamePreModifier'], a['StreetNamePreDirectional'], a['StreetNamePreType'], a['StreetName'], a['StreetNamePostType'], a['StreetNamePostDirectional'], a['StreetNamePostModifier'])) + '"',
        '"' + ' '.join((a['PlaceName'], a['StateName'], a['ZipCode'])) + '"'
    )
    
def main():
    parser = argparse.ArgumentParser(description='Extract some addresses.')
    parser.add_argument('input', type=argparse.FileType('r'), help='the input file')
    parser.add_argument('-o', type=argparse.FileType('w'), default=sys.stdout, help='the output file. Defaults to stdout', metavar='OUTPUT')
    
    if len(sys.argv) == 1:
        parser.print_help()
        return 1
    args = parser.parse_args()
    
    lines = [line.replace('"', '').strip() for line in args.input]
    args.input.close()
    
    print('{} lines in input'.format(len(lines)))
    
    county = re.compile('(\d{5}),.*')
    
    parsed = []
    errored = []
    
    for line in lines:
        try:
            parsed.append(usaddress.tag(re.sub(county, r'\1', line)))
        except(usaddress.RepeatedLabelError):
            errored.append(line)
            
    for address in parsed:
        
        args.o.write(','.join(parsed_address_to_human(address)) + '\n')
    args.o.close()
    
    for error in errored:
        sys.stderr.write('{}\n'.format(error))
    sys.stderr.write('{} lines unable to be parsed\n'.format(len(errored)))

if __name__ == '__main__':
    sys.exit(main())
