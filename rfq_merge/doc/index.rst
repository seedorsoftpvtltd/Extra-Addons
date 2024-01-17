=====================
Merge Purchase Orders
=====================

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
- Purchase - purchase
- Inventory - stock
- Sales - sale_management

Installing:

1. Download the ZIP, do not unzip it

2. From the Apps Switcher screen, activate Odoo Studio:

.. image:: https://raw.githubusercontent.com/odoo-tm/apps/13.0/rfq_merge/doc/odoo_studio_button.png

3. From the Customizations Menu on the left, select Import

4. Upload the ZIP file and click IMPORT

Setup:

Optionally, if you have Make to Order setup and want ONE RFQ per Sales Order:

From the Inventory --> Configuration -- > Routes Menu, select the "Buy" Route.

Click EDIT, open the "Buy" rules and change the value of "Propagation of Procurement Group" to "Propagate"

Use:

Select more than one RFQ and, from the Action Menu, select "Merge RFQ's"

Note: you can only merge non-canceled RFQ's with a matching Vendor and matching Deliver To location.
