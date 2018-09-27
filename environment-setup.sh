# Install Erlang

wget https://packages.erlang-solutions.com/erlang-solutions_1.0_all.deb
sudo dpkg -i erlang-solutions_1.0_all.deb
sudo apt-get update -y
sudo apt-get install erlang -y

#Install RabbitMQ from source
echo 'echo "deb http://www.rabbitmq.com/debian/ testing main" >> /etc/apt/sources.list' | sudo -s
wget https://www.rabbitmq.com/rabbitmq-signing-key-public.asc
sudo apt-key add rabbitmq-signing-key-public.asc
sudo apt-get update -y
sudo apt-get install rabbitmq-server -y

# add user and give authorization
sudo rabbitmqctl add_user username password
sudo rabbitmqctl authenticate_user username password
sudo rabbitmqctl set_permissions -p /myvhost test ".*" ".*" ".*"