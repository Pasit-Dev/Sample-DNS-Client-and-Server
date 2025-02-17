import dns.resolver

def dns_client(domain):
    try:
        answers = dns.resolver.resolve(domain, 'A')
        for rdata in answers:
            print(f'IP address for {domain}: {rdata.address}')
    except Exception as e:
        print(f'Failed to resolve domain {domain}: {e}')

dns_client('example.com')