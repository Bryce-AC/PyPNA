# PyPNA
This library provides basic support for interfacing between Keysight PNA and Python. This means you can take control of the PNA with python programs, query data, update settings etc to streamline data acquisition. The library contains the minimal built in capability as it stands, but enough to setup and acquire s-parameters as it stands currently. To build upon this simple capability the pna.write() function can be used to realise more complicated functionallity, refering to the keysight support website below for a list of commands.

Included in this repository are two example files. The first is a bare-bones example of how to retrieve data from the PNA, originally constructed as a performance test to see how quickly data could be acquired. The second is a data acquisition setup with accompanying GUI for everyday use. The GUI features integrated time domain calculation and ability to automatically normalise. These should be enough to get started with the library!

This library is a work in progress, please let us know if you find issues.

Install: `pip install PyPNA`

Commands from: http://na.support.keysight.com/pna/help/latest/Programming/XComFinderSet.htm

Guide: https://towardsdatascience.com/deep-dive-create-and-publish-your-first-python-library-f7f618719e14

## Citation
If you use PyPNA for your research an acknowledgement, mention, or citation would be greatly appreciated where appropriate.

## Contact
If you have any feedback please contact either harrison.lees@adelaide.edu.au or bryce.chung@adelaide.edu.au.

PyPNA was developed by Bryce Chung and Harrison Lees as part of PhD research conducted at the Terahertz Engineering Laboratory, The University of Adelaide. For more details visit https://www.thz-el.org/.