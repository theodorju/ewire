# Ewire
Project is still under development.


## Assumptions:
Daily load forecast is generated from an outside system based on the requirements of [ADMIE](https://www.admie.gr/en). The algorithm that performs the scrapping of ADMIE site to download the latest forecast files was designed based on the way those files are uploaded, as of Feb. 2021. 
The following assumptions were made:
- Daily Load Forecast file:
    - The file will be in `xlsx` format.
    - The Excel file will have only one sheet.
    - The file will be uplodaded daily on: `https://www.admie.gr/systima/leitourgia/anafores-leitourgias-systimatos`.
    - The file will be named: `YYYYmmDD_ISPXDayAheadLoadForecast*` where X is either 1 or 2 based on the file version.
    - Daily load forecast will have a value for each 30-minute interval of each day, i.e. 48 daily values.
    - Daily load forecast values will begin on column 'C4' and will end on column 'AY4'. Column 'AK4' will be 

- Working assumptions:
    - If for whatever reason the download of a new file files, the old file will be used instead an a pop-up should notify the users.

If those assumptions are not true, the website is not guaranteed to perform as expected. It is possible that extra modifications in code would be necessary.

## Environmental variables:
- To be able to start the server with `flask run` export:
`export FLASK_APP=App`

- To use Flask under development export:
`export FLASK_ENV=development`

- To be able to receive mails from the contact form export:
`export EWIRE_MAIL=<your_email>`
`export MAIL_PASSWORD=<your_password>`

