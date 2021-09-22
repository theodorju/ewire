# Ewire
Project is still under development.

### Database
SQLite was chosen as database because it doesn't require setting up a separate database server and is built-in to Python.
Even though concurrent write request are processes sequentially and might cause the application to slow down, this application is small and such cases are not expected here.

### Assumptions:
Daily load forecast and renewable energy infusion predictions are generated from an outside system based on the requirements of [ADMIE](https://www.admie.gr/en). The algorithm that performs the scrapping of ADMIE site to download the latest forecast files was designed based on the way those files are uploaded, as of Feb. 2021. 
The following assumptions were made:
- Daily Load Forecast and Renewable Infusion Forecast:
    - The files must be in `xlsx` format.
    - The Excel files must have only one sheet.
    - The files must be uploaded daily on: `https://www.admie.gr/systima/leitourgia/anafores-leitourgias-systimatos`.
    - The files must be named: `YYYYmmDD_ISPXDayAhead<Mode>Forecast*` where X is either 1 or 2 based on the file version and `<Mode>` is Load for the daily load forecast file or RES for the renewable energy injection prediction file.
    - The files must have a value for each 30-minute interval of each day, i.e. 48 daily values.
    - The values in each file must begin on column `C4` and end on column `AY4`. 

- Working assumptions:
    - If for whatever reason the download of a new file fails, the old values will be used instead an a pop-up should notify the users.

If those assumptions are not true, the website is not guaranteed to perform as expected. It is possible that extra modifications in code would be necessary.

### Conda environment:
- To create an anaconda environment based on yml file execute:
`conda env create -f environment.yml`
<br>This creates a development environment with all the necessary packages, named `ewire`.

- To activate the environment execute:
`conda activate ewire`

### Environmental variables:
- To be able to start the server with `flask run` export:
`export FLASK_APP=ewire`

- To use Flask under development export:
`export FLASK_ENV=development`
