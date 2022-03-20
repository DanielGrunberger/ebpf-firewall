
import optparse
import filter
import ipaddress

SOURCE_FILE = 'ebpf.c'

def init_parser():
    parser = optparse.OptionParser()
    parser.add_option("-m", "--mode", dest="mode", help="Filter mode. Options: ingress, egress")
    parser.add_option("-c", "--container", dest="container", help="The container name")
    parser.add_option("-i", "--interface", dest="interface", help="The interface name")
    parser.add_option( "--ips", dest="ips", help="IPs list")
    parser.add_option( "--block", dest="block", help="blacklist", default=True,  action="store_true")
    return parser.parse_args()


def validate_args(options):
    print(options)
    if not options.mode:
        print("[E] No mode specified.  -h for help.")
        exit(0)
    elif not options.ips:
        print("[E] No ips specified.  -h for help.")
        exit(0)

def main():
    (options, arguments) = init_parser()
    
    options.ips=[ipaddress.ip_address(ip) for ip in  options.ips.split(",")]

    validate_args(options)
    if options.mode == filter.EGRESS_TYPE:
        if options.container:
            print('bu')
        else:
            firewall = filter.Firewall( 'tc_egress',options.interface,filter.EGRESS_TYPE,options.ips, options.block,filter.HOST_MODE,SOURCE_FILE)
            attrs = vars(firewall)
            print(', '.join("%s: %s" % item for item in attrs.items()))
            firewall.apply_egress_filter_for_host()

    elif options.mode == filter.INGRESS_TYPE:
        firewall = filter.Firewall( 'tc_ingress',options.interface,filter.INGRESS_TYPE,options.ips, options.block,filter.HOST_MODE,SOURCE_FILE)
        attrs = vars(firewall)
        print(', '.join("%s: %s" % item for item in attrs.items()))
        firewall.apply_egress_filter_for_host()

  
if __name__ == "__main__":
    main()

# python main.py -m egress -i eth0 --ips 216.58.212.206
# tshark -i eth0 -f 'icmp'  -Tfields -e ip.src  -e ip.dst -E header=y 
#tc qdisc del dev vetha6b026c parent ffff: