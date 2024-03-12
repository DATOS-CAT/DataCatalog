# Mica Data Catalog Generator
This repository provides a tool to automate the creation of the template (Excel file) needed for the Mica data catalog, an [OBiBa](https://www.obiba.org/) tool used for research data management. The generated template facilitates the process of cataloging research data, enabling researchers to efficiently organize and document their datasets within Mica.

![image](https://github.com/DATOS-CAT/DataCatalog/assets/122832755/2b296f25-c1aa-4a02-8b12-efbc3309003a)


## How to Use
1. Clone this repository
2. Install dependencies
3. Have located the database from which you want to create a catalog. 
    > NOTE: 
    > We recommend you that if you want to generate different catalogs from different databases at the same time, you have all the data in the same folder to facilitate the process. 

4. Create an ScanReport from that database by using [`WhiteRabbit`](https://github.com/OHDSI/WhiteRabbit). 
    If you have the database/s in excel or csv format, go to "Scan" tab and "*Add*" the database/s.

    ![image](https://github.com/bsc-health-data/DATOS-CAT/assets/122832755/1c515b12-df98-4b39-a520-e39a92ae162d)


    > NOTE
    > Check the delimiter in the *Locations* tab!

5. Once your ScanReport is created, you can run the script. You only need to specify the "*path*" to the ScanReport and the "*name of the scan report*".

