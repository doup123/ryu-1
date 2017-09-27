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

from ryu.services.protocols.bgp.bgpspeaker import BGPSpeaker

def dump_remote_best_path_change(event):
    print 'the best path changed:', event.remote_as, event.prefix,\
        event.nexthop, event.is_withdraw

def detect_peer_down(remote_ip, remote_as):
    print 'Peer down:', remote_ip, remote_as


speaker = BGPSpeaker(as_number=64512, router_id='10.0.0.1',
                     best_path_change_handler=dump_remote_best_path_change,
                     peer_down_handler=detect_peer_down)

speaker.neighbor_add(address='147.102.13.199', remote_as=64513,enable_ipv4fs=True)

# uncomment the below line if the speaker needs to talk with a bmp server.
# speaker.bmp_server_add('192.168.177.2', 11019)
count = 1
while True:
    eventlet.sleep(30)
    prefix = '10.20.' + str(count) + '.0/24'
    print "add a new prefix", prefix
    speaker.flowspec_prefix_add(
        flowspec_family='ipv4fs',
        rules=
        {'dst_prefix': '10.60.1.0/24'},
        actions=
        {'traffic_rate':
             {'Rate information': 0}}

    )
    print "-----"
    print speaker.attribute_map_get(address='147.102.13.199',route_family='ipv4fs' )
    print "-----"
    count += 1
    if count == 4:
        speaker.shutdown()
        break
