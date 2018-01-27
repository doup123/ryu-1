import eventlet

# BGPSpeaker needs sockets patched
eventlet.monkey_patch()
# initialize a log handler
# this is not strictly necessary but useful if you get messages like:
#    No handlers could be found for logger "ryu.lib.hub"
import logging
import sys
log = logging.getLogger()
log.addHandler(logging.StreamHandler(sys.stderr))
from ryu.lib.packet.bgp import *
from ryu.services.protocols.bgp.bgpspeaker import BGPSpeaker
from ryu.services.protocols.bgp.info_base.base import AttributeMap,PrefixFilter
def dump_remote_best_path_change(event):
    print 'the best path changed:', event.remote_as, event.prefix,\
        event.nexthop, event.is_withdraw

def detect_peer_down(remote_ip, remote_as):
    print 'Peer down:', remote_ip, remote_as


speaker = BGPSpeaker(as_number=1000, router_id='10.0.0.1',
                     best_path_change_handler=dump_remote_best_path_change,
                     peer_down_handler=detect_peer_down)

speaker.neighbor_add('147.102.13.156',1000,enable_ipv4fs=True)

# uncomment the below line if the speaker needs to talk with a bmp server.
# speaker.bmp_server_add('192.168.177.2', 11019)
# pref_filter = PrefixFilter('147.102.0.0/16',PrefixFilter.POLICY_PERMIT)

# attribute_map = AttributeMap([pref_filter],
#                                      AttributeMap.ATTR_LOCAL_PREF, 250)
# speaker.prefix_del()
#speaker.attribute_map_set("147.102.13.156",attribute_maps=attribute_map)
malicious_ips=lst = ["147.102."+str(j)+"."+str(k)+"/32" for j in range(1,101) for k in range(1,101)]
from time import time
list=[]
dic={}
count = 1
while True:
    eventlet.sleep(30)
    for k in range(1,10):
        x = time()
        dic[k]=[]
        end=k*100

        for i in range(1, end):
            speaker.flowspec_prefix_add(
                flowspec_family='ipv4fs',
                rules=
                {'src_prefix': malicious_ips[i]},
                actions=
                {'traffic_rate':
                    {'as_number':1000,'rate_info': 0}})
        # {'dst_prefix': '172.16.1.3/32'},
            # actions=
            # {'traffic_marking':
            #      { 'dscp': 24}}
        y=time()
        dic[k].append(y-x)
    print "-----"
    eventlet.sleep(30)
    if count == 1:

        speaker.shutdown()
        print dic
        break
