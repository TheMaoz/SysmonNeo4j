def registry_events_insertion(registry_events):
    """
    :desc This function receives a list of registry events,
    parse it and save the output to the DBMS import directory.
    registry_events: list of registry events (id 12,13,14),
    """
    registry = []

    # Iterate through registry events.
    for event in registry_events:
        event_id = event['Event']['System']['EventID']

        # Registry key create or deleted.
        if event_id == 12:
            desc = "Key or value were created or deleted."

        # Registry key value set.
        elif event_id == 13:
            desc = "Key value was set."

        # Registry key and value renamed.
        elif event_id == 14:
            desc = "Key or value were renamed."
        event_data = event['Event']['EventData']
        event_data.update({"Description": desc})
        registry.append(event_data)
