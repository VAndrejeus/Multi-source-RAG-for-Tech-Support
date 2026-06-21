## Query 1
Ask an OpenEMR support question: How do I enable the patient portal?

Answer:

There are two options for setting up a patient portal: the Native Patient Portal included with OpenEMR or using the CMS patient portal which utilizes WordPress.  To set up either option, your OpenEMR instance will need to be accessible on the web securely. 




Sources Used:

- documentation | Patient Portal | https://www.open-emr.org/wiki/index.php/Patient_Portal

## Query 2

Ask an OpenEMR support question: How do I upgrade OpenEMR?

Answer:

To upgrade OpenEMR, you need to manually follow the instructions outlined in the "Upgrading" section of the INSTALL file located in the Documentation directory of your OpenEMR installation.  The documentation also provides guidance on upgrading your MySQL database to UTF-8 if you are upgrading from a previous version. 




Sources Used:

- documentation | OpenEMR Upgrade Guides | https://www.open-emr.org/wiki/index.php/OpenEMR_Upgrade_Guides
- documentation | openemr_3_1_users_guide | data_sources\documentation\pdfs\openemr_3_1_users_guide.pdf
- documentation | openemr_4_1_users_guide | data_sources\documentation\pdfs\openemr_4_1_users_guide.pdf

## Query 3

Ask an OpenEMR support question: How do I secure OpenEMR?

Answer:

To secure OpenEMR, ensure you have installed the most recent patch and remove unnecessary scripts like setup.php, acl_setup.php, and admin.php.  Additionally, it's recommended to remove or restrict access to other listed scripts in the "Securing OpenEMR" documentation. 




Sources Used:

- documentation | openemr_3_1_users_guide | data_sources\documentation\pdfs\openemr_3_1_users_guide.pdf
- documentation | openemr_4_1_users_guide | data_sources\documentation\pdfs\openemr_4_1_users_guide.pdf
- documentation | Securing OpenEMR | https://www.open-emr.org/wiki/index.php/Securing_OpenEMR

## Query 4

Ask an OpenEMR support question: How do I add a new patient?

Answer:

To add a new patient, select 'Patient/Client – New/Search' from the navigation menu on the left side of the screen.  Enter the patient's name and birth date in the Search or Add Patient page, and click 'Create New Patient' when finished. 




Sources Used:

- documentation | openemr_3_1_users_guide | data_sources\documentation\pdfs\openemr_3_1_users_guide.pdf
- documentation | openemr_4_1_users_guide | data_sources\documentation\pdfs\openemr_4_1_users_guide.pdf
- documentation | openemr_4_1_users_guide | data_sources\documentation\pdfs\openemr_4_1_users_guide.pdf

## Query 5

Ask an OpenEMR support question: How do I configure facilities?

Answer:

To configure facilities in OpenEMR, start by logging into your account and selecting 'Administration' from the navigation list on the left of the screen.  Next, click on 'Facilities' to bring up the Facility Administration page where you can update the default clinic information with your clinic's details. 




Sources Used:

- documentation | openemr_3_1_users_guide | data_sources\documentation\pdfs\openemr_3_1_users_guide.pdf
- documentation | openemr_4_1_users_guide | data_sources\documentation\pdfs\openemr_4_1_users_guide.pdf

## Query 6

Ask an OpenEMR support question: How do I upload documents?

Answer:

To upload documents in OpenEMR, select 'Documents' from the navigation menu on the left.  Choose the appropriate Document Category for your file, click 'Browse' to locate it on your computer, and then click 'Upload'. Once uploaded, you can view the new file by clicking the arrow next to the document category and selecting its name. 


Source Priority:
Sources were ranked by authority before answer generation. When potentially conflicting information was retrieved, higher-authority sources were prioritized.

Sources Used:

- documentation | openemr_3_1_users_guide | data_sources\documentation\pdfs\openemr_3_1_users_guide.pdf
- forum | Small change in code to switch on/off pacient ability to schedule own appointments on portal | https://community.open-emr.org/t/15455.json

## Query 7

Ask an OpenEMR support question: What is OpenEMR version 8?

Answer:

OpenEMR version 8 is an ONC certified release that includes dozens of new features, improvements, and fixes.  

It aims to support interoperability, streamline workflows, and improve patient care. You can find a full list of release features, upgrade guides, and installation instructions on the OpenEMR website. 


Source Priority:
Sources were ranked by authority before answer generation. When potentially conflicting information was retrieved, higher-authority sources were prioritized.

Sources Used:

- blog | OpenEMR Version 8 Released | https://www.open-emr.org/blog/openemr-version-8-released/
- documentation | OpenEMR Wiki Home Page | https://www.open-emr.org/wiki/index.php/OpenEMR_Wiki_Home_Page
- blog | OpenEMR Achieves ONC Certification with Groundbreaking Release 7.0 | https://www.open-emr.org/blog/openemr-achieves-onc-certification-with-groundbreaking-release-70/

## Query 8
Ask an OpenEMR support question: What ONC certification did OpenEMR achieve?

Answer:

OpenEMR version 7.0 achieved ONC Certification through the SLI Compliance Certification Body.  This certification meets the ONC 2015 Certification criteria. 




Source Priority:
Sources were ranked by authority before answer generation. When potentially conflicting information was retrieved, higher-authority sources were prioritized.

Sources Used:

- documentation | OpenEMR Wiki Home Page | https://www.open-emr.org/wiki/index.php/OpenEMR_Wiki_Home_Page
- blog | OpenEMR Achieves ONC Certification with Groundbreaking Release 7.0 | https://www.open-emr.org/blog/openemr-achieves-onc-certification-with-groundbreaking-release-70/
- blog | Join Us in Funding OpenEMR's 2025 Certification | https://www.open-emr.org/blog/join-us-in-funding-openemr-2025-certification/

## Query 9

Ask an OpenEMR support question: Can patients schedule appointments through the portal?

Answer:

The provided documentation does not contain information about whether or not patients can schedule appointments through the portal.  To get a definitive answer, you would need to consult additional sources like the OpenEMR user forum or official support channels. 




Sources Used:

- documentation | openemr_3_1_users_guide | data_sources\documentation\pdfs\openemr_3_1_users_guide.pdf
- documentation | openemr_4_1_users_guide | data_sources\documentation\pdfs\openemr_4_1_users_guide.pdf
- documentation | openemr_4_1_users_guide | data_sources\documentation\pdfs\openemr_4_1_users_guide.pdf

## Query 10

Ask an OpenEMR support question: Why can I not edit an insurance form?

Answer:

The issue might be related to your Apache site configuration and rewrite rules for the APIs directory.  Make sure you have a rewrite rule in place that allows API calls, as clicking the Insurance Edit button triggers an API request. 




Sources Used:

- forum | Cannot edit insurance form | https://community.open-emr.org/t/25497.json
- forum | Cannot edit insurance form | https://community.open-emr.org/t/25497.json