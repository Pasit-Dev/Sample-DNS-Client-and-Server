import socket
import dns.message
import dns.name
import dns.query
import dns.rrset
import dns.rcode
import dns.rdatatype

def handle_query(data, address, sock):
    # แปลงข้อมูลที่ได้รับมาเป็น DNS message
    try:
        query = dns.message.from_wire(data)
    except Exception as e:
        print(f"Failed to parse query: {e}")
        return

    # สร้าง DNS response
    response = dns.message.make_response(query)

    # ตรวจสอบว่าเป็นคำขอประเภท A record หรือไม่
    for question in query.question:
        if question.rdtype == dns.rdatatype.A:
            # เพิ่มคำตอบใน response (เช่น return IP 127.0.0.1 สำหรับ domain ใด ๆ)
            rrset = dns.rrset.from_text(question.name, 300, 'IN', 'A', '127.0.0.1')
            response.answer.append(rrset)

    # ส่ง response กลับไปให้ client
    sock.sendto(response.to_wire(), address)


def simple_dns_server(ip='0.0.0.0', port=1053):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))

    print(f"DNS Server running on {ip}:{port}")

    try:
        while True:
            data, addr = sock.recvfrom(512)  # รับข้อมูลสูงสุด 512 ไบต์
            handle_query(data, addr, sock)
    except KeyboardInterrupt:
        print("Shutting down DNS server.")
    finally:
        sock.close()

if __name__ == '__main__':
    simple_dns_server()