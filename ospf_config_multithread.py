import myparamiko
import threading
import time


def config_ospf(router):
    client = myparamiko.connect(**router)
    shell = myparamiko.get_shell(client)

    myparamiko.send_command(shell, 'enable')
    myparamiko.send_command(shell, 'cisco')
    myparamiko.send_command(shell, 'conf t')
    myparamiko.send_command(shell, 'router ospf 1')
    myparamiko.send_command(shell, 'net 0.0.0.0 0.0.0.0 area 0')
    myparamiko.send_command(shell, 'end')
    myparamiko.send_command(shell, 'terminal length 0')
    myparamiko.send_command(shell, 'sh ip protocols')
    time.sleep(2)

    output = myparamiko.show(shell)
    # print(output)
    output_list = output.splitlines()
    output_list = output_list[11:-1]
    # print(output_list)
    output = '\n'.join(output_list)
    # print(output)

    from datetime import datetime
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute

    file_name = f'(ospf_config_output){router["server_ip"]}_{year}-{month}-{day}.txt'
    with open(file_name, 'w') as f:
        f.write(output)

    myparamiko.close(client)


# creating a dictionary for each device to connect to
router1 = {'server_ip': '192.168.122.10',
           'server_port': '22', 'user': 'u1', 'passwd': 'cisco'}
router2 = {'server_ip': '192.168.122.20',
           'server_port': '22', 'user': 'u1', 'passwd': 'cisco'}
router3 = {'server_ip': '192.168.122.30',
           'server_port': '22', 'user': 'u1', 'passwd': 'cisco'}

# creating a list of dictionaries (of devices)
routers = [router1, router2, router3]

# creating an empty list (it will store the threads)
threads = list()

# iterating over the list (over the devices) and backup the config
for router in routers:
    # creating a thread for each router that executes the config function
    th = threading.Thread(target=config_ospf, args=(router,))
    threads.append(th)  # appending the thread to the list

# starting the threads
for th in threads:
    th.start()

# waiting for the threads to finish
for th in threads:
    th.join()
