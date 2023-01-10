from app import write_json

def network_events_insertion(network_events):
    '''
    :desc This function receives a list of network events,
    aggregate network connections in dictionary keys, if Image[PID]->IP:PORT are the same.
    Stores the UTC times a connection was made for a specific key under 'UtcTimes' key.
    Saves the output to the DBMS import directory.
    network_events: list of Sysmon network events(3).
    '''
    networks = {}
    network_ids = []

    # Iterate through network events.
    for event in network_events:
        event_data = event['Event']['EventData']
        image = event_data['Image']
        pid = event_data['ProcessId']
        dst_ip = event_data['DestinationIp']
        dst_port = event_data['DestinationPort']
        network_id = f"{image}[{pid}]->{dst_ip}:{dst_port}"
        
        # Check if a network connection key already exists.
        if network_id not in network_ids:
            utc_times = []
            utc_times.append(event_data.pop('UtcTime',None))
            event_data['UtcTimes'] = utc_times
            networks[network_id] = event_data
            network_ids.append(network_id)
        else:
            utc_time = event_data.pop('UtcTime',None)
            networks[network_id]['UtcTimes'].append(utc_time)
    write_json(list(networks.values()), "network")
