address_extractor
=================
A script to extract US-style street addresses from a text file

::

    $ address_extractor
    1600 Pennsylvania Ave NW, Washington, DC 20500 ^D
    1 lines in input
    ,1600 Pennsylvania Ave NW,Washington DC 20500
    $ address_extractor -o output.csv input.csv
    4361 lines in input
    *snip*
    11 lines unable to be parsed
    $ ls
    output.csv


:code:`address_extractor` takes text or a text file containing address-like data, one address per line, and parses it into a uniform format with the `usaddress` package.

Command-line Usage
------------------

::

    address_extractor [-h] [-o OUTPUT] [--remove-post-zip] [input]

    positional arguments:
      input                 the input file. Defaults to stdin.

    optional arguments:
      -h, --help            show this help message and exit
      -o OUTPUT, --output OUTPUT
                            the output file. Defaults to stdout. 
      --remove-post-zip, -r
                            when scanning the input lines, remove everything after
                            a sequence of 5 digits followed by a comma. The
                            parsing library used by this script chokes on
                            addresses containing this kind of information, often a
                            county name.

Lines that could not be parsed will be printed to :code:`STDERR`. They can be saved to a file with standard :code:`bash` redirection techniques:

::

    $ address_extractor -o good_addresses.csv has_some_bad_addresses.txt 2> bad_addresses.txt

Usage as a Module
-----------------
:code:`address_extractor` can be used as a Python module:

::

    >>> import address_extractor
    >>> address_extractor.main(input=input_file_object, output=output_file_object, remove_post_zip=a_bool)

There are some small issues with this implementation:

* If using :code:`sys.stdin` or :code:`sys.stdout` for input or output, respectively, the file objects will still be closed. This presents issues trying to use these in the future.
* Errored lines are still printed to :code:`sys.stderr` which may not be expected.
