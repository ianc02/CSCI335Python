from satellite import *
from pyhop_anytime import *

# To install pyhop_anytime: pip3 install git+https://github.com/gjf2a/pyhop_anytime


# Every pyhop planner should have a method named start which sets up the initial task list from the goals
def start(state, goals):
    try:
        a = goals.pointing
    except:
        differentPointing = []
    else:
        differentPointing = list(set(goals.pointing).difference(set(state.pointing)))
    neededPictures = list(set(goals.have_image).difference(set(state.have_image)))
    if (len(differentPointing) == 0) and (len(neededPictures) == 0):
        return TaskList(completed=True)
    else:
        return TaskList([('find', differentPointing, neededPictures, goals), ('start', goals)])


def find(state, differentPointing, neededPictures, goals):
    ## YOUR CODE HERE ##
    if (len(neededPictures) >0):
        event, type = neededPictures[0]
        for supporter in state.supports:
            instrument, imagetype = supporter
            if type == imagetype:
                for instrumentAndSatellite in state.on_board:
                    sat_instrument, satellite = instrumentAndSatellite
                    if instrument == sat_instrument:
                        if instrument not in state.power_on:
                            return TaskList([('turn_on', instrument, satellite)])
                        if instrument not in state.calibrated:
                            return TaskList([('calibrate_helper', satellite, instrument, event)])
                        if event == get_pointing_at(state, satellite):
                            return TaskList([('take_image', satellite, event, instrument, type)])
                        else:
                            return TaskList([('turn_to', satellite, event, get_pointing_at(state,satellite)), ('take_image', satellite, event, instrument, type)])
    if (len(differentPointing) > 0):
        satellite, event = differentPointing[0]
        return TaskList([('turn_to', satellite, event, get_pointing_at(state, satellite))])

def turn_on(state, instrument, satellite):
    if satellite in state.power_avail:
        return TaskList([('switch_on', instrument, satellite)])
    else:
        for ins in state.power_on:
            if (ins, satellite) in state.on_board:
                return TaskList([('switch_off', ins, satellite), ('switch_on', instrument, satellite)])


def calibrate_helper(state,satellite, instrument, event):
        previous = None
        new = None
        previous = get_pointing_at(state, satellite)
        new = get_calibrator(state, instrument)
        if previous != new:
            return TaskList([('turn_to', satellite, new, previous), ('calibrate', satellite, instrument, new)])
        else:
            return TaskList([('calibrate', satellite, instrument, new)])

def get_pointing_at(state, satellite):
    for p in state.pointing:
        sat, thing = p
        if sat == satellite:
            return thing
def get_calibrator(state, instrument):
    for target in state.calibration_target:
        ins, loc = target
        if ins == instrument:
            return loc



## WRITE ADDITIONAL METHODS HERE ##

def make_satellite_planner():
    planner = Planner()
    planner.declare_operators(calibrate, switch_off, switch_on, take_image, turn_to)
    planner.declare_methods(start, find, turn_on, calibrate_helper)  # Include all other methods you write as parameters
    return planner


if __name__ == '__main__':
    anyhop_main(make_satellite_planner())
