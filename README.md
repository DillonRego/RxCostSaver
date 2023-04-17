# DatabaseProject
Dillon Rego, drego@calpoly.edu
Sean Tomer, stomerho@calpoly.edu
Christian De Vera, chdevera@calpoly.edu

Our project will extrapolate and present data on the cost of various Drugs paid through the Medicaid program. We will display data showing the change in cost for various drugs overtime, and the change in average spending for various drugs over time. We also display data that shows which drugs are produced by which manufacturer. The last feature we’ll implement is the comparison of data(ex: cost of drugs) between different companies that produce the same drugs.


#Technical Specifications

User stories/User Requirements:
1. As a healthcare provider, I want to search for a specific drug to see its average spending per dosage unit and how it has changed over time, so that I can make informed prescribing decisions.

Flow:
The user lands on the homepage and sees two search bars.
The user enters the generic name and the manufacturer name of the drug they want to search for.
The application returns a page with information on the drug's average spending per dosage unit and its change over time, based on the Medicaid by Drug dataset.


2. As a healthcare provider, I want to search for a specific drug to see its average spending per dosage unit and how it has changed over time for every manufacturer that has made the drug, so that I can make informed prescribing decisions.


Flow:
The user lands on the homepage and sees two search bars.
The user enters the generic name of the drug they want to search for.
The application returns a page with information on the drug's average spending per dosage unit and its change over time for each manufacturer that has made it, based on the Medicaid by Drug dataset.


3. As a healthcare provider, I want to search for every drug a manufacturer has made and each drug’s average spending per dosage unit and how it has changed over time, so that I can make informed prescribing decisions.

Flow:
The user lands on the homepage and sees two search bars.
The user enters the name of the manufacturer they want to search for.
The application returns a page with information on every drug a manufacturer has made and each drug’s average spending per dosage unit and how it has changed over time, based on the Medicaid by Drug dataset.


Endpoints:

Get_endpoints

/claims

     Inputs: sort (top or bottom, limit, offset
     This endpoint will return a list of drugs for each drug it returns the following aggregated for all manufacturers:
     total_spending : a list of total yearly spending on that drug
     Avg_spending : a list of tuples containing average spending by claims and by units
     total_dsg : a list of yearly dosage units
     outlier_years : a list of years in which the drug was considered an outlier

     You can change the sort of the list with the sort input, change how many results with the limit input and change where the list begins with offset

/manufacturers

      Inputs : generic_name, brand_name
      This endpoint returns a list of manufacturers that manufacture a given drug. For each manufacturer it returns:
      name : the name of the manufacturer
      year : the year production began for that drug by a given manufacturer
      generic_name : the generic_name of the drug
      brand_name : the manufacturers given name for the drug
      You can filter for only manufacturers that make a given generic_name, brand_name or both

/gross_cost:

      Inputs: Manufacturer_Name, total_spending, year
      Output: Cost medicaid spent for a given company
      This endpoint returns the total reimbursement medicaid paid to a given manufacturer for a given year 

/change_average_spending:

      Inputs: drug_type(Generic Name), year_1, year_2
      Output: List of various Generic Name Drug with their change in rate for average spending over the year

      This endpoint returns a tupled list showing the change in rate of average spending over the year for a given drug produced by all the manufacturers

Request_endpoints:
/add_entry:

      Inputs: brnd_name, gnrc_name, tot_mftr, tot_spending, tot_dsg_unit tot_claims, avg_spnd_per_dsg_unt_wghtd, avg_spnd_per_clm, outlier_flag, year

      This endpoint will insert a new row into the database with the given information, if the year is not specified it will default to the earliest year not already         filled. If a year is given it will only fill in the drug data for the given year, (all inputs after tot_mftr) 

/delete_entry

      Inputs: brnd_name, gnrc_name, year

      This endpoint will delete entries under the given brand name and generic drug name. If no year is specified it will automatically delete all for that entry, if a       year is given it will only delete information for that calendar year.

Edge Cases:

       Some manufacturers entered the market later than the database’s start date causing the entries for those years to be left blank. For example Medicaid did not          buy Overall’s 8hr Arthritis Pain medication (generic: acetaminophen) until 2019. We will ignore any manufacturer and year combination where this is the case.

      Sometimes the generic and brand name of the drug are the same for more than one manufacturer so we should require the manufacturers name when giving calculations       or default to some kind of aggregation of the data.
