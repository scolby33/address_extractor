#!/usr/bin/env python3
"""A script to extract US-style street addresses from a text file."""
import argparse
import collections
import os
import re
import sys

import usaddress

def parsed_address_to_human(address):
    """Turns a `usaddress` address tuple into a 3-tuple of strings roughly divided by the lines you would write on an envelope (recipient name, address and street, city state and zip)
    
    :param address: A tuple of the form returned by `usaddress.tag()`
    :type address: tuple
    :returns: An "envelope address" as a tuple
    :rtype: tuple of 
    """
    a = collections.defaultdict(str, address[0])

    lines = []
    
    lines.append([
        a['Recipient'],
        a['BuildingName']
    ])
    lines.append([
        a['AddressNumberPrefix'],
        a['AddressNumber'],
        a['AddressNumberSuffix'],
        a['StreetNamePreModifier'],
        a['StreetNamePreDirectional'],
        a['StreetNamePreType'],
        a['StreetName'],
        a['StreetNamePostType'],
        a['StreetNamePostDirectional'],
        a['StreetNamePostModifier']
    ])
    lines.append([
        a['PlaceName'],
        a['StateName'],
        a['ZipCode']
    ])
    
    return tuple(' '.join([item for item in line if item]) for line in lines)

def main(**kwargs):
    """The main function of the script. Performs most of the address parsing work and all output.
    
    :param input: a text file object that will be read from. Should contain address-like data, one address per line
    :param output: a text file object where parsed output will be written. Parsed output will be similar to CSV data
    :param remove_post_zip: a boolean value whether to remove data on each line following a sequence of 5 digits and a comma
    :type input: text file object in read mode
    :type output: text file object in write mode
    :type remove_post_zip: bool
    """
    lines = [line.replace('"', '').strip() for line in kwargs['input']]
    kwargs['input'].close()
    
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
        
        kwargs['output'].write(','.join(parsed_address_to_human(address)) + '\n')
    kwargs['output'].close()
    
    for error in errored:
        sys.stderr.write('{}\n'.format(error))
    if len(errored):
        sys.stderr.write('{} lines unable to be parsed\n'.format(len(errored)))
    
    return 0

def run():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=argparse.FileType('r'), default=sys.stdin, nargs='?', help='the input file. Defaults to stdin.')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout, help='the output file. Defaults to stdout', metavar='OUTPUT')
    parser.add_argument('--remove-post-zip', '-r', action='store_true', default=False, help='when scanning the input lines, remove everything after a sequence of 5 digits followed by a comma. The parsing library used by this script chokes on addresses containing this kind of information, often a county name.')
    args = parser.parse_args()
    main(**vars(args))

if __name__ == '__main__':
    run()
