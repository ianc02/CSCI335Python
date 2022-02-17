def calibrate(state, satellite, instrument, destination):
    if (instrument, satellite) in state.on_board and (instrument, destination) in state.calibration_target and (satellite, destination) in state.pointing and instrument in state.power_on:
        state.calibrated.add(instrument)
        return state


def switch_off(state, instrument, satellite):
    if (instrument, satellite) in state.on_board and instrument in state.power_on:
        state.power_on.discard(instrument)
        state.power_avail.add(satellite)
        return state


def switch_on(state, instrument, satellite):
    if (instrument, satellite) in state.on_board and satellite in state.power_avail:
        state.power_on.add(instrument)
        state.calibrated.discard(instrument)
        state.power_avail.discard(satellite)
        return state


def take_image(state, satellite, destination, instrument, imageType):
    if instrument in state.calibrated and (instrument, satellite) in state.on_board and (instrument, imageType) in state.supports and instrument in state.power_on and (satellite, destination) in state.pointing and instrument in state.power_on:
        state.have_image.add((destination, imageType))
        return state


def turn_to(state, satellite, d_new, d_prev):
    if (satellite, d_prev) in state.pointing and d_new != d_prev:
        state.pointing.add((satellite, d_new))
        state.pointing.discard((satellite, d_prev))
        return state


