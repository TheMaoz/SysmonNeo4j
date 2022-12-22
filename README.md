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
   - Create Database: DBMS version must be 5.0+
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
     - Configure Database Apoc Settings File:
       - Windows Users: On the DBMS click on the three dots then select Open folder --> DBMS.
          - navigate to "conf" folder.
          - Create a file "apoc.conf" and insert following lines to it:
         ```
         apoc.export.file.enabled=true
         apoc.import.file.enabled=true
         ```
         Restart DBMS and reload it.
       - Linux Users: Same as above, in the neo4j.conf file --> check every folder path in Neo4j: https://neo4j.com/docs/operations-manual/current/configuration/file-locations/
       
### **3) Install requirements.txt**
   - SysmonNeo4j Uses: evtx, neo4j
   - ``` virtualenv venv ```
   - ``` .\venv\Scripts\activate```
   - ``` pip install -r requirements.txt ```    


# **Run SysmoNeo4j**
```
// Default
python SysmonNeo4j.py -s STARTTIME -e ENDTIME -u BOLT_URL -n USERNAME -p PASSWORD 
// Example Command
.\SysmonNeo4j.py -s 2022-11-22-20:30:05 -e 2022-11-22-20:30:35 -f .\firstsample.evtx -p password -u neo4j -l "bolt://localhost:7687"
// Default Run Example in Ubuntu
sudo python3 SysmonNeo4j.py -s STARTTIME -e ENDTIME -u BOLT_URL -n USERNAME -p PASSWORD 
``` 