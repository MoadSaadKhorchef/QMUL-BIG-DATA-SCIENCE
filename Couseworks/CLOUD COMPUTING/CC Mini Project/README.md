### ARCHITECTURE
-   DATABASE: AWS RDS
-   REST API SERVER: NGINX + GUNICORN +FLASK

### FEATURES IMPLEMENTED:
-   REST-based service interface for CRUD operations 
-   Interaction with external REST services
-   Use of an external Cloud database for persisting information.(AWS RDS)

### ADDITIONAL FEATURES Implemented:
-   Serving the application over https.
-   Implementing hash-based authentication.
-   Implementing user accounts and access management.
-   Securing the database with role-based policies.

# REST API
Our REST API makes use for two external APIs to deliver information for surfers for potential times when tides are high and UV index is moderate.


## External APIs
- OpenUV (UV Index Forecast)
- Stormglass (Tide forecast)

Our API implement GET, POST, PUT and DELETE methods. Following are details of API calls.
## POST
### CREATE City (Only user with admin role)
### Unsuccessful POST Request
POST request is missing one parameter 'lng' due to which server returns **HTTP/1.0 400 BAD REQUEST**
```
curl -u mehwish:qmul123 -i -H "Content-Type: application/json" -X POST -d '{"city":"Paris", "lat":"48.864716"}' https://ec2-54-162-9-23.compute-1.amazonaws.com/add
```
### UNAUTHORIZED ACCESS
POST request with missing credientails or non admin user will serve unauthorized access error
```
curl -i -H "Content-Type: application/json" -X POST -d '{"city":"Paris", "lat":"48.864716", "lng":"2.349014"}' https://ec2-54-162-9-23.compute-1.amazonaws.com/add
```
### Successful POST Request
```
curl -u mehwish:qmul123 -i -H "Content-Type: application/json" -X POST -d '{"city":"Paris", "lat":"48.864716", "lng":"2.349014"}' https://ec2-54-162-9-23.compute-1.amazonaws.com/add
```
### CREATE USER (Only user with admin role)
### Successful POST Request 
```
curl -u mehwish:qmul123 -i -H "Content-Type: application/json" -X POST -d '{"userName":"aashna", "password":"12345", "role":"admin"}' https://ec2-54-162-9-23.compute-1.amazonaws.com/add_user
```

## GET
### Successful GET Request
Returns **HTTP/1.0 200 OK**
```
curl -u mehwish:qmul123 -i https://ec2-54-162-9-23.compute-1.amazonaws.com/location/london/
```
### Usuccessful GET Request
when data doesn't exits
Returns **HTTP/1.0 404 NOT FOUND**
```
curl -u mehwish:qmul123 -i https://ec2-54-162-9-23.compute-1.amazonaws.com/location/newyork/
```
### UNAUTHORIZED ACCESS
POST request with missing credientails or non admin user will serve unauthorized access error
```
curl -i https://ec2-54-162-9-23.compute-1.amazonaws.com/location/newyork/
```
## PUT
### Successful PUT Request
Returns **HTTP/1.0 201 CREATED**
```
curl -u mehwish:qmul123 -i -H "Content-Type: application/json" -X PUT -d '{"city":"Paris", "lat":"51.5074", "lng":"0.1278"}' https://ec2-54-162-9-23.compute-1.amazonaws.com/edit
```
### Successful PUT Request
Returns **HTTP/1.0 404 NOT FOUND**
```
curl -u mehwish:qmul123 -i -H "Content-Type: application/json" -X PUT -d '{"city":"Newyork", "lat":"51.5074", "lng":"0.1278"}' https://ec2-54-162-9-23.compute-1.amazonaws.com/edit
```
### UNAUTHORIZED ACCESS
PUT request with missing credientails or non admin user will serve unauthorized access error
```
curl -i -H "Content-Type: application/json" -X PUT -d '{"city":"Paris", "lat":"51.5074", "lng":"0.1278"}' https://ec2-54-162-9-23.compute-1.amazonaws.com/edit
```
```
curl -u mehwish:qmul123 -i -H "Content-Type: application/json" -X PUT -d '{"city":"Newyork", "lng":"0.1278"}' https://ec2-54-162-9-23.compute-1.amazonaws.com/edit
```

## DELETE
### Successful DELETE Request
Returns **HTTP/1.0 200 OK**
```
curl -u mehwish:qmul123 -X DELETE https://ec2-54-162-9-23.compute-1.amazonaws.com/delete/paris
```
### Unsuccessful DELETE Request
Returns **HTTP/1.0 404 NOT FOUND** if record does not exist in table
```
curl -u mehwish:qmul123 -X DELETE https://ec2-54-162-9-23.compute-1.amazonaws.com/delete/paris
```
### UNAUTHORIZED ACCESS
DELETE request with missing credientails or non admin user will serve unauthorized access error
```
curl -X DELETE https://ec2-54-162-9-23.compute-1.amazonaws.com/delete/paris
```
