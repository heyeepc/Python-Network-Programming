import socket
import threading
import time  # 导入时间模块，用于控制频率

def handle_client(client_sock, addr):
    """
    处理客户端请求的子线程函数
    """
    print(f'[*] 建立新连接: {addr[0]}:{addr[1]}')
    
    # 向客户端发送欢迎语
    client_sock.send(b"Welcome to the server! Type 'exit' to quit.")

    try:
        while True:
            # 接收客户端发来的数据
            data = client_sock.recv(1024)
            
            # 延迟1秒，方便观察多线程并发效果
            time.sleep(1) 
            
            # 逻辑判断：如果收到空数据或 'exit'，则断开
            if not data or data.decode('utf-8').strip().lower() == 'exit':
                break
                
            # 处理数据：这里简单的把收到的话变成大写再发回去
            msg = data.decode('utf-8')
            print(f"[{addr[1]}] 客户端说: {msg}")
            client_sock.send(f"Server received: {msg.upper()}".encode('utf-8'))
            
    except ConnectionResetError:
        print(f"[!] 客户端 {addr} 强制断开了连接")
    finally:
        # 无论发生什么，最后一定要关闭连接，释放系统资源
        client_sock.close()
        print(f'[*] 连接关闭: {addr[0]}:{addr[1]}')

def start_server():
    # 创建基于 IPv4 和 TCP 协议的 Socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 绑定 IP 和 端口
    server.bind(('127.0.0.1', 8080))
    
    # 开始监听，5 代表最大等待队列长度
    server.listen(5)
    print('[*] 服务器启动，监听端口 8080...')

    while True:
        # 阻塞等待，直到有客户端连接
        # sock 是新的通信套接字，addr 是客户端的 IP 和端口
        sock, addr = server.accept()
        
        # 为每个连接创建一个独立的线程，防止一个客人卡住全店
        client_handler = threading.Thread(target=handle_client, args=(sock, addr))
        client_handler.start()

if __name__ == "__main__":
    start_server()
