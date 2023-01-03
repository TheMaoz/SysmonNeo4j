from app import write_json

def network_events_insertion(network_events):
    '''
    This function receives a list of network events,
    parse it and save the output to the DBMS import directory.
    '''
    write_json(network_events,"network")
