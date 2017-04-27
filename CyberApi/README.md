# CySpyder
##### Developed by: Joseph Dodson & Chase Brown


### Project Description

At its core, CySpyder is a web scraper purpose built to deliver cybersecurity blogs/articles in an easy to navigate format. All of the data extraction takes places remotely, so all the user has to do is open up the application and begin searching for the articles they want.

* Main Project Components
  * 'Spiders' that scrape a set list of websites routinely and extract data from every cybersecurity news article they find
    * This is done completely remotely, so the user doesn't have to worry about collection of data
  * A Cloud-Hosted database that stores the article data
  * A Web API to act as an intermediary between our other components and the database
  * A text analysis program that helps the user browse articles by listing main topics/subjects
  * User Interface designed to make searching for and working articles as simple as possible

### Setup

Simply download and extract the zip file and click on the **CySpyder** shortcut in the main directory. There are no other dependencies.


### Usage and Examples

Refer to provided pdf for screenshots with explanations of how to use the UI.


### Major Components/Frameworks Used in Development

* UI and spiders written and tested in Python 3.5
* API written in Node.js, hosted on with Apigee
* MongoDB Cloud Storage for article data

* Scrapy - Free Web Scraping Framework - Maintained by ScrapingHub
* SpaCy - Free Open Source NLP Framework
* ReportLab - PDF Generation Library
* Python-docx - Docx Generation Library
* BeautifulSoup4 - HTML Data Extraction Library
* lxml - HTML/XML Parsing Library used by BeautifulSoup4

