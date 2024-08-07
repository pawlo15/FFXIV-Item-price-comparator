# FFXIV-Item-price-comaprator v1.0
The Item Price Comparator is designed to help players search for the lowest price of specified items in the region and in individual data centers. With the app, users can quickly and easily see where the purchase of an item will be the most advantageous.

## Dependencies

The application could not work if it were not for the hard work of those involved in the project https://github.com/Universalis-FFXIV/Universalis

The project uses the API provided at: https://universalis.app/api/v2

The API documentation is available at: https://docs.universalis.app/

## Downloads

   File: FFXIV_Comparator_v1.0.exe
   
   MD5: 8A9CE64D4EDC3C8F8838274B3AE04BA5
   
   SHA256: B3EEB2A785FF21FCA5B7B2384CE4A3BC44B5322647F74823EB0CFE038EEEF22F

## Support

If there are problems with the operation of the script or application, please contact me.
If you've downloaded my script or app and liked how it works, I'd be happy if you leave a star on GitHub or buy me a coffee.

# Manual

The source code of the application is in the repository, all changes will be uploaded to the repository on an ongoing basis.

## Method 1 using python

If you have python installed on your computer, you can run the comparator.py file with the appropriate arguments.

`--region`  takes the name of the region (Note, the argument is case sensitive)

`--file` takes the path to the file with the items to be downloade

Example:

    python .\Comparator.py --region Europe --file "presets\crystals.csv"

## Method 2 using the .exe file

Download the .exe file from the repository and click on it twice. 
After the application turns on, enter the region you are interested in (*Note the field is case sensitive*) and select the item file to search. 
The item file must be in .csv format, the sample file is in the presets directory. The file must have two columns, the first with the item ID (ID according to *universalis.app* ), and the second with the item name (the name can be whatever the user wants).
Click the search button. After a few seconds, you should see a table with the lowest price of a specific item, and if you click on a record, additional price information will appear.
