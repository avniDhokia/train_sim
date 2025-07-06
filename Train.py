import math
import random
from TrackNode import TrackNode, Station, Signal, Approaching_Station_Signal

class Train:

    def __init__(self, name, route, start_index, cycle):
        self.name = name
        self.route = route          # array of TrackNodes including stations, signals and junctions
        self.route_index = start_index

        self.speed = random.randint(14, 16)

        self.wait = False           # used for waiting at signals
        self.wait_time = 0          # used for waiting a set amount of time at a station

        self.cycle_route = cycle    # true -> route is a loop
                                    # false -> route is a line
        self.active = True          # will be set to false when the train is no longer active (eg reaches end of line route)

        self.position = [0,0]
        self.position[0] = route[0].get_track_coords()[0]
        self.position[1] = route[0].get_track_coords()[1]

        return
    

    # get the train's name
    def get_name(self):
        return self.name

    
    # get a string describing the train
    def get_description(self):
        string = "Train " + self.name + " heading to " + self.get_next_stop().get_name() + "."

        if not self.cycle_route:
            string = string + " This train will terminate at " + self.route[-1].get_name() + "."
        
        return string


    # using the current position and the next node, return the x and y distances to get there
    def get_travel_dir(self):
        next_station_coord = self.get_next_stop().get_track_coords()

        x = next_station_coord[0] - self.position[0]
        y = next_station_coord[1] - self.position[1]

        return (x,y)
    

    # get the train's current x and y coords
    def get_coords(self):
        return self.position


    # get the next stop on the train's route
    def get_next_stop(self):

        if self.route_index >= len(self.route)-1:
            return self.route[0] ###

            if self.cycle_route:
                return self.route[0]
            else:
                return None
        
        return self.route[self.route_index+1]


    # does this train have more stops to cover
    def get_active(self):
        return self.active

    def collision_occured(self):
        self.active = False

        # if waiting at a station when the collision happened, make sure the station is considered free now
        if self.wait_time > 0 or self.wait:
            self.route[self.route_index].train_depart()

        return


    # get the latest stop passed on the train's route
    def get_latest_stop(self):
        return self.route[self.route_index]


    # has the train reached the next stop
    def has_train_reached_stop(self):

        prev_coords = self.get_latest_stop().get_track_coords()
        next_coords = self.get_next_stop().get_track_coords()
    
        x = self.position[0]
        y = self.position[1]

        if (x==next_coords[0] and y==next_coords[1]):
            return True

        if (x <= prev_coords[0] and x > next_coords[0]) or (x >= prev_coords[0] and x < next_coords[0]) or (y <= prev_coords[1] and y > next_coords[1]) or (y >= prev_coords[1] and y < next_coords[1]):
            return False
        
        return True
        

    # if the train reaches a node, it will increase its route index so it knows where to head next
    def reach_node(self):
        MAX_WAIT_TIME = 25

        self.route_index = self.route_index + 1
    
        # if route is not a loop and train is at final stop, make the train go to first stop
        if not self.cycle_route and self.route_index == len(self.route)-1:
            self.position = [self.route[0].get_track_coords()[0], self.route[0].get_track_coords()[1]]
            #self.active = False
            self.route[-1].train_depart()
            return

        # restart route if at final node
        if self.route_index == len(self.route):
            self.route_index = 0
        
        # let the node know a train has arrived
        self.route[self.route_index].train_arrive()
    
        # if node wants the train to stop, wait for some time
        if self.route[self.route_index].train_stop():

            if isinstance(self.route[self.route_index], Station):
                self.wait_time = MAX_WAIT_TIME
            elif isinstance(self.route[self.route_index], Approaching_Station_Signal):
                self.wait = True
                

        # ensure the train is set to the correct position
        self.position[0] = self.route[self.route_index].get_track_coords()[0]
        self.position[1] = self.route[self.route_index].get_track_coords()[1]

        return


    # the train will travel along the track, changing it's position
    # this method takes into account waiting at stations
    def travel(self, time):

        # waiting at condition-based node (eg signals)
        if self.wait == True:
            self.wait = self.route[self.route_index].train_stop()

            if not self.wait:
                self.route[self.route_index].train_depart()
                self.wait_time = 10
            return

        # waiting at time-based node (eg stations)
        if self.wait_time > 0:
            self.wait_time = self.wait_time - 1

            # check if done waiting
            if self.wait_time == 0:
                self.route[self.route_index].train_depart()
            
            return
        
        # check if train should be inactive now
        if not self.active:
            return

        dir_x, dir_y = self.get_travel_dir()
        
        distance = math.sqrt( math.pow(dir_x, 2) + math.pow(dir_y, 2) )
        

        if self.has_train_reached_stop() or (distance) < 0.05*self.speed:
            self.reach_node()
        else:
            total_dir = abs(dir_x) + abs(dir_y)

            if dir_x < 0:
                self.position[0] = self.position[0] - abs(self.speed * time * (dir_x / total_dir))
            else:
                self.position[0] = self.position[0] + abs(self.speed * time * (dir_x / total_dir))
            
            if dir_y < 0:
                self.position[1] = self.position[1] - abs(self.speed * time * (dir_y / total_dir))
            else:
                self.position[1] = self.position[1] + abs(self.speed * time * (dir_y / total_dir))

        
        return