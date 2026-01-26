"""
Single Gateway of Thailand (Conceptual Simulation)
Author: Techasit Luanthon
License: MIT

This single-file project demonstrates a conceptual model of a national
single internet gateway for monitoring, routing, and cybersecurity control.
It is for EDUCATIONAL & SIMULATION purposes only.
"""

import time
import hashlib
import random

class SingleGatewayThailand:
    def __init__(self):
        self.allowed_domains = set()
        self.blocked_domains = set()
        self.logs = []

    def allow_domain(self, domain: str):
        self.allowed_domains.add(domain)

    def block_domain(self, domain: str):
        self.blocked_domains.add(domain)

    def inspect_packet(self, source_ip: str, domain: str, payload: str):
        packet_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]
        decision = "ALLOWED"

        if domain in self.blocked_domains:
            decision = "BLOCKED"
        elif self.allowed_domains and domain not in self.allowed_domains:
            decision = "REJECTED"

        log = {
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "source_ip": source_ip,
            "domain": domain,
            "packet_id": packet_hash,
            "decision": decision
        }
        self.logs.append(log)
        return decision

    def show_logs(self):
        for log in self.logs:
            print(log)

if __name__ == "__main__":
    gateway = SingleGatewayThailand()

    gateway.allow_domain("gov.th")
    gateway.allow_domain("health.th")
    gateway.block_domain("malware.com")

    test_packets = [
        ("192.168.1.10", "gov.th", "secure government data"),
        ("192.168.1.11", "malware.com", "attack payload"),
        ("192.168.1.12", "unknown.com", "random data"),
    ]

    for ip, domain, payload in test_packets:
        result = gateway.inspect_packet(ip, domain, payload)
        print(f"Packet from {ip} to {domain}: {result}")

    print("\n--- Gateway Logs ---")
    gateway.show_logs()
