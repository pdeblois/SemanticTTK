import TTKFile
import Controller

ttk_file = TTKFile.TTKFile()
controller = Controller.Controller(ttk_file=ttk_file)

controller.accelerate(frame_range=(137,511)) 

controller.turn(7, start_frame=168, duration=300)

controller.wheelie(frame=259)

ttk_file.save("C:/Users/Philippe/Documents/MKWii/TAS/pycore.245/x64/User/Load/Scripts/MKW_Inputs/TTK_Player_Inputs_MT.csv")
