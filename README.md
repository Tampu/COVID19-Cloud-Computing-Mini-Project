                                           ECS781P - CLOUD COMPUTING: Mini Project

                                             COVID-19 TRACKER WEB APPLICATION

This Covid-19 Tracker web application is a prototype of a Cloud application developed in Python and Flask where one can use GET, POST, PUT and DELETE methods to interact with the application. It functions as a easy-to-use app which allows its users to access the coronovirus world count of new confirmed cases, new deaths, new recoverred cases in each country.It is a REST-based service interface and makes use of an external REST service being the Covid19 API (https://covid19api.com/) in order to fill the covid stats table. The REST API responses conform to REST standards.

Additionally, it makes use of a Cloud database in Apache Cassandra, the free and open-source NoSQL database management system. This is where a table of the covid statistics is stored and and managed. See details of set-up below.

((Finally, cloud security measures have been implemented. The application is served over HTTPS, with certification granted through EFF's Certbot whilst using the WSGI server Gunicorn along with hash-based authentication where the usernames and hashed passwords are stored in the CQL database. See details of set-up below.))

Please use the requirements.txt file for all the packages and specific versions used to build this application.
