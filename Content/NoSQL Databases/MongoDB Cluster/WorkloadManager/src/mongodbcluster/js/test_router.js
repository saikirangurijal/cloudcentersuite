var check = sh.addShard( "shardreplica01/hostname:27017")
printjson(check)
var st = sh.status()
printjson(st)
