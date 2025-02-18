import argparse
import socket
import threading
from dnslib import DNSRecord, QTYPE, RR, A
from dnslib.server import DNSServer, BaseResolver

class CustomDNSResolver(BaseResolver):
    """
    ตัวจัดการ DNS ที่รองรับทั้งโหมด Custom และ Forward
    """
    def __init__(self, use_custom_dns=True, forward_dns="1.1.1.1", port=53):
        self.use_custom_dns = use_custom_dns
        self.forward_dns = forward_dns
        self.port = port

    def resolve(self, request, handler):
        reply = request.reply()

        for question in request.questions:
            question_name = str(question.get_qname())

            if self.use_custom_dns and question.qtype == QTYPE.A and question_name == 'example.com.':
                # ตอบกลับค่า custom สำหรับ example.com
                reply.add_answer(RR('example.com', QTYPE.A, rdata=A('192.168.1.1'), ttl=60))
            else:
                # Forward คำขอไปยัง Cloudflare หรือ Google DNS
                try:
                    response_data = DNSRecord.question(question_name).send(self.forward_dns, self.port)
                    response = DNSRecord.parse(response_data)
                    return response
                except socket.error:
                    print(f"❌ Failed to forward request to {self.forward_dns}")

        return reply

def start_dns_server(port=5353, use_custom_dns=True, forward_dns="1.1.1.1"):
    """
    เริ่มต้น DNS Server และรองรับโหมด Custom หรือ Forward
    """
    resolver = CustomDNSResolver(use_custom_dns=use_custom_dns, forward_dns=forward_dns)
    server = DNSServer(resolver, port=port, address='0.0.0.0')
    server_thread = threading.Thread(target=server.start)
    server_thread.daemon = True
    server_thread.start()
    mode = "Custom DNS (example.com → 192.168.1.1)" if use_custom_dns else f"Forwarding to {forward_dns}"
    print(f"🚀 DNS server started on port {port}, mode: {mode}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Custom or Forwarding DNS Server")

    # ตัวเลือกให้เลือกโหมดผ่าน Terminal
    parser.add_argument("--custom", action="store_true", help="ใช้ DNS ที่กำหนดเอง (example.com -> 192.168.1.1)")
    parser.add_argument("--forward", type=str, default="1.1.1.1", help="ตั้งค่า DNS resolver สำหรับ forward (default: Cloudflare 1.1.1.1)")
    parser.add_argument("--port", type=int, default=5353, help="พอร์ตของ DNS Server (default: 5353)")

    args = parser.parse_args()

    start_dns_server(port=args.port, use_custom_dns=args.custom, forward_dns=args.forward)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n🛑 Stopping DNS server")
