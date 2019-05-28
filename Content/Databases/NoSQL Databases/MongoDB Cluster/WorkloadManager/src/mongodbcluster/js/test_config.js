var conf =  {
    _id: "replconfig01",
    configsvr: true,
    members: [
      { _id : 0, host : "hostname:27010" }
    ]
}

var check = rs.initiate(conf)
printjson(check)

