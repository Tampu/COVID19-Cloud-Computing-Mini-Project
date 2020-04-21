#                                           ECS781P - CLOUD COMPUTING: Mini Project

##                                             COVID-19 TRACKER WEB APPLICATION

This COVID-19 Tracker web application is a prototype of a Cloud Application developed in Python and Flask where one can use GET, POST, PUT and DELETE methods to interact with the application. It functions as an easy-to-use app which allows its users to access the Coronovirus World Count of New Confirmed Cases, New Deaths, New Recovered Cases in each country which gets updated everyday.It is a REST-based service interface and makes use of an external REST service being the Covid19 API (https://covid19api.com/) in order to fill the covid stats table. The REST API responses conform to REST standards.

Additionally, it makes use of a Cloud database in Apache Cassandra, the free and open-source NoSQL database management system. This is where a table of the covid statistics is stored and managed. See details of set-up below.

Finally, cloud security measures have been implemented. The application is served over HTTPS by using SSL certification. See details of set-up below.

Please use the requirements.txt file for all the packages and specific versions used to build this application.

# About COVID-19 Tracker Application 

Index.html is created inside a templates folder. 
Flash uses this folder and file to render the HTML page to the user.

**The Root URL**: 
`@app.route("/", methods=['GET', 'POST'])`

Directs the user to the "Covid-19 Tracker" page which allows user to browse the Coronovirus World Count data countrywise. The user needs to input the country name inorder to get the count in that particular country. For example, when the user inputs United Kingdom, the following output can be obtained.

![img](/appdemo.PNG)

# To Run the App
1. Start an AWS EC2 instance server.

2. Build an image in Cassandra.
Apache Cassandra is a free and open-source, NoSQL database management system designed to handle large amounts of data across many commodity servers, providing high availability with no single point of failure.[Learn More.](https://cassandra.apache.org/)


To build image
```
sudo docker build . --tag=cassandrarest:v1
```
3. Run the app
```
sudo docker run -p 80:80 cassandrarest:v1
```
To run the app over https:
```
sudo docker run -p 443:443 cassandrarest:v1 
```
# REST-based services served by the App
1. GET 


```GET /
https://ec2-54-92-130-85.compute-1.amazonaws.com/covid
```
Response:

A list of all countries and their covid statistics
```
[
  {
    "country": "dominica", 
    "newconfirmed": 0, 
    "newdeaths": 0, 
    "newrecovered": 0
  }, 
  {
    "country": "niger", 
    "newconfirmed": 0, 
    "newdeaths": 0, 
    "newrecovered": 0
  }, 
  ...
```
2. POST

To add a new entry into the covid statistics database (It is a Cassandra Database)
```
curl -k -i -H "Content-Type: application/json" -X POST -d '{"country":"NewCountry", "newconfirmed":2196, "newdeaths":5, "newrecovered":90}' https://ec2-54-92-130-85.compute-1.amazonaws.com/covid

```

Response:

```
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 46
Server: Werkzeug/1.0.1 Python/3.7.7
Date: Tue, 21 Apr 2020 10:39:29 GMT

{
  "message": "created: /covid/NewCountry"
}
```

3. PUT

To update the new entry into the covid statistics database 
```
curl -k -i -H "Content-Type: application/json" -X PUT -d '{"country":"NewCountry", "newconfirmed":2196, "newdeaths":5, "newrecovered":90}' https://ec2-54-92-130-85.compute-1.amazonaws.com/covid

```

Response:

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 46
Server: Werkzeug/1.0.1 Python/3.7.7
Date: Tue, 21 Apr 2020 10:43:33 GMT

{
  "message": "updated: /covid/NewCountry"
}
```
4. DELETE

To delete an entry from the covid statistics database 
```
curl -k -i -H "Content-Type: application/json" -X DELETE -d '{"country":"NewCountry"}' https://ec2-54-92-130-85.compute-1.amazonaws.com/covid  

```

Response:
```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 48
Server: Werkzeug/1.0.1 Python/3.7.7
Date: Tue, 21 Apr 2020 11:04:18 GMT

{
  "message": "deleted: /country/NewCountry"
}
```

## Running Flask Application Over HTTPS

This is done using Self Signed Certificates 
```
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
````
This command is used to write a new certificate in cert.pem with its corresponding private key in key.pem. 
Both have a validity period of 365 days
````
Generating a 4096 bit RSA private key
......................++
.............++
writing new private key to 'key.pem'
-----
About to be asked to enter information that will be incorporated
into the certificate request.This is called a Distinguished Name or a DN.
There are quite a few fields which can be leftblank
For some fields there will be a default value, enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:UK
State or Province Name (full name) [Some-State]:London
Locality Name (eg, city) []:Stratford
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Cloud Computing Mini Project
Organizational Unit Name (eg, section) []: QMUL
Common Name (e.g. server FQDN or YOUR name) []:Tampu
Email Address []:
```
````
To use this new self-signed certificate in Flask application,ssl_context argument in app.run() is set with a tuple consisting of the certificate and private key files along with port=443.
[Learn more](https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https)

## Load Balancing service : Kubernetes
Kubernetes is a portable, extensible, open-source platform for managing containerized workloads and services, that facilitates both declarative configuration and automation. It has a large, rapidly growing ecosystem.It gives Pods their own IP addresses and a single DNS name for a set of Pods, and can load-balance across them.[Learn more](https://kubernetes.io/)

Install Kubernetes
```
sudo snap install microk8s --classic
```

  1. Build cassandra-image 
  ```
  sudo microk8s enable registry #to enable registry
  sudo docker build . -t localhost:32000/cassandra-test:registry #To build and tag cassandra image
  ```
  2. Push to registry
  ```
  sudo docker push localhost:32000/cassandra-test # To push it to the registry
  ```
  3. Restart and start docker again
  ````
  sudo systemctl restart docker 
  sudo docker start cassandra-test
  ````
  4. Configure the deploy.yaml file
  ```
  sudo nano deploy.yaml 
  ```
  5. Deploy the docker container image present in the registry 
  ```
  sudo microk8s kubectl apply -f deploy.yaml
  sudo microk8s kubectl expose deployment covidapp-deployment --type=LoadBalancer --port=443 --target-port=443
  ```
  6. Check services for the IP address
  ```
  sudo microk8s kubectl get services
  ```

## Built With

* [Cassandra](http://cassandra.apache.org/doc/latest/) - Database used
* [Flask](http://flask.pocoo.org/docs/1.0/) - Web framework used
* [COVID19](https://covid19api.com/) - External API used
* [Kubernetes](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/) - Load balancing & Scaling
* [Security](https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https) - SSL Certificates

## Authors

**Tampu Ravi Kumar** [Tampu](https://github.com/Tampu/COVID19-Cloud-Computing-Mini-Project)
