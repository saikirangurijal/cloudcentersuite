ALTER USER cassandra WITH PASSWORD '%DB_PASS%';
create keyspace %DB_NAME% with replication ={'class':'SimpleStrategy', 'replication_factor': '1'};