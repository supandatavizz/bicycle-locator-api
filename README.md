# Bicycle Locator API

1. Start MySQL Docker Container
   - docker pull mysql:latest
   - docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=my-secret-pw -d -p 3306:3306 mysql:latest
   - create database in mysql docker container -> create database bicycle_data;
2. Loading Data Into MySQL Database
   - create python virtual environment -> python3 -m venv env -> source env/bin/activate
   - Install Requirements -> pip install --no-cache-dir -r requirements.txt
   - Run python3 load_data_to_mysql.py
3. Grep Docker Container IP
   - MySQL Docker Container IP -> docker exec mysql-container | grep IPAddress
   - Add it into app.py file
4. Build Application
   - docker build -t bicycle_api .
   - docker run -p 5000:5000 bicycle_api

# Test API
1. Open Postman
2. Create Request : GET http://127.0.0.1:5000/closest_bicycle
3. Params : latitude : <value>, longitude : <value>, num_results : <value>

Result : API Will Return Number of Results Of Bicycles Nearest To Location. 

# Plot Map
- Enter Your API Url In map.py file & Run Python File.
- It will create .html file which contains graph.
- Run html file which will show location point of bicycles.