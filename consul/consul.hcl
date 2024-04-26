data_dir = "/opt/consul"
datacenter = "dc1"
data_dir = "/opt/consul"
encrypt = "YujpIMI/ieIyw/i3d/j/+YEBeuD+zrLbJJ5LUTpgIWA="
bootstrap_expect=3
verify_incoming = true
verify_outgoing = true
verify_server_hostname = true
ui_config{
  enabled = true
}
server = true
performance {
  raft_multiplier = 1
}
bind_addr = "10.33.12.20"
ca_file = "/etc/consul.d/consul-agent-ca.pem"
cert_file = "/etc/consul.d/dc1-server-consul-0.pem"
key_file = "/etc/consul.d/dc1-server-consul-0-key.pem"
auto_encrypt {
  allow_tls = true
}
retry_join = ["10.33.12.209","10.33.66.10"]
acl {
  enabled = false
  default_policy = "allow"
  enable_token_persistence = true
}
#log_level="debug"
enable_script_checks = true