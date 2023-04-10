#User Manual#

1- Open the location where the cimriUrunler Python file is located in the command prompt [cmd] and run the cimriUrunler.py file with Python.
When the application opens,

Options:

Get Data from Product List: It fetches all products from the product list on the 'https://www.cimri.com/sitemaps/product.xml' site map in sequence until they run out.

Get Data from Bottom Categories: It fetches all products in sequence from the bottom categories by browsing through the category lists in 'https://www.cimri.com/sitemaps/category.xml'.

Get Data from Bottom Categories in a Txt File (recommended): The bottom categories are placed in a txt file with one link per line, and data is retrieved from the placed categories.

Detect and Retrieve Data from Bottom Categories in a Txt File: The categories with links pasted on each line in a txt file are first detected for their bottom categories, and then data retrieval process is initiated for those bottom categories.

Optional VPN:

As the website blocks web traffic, the ProtonVPN extension is included in the program. Proton VPN must be installed on your computer for this option.
It can be downloaded from this link, https://protonvpn.com/download
If you approve this optional option with option "e", when web traffic occurs or when the IP address is blocked,
the VPN is opened and connected to the fastest server. When there is traffic on the connected server, the VPN is turned off, and the process continues through the local IP.
This process continues in a loop to ensure that there are no problems or speed loss while retrieving data.
#It should be selected to avoid speed loss.
