# Ewire

## General Information
The project is based on my thesis for Aristotle University of Thessaloniki. The thesis can be found [here](https://ikee.lib.auth.gr/record/294600/files/theodor-athanasiadis-thesis.pdf).

The main goal of the thesis was to bridge the gap in the relation between the electrical consumers and the electrical grid. In particular, through the webpage which was acompannied by a smart-lamp (using Rapsberry-PI), the users would have information regarding the hourly state of the electrical grid, namely
its load and the renewable energy infusion. This repository includes the code for an updated version of the webpage.

The webpage aims to quickly provide comprehensive graphs of daily load forecast and renewable energy infusion in Greece's Electrical Grid. The information for the daily load forecast as well as the renewable energy infusion are provided as excel files from the the Indepented Power Transmission Operator (IPTO) of Greece. Using python, those files are downloaded on the server and then plotted, each on a corresponding page.

## Page Sections

### Landing Page
Landing Page including the logo and a responsive navigation bar.
![](/static/assets/read-me-images/main-section.png)

### Visualizations
Visualization section where the users can view the latest Daily Load forecasted values or the latest Renewable Energy Infusion forecasted values.
![](/static/assets/read-me-images/visualizations.png)

### Contact form
Contact form with working validation. The contact form cannot be submitted with empty values or with an email that does not pass a (albeit basic) email validation. The messages are saved in an SQLite Database.
![](/static/assets/read-me-images/contact-form.png)

### Daily Load Forecast Graph
Graph of Daily Load Forecast updated each day based on a scheduler. Bokeh was used to generate the graph.
![](/static/assets/read-me-images/daily-forecast.png)

### Renewable Energy Infusion
Graph of Renewable Energy Infusion updated each day based on a scheduler. Bokeh was used to generate the graph.
![](/static/assets/read-me-images/renewable-forecast.png)


## Further information

### Assumptions:
Daily load forecast and renewable energy infusion predictions are generated from an outside system based on the requirements of [IPTO](https://www.IPTO.gr/en). The algorithm that performs the scrapping of IPTO site to download the latest forecast files was designed based on the way those files are uploaded, as of Feb. 2021. 
The following assumptions were made:
- Daily Load Forecast and Renewable Infusion Forecast:
    - The files must be in `xlsx` format.
    - The Excel files must have only one sheet.
    - The files must be uploaded daily on: `https://www.IPTO.gr/systima/leitourgia/anafores-leitourgias-systimatos`.
    - The files must be named: `YYYYmmDD_ISPXDayAhead<Mode>Forecast*` where X is either 1 or 2 based on the file version and `<Mode>` is Load for the daily load forecast file or RES for the renewable energy injection prediction file.
    - The files must have a value for each 30-minute interval of each day, i.e. 48 daily values.
    - The values in each file must begin on column `C4` and end on column `AY4`. 

- Working assumptions:
    - If for whatever reason the download of a new file fails, the old values will be used instead an a pop-up should notify the users.

If those assumptions are not true, the website is not guaranteed to perform as expected. It is possible that extra modifications in code would be necessary.

### Database
SQLite was chosen as database because it doesn't require setting up a separate database server and is built-in to Python.
Even though concurrent write request are processes sequentially and might cause the application to slow down, this application is small and such cases are not expected here.

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
