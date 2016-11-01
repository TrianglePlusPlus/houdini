# encoding: utf-8
# -*- mode: ruby -*-

require "yaml"

dir = File.dirname(File.expand_path(__FILE__))
config = YAML.load_file("#{dir}/config.yml")
yaml = config["config"]["vagrant"]

Vagrant.configure(2) do |config|
	config.vm.box = "corpit/postgres"
	
	# comment out this line if you are using windows
	config.vm.network "private_network", ip: yaml["ip"]
	
	config.vm.network "forwarded_port", guest: 80, host: 8080
	config.ssh.insert_key = false
	config.vm.synced_folder ".", "/home/thecorp/django/" + yaml["repo_name"]
	config.vm.provision "shell" do |s|
		s.path = "vagrant.sh"
		s.args = [yaml["repo_name"], yaml["db_name"], yaml["db_user"], yaml["db_pass"]]
	end
end