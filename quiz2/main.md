# CompSci 311 Quiz 2

## Q1

Answer the questions below about the OSPF link-state protocol. Justify your answers.

1. What is an advantage of using a routing protocol like OSPF compared to the spanning tree algorithm used by Ethernet?
2. Why does the reception of an OSPF link-state packet needs to be confirmed by the receiver to the transmitter?

### Answer

1. OSPF, a dynamic routing protocol, offers better scalability, adaptability, and efficient resource use compared to the spanning tree algorithm used in Ethernet. OSPF calculates the shortest path based on link costs, leading to efficient routing and faster convergence. On the other hand, the spanning tree algorithm in Ethernet, specifically STP, focuses on preventing network loops and creating a loop-free topology but doesn't consider link costs or performance metrics, resulting in less efficient routes and slower convergence.

2. In OSPF, confirming the reception of a link-state packet is crucial for maintaining a consistent network topology. Routers share topology information through Link State Advertisements (LSAs). Acknowledgments ensure that all routers have the same information and that no LSAs are lost or corrupted. If an acknowledgment isn't received, the sender will retransmit the LSA, keeping the network topology updated and synchronized across all routers.

[ref:https://book.systemsapproach.org/internetworking/routing.html]

---

# Q2

Consider the differences and similarities between learning switches and routers. Answer the following questions:

1. Why is the device-to-port learning algorithm suitable for switches but not routers?
2. Why is the spanning tree algorithm inadequate for routers?

### Answer

1. The device-to-port learning algorithm is suitable for switches but not routers because switches operate at Layer 2 (data link layer) of the OSI model and use MAC addresses to forward frames. Routers, on the other hand, operate at Layer 3 (network layer) and use IP addresses for routing decisions. The device-to-port learning algorithm is not suitable for routers, as they require routing protocols like OSPF or RIP to make decisions based on network layer information.

2. The spanning tree algorithm is inadequate for routers because it is designed to create a loop-free Layer 2 topology in Ethernet networks, preventing broadcast storms and network loops. Routers operate at Layer 3 and use routing protocols to find the best path to a destination based on network layer information.

---

## Q3

When a router receives an IP packet, it checks its forwarding table to verify if the destination network is directly connected to one of its interfaces or if it is necessary to forward the packet to another router on the path to the destination. If the destination network is directly connected, the router delivers the packet directly. The delivery process requires using the ARP protocol on the router.

1. In layman's terms, what is the main task handled by the ARP protocol?
2. Describe the content of the following fields in the ARP request sent by the router:
* Source MAC address
* Destination MAC address
* ARP request contents
3. Describe the content of the following fields in the ARP response sent by the destination:
* Source MAC address
* Destination MAC address
* ARP response contents

### Answer

1. In layman's terms, the main task handled by the ARP is to find the MAC address associated with a given IP address within a local network. This helps devices on the same network communicate with each other using their MAC addresses.

2. In the ARP request sent by the router:
- Source MAC address: The MAC address of the router's interface that's sending the request.
- Destination MAC address: The broadcast MAC address (FF:FF:FF:FF:FF:FF) to ensure all devices on the local network receive the request.
- ARP request contents: Includes the source IP and MAC addresses, the target IP address, and a request for the target's MAC address.

3. In the ARP response sent by the destination:
- Source MAC address: The MAC address of the destination device that's responding.
- Destination MAC address: The MAC address of the router's interface that sent the original ARP request.
- ARP response contents: Includes the destination device's IP and MAC addresses, confirming the association between the two.

[ref:https://book.systemsapproach.org/internetworking/basic-ip.html]

---

## Q3

Answer the following points about packet fragmentation:

1. Describe an alternative to packet fragmentation.
2. Discuss advantages and disadvantages of packet fragmentation compared to the alternative in item 

### Answer

1. An alternative to packet fragmentation is Path MTU Discovery (PMTUD). PMTUD is a technique that determines the maximum transmission unit (MTU) size of the entire path between two devices, helping to avoid fragmentation by adjusting the packet size accordingly.


2. Advantages and disadvantages of packet fragmentation compared to PMTUD:

- **Advantages**: Fragmentation ensures that packets are delivered even when there's a mismatch in MTU sizes along the path since it splits the packet into smaller parts that fit the MTU size of the network.

- **Disadvantages**: Packet fragmentation increases overhead, as each fragment requires its own header, which consumes additional bandwidth.


[ref:https://www.ibm.com/docs/fi/SSB27U_7.2.0/com.ibm.zvm.v720.hcpa6/hcpa662.htm]