
class TrackNode:
    def __init__(self, name, actual_coords, track_coords):
        self.coords = actual_coords
        self.track_coords = track_coords
        self.name = name
        self.node_free = True
        return

    # get the TrackNode's coordinates
    def get_track_coords(self):
        return self.track_coords

    # get the TrackNode's track reference coordinates
    def get_coords(self):
        return self.coords
    
    def get_name(self):
        return self.name
    
    def is_node_free(self):
        return self.node_free

    # are trains required to stop at TrackNodes
    def train_stop(self):
        return False
    
    # train arrives, so the node is no longer free
    def train_arrive(self):
        self.node_free = False
        return

    # train departs node, so node is free now
    def train_depart(self):
        self.node_free = True        
        return




class Signal (TrackNode):
    def __init__(self, name, actual_coords, track_coords):
        super().__init__(name, actual_coords, track_coords)
        self.safe = True
        self.automatic = True   # automomatic == true  ->   they automatically change to red or green
                                # automomatic == false  ->   the user can toggle them red or green, they will not automatically change to red or green
        return
   
    # are trains required to stop this signal
    def train_stop(self):
        return not self.safe
    
    def set_automatic(self):
        self.automatic = True
        return
    
    def set_manual(self):
        self.automatic = False
        return
    
    # toggle whether this signal is automatic or manual
    def toggle_automatic(self):
        self.automatic = not self.automatic
        return
    
    def get_automatic(self):
        return self.automatic
    
    # toggle the safety of the signal
    def toggle(self):
        self.safe = not self.safe
        return

    # make the signal show it is safe
    def set_safe(self):
        self.safe = True
        return

    # make the signal show it is not safe
    def set_not_safe(self):
        self.safe = False
        return



class Approaching_Station_Signal (Signal):
    def __init__(self, name, actual_coords, track_coords, assigned_station):
        super().__init__(name, actual_coords, track_coords)
        self.station = assigned_station
        self.danger_zone = False
        self.temp_train_pass = False
        self.linked_signals = []

        ## link signals so if one is red, the linked signals mirror that

        return

    def get_assigned_station(self):
        return self.station

    # are trains required to stop this signal
    def train_stop(self):

        # only check if the signal is automatic
        if self.automatic:

            # safe only if both danger_zone is false and the station is free
            if not self.danger_zone and self.station.is_node_free():
                self.safe = True
            else:
                self.safe = False
            
            # after a train passes the signal, the train is now in the danger zone and the signal sohuld be red
            if self.temp_train_pass:
                self.danger_zone = True
                self.temp_train_pass = False
            
            # if the station is occupied and self.danger_zone is true, then set danger_zone to false
            if not self.station.is_node_free() and self.danger_zone:
                self.danger_zone = False
            
            # if one of the linked signals is red, this signal should also be red
            for signal in self.linked_signals:
                if not signal.safe:
                    return True

        return not self.safe

    def link_signals(self, signals, chain):
        self.linked_signals = self.linked_signals + signals

        if chain:
            # also link this signal to the others
            for signal in signals:
                signal.link_signals([self], False)

        
        return

    def train_arrive(self):
        self.temp_train_pass = True
        return


class Station (TrackNode):
    def __init__(self, name, actual_coords):
        super().__init__(name, actual_coords, actual_coords)

    # are trains required to stop at stations
    def train_stop(self):
        return True
