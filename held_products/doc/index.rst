=============
Held Products
=============

Note:

- Note that this app may require changes for your particular organization.  
- It has only been tested in databases created with the Country setting of the United States and may need to be localized for other countries. 
- Discuss your requirements with your Odoo Advisor or an Odoo Partner to understand the best way to leverage this kind of functionality.

Target Platform, Edition and Version:

- Online, Odoo.sh or On-Premise.
- Enterprise Edition.  
- Version 13.0.  

Required Apps:

- Odoo Studio - web_studio
- Inventory - stock
- Sales - sale_management

Installing:

1. Download the ZIP, do not unzip it

2. From the Apps Switcher screen, activate Odoo Studio:

.. image:: https://raw.githubusercontent.com/odoo-tm/apps/13.0/held_products/doc/odoo_studio_button.png

3. From the Customizations Menu on the left, select Import

4. Upload the ZIP file and click IMPORT

Setup:

From the Inventory --> Configuration --> Settings Menu, check on Delivery Packages

From the Inventory --> Configuration --> Operation Types Menu, open the Receipts Operation and check on Show Detailed Operations and Pre-fill Detailed Operations

Use:

On a Customer, you will see a new Action Menu option called 'Create Held Products Package'.  You can also find this in the Action menu via the List View.  This is used to automatically make a Customer Package in advance of products being received.

On a Package, you will see a new field called 'Held For' where you assign the Customer to the Package if you make it manually at the time of products being received.

In the Inventory --> Reporting Menu, you will see a new Menu option called 'Held Products'

When Receiving (processing a Receipt Stock Transfer)
Select or Create the package on each Detailed Operations line under Destination Package each time you receive products for a specific Customer.

When Delivering (processing a Delivery Stock Transfer):
Select the package on Detailed Operations line under Source Package - make sure Destination Package is blank or relates to your Shipping Packaged (if used)
