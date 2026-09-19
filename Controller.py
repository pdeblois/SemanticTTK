import TTKFile

class Controller:

    def __init__(self, ttk_file: TTKFile.TTKFile):
        self.ttk_file: TTKFile.TTKFile = ttk_file

    # ==========================================
    # NAMED ACTIONS
    # ==========================================

    def accelerate(self, frame_range):
        self.ttk_file.set_inputs_frame_range({'accelerate':1}, frame_range)

    def turn(self, x_value, start_frame, duration):
        self.ttk_file.set_inputs_duration({'h_stick':x_value}, start_frame, duration)

    def wheelie(self, frame):
        self.ttk_file.set_inputs_frame({'dpad':1}, frame)
