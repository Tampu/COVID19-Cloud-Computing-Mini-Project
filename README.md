#                                           ECS781P - CLOUD COMPUTING: Mini Project

##                                             COVID-19 TRACKER WEB APPLICATION

This Covid-19 Tracker web application is a prototype of a Cloud application developed in Python and Flask where one can use GET, POST, PUT and DELETE methods to interact with the application. It functions as an easy-to-use app which allows its users to access the Coronovirus World Count of New Confirmed Cases, New Deaths, New Recovered Cases in each country which gets updated everyday.It is a REST-based service interface and makes use of an external REST service being the Covid19 API (https://covid19api.com/) in order to fill the covid stats table. The REST API responses conform to REST standards.

Additionally, it makes use of a Cloud database in Apache Cassandra, the free and open-source NoSQL database management system. This is where a table of the covid statistics is stored and managed. See details of set-up below.

Finally, cloud security measures have been implemented. The application is served over HTTPS by using SSL certification. See details of set-up below.

Please use the requirements.txt file for all the packages and specific versions used to build this application.

# Interacting with the Web Application
**Accessing the Root URL**: 
`@app.route("/", methods=['GET', 'POST'])`

Directs the user to the "Covid-19 Tracker" page which allows user to browse the Coronovirus World Count data countrywise. The user needs to input the country name inorder to get the count in that particular country.
Application demo

![img](/appdemo.PNG)





