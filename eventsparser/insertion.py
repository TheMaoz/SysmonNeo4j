import json
from datetime import datetime
from evtx import PyEvtxParser
from pathlib import Path


class Insertion:
    app = None

    def __init__(self, app, events, event_ids) -> None:

        self.app = app
        # Creating lists of events group by object type.
        self.process_events = [event for event in events if event['Event']
                               ['System']['EventID'] in event_ids['process']]
        self.file_events = [event for event in events if event['Event']
                            ['System']['EventID'] in event_ids['file']]
        self.registry_events = [event for event in events if event['Event']
                                ['System']['EventID'] in event_ids['registry']]
        self.network_events = [event for event in events if event['Event']
                               ['System']['EventID'] in event_ids['network']]

        # Inserting data to the DBMS import directory.
        self.process_events_insertion(self.process_events)
        self.file_events_insertion(self.file_events)
        self.registry_events_insertion(self.registry_events)
        self.network_events_insertion(self.network_events)

    def write_json(func):
        """
        :desc This function receives list of events and the name of the event object.
        write the data as .json in the DBMS import dir.
        :data: list of json events.
        :event_type: name of object type to defer which .json is created (processes/registry/files/etc).
        """

        def inner(self, data, event_type):
            data, event_type = func(self, data, event_type)
            print(self.app.import_dir)
            path = (Path(self.app.import_dir, event_type)).with_suffix(".json")
            with open(path, "w", encoding='utf-8') as write:
                json.dump(data, write)
        return inner

    @write_json
    def registry_events_insertion(self, registry_events):
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
        return registry, "registry"

    @write_json
    def process_events_insertion(self, process_events):
        '''
        :desc This function receives a list of process events,
        aggregate process events in dictionary keys, if Image[PID] are the same.
        Stores the UTC times a process was terminated under 'EndUTCTime' key.
        Saves the output to the DBMS import directory.
        process_events: list of Sysmon process events(1 & 5).
        '''
        process_ids = []
        processes = {}

        # Iterate through process events.
        for event in process_events:
            event_id = event['Event']['System']['EventID']
            event_data = event['Event']['EventData']
            image = event_data['Image']
            pid = event_data['ProcessId']
            process_id = f"{image}[{pid}]"

            # Process creation.
            if event_id == 1 and process_id not in process_ids:
                process_ids.append(process_id)
                event_data["Description"] = "Process was created."
                processes[process_id] = event_data

            # Process was created and terminated.
            elif event_id == 5 and process_id in process_ids:
                end_time = event_data["UtcTime"]
                end_time = end_time[:end_time.find("."):]
                # find matching process in order to add EndUTCTime and Description.
                processes[process_id]["EndUTCTime"] = end_time
                processes[process_id]["Description"] = "Process was created and terminated."

            # Termination of a process which its creation was not logged, or not in time range.
            elif event_id == 5 and process_id not in process_ids:
                process_ids.append(process_id)
                event_data["Description"] = "Process was terminated."
                processes[process_id] = event_data

        return list(processes.values()), "processes"

    @write_json
    def network_events_insertion(self, network_events):
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
                utc_times.append(event_data.pop('UtcTime', None))
                event_data['UtcTimes'] = utc_times
                networks[network_id] = event_data
                network_ids.append(network_id)
            else:
                utc_time = event_data.pop('UtcTime', None)
                networks[network_id]['UtcTimes'].append(utc_time)
        return list(networks.values()), "network"

    @write_json
    def file_events_insertion(self, file_events):
        """
        :desc This function receives a list of file events,
        aggregate file events in dictionary keys, if Image[PID] -> TargetFilename are the same.
        Stores a description about the file operations under 'Description' key.
        If a file was created and deleted by the same process stores deletion time under "EndUTCTime".
        Saves the output to the DBMS import directory.
        file_events: list of Sysmon file events(11, 23, 26).
        """
        file_ids = []
        files = {}

        # Iterate through file events.
        for event in file_events:
            event_id = event['Event']['System']['EventID']
            event_data = event['Event']['EventData']
            image = event_data['Image']
            pid = event_data['ProcessId']
            target_file = event_data['TargetFilename']

            file_id = f"{image}[{pid}]->{target_file}"

            # File creation.
            if event_id == 11:
                file_ids.append(file_id)
                event_data["Description"] = "File was created."
                files[file_id] = event_data

            # File was created and deleted.
            elif event_id in (23, 26) and file_id in file_ids:
                end_time = event_data["UtcTime"]
                end_time = end_time[:end_time.find("."):]
                files[file_id]["EndUTCTime"] = end_time
                files[file_id]["Description"] = "File was created and deleted."

            # File deletion of a file which its creation was not logged, or not in time range.
            elif event_id in (23, 26) and file_id not in file_ids:
                file_ids.append(file_id)
                event_data["Description"] = "File was deleted."
                files[file_id] = event_data
        return list(files.values()), "files"
