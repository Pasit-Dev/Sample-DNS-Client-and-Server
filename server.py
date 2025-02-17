import dns.message
import dns.query
import dns.rcode
import dns.rrset
import socket

def start_dns_server(ip="0.0.0.0", port=1053):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    print(f"DNS server started on {ip}:{port}")

    try:
        while True:
            data, addr = sock.recvfrom(512)
            response = handle_dns_query(data)
            if response:
                sock.sendto(response.to_wire(), addr)
    except KeyboardInterrupt:
        print("Stopping the DNS server.")
    finally:
        sock.close()

def handle_dns_query(data):
    try:
        query = dns.message.from_wire(data)
        response = dns.message.make_response(query)
        qname = query.question[0].name
        qtype = query.question[0].rdtype

        if qtype == dns.rdatatype.A:
            rrset = dns.rrset.from_text(qname, 60, "IN", "A", "127.0.0.1")
            response.answer.append(rrset)
        else:
            response.set_rcode(dns.rcode.SERVFAIL)

        return response
    except Exception as e:
        print(f"Error processing DNS request: {e}")
        return None

if __name__ == "__main__":
    start_dns_server()