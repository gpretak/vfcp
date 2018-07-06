# vfcp
Uses Department of Labor web page to calculate lost earnings through the Voluntary Fiduciary Correction Program. 

Reference DOL web page for more information:
https://dol.gov/agencies/ebsa/employers-and-advisers/plan-administration-and-compliance/correction-programs/vfcp

Requirements:
panads==0.20.2
selenium==3.11.0

Instructions:
- Use the file in the template folder to create your document
- Save and place the document in the input folder
- run main.py and include the document name as the first argurment and the calculated/completed document name as the second argument
- run the program
- navigate to the output folder for your completed document

Tests:
- 5 records in ~25 seconds
- 25 records in ~68 seconds
