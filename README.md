# Access Rules GUI

> A GUI for manage path based access rules, targetting Collab Subversion Edge access rule configuration file

## Process

1. Extract components from path based access rule file as JSON
2. Deal with the JSON data, store information to database

## Things to Keep in Mind

1. Within groups declaration, a group may contain multiple other groups and usernames
2. Order of access rules matters


## Preparation

1. Create a python file named **dbconnection.py** in **process\_data** folder with a function named **get_connection_config** which returns a **pymysql** connection config
2. Initialize a database with **db/svn.sql**
3. Place the access rule file exported from Subversion Edge management console into **data**, run **process_data/extract-data.py** and **persist-do.py** in order
4. With above steps you should be able to see parsed access rules in database
5. Do the following to start the web GUI to modify and generation new access rule configurations.


## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report

# run unit tests
npm run unit

# run all tests
npm test
```