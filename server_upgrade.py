import argparse
import socket
import threading
from dnslib import DNSRecord, QTYPE, RR, A
from dnslib.server import DNSServer, BaseResolver

class CustomDNSResolver(BaseResolver):
    def __init__(self, use_custom_dns=True, forward_dns="1.1.1.1", port=53):
        self.use_custom_dns = use_custom_dns
        self.forward_dns = forward_dns
        self.port = port

    def resolve(self, request, handler):
        reply = request.reply()
        for question in request.questions:
            domain = str(question.get_qname())

            # ✅ Custom DNS (example.com -> 192.168.1.1)
            if self.use_custom_dns and question.qtype == QTYPE.A and domain == 'example.com.':
                reply.add_answer(RR('example.com', QTYPE.A, rdata=A('192.168.1.1'), ttl=60))
            else:
                # ✅ Forward ไปยัง Cloudflare / Google DNS
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                        s.settimeout(5)  # Timeout 5 วินาที
                        request_data = request.pack()
                        s.sendto(request_data, (self.forward_dns, self.port))
                        response_data, _ = s.recvfrom(1024)
                    return DNSRecord.parse(response_data)

                except socket.timeout:
                    print(f"❌ Timeout: DNS forward to {self.forward_dns} failed")
                except Exception as e:
                    print(f"❌ Forwarding error: {e}")

        return reply

def start_dns_server(port=53, use_custom_dns=True, forward_dns="8.8.8.8"):
    resolver = CustomDNSResolver(use_custom_dns=use_custom_dns, forward_dns=forward_dns)
    server = DNSServer(resolver, port=port, address='0.0.0.0')
    server_thread = threading.Thread(target=server.start)
    server_thread.daemon = True
    server_thread.start()
    mode = "Custom DNS (example.com → 192.168.1.1)" if use_custom_dns else f"Forwarding to {forward_dns}"
    print(f"🚀 DNS server started on port {port}, mode: {mode}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Custom or Forwarding DNS Server")
    parser.add_argument("--custom", action="store_true", help="ใช้ DNS ที่กำหนดเอง (example.com -> 192.168.1.1)")
    parser.add_argument("--forward", type=str, default="8.8.8.8", help="ตั้งค่า DNS Forwarding (default: 8.8.8.8)")
    parser.add_argument("--port", type=int, default=53, help="พอร์ตของ DNS Server (default: 53)")

    args = parser.parse_args()

    start_dns_server(port=args.port, use_custom_dns=args.custom, forward_dns=args.forward)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n🛑 Stopping DNS server")
