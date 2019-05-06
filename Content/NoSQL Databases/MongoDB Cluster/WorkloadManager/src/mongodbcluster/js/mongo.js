db = db.getSiblingDB("admin")
db.createUser({ user: "%DB_USER%", pwd: "%DB_PASS%", roles: [ "readWrite", "dbAdmin", "userAdmin" ]})
db.auth("%DB_USER%","%DB_PASS%")
db = db.getSiblingDB("%DB_NAME%")
sh.enableSharding("%DB_NAME%")
sh.status()
sh.shardCollection("%DB_NAME%.people", {"name":1})
sh.status()

var db = db.getSisterDB('demo');
sh.enableSharding("demo")
var msg = {from: 'Christian',to: ['Peter', 'Paul'],sent_on: new Date(),message: 'Hello world'}

for(var i = 0; i < msg.to.length; i++) {
  var result = db.users.findAndModify({ query: { user_name: msg.to[i] }, update: { '$inc': {msg_count: 1} },upsert: true,new: true})
  var count = result.msg_count;
  var sequence_number = Math.floor(count/50);
  db.inbox.update({ owner: msg.to[i], sequence: sequence_number} ,{ $push: {messages: msg} },{ upsert:true });
}
db.inbox.find({owner: 'Peter'}).sort({sequence: -1}).limit(2);