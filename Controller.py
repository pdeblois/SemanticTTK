from collections import namedtuple

import TTKFile

TimedStickPos = namedtuple("TimedStickPos", ["stick_pos", "start_frame"])

class Controller:
    '''
    Emulates a physical controller, with additional helper methods.
    Implements checks that ensure chronological and logical self-consistency
    of the requested inputs (e.g. if you ask to stop accelerating, it will
    first check if you were already accelerating).
    '''
    def __init__(self, ttk_file: TTKFile.TTKFile):
        self.ttk_file: TTKFile.TTKFile = ttk_file
        self.accelerate_start_frame = None
        self.brake_start_frame = None
        self.rapid_fire_hop_start_frame = None
        self.stick_x_prev = TimedStickPos(stick_pos=0,start_frame=0)
        self.stick_y_prev = TimedStickPos(stick_pos=0,start_frame=0)

    # ==========================================
    # NAMED ACTIONS
    # ==========================================

    def flush(self, last_frame):
        if (self.accelerate_start_frame is not None):
            print(f"Flushing accel : {(self.accelerate_start_frame, last_frame)}")
            self.stop_accelerate(last_frame)
        if (self.brake_start_frame is not None):
            print(f"Flushing brake : {(self.brake_start_frame, last_frame)}")
            self.stop_brake(last_frame)
        #self.move_stick_xy(self.stick_x_prev.stick_pos, self.stick_y_prev.stick_pos, last_frame)
        return last_frame

    def accelerate(self, frame_range):
        self.start_accelerate(frame_range[0])
        return self.stop_accelerate(frame_range[1])

    def start_accelerate(self, frame):
        if (self.accelerate_start_frame is not None):
            raise ValueError("Accelerate is already ongoing, tried to start it again before stopping it.")
        self.accelerate_start_frame = frame
        return frame

    def stop_accelerate(self, frame):
        if (self.accelerate_start_frame is None):
            raise ValueError("Tried to stop accelerate before starting it.")
        last_accelerate_frame = frame - 1
        if (last_accelerate_frame < self.accelerate_start_frame):
            raise ValueError("Tried to stop accelerate earlier or at the same time than its start.")
        self.ttk_file.set_inputs_frame_range({'accelerate':1}, (self.accelerate_start_frame, last_accelerate_frame))
        self.accelerate_start_frame = None
        return frame

    def brake(self, frame_range):
        self.start_brake(frame_range[0])
        return self.stop_brake(frame_range[1])
    
    def start_brake(self, frame):
        if (self.brake_start_frame is not None):
            raise ValueError("Brake is already ongoing, tried to start it again before stopping it.")
        self.brake_start_frame = frame
        return frame

    def stop_brake(self, frame):
        if (self.brake_start_frame is None):
            raise ValueError("Tried to stop brake before starting it.")
        last_brake_frame = frame - 1
        if (last_brake_frame < self.brake_start_frame):
            raise ValueError("Tried to stop brake earlier or at the same time than its start.")
        self.ttk_file.set_inputs_frame_range({'brake':1}, (self.brake_start_frame, last_brake_frame))
        self.brake_start_frame = None
        return frame

    def turn(self, x_value, start_frame, duration):
        return self.ttk_file.set_inputs_duration({'h_stick':x_value}, start_frame, duration)

    def pitch(self, y_value, start_frame, duration):
        return self.ttk_file.set_inputs_duration({'v_stick':y_value}, start_frame, duration)

    def move_stick_x(self, x_value, frame):
        if (frame <= self.stick_x_prev.start_frame):
            raise ValueError("Tried to move stick X at an earlier point in time than a previous move.")
        if (self.stick_x_prev.start_frame > 0):
            # Write values for the previous stick position since we now know its ending frame
            # No need to write the dummy initial stick pos hence the if check
            frame_range = (self.stick_x_prev.start_frame, frame - 1)
            self.ttk_file.set_inputs_frame_range({'h_stick':self.stick_x_prev.stick_pos}, frame_range)
        self.stick_x_prev = TimedStickPos(stick_pos=x_value, start_frame=frame)
        return frame

    def reset_stick_x(self, frame):
        return self.move_stick_x(0, frame)

    def move_stick_y(self, y_value, frame):
        if (frame <= self.stick_y_prev.start_frame):
            raise ValueError("Tried to move stick Y at an earlier point in time than a previous move.")
        if (self.stick_y_prev.start_frame > 0):
            # Write values for the previous stick position since we now know its ending frame
            # No need to write the dummy initial stick pos hence the if check
            frame_range = (self.stick_y_prev.start_frame, frame - 1)
            self.ttk_file.set_inputs_frame_range({'v_stick':self.stick_y_prev.stick_pos}, frame_range)
        self.stick_y_prev = TimedStickPos(stick_pos=y_value, start_frame=frame)
        return frame

    def reset_stick_y(self, frame):
        return self.move_stick_y(0, frame)

    def move_stick_xy(self, x_value, y_value, frame):
        self.move_stick_x(x_value, frame)
        self.move_stick_y(y_value, frame)
        return frame

    def wheelie(self, frame):
        return self.ttk_file.set_inputs_frame({'dpad':1}, frame)

    def wheelie_cancel(self, frame):
        return self.ttk_file.set_inputs_frame({'dpad':2}, frame)

    def hop(self, frame):
        if (self.brake_start_frame is not None):
            raise ValueError("Tried to hop while brake is already ongoing.")
        return self.ttk_file.set_inputs_frame({'brake':1}, frame)

    def up_trick(self, frame):
        return self.ttk_file.set_inputs_frame({'dpad':1}, frame)

    def down_trick(self, frame):
        return self.ttk_file.set_inputs_frame({'dpad':2}, frame)

    def left_trick(self, frame):
        return self.ttk_file.set_inputs_frame({'dpad':3}, frame)

    def right_trick(self, frame):
        return self.ttk_file.set_inputs_frame({'dpad':4}, frame)