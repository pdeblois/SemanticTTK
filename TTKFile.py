import csv

class TTKFile:
    # Define valid ranges for validation
    INPUT_RANGES = {
        'accelerate': (0, 1),
        'brake': (0, 1),
        'item': (0, 1),
        'h_stick': (-7, 7),
        'v_stick': (-7, 7),
        'dpad': (0, 4),
        'drift': (-1, 1)
    }

    NB_INPUTS = len(INPUT_RANGES)

    # Define default values as fallbacks
    INPUT_DEFAULTS = {
        'accelerate': 0,
        'brake': 0,
        'item': 0,
        'h_stick': 0,
        'v_stick': 0,
        'dpad': 0,
        'drift': -1
    }

    def __init__(self, csv_filepath=None):
        self.frames = {}
        if csv_filepath:
            self.load(csv_filepath)

    def _get_frame(self, frame_num):
        """Fetches a frame's values, creating it with defaults if it doesn't exist."""
        frame_index = frame_num - 1
        if frame_index not in self.frames:
            self.frames[frame_index] = self.INPUT_DEFAULTS.copy()
        return self.frames[frame_index]

    def _clamp(self, value, min_val, max_val):
        """Ensures values stay within the gamepad's physical limits."""
        return max(min_val, min(value, max_val))

    # ==========================================
    # LOAD / SAVE
    # ==========================================

    def load(self, csv_filepath):
        """Loads an existing CSV file into memory."""
        with open(csv_filepath, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row_index, row_data in enumerate(csv_reader):
                if len(row_data) == self.NB_INPUTS:
                    self.frames[row_index] = {
                        'accelerate': int(row_data[0]),
                        'brake': int(row_data[1]),
                        'item': int(row_data[2]),
                        'h_stick': int(row_data[3]),
                        'v_stick': int(row_data[4]),
                        'dpad': int(row_data[5]),
                        'drift': int(row_data[6])
                    }
                else:
                    raise ValueError(f"Row {row_index + 1} contained {len(row_data)} values, expected {self.NB_INPUTS}")

    def save(self, filepath, total_frames=None):
        """Exports the data to a CSV file, filling in untouched frames with defaults."""
        if total_frames is None:
            # Output up to the highest modified frame
            total_frames = max(self.frames.keys(), default=-1) + 1

        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            for i in range(total_frames):
                frame = self.frames.get(i, self.INPUT_DEFAULTS)
                writer.writerow([
                    frame['accelerate'],
                    frame['brake'],
                    frame['item'],
                    frame['h_stick'],
                    frame['v_stick'],
                    frame['dpad'],
                    frame['drift']
                ])

    # ==========================================
    # RAW INPUT
    # ==========================================

    def set_inputs_frame(self, inputs, frame_num):
        """
        Directly specify inputs for a single frame.
        Only modifies the keys passed in; leaves other inputs on that frame untouched.
        """
        frame_data = self._get_frame(frame_num)
        for key, value in inputs.items():
            if key in self.INPUT_RANGES:
                min_val, max_val = self.INPUT_RANGES[key]
                frame_data[key] = self._clamp(int(value), min_val, max_val)
            else:
                raise ValueError(f"Unknown input: {key}")
    
    def set_inputs_frame_range(self, inputs, frame_range):
        """
        Directly specify inputs for a range of frames.
        Only modifies the keys passed in; leaves other inputs on that frame untouched.
        """
        for frame in range(frame_range[0], frame_range[1] + 1):
            self.set_inputs_frame(inputs, frame)

    def set_inputs_duration(self, inputs, start_frame, duration):
        """
        Directly specify inputs starting at a frame and lasting for a given duration.
        The start frame is included in the duration.
        Only modifies the keys passed in; leaves other inputs on that frame untouched.
        """
        self.set_inputs_frame_range(inputs, (start_frame, start_frame + duration - 1))
