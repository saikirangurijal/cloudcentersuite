var conf =  {
     _id : "shardreplica01",
     members: [
       { _id : 0, host : "hostname:27017" }
     ]
   }

var check = rs.initiate(conf)
printjson(check)

