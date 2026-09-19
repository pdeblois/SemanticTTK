import TTKFile

ttk_file = TTKFile.TTKFile()

ttk_file.accelerate(frame_range=(137,511)) 

ttk_file.turn(start_frame=168, duration=300, direction_value=7)

ttk_file.wheelie(frame=259)

ttk_file.save("C:/Users/Philippe/Documents/MKWii/TAS/pycore.245/x64/User/Load/Scripts/MKW_Inputs/TTK_Player_Inputs_MT.csv")
