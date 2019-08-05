current_dir = File.dirname(__FILE__)

log_location     STDOUT
chef_server_url  "https://%CHEF_HOSTNAME%/organizations/%CHEF_ORGANIZATION%"
validation_client_name "%VALIDATION_CLIENT%"
validation_key "#{current_dir}/%VALIDATION_CLIENT%.pem"
node_name "%NODE_NAME%"
trusted_certs_dir "/etc/chef/trusted_certs"