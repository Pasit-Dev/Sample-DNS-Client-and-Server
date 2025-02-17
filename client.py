import dns.resolver

def resolve_domain(domain):
    try:
        # Query A records 
        result = dns.resolver.resolve(domain, 'A')
        print(f"IP addresses for {domain}:")
        for ipval in result:
            print(ipval.to_text())
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    domain = "example.com"
    resolve_domain(domain)