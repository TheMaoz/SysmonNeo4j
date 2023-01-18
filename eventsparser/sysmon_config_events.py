from app import write_json


def config_events_insertion(config_events_list):
    """
    :desc: This function receives a list of sysmon config changes events,
    parse it and save the output to the DBMS import directory.
    config_events_list: list of config events (id 4,16).
    """
    events = []

    # Iterate through config events.
    for event in config_events_list:
        event_id = event['Event']['System']['EventID']

        # Sysmon service state changed.
        if event_id == 4:
            desc = "Sysmon service state changed."

        # Sysmon config state changed.
        elif event_id == 16:
            desc = "Sysmon configuration state changed."
        event_data = event['Event']['EventData']
        event_data.update({"Description": desc})
        events.append(event_data)
    write_json(events, "sysmon_config_events")
