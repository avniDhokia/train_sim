import pygame
from TrackNode import TrackNode, Station, Signal, Approaching_Station_Signal
from Train import Train
from Track import Track
import math


# colours
background_colour = (184, 240, 249)
station_default_colour = (252, 63, 91)
track_default_colour = (249, 155, 54)
train_default_colour = (22, 175, 252)

# thicknesses
track_thickness = 5
station_thickness = 6
signal_thickness = 6
train_thickness = 6


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1300, 800))
clock = pygame.time.Clock()
running = True


# given 2 stations, give the position a signal should be between them
def mid_coords_from_stations(previous_station, assigned_station):
    previous_coords = previous_station.get_track_coords()
    assigned_coords = assigned_station.get_track_coords()

    x = (previous_coords[0] + assigned_coords[0]) / 2
    y = (previous_coords[1] + assigned_coords[1]) / 2

    return (x, y)

# given a track node, mouse x and y coords and thickness of the rendered node, is the mouse hovering over the node?
def mouse_hover_over(obj, x, y, thickness):
    obj_x, obj_y = obj.get_coords()
    x_diff = obj_x - x
    y_diff = obj_y - y

    if (math.pow(x_diff,2) + math.pow(y_diff,2)) <= math.pow(thickness+10,2):
        return True
    
    return False

# draw a signal
def draw_signal(screen, signal):
    red = [242, 58, 61]
    green = [29, 226, 72]

    if signal.train_stop() == True:
        colour = red
    else:
        colour = green

    # black line for signal pole
    pygame.draw.line(screen, [0, 0, 0], signal.get_coords(), [signal.get_coords()[0], signal.get_coords()[1] + signal_thickness*2], 3)

    # black circle behind red/green light
    pygame.draw.circle(screen, [0, 0, 0], signal.get_coords(), signal_thickness + 1)

    # red/green light                                         
    pygame.draw.circle(screen, colour, signal.get_coords(), signal_thickness-2)

    # reference point on track
    pygame.draw.circle(screen, [0, 0, 0], signal.get_track_coords(), signal_thickness/2)

    return

# check for collisions between trains
def check_train_collisions(trains, thickness):
    for i in range(len(trains)):
        for j in range(i + 1, len(trains)):
            train1 = trains[i]
            train2 = trains[j]

            if train1.get_active() and train2.get_active():
                x1, y1 = train1.get_coords()
                x2, y2 = train2.get_coords()

                distance = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))

                if distance < (thickness * 2):
                    print(f"Train {train1.get_name()} has collided with train {train2.get_name()} - both trains are now inactive for repairs")
                    train1.collision_occured()
                    train2.collision_occured()

    return


# other setup

mainland_points = [(300, 60), (370, 60), (440, 100), (470, 80), (510, 100), (550, 100), (520, 170), (565, 150), (610, 100), (660, 120), (745, 90), (790, 100), (855, 90), (840, 160), (850, 220), (860, 165), (885, 100), (920, 70), (960, 110), (1010, 115), (1080, 100), (1145, 110), (1200, 180), (1210, 285), (1240, 350), (1215, 390), (1150, 400), (1110, 425), (1160, 415), (1200, 450), (1175, 540), (1180, 600), (1130, 680), (1120, 740), (1050, 730), (975, 750), (880, 745), (800, 725), (785, 680), (815, 650), (870, 600), (790, 585), (800, 640), (710, 660), (725, 740), (655, 745), (550, 740), (400, 720), (300, 680), (250, 600), (295, 515), (345, 500), (385, 415), (420, 310), (350, 255), (295, 215), (245, 195), (235, 110)]
island_points = [(210, 210), (250, 280), (280, 280), (335, 300), (360, 310), (363, 350), (260, 400), (220, 440), (190, 510), (100, 490), (85, 400), (65, 350), (90, 300), (115, 265), (155, 225)]
land = [mainland_points, island_points]

# stations

# island stations
fern = Station("Fern", [163, 251])#, [163, 251])
lilypad = Station("Lilypad", [295, 315])#, [295, 315])
moss = Station("Moss", [240, 395])#, [240, 395])
cactus = Station("Cactus", [140, 470])#, [140, 470])
evergreen = Station("Evergreen", [110, 340])#, [110, 340])

# mainland stations
north_west_point = Station("North West Point", [310, 120])#, [310, 120])#1
windy_way = Station("Windy Way", [410, 190])#, [410, 190])
rocky_roll = Station("Rocky Roll", [500, 250])#, [500, 250])
eddington = Station("Eddington", [716, 162])#, [680, 220])
fishy = Station("Fishy", [814, 275])#, [860, 310])#5
pington_bington = Station("Pington Bington", [986, 335])#, [1025, 275])
marrow = Station("Marrow", [925, 175])#, [925, 175])
acorn_hut = Station("Acorn Hut", [1100, 175])#, [1100, 175])
little_hook = Station("Little Hook", [1150, 320])#, [1150, 320])
penny_pickle = Station("Penny Pickle", [485, 415])#, [520, 390])#10
snapple = Station("Snapple", [651, 272])#, [615, 320])
central = Station("Central", [760, 385])#, [760, 385])
brickle_lane = Station("Brickle Lane", [920, 465])#, [920, 465])
bendy_way = Station("Bendy Way", [1040, 440])#, [1040, 440])
wingle_flap = Station("Wingle Flap", [450, 515])#, [450, 515])#15
intrantum = Station("Intrantum", [603, 425])#, [620, 460])
bubble_ship = Station("Bubble Ship", [760, 510])#, [815, 510])
criss_cross = Station("Criss Cross", [1005, 570])#, [1005, 570])
nice_park = Station("Nice Park", [1120, 510])#, [1120, 510])
south_west_terminal = Station("South West Terminal", [382, 637])#, [382, 637])#20
triangle = Station("Triangle", [600, 615])#, [600, 615])
yoghurt = Station("Yoghurt", [1060, 675])#, [1060, 675])
big_hook = Station("Big Hook", [900, 700])#, [900, 700])#23


# all signals
signals = [Approaching_Station_Signal("Oak", [233, 301], mid_coords_from_stations(fern, lilypad), lilypad),
            Approaching_Station_Signal("Willow", [285, 352], mid_coords_from_stations(lilypad, moss), moss),
            Approaching_Station_Signal("Elm", [190, 420], mid_coords_from_stations(moss, cactus), cactus),
            Approaching_Station_Signal("Beech", [114, 390], mid_coords_from_stations(cactus, evergreen), evergreen),
            Approaching_Station_Signal("Chesnut", [125, 287], mid_coords_from_stations(evergreen, fern), fern),
            Approaching_Station_Signal("S1", [568, 634], [568, 618], triangle),
            Approaching_Station_Signal("S2", [480, 275], [499, 279], rocky_roll),
            Approaching_Station_Signal("S3", [747, 339], [745, 366], central),
            Approaching_Station_Signal("S4", [745, 405], [745, 391], central),
            Approaching_Station_Signal("S5", [632, 610], [619, 605], triangle)]

# link some signals together
signals[7].link_signals([signals[8]], True)
signals[9].link_signals([signals[5]], True)

# all routes
green_route = [fern, signals[0], lilypad, signals[1], moss, signals[2], cactus, signals[3], evergreen, signals[4]]  # loop
central_route = [rocky_roll, eddington, fishy, pington_bington, bendy_way, criss_cross, bubble_ship, signals[9], triangle, wingle_flap, penny_pickle, signals[6]]    # loop
ziggy_route = [north_west_point, windy_way, rocky_roll, snapple, signals[7], central, brickle_lane, bendy_way, nice_park, yoghurt, big_hook]  # linear
zaggy_route = [south_west_terminal, signals[5], triangle, intrantum, signals[8], central, fishy, marrow, acorn_hut, little_hook]    # linear

# all stations
stations = [fern, lilypad, moss, cactus, evergreen, north_west_point,
            windy_way, rocky_roll, eddington, fishy, pington_bington,
            marrow, acorn_hut, little_hook, penny_pickle, snapple, central,
            brickle_lane, bendy_way, wingle_flap, intrantum, bubble_ship,
            criss_cross, nice_park, south_west_terminal, triangle, yoghurt, big_hook]

# tracks to be drawn
tracks = [Track(green_route, True, [5, 196, 24]), Track(central_route, True, [252, 107, 63]), Track(ziggy_route, False, [244, 129, 216]), Track(zaggy_route, False, [237, 252, 78])]

# make trains with routes
green_one = Train("Green One", green_route, 0, True)
green_two = Train("Green Two", green_route, 4, True)
central_one = Train("Central One", central_route, 0, True)
central_two = Train("Central Two", central_route, 5, True)
ziggy_one = Train("Ziggy One", ziggy_route, 0, False)
zaggy_one = Train("Zaggy One", zaggy_route, 0, False)
ziggy_two = Train("Ziggy Two", ziggy_route, 5, False)
zaggy_two = Train("Zaggy Two", zaggy_route, 4, False)
trains = [green_one, green_two, central_one, central_two, ziggy_one, zaggy_one, ziggy_two, zaggy_two]


print("###  ANNOUNCEMENTS  ###")

while running:

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # fill the screen with a color to wipe away anything from last frame
    screen.fill(background_colour)


    # render game

    # render land
    for points in land:
        pygame.draw.polygon(screen, [116, 252, 116], points)

    # render tracks
    for i in range(0, len(tracks)):
        
        track = tracks[i]
        coord_list = []

        for node in track.track_coords:
            x = node.get_track_coords()[0]
            y = node.get_track_coords()[1]

            coord_list.append((x,y))
        
        pygame.draw.lines(screen, track.colour, track.closed, coord_list, track_thickness)

    # render stations
    for station in stations:
        coord = station.get_coords()
        pygame.draw.circle(screen, station_default_colour, (coord[0], coord[1]), station_thickness)
    
    # render signals
    for signal in signals:
        draw_signal(screen, signal)

    # render trains
    for train in trains:

        # only render train if it is still active
        if train.get_active():
            train.travel(0.1)
            coord = train.get_coords()
            pygame.draw.circle(screen, train_default_colour, (coord[0], coord[1]), train_thickness)
        else:
            trains.remove(train)
    

    # check if hover, and render info panel
    hover = False
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for station in stations:
        
        if mouse_hover_over(station, mouse_x, mouse_y, station_thickness):
            hover = True

            # render info panel
            font = pygame.font.SysFont('Comic Sans MS', 30)
            text_surface = font.render(station.get_name() + " Station", False, (0, 0, 0), (255, 255, 255))
            screen.blit(text_surface, (25,25))

            break
    
    if not hover:
        for train in trains:
            if mouse_hover_over(train, mouse_x, mouse_y, train_thickness):
                hover = True

                # render info panel
                font = pygame.font.SysFont('Comic Sans MS', 30)
                text_surface = font.render(train.get_description(), False, (0, 0, 0), (255, 255, 255))
                screen.blit(text_surface, (25,25))

                break
    
    if not hover:
        for signal in signals:
            if mouse_hover_over(signal, mouse_x, mouse_y, signal_thickness):
                hover = True
                automatic = "Manual"

                if signal.get_automatic():
                    automatic = "Automatic"
                

                # render info panel
                font = pygame.font.SysFont('Comic Sans MS', 30)
                
                if isinstance(signal, Approaching_Station_Signal):
                    text_surface = font.render(automatic + " Signal " + signal.get_name() + " (assigned to " + signal.get_assigned_station().get_name() + " Station)", False, (0, 0, 0), (255, 255, 255))
                else:
                    text_surface = font.render("Signal " + signal.get_name(), False, (0, 0, 0), (255, 255, 255))

                
                screen.blit(text_surface, (25,25))

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    signal.toggle()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    signal.toggle_automatic()

                break
    
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        print("clicked point: (" + str(mouse_x) + ", " + str(mouse_y) + ")")

    check_train_collisions(trains, train_thickness)

    # flip() the display to put your work on screen
    pygame.display.flip()


    clock.tick(60)  # limits FPS to 60

pygame.quit()


