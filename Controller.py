import TTKFile

class Controller:

    def __init__(self, ttk_file: TTKFile.TTKFile):
        self.ttk_file: TTKFile.TTKFile = ttk_file
        self.accelerate_start_frame = None
        self.brake_start_frame = None

    # ==========================================
    # NAMED ACTIONS
    # ==========================================

    def accelerate(self, frame_range):
        return self.ttk_file.set_inputs_frame_range({'accelerate':1}, frame_range)

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

    def flush_accelerate(self, max_frame):
        if (self.accelerate_start_frame is not None):
            print(f"Flushing accel : {(self.accelerate_start_frame, max_frame)}")
            self.stop_accelerate(max_frame)
        return max_frame

    def brake(self, frame_range):
        return self.ttk_file.set_inputs_frame_range({'brake':1}, frame_range)
    
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

    def flush_brake(self, max_frame):
        if (self.brake_start_frame is not None):
            self.stop_brake(max_frame)
        return max_frame

    def turn(self, x_value, start_frame, duration):
        return self.ttk_file.set_inputs_duration({'h_stick':x_value}, start_frame, duration)

    def wheelie(self, frame):
        return self.ttk_file.set_inputs_frame({'dpad':1}, frame)

    def wheelie_cancel(self, frame):
        return self.ttk_file.set_inputs_frame({'dpad':2}, frame)

    def hop(self, frame):
        return self.ttk_file.set_inputs_frame({'brake':1}, frame)

    def up_trick(self, frame):
        return self.ttk_file.set_inputs_frame({'dpad':1}, frame)