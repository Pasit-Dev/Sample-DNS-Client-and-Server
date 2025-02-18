import dns.resolver

def query_dns(domain_name, server_ip='127.0.0.1', server_port=5353):
    try:
        # ตั้งค่า Resolver ให้ส่งคำขอไปที่ DNS Server ของเรา
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = [server_ip]
        resolver.port = server_port  # ใช้พอร์ตเดียวกับ dns_server.py

        # Query บันทึก A (IPv4 Address)
        answer = resolver.resolve(domain_name, 'A')

        # แสดงที่อยู่ IP ที่ได้รับ
        for ip in answer:
            print(f"✅ The IP address for {domain_name} is {ip}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

def main():
    print("🔍 DNS Query Client (Type 'exit' to quit)")
    server_ip = input("Enter DNS Server IP (default 127.0.0.1): ") or "127.0.0.1"
    server_port = int(input("Enter DNS Server Port (default 5353): ") or 5353)

    while True:
        domain_name = input("\nEnter domain name to query: ")
        if domain_name.lower() == 'exit':
            print("👋 Exiting...")
            break
        query_dns(domain_name, server_ip, server_port)

if __name__ == "__main__":
    main()
