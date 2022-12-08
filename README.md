# SysmoNeo4j
Open Source Tool - Sysmon Neo4j Visulaizer

# **Prerequisites**

_3 + 1 Steps to run SysmoNeo4j Tool_

### **1) Download and Install Neo4j Desktop**
   - Windows Users: https://neo4j.com/download/
     
     Create an account to get the license (totally free), download and install Neo4j Desktop.
     
     Useful Video: https://tinyurl.com/yjjbn8jx
   - Linux Users:
   
      ```
      sudo apt update
      sudo apt install apt-transport-https ca-certificates curl software-properties-common
      curl -fsSL https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
      sudo add-apt-repository "deb https://debian.neo4j.com stable 4.1"
      sudo apt install neo4j
      sudo systemctl enable neo4j.service
      sudo systemctl status neo4j.service
      ```
      
      You should have output that is similar to the following:
      ```
      ● neo4j.service - Neo4j Graph Database
     Loaded: loaded (/lib/systemd/system/neo4j.service; enabled; vendor preset: enabled)
     Active: active (running) since Fri 2020-08-07 01:43:00 UTC; 6min ago
     Main PID: 21915 (java)
     Tasks: 45 (limit: 1137)
     Memory: 259.3M
     CGroup: /system.slice/neo4j.service
     . . .
     ``` 
     Useful Video: https://tinyurl.com/vvpjf3dr
     
### **2) Create and Configure the Database**
   - Create Database:
     - Windows Users:
       
       You can create databases in whatever version you want (latest version preferable) through GUI or Neo4j Terminal.
       - Create a new database in GUI: Just click the (+), set DB Name, Username and Password. Useful Tutorial: https://www.sqlshack.com/getting-started-with-the-neo4j-graph-database/
       - Through Neo4j Shell: https://neo4j.com/docs/cypher-manual/current/databases/
     - Linux Users: When you start neo4j through systemctl, type ``` cypher-shell ```, then ``` create database NAME; ```. Now you have to set this database, as default so when you start neo4j you start automatically this database. Go to /etc/neo4j/neo4j.conf and uncomment ``` dbms.default_database=neo4j ``` and change it with your new database name. Restart neo4j service and you are ready. 
   - Configure Database:
     - Install APOC Plugin:
       - Windows Users: In Neo4j Desktop Main Page --> Choose your Database --> Click Plugins --> APOC --> Install
       - Linux Users:
         - Download APOC jar File: https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases (*-*-all.jar file)
         - Place it in Plugins Folder --> check every folder path in Neo4j: https://neo4j.com/docs/operations-manual/current/configuration/file-locations/
         - Modify the Database Configuration File to approve apoc procedures.
           
           Uncomment: ``` dbms.directories.plugins=plugins ```
           
           Uncomment and Modify:
           ```
            dbms.security.procedures.unrestricted=apoc.*
            dbms.security.procedures.whitelist=apoc.*,apoc.coll.*,apoc.load.*
            #loads unrestricted and white-listed procedures/plugins to the server
           ```
           
           Restart Neo4j: ```systemctl restart neo4j```
     - Configure Database Settings File:
       - Windows Users: In Neo4j Desktop Main Page --> Choose your Database --> ... (Three Dots) --> Settings --> Go to last line and set the commands below --> Apply and Restart the Database
        
         ```
         apoc.export.file.enabled=true
         apoc.import.file.enabled=true
         apoc.import.file.user_neo4j_config=false
         cypher.lenient_create_relationship = true
         ```
         
       - Linux Users: Same as above, in the neo4j.conf file --> check every folder path in Neo4j: https://neo4j.com/docs/operations-manual/current/configuration/file-locations/

     - Configure Memory Usage:
       
       In Neo4j Configuration File (neo4j.conf):
       For 16GB RAM you can use 8G + 4G for heap. For 8GB RAM you can use 4G + 2G etc.
       ```
       dbms.memory.heap.initial_size=4G
       dbms.memory.heap.max_size=8G
       dbms.memory.pagecache.size=4G
       ```
       
### **3) Install requirements.txt**
   - SysmonNeo4j Uses: xmltodict, neo4j, requests, beautifulsoup4
   - ``` pip install -r requirements.txt ```    


# **Run SysmoNeo4j**
### **5) Open NEO4J Desktop and create Project and DBMS**
    - Password for DBMS should be 1234 (:TODO: Add cli object to change password).
### **6) Create apoc.conf file**
    This is necessary for neo4j to work with json file.
    On the DBMS click on the three dots then select Open folder --> DBMS.
    navigate to "conf" folder.
    Create a file "apoc.conf" and insert following lines to it:
        apoc.import.file.enabled=true
        apoc.import.file.use_neo4j_config=true
    Restart DBMS and reload it.
### **7) Create .Json to manually paste to neo4j(NOT FOR PRODUCTION, MAOZ ONLY.)**
    put a comment on main (xD)
    Instead, run maozTest.
    and copy output to a .json file
    Of course, it is possible to use args... 
    .\SysmoNeo4j.py > events.json

### **8) MANUALLY LOAD .JSON FILE (NOT FOR PRODUCTION, MAOZ ONLY.)**
    On the DBMS click on the three dots then select Open folder --> Import.
    paste .json file (generated by python method) here.
    drag .cypher script to browser GUI and select paste in editor.
    run script.



```
// Default
python main.py -u BOLT_URL -n USERNAME -p PASSWORD -d IMPORT_PATH
// Run and Open Neo4j Browser
python main.py -u BOLT_URL -n USERNAME -p PASSWORD -d IMPORT_PATH -b y
// Run and Open Graphlytic App
python main.py -u BOLT_URL -n USERNAME -p PASSWORD -d IMPORT_PATH -g y
// Default Run Example in Ubuntu
sudo python3 main.py -u BOLT_URL -n USERNAME -p PASSWORD -d /var/lib/neo4j/import/
``` 
