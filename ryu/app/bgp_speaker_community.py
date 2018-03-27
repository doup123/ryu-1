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


speaker = BGPSpeaker(as_number=64512, router_id='10.0.0.2',
                     best_path_change_handler=dump_remote_best_path_change,
                     peer_down_handler=detect_peer_down)

speaker.neighbor_add("147.102.13.239",64512)
# uncomment the below line if the speaker needs to talk with a bmp server.
# speaker.bmp_server_add('192.168.177.2', 11019)
# pref_filter = PrefixFilter('147.102.0.0/16',PrefixFilter.POLICY_PERMIT)

# attribute_map = AttributeMap([pref_filter],
#                                      AttributeMap.ATTR_LOCAL_PREF, 250)
# speaker.prefix_del()
#speaker.attribute_map_set("147.102.13.156",attribute_maps=attribute_map)
from time import time
from collections import OrderedDict
random_generated_ips=["100.0."+str(i)+"."+str(j)+"/32" for i in range(250) for j in range(250)]
Results=OrderedDict()
count = 1
while True:
    eventlet.sleep(30)
    for j in range(1,20):
        eventlet.sleep(5)
        start=time()
        end_value=j*50
        for i in range(1,end_value):
            prefix=random_generated_ips[j*1000+i]
            speaker.prefix_add(prefix)
        end=time()
        res=end_value
        Results[res]=end-start

    count += 1
    eventlet.sleep(10)
    if count == 2:
        speaker.shutdown()
        for key,value in Results.items():
            value_formatted=str(value).replace(".",",")
            print("%s %s"%(key,value_formatted))
        print Results
        break
