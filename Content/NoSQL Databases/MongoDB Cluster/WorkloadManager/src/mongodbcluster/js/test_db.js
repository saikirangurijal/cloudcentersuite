use mydb
sh.enableSharding("mydb")
sh.status()
sh.shardCollection("mydb.people", {"name":1})
sh.status()
