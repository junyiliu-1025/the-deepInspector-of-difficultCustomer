import socket
import os
import datetime


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ss.connect(('8.8.8.8', 80))
        ip = ss.getsockname()[0]
    finally:
        ss.close()

    return ip


def socket_Sever():
    CHUNKSIZE = 1_000_000
    ip = get_host_ip()
    # Make a directory for the received files.
    #os.makedirs('Downloads',exist_ok=True)

    sock = socket.socket()
    sock.bind((ip,5000))
    sock.listen(1)

    with sock:
        while True:
            client,addr = sock.accept()
            
            flag = client.recv(1024)
            print(flag)
            t = datetime.datetime.now().strftime('%Y_%m_%d_%H-%M-%S-%f')
        # Use a socket.makefile() object to treat the socket as a file.
        # Then, readline() can be used to read the newline-terminated metadata.
            if flag == b'1':    
                with client, client.makefile('rb') as clientfile:
                    filename = clientfile.readline().strip().decode()
                    length = int(clientfile.readline())
                    print(f'Downloading {filename}:{length}...')
                    path = os.path.join('./faces/train/okes',t+".bmp")

                    # Read the data in chunks so it can handle large files.
                    with open(path,'wb') as f:
                        while length:
                            chunk = min(length,CHUNKSIZE)
                            data = clientfile.read(chunk)
                            if not data: break # socket closed
                            f.write(data)
                            length -= len(data)

                    if length != 0:
                        print('Invalid download.')
                    else:
                        print('Done.')
            if flag == b'2':    
                with client, client.makefile('rb') as clientfile:
                    filename = clientfile.readline().strip().decode()
                    length = int(clientfile.readline())
                    print(f'Downloading {filename}:{length}...')
                    path = os.path.join('./faces/train/unokes',t+".bmp")

                    # Read the data in chunks so it can handle large files.
                    with open(path,'wb') as f:
                        while length:
                            chunk = min(length,CHUNKSIZE)
                            data = clientfile.read(chunk)
                            if not data: break # socket closed
                            f.write(data)
                            length -= len(data)

                    if length != 0:
                        print('Invalid download.')
                    else:
                        print('Done.')
            if flag == b'3':
                folder_dict = "./models/model_oka/"
                foldername = client.recv(1024).decode()
                foldername2 = folder_dict+foldername
                with client, open(foldername2,'rb') as f:
                    client.sendall(foldername.encode() + b'\n')
                    client.sendall(f'{os.path.getsize(foldername2)}'.encode() + b'\n')
                    while True:
                        data = f.read(CHUNKSIZE)
                        if not data: break
                        client.sendall(data)           
            if flag == b'4':
                meg = "yes"
                meg = meg.encode('utf-8')
                client.sendall(meg)   
socket_Sever()