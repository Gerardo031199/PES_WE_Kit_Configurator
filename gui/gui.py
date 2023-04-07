import pymem
import webbrowser
from tkinter import (Listbox, StringVar, Tk, messagebox, Menu, Spinbox, IntVar, Button, TclError, filedialog, 
Label, ttk, LabelFrame)
from tkinter.colorchooser import askcolor

from config_kits.team_kit_data import TeamKitData
from .config import Config

class Gui(Tk):
    filename =""
    team_id =""
    def __init__(self):
        super().__init__()
        self.appname='PES Kit Configurator'
        self.version= '1.1.0'
        self.author= 'PES Indie Team'
        self.title(f"{self.appname} {self.version}")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        try:
            self.create_config()
        except FileNotFoundError as e:
            messagebox.showerror(title=self.appname, message=f"No config files found code error {e}")

        # Creating Menubar
        self.menubar = Menu(self)
        self.config(menu = self.menubar)
          
        # Adding File Menu and commands
        self.file = Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label ='File', menu = self.file)
        self.file.add_command(label='Open', command = None, accelerator="Ctrl+O", state='disabled')
        self.file.add_separator()
        self.file.add_command(label='Exit', command = self.on_closing, accelerator="Ctrl+Q")

        self.edit_menu = Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label='Edit', menu = self.edit_menu)

        self.edit_submenu = Menu(self.menubar, tearoff=0)
        self.edit_menu.add_cascade(label="Game Version", menu=self.edit_submenu)

        for i in range(len(self.my_config.games_config)):
            self.edit_submenu.add_radiobutton(label=self.my_config.games_config[i],command= lambda i=i: self.change_config(self.my_config.filelist[i]))

        self.edit_menu.add_separator()     
        self.edit_menu.add_command(label ='Export nations kit config', command= lambda: self.export_kit_config(self.national_kits), state="disabled")
        self.edit_menu.add_command(label ='Export clubs kit config', command= lambda: self.export_kit_config(self.club_kits), state="disabled")

        # Adding Help Menu
        self.help_ = Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label ='Help', menu = self.help_)
        self.help_.add_command(label ='Donate', command = self.donate)
        self.help_.add_command(label ='YouTube', command = self.youtube)
        self.help_.add_separator()
        self.help_.add_command(label ='About', command = self.about)

        self.frame1 = ttk.Frame(self)
        self.frame1.grid(row=0, column=0, rowspan=2, padx=5, pady=5)

        self.kit_combox = ttk.Combobox(self.frame1, state="disabled", values=["GA","PA","GB","PB"], )
        self.kit_combox.bind("<<ComboboxSelected>>", lambda event: self.set_kit_info(self.lbox_teams.get(0, "end").index(self.lbox_teams.get(self.lbox_teams.curselection()))))
        self.kit_combox.current(0)
        self.kit_combox.grid(row=0, column=0, sticky="NWE")  
        
        self.lbox_teams = Listbox(self.frame1, exportselection=False, width=25, height=25)#selectmode="SINGLE"
        self.lbox_teams.grid(row=1, column=0, pady=5, sticky="NWE")

        self.scrollbar = ttk.Scrollbar(self.frame1, orient="vertical", command=self.lbox_teams.yview)
        self.scrollbar.grid(row=1, column=1, pady=5, sticky="NS")
        self.lbox_teams.config(yscrollcommand=self.scrollbar.set)

        frame_01 = LabelFrame(self, text="Menu")
        frame_01.grid(column=1, row=0, padx=5, pady=5, sticky="NWE")

        Label(frame_01, text="Option").grid(column=1, row=0, padx=5, pady=5, sticky="N")

        Label(frame_01, text="Size").grid(column=2, row=0, padx=5, pady=5, sticky="N")

        Label(frame_01, text="X").grid(column=3, row=0, padx=5, pady=5, sticky="N")

        Label(frame_01, text="Y").grid(column=4, row=0, padx=5, pady=5, sticky="N")

        Label(frame_01, text="Type").grid(column=5, row=0, padx=5, pady=5, sticky="N")

        Label(frame_01, text="Shirt Font").grid(column=0, row=1, padx=5, pady=5,  sticky="WE")
        
        self.font_shirt_status = ttk.Combobox(frame_01, values=["Off","On"],width=5,state="readonly")
        self.font_shirt_status.bind("<<ComboboxSelected>>",  lambda event: self.update_kit_info())
        self.font_shirt_status.grid(column=1, row=1, padx=10, pady=5, sticky="W")
        
        self.font_spb_size_var = IntVar()
        self.font_spb_size_var.set(0)

        self.font_spb_size = Spinbox(frame_01,textvariable=self.font_spb_size_var, from_=0, to=30, command=self.update_kit_info, width=5)
        self.font_spb_size.bind('<Return>', lambda event: self.update_kit_info())
        self.font_spb_size.grid(column=2, row=1, padx=10, pady=5, sticky="W")
        
        self.y_position_font_shirt_var = IntVar()
        self.y_position_font_shirt_var.set(0)

        self.y_position_font_shirt = Spinbox(frame_01, textvariable=self.y_position_font_shirt_var, from_=0, to=29,  command=self.update_kit_info, width=5)
        self.y_position_font_shirt.bind('<Return>', lambda event: self.update_kit_info())
        self.y_position_font_shirt.grid(column=4, row=1, padx=10, pady=5, sticky="W")

        self.font_curve_type = ttk.Combobox(frame_01, values=["Linear","Light","Medium","Maximum"],width=7,state="readonly")
        self.font_curve_type.bind("<<ComboboxSelected>>",  lambda event: self.update_kit_info())
        self.font_curve_type.grid(column=5, row=1, padx=10, pady=5, sticky="W")

        Label(frame_01, text="Front Number").grid(column=0, row=2, padx=5, pady=5, sticky="WE")

        self.front_number_status = ttk.Combobox(frame_01, values=["Off","On"],width=5,state="readonly")
        self.front_number_status.bind("<<ComboboxSelected>>",  lambda event: self.update_kit_info())
        self.front_number_status.grid(column=1, row=2, padx=10, pady=5, sticky="W")

        self.front_number_size_var = IntVar()
        self.front_number_size_var.set(0)

        self.front_number_size = Spinbox(frame_01, textvariable=self.front_number_size_var,  from_=0, to=22,command=self.update_kit_info, width=5)
        self.front_number_size.bind('<Return>', lambda event: self.update_kit_info())
        self.front_number_size.grid(column=2, row=2, padx=10, pady=5, sticky="W")

        self.x_position_front_number_var = IntVar()
        self.x_position_front_number_var.set(0)

        self.x_position_front_number = Spinbox(frame_01, textvariable=self.x_position_front_number_var, from_=0, to=29, command=self.update_kit_info, width=5)
        self.x_position_front_number.bind('<Return>', lambda event: self.update_kit_info())
        self.x_position_front_number.grid(column=3, row=2, padx=10, pady=5, sticky="W")

        self.y_position_front_number_var = IntVar()
        self.y_position_front_number_var.set(0)

        self.y_position_front_number = Spinbox(frame_01, textvariable=self.y_position_front_number_var, from_=0, to=29,  command=self.update_kit_info, width=5)
        self.y_position_front_number.bind('<Return>', lambda event: self.update_kit_info())
        self.y_position_front_number.grid(column=4, row=2, padx=10, pady=5, sticky="W")

        Label(frame_01, text="Back Number").grid(column=0, row=3, padx=5, pady=5, sticky="WE")

        self.back_number_size_var = IntVar()
        self.back_number_size_var.set(0)

        self.back_number_size = Spinbox(frame_01, textvariable=self.back_number_size_var, from_=0, to=31,  command=self.update_kit_info, width=5)
        self.back_number_size.bind('<Return>', lambda event: self.update_kit_info())
        self.back_number_size.grid(column=2, row=3, padx=10, pady=5, sticky="W")

        self.y_position_number_back_var = IntVar()
        self.y_position_number_back_var.set(0)

        self.y_posc_num_back_spb = Spinbox(frame_01, textvariable=self.y_position_number_back_var, from_=0, to=18,  command=self.update_kit_info, width=5)
        self.y_posc_num_back_spb.bind('<Return>', lambda event: self.update_kit_info())
        self.y_posc_num_back_spb.grid(column=4, row=3, padx=10, pady=5, sticky="W")

        Label(frame_01, text="Short Number").grid(column=0, row=4, padx=5, pady=5, sticky="WE")

        self.shorts_number_status = ttk.Combobox(frame_01, values=["Off","Left","Right"],width=5,state="readonly")
        self.shorts_number_status.bind("<<ComboboxSelected>>",  lambda event: self.update_kit_info())
        self.shorts_number_status.grid(column=1, row=4, padx=10, pady=5, sticky="W")

        self.short_number_size_var = IntVar()
        self.short_number_size_var.set(0)

        self.short_number_size = Spinbox(frame_01, textvariable=self.short_number_size_var, from_=0, to=28,  command=self.update_kit_info, width=5)
        self.short_number_size.bind('<Return>', lambda event: self.update_kit_info())
        self.short_number_size.grid(column=2, row=4, padx=10, pady=5, sticky="W")

        self.x_position_shorts_number_var = IntVar()
        self.x_position_shorts_number_var.set(0)

        self.x_position_shorts_number = Spinbox(frame_01, textvariable=self.x_position_shorts_number_var, from_=0, to=25,  command=self.update_kit_info, width=5)
        self.x_position_shorts_number.bind('<Return>', lambda event: self.update_kit_info())
        self.x_position_shorts_number.grid(column=3, row=4, padx=10, pady=5, sticky="W")

        self.y_position_shorts_number_var = IntVar()
        self.y_position_shorts_number_var.set(0)

        self.y_position_shorts_number = Spinbox(frame_01, textvariable=self.y_position_shorts_number_var, from_=0, to=19,  command=self.update_kit_info, width=5)
        self.y_position_shorts_number.bind('<Return>', lambda event: self.update_kit_info())
        self.y_position_shorts_number.grid(column=4, row=4, padx=10, pady=5, sticky="W")
        
        Label(frame_01, text="Overlay").grid(column=0, row=5, padx=5, pady=5, sticky="WE")

        self.overlay_type_var = IntVar()
        self.overlay_type_var.set(0)

        self.overlay_type = Spinbox(frame_01, textvariable=self.overlay_type_var, from_=0, to=14,  command=self.update_kit_info, width=5)
        self.overlay_type.bind('<Return>', lambda event: self.update_kit_info())
        self.overlay_type.grid(column=1, row=5, padx=10, pady=5, sticky="W")

        self.y_position_long_sleeve_overlay_var = IntVar() #y_position_long_sleeve_overlay_var
        self.y_position_long_sleeve_overlay_var.set(0)
        
        Label(frame_01, text="Long sleeve overlay").grid(column=0, row=6, padx=5, pady=5, sticky="WE")
        self.y_position_long_sleeve_overlay = Spinbox(frame_01, textvariable=self.y_position_long_sleeve_overlay_var, from_=0, to=10,  command=self.update_kit_info, width=5)
        self.y_position_long_sleeve_overlay.bind('<Return>', lambda event: self.update_kit_info())
        self.y_position_long_sleeve_overlay.grid(column=4, row=6, padx=10, pady=5, sticky="W")
      
        self.y_position_short_sleeve_overlay_var = IntVar()
        self.y_position_short_sleeve_overlay_var.set(0)
        
        Label(frame_01, text="Short sleeve overlay").grid(column=0, row=7, padx=5, pady=5, sticky="WE")
        self.y_position_short_sleeve_overlay = Spinbox(frame_01, textvariable=self.y_position_short_sleeve_overlay_var, from_=0, to=10,  command=self.update_kit_info, width=5)
        self.y_position_short_sleeve_overlay.bind('<Return>', lambda event: self.update_kit_info())
        self.y_position_short_sleeve_overlay.grid(column=4, row=7, padx=10, pady=5, sticky="W")
        
        Label(frame_01, text="Model").grid(column=0, row=8, padx=5, pady=5, sticky="WE")
        self.model_type_var = IntVar()
        self.model_type_var.set(0)

        self.model_type = Spinbox(frame_01, textvariable=self.model_type_var, from_=0, to=154, command=self.update_kit_info, width=5)
        self.model_type.bind('<Return>', lambda event: self.update_kit_info())
        self.model_type.grid(column=1, row=8, padx=10, pady=5, sticky="W")

        Label(frame_01, text="License").grid(column=0, row=9, padx=5, pady=5, sticky="WE")
    
        self.license_type = ttk.Combobox(frame_01, values=["NL","LC"],width=5,state="readonly")
        self.license_type.bind('<<ComboboxSelected>>',  lambda event: self.update_kit_info())
        self.license_type.grid(column=1, row=9, padx=9, pady=5, sticky="W")

        Label(frame_01, text="Radar Color").grid(column=0, row=10, padx=5, pady=5, sticky="WE")
        
        self.colors_rgb_int_var = StringVar()

        self.btn_radar = Button(frame_01,width=7, textvariable=self.colors_rgb_int_var, command=self.select_color)
        self.btn_radar.grid(column=1, row=10, padx=10, pady=5, sticky="W")

        frame_02 = LabelFrame(self, text="Macro for all teams")
        frame_02.grid(column=1, row=1, padx=5, pady=5, sticky="W")

        Label(frame_02, text="Model:").grid(column=0, row=0, padx=1, pady=5, sticky="W")

        self.model_combox = ttk.Combobox(frame_02, values=[x for x in range(155)], width=5, state="readonly")
        self.model_combox.grid(column=1, row=0, padx=9, pady=5, sticky="W")
        self.model_combox.set(0)

        btn = ttk.Button(frame_02, text="Apply", command=lambda : self.set_model_to_all_team(self.model_combox.current()))
        btn.grid(column=2, row=0, padx=9, pady=5)

        Label(frame_02, text="License:").grid(column=3, row=0, padx=1, pady=5, sticky="W")

        license_btn = ttk.Button(frame_02, text="Licensed", command=lambda : self.set_license_to_all_team("LC"))
        license_btn.grid(column=4, row=0, padx=10, pady=5)

        unlicense_btn = ttk.Button(frame_02, text="Unlicensed", command=lambda : self.set_license_to_all_team("NL"))
        unlicense_btn.grid(column=5, row=0, padx=10, pady=5)
        
    def scroll_to_match(self, event):
        valor = event.keysym
        indice = self.lbox_teams.curselection()
        if indice:
            indice = int(indice[0])
        else:
            indice = 0
        encontrado = False
        if valor.isalnum():
            for i in range(indice, self.lbox_teams.size()):
                if valor.lower() in self.lbox_teams.get(i).lower():
                    self.lbox_teams.see(i)
                    self.lbox_teams.selection_clear(0, "end")
                    self.lbox_teams.selection_set(i)
                    encontrado = True
                    break
            if not encontrado:
                for i in range(indice, -1, -1):
                    if valor.lower() in self.lbox_teams.get(i).lower():
                        self.lbox_teams.see(i)
                        self.lbox_teams.selection_clear(0, "end")
                        self.lbox_teams.selection_set(i)
                        encontrado = True
                        break

        
    def create_config(self):
        self.my_config = Config()
    
    def change_config(self, file):
        self.my_config.load_config(file)
        self.refresh_gui()

    def refresh_gui(self):
        self.lbox_teams.delete(0,'end')
        self.run_program()
        self.title(f'{self.appname} {self.version} - {self.my_config.file["Gui"]["Game Name"]}')

    def run_program(self):
        try:
            self.nation_start_address = self.my_config.game_data['Nation Start Address']
            self.national_kit_length = self.my_config.game_data['National Kit Length']
            self.total_national = self.my_config.game_data['Total National']
            self.clubes_kit_length = self.my_config.game_data['Clubes Kit Length']
            self.total_clubes = self.my_config.game_data['Total Clubes']
            self.total_teams = self.total_national + self.total_clubes
            
            self.process_name = self.my_config.settings['Process Name']
            self.filename = self.process_name
            
            teams_table_offset = self.my_config.game_data['Teams Table Offset']
            teams_table_size = self.total_teams * 16 

            teams_text_data_offset = self.my_config.game_data['Teams Text Data Offset']
            
            self.memory = pymem.Pymem(self.process_name)
            self.club_start_address = self.nation_start_address + (self.total_national* self.national_kit_length)
            
            teams_table = self.memory.read_bytes(teams_table_offset, teams_table_size)
                        
            int_list_full_name = []
            int_list_abb_name = []
            for j in range(0, len(teams_table), 16):
                first_half_bytes = teams_table[j : j + 4]
                first_int = int.from_bytes(first_half_bytes, byteorder='little')
                
                second_half_bytes = teams_table[j + 4 : j + 8]
                second_int = int.from_bytes(second_half_bytes, byteorder='little')
                
                int_list_full_name.append(first_int)
                int_list_abb_name.append(second_int)

            teams_text_data = self.memory.read_bytes(teams_text_data_offset, int_list_abb_name[-1] - int_list_full_name[0])

            self.national_kits = [TeamKitData(bytearray(self.memory.read_bytes(self.nation_start_address + (i *self.national_kit_length),self.national_kit_length))) for i in range(self.total_national)]
            self.club_kits = [TeamKitData(bytearray(self.memory.read_bytes(self.club_start_address + (i *self.clubes_kit_length),self.clubes_kit_length))) for i in range(self.total_clubes)]
            
            list_teams = []
            for i in range(0, len(int_list_full_name), 1):
                start_range = int_list_full_name[i] - int_list_full_name[0]

                j = start_range
                while j < len(teams_text_data):
                    if teams_text_data[j:j+1] == bytearray([0x00]):
                        end_range = j
                        break
                    j += 1
                
                sub_bytearray = teams_text_data[start_range:end_range].decode('utf-8')
                list_teams.append(sub_bytearray)
            
            self.lbox_teams.insert('end', *list_teams)
            self.lbox_teams.selectedindex = 0
            self.lbox_teams.select_set(0)
            self.lbox_teams.bind("<<ListboxSelect>>", lambda event: self.set_team_kit_info())

            self.kit_combox.configure(state='readonly')

            self.edit_menu.entryconfig('Export nations kit config', state="normal")
            self.edit_menu.entryconfig('Export clubs kit config', state="normal")

        except pymem.exception.MemoryReadError as e:
            messagebox.showerror(title=self.appname, message=f"pymem error code {e}")
            return 0

    def export_kit_config(self, bytes_list):
        if self.filename=="":
            messagebox.showerror(title=self.appname, message="You must first run the game before attempting to read or set any data")
            return 0

        file = filedialog.asksaveasfile(mode='wb', title = "Save file as", initialfile="", defaultextension=".bin" , filetypes=(("bin files","*.bin"),("all files","*.*")))
        if file:
            for item in bytes_list:
                file.write(item.data)
            messagebox.showinfo(title=self.appname, message="The kit configuration file has been exported")
        return 0
    
    def set_model_to_all_team(self, new_model):
        if self.filename=="":
            messagebox.showerror(title=self.appname, message="You must first run the game before attempting to read or set any data")
            return 0
        
        answer = messagebox.askyesno(title=self.appname,message=f"Are you sure you to assign the model number {new_model} to all teams?")
        
        if answer:
            for x in range(len(self.national_kits)):
                self.national_kits[x].GA.update_model_type(new_model)
                self.national_kits[x].PA.update_model_type(new_model)
                self.national_kits[x].GB.update_model_type(new_model)
                self.national_kits[x].PB.update_model_type(new_model)
                self.national_kits[x].update_data()
                self.memory.write_bytes(self.nation_start_address + (x * self.national_kit_length), bytes(self.national_kits[x].data), self.national_kit_length)

            for x in range(len(self.club_kits)):
                self.club_kits[x].GA.update_model_type(new_model)
                self.club_kits[x].PA.update_model_type(new_model)
                self.club_kits[x].GB.update_model_type(new_model)
                self.club_kits[x].PB.update_model_type(new_model)

                self.club_kits[x].update_data()
                self.memory.write_bytes(self.club_start_address + (x * self.clubes_kit_length), bytes(self.club_kits[x].data), self.clubes_kit_length)

            messagebox.showinfo(title=self.appname,message=f"Model {new_model} set to all teams")
        else:
            return 0

    def set_license_to_all_team(self, new_value):
        if self.filename=="":
            messagebox.showerror(title=self.appname, message="You must first run the game before attempting to read or set any data")
            return 0
        
        answer = messagebox.askyesno(title=self.appname,message=f"Are you sure you to assign the license to {new_value} in all teams?")
        
        if answer:
            for x in range(len(self.national_kits)):
                self.national_kits[x].GA.update_license(new_value)
                self.national_kits[x].PA.update_license(new_value)
                self.national_kits[x].GB.update_license(new_value)
                self.national_kits[x].PB.update_license(new_value)
                self.national_kits[x].update_data()
                self.memory.write_bytes(self.nation_start_address + (x * self.national_kit_length), bytes(self.national_kits[x].data), self.national_kit_length)

            for x in range(len(self.club_kits)):
                self.club_kits[x].GA.update_license(new_value)
                self.club_kits[x].PA.update_license(new_value)
                self.club_kits[x].GB.update_license(new_value)
                self.club_kits[x].PB.update_license(new_value)

                self.club_kits[x].update_data()
                self.memory.write_bytes(self.club_start_address + (x * self.clubes_kit_length), bytes(self.club_kits[x].data), self.clubes_kit_length)
            
            messagebox.showinfo(title=self.appname,message=f"License set to {new_value} in all teams")
        else:
            return 0
    
    def select_color(self):
        if self.filename=="" or self.team_id=="":
            messagebox.showerror(title=self.appname, message="You must first run the game before attempting to read or set any data")
            return 0

        colors = askcolor(title="Select a color", initialcolor=self.colors_rgb_int_var.get())
        if colors[0] is not None :
            self.colors_rgb_int_var.set(colors[1])

            self.btn_radar.configure(bg=colors[1])

            self.update_kit_info()
        else:
            return 0

    def set_team_kit_info(self):
            self.team_id = self.lbox_teams.get(0, "end").index(self.lbox_teams.get(self.lbox_teams.curselection()))
            
            #self.kit_combox.current(0)            
            self.set_kit_info(self.team_id)

    def set_kit_info(self, team_id:int):
        if 0 <= team_id < self.total_national:
            kit_list = self.national_kits
        
        elif self.total_national <= team_id < self.total_teams:
            team_id -= self.total_national
            kit_list = self.club_kits


        kit_type = self.kit_combox.current()
        if kit_type == 0:
            variable = kit_list[team_id].GA
            
        elif kit_type == 1:
            variable = kit_list[team_id].PA

        elif kit_type == 2:
            variable = kit_list[team_id].GB

        elif kit_type == 3:
            variable = kit_list[team_id].PB

        self.license_type.current(variable.license_type)
        self.model_type_var.set(variable.model_type)

        self.font_shirt_status.current(variable.font_shirt_status)
        self.y_position_font_shirt_var.set(variable.y_position_font_shirt)
        
        self.front_number_status.current(variable.front_number_status)

        self.shorts_number_status.current(variable.shorts_number_status)
        self.overlay_type_var.set(variable.overlay_type)
        
        self.y_position_long_sleeve_overlay_var.set(variable.y_position_long_sleeve_overlay)
        
        self.y_position_short_sleeve_overlay_var.set(variable.y_position_short_sleeve_overlay)
        
        self.font_curve_type.current(variable.font_curve_type)
        self.font_spb_size_var.set(variable.font_size)
        
        self.back_number_size_var.set(variable.number_size_back)

        self.short_number_size_var.set(variable.shorts_number_size)
        self.front_number_size_var.set(variable.front_number_size)
        self.y_position_number_back_var.set(variable.y_position_back_number)
        self.x_position_front_number_var.set(variable.x_position_front_number)
        self.y_position_front_number_var.set(variable.y_position_front_number)
        
        self.x_position_shorts_number_var.set(variable.x_position_shorts_number)
        self.y_position_shorts_number_var.set(variable.y_position_shorts_number)
        
        self.btn_radar.configure(bg=variable.rgb_hex)
        self.colors_rgb_int_var.set(variable.rgb_hex.upper())

    def update_kit_info(self):
        if self.filename=="":
            messagebox.showerror(title=self.appname, message="You must first run the game before attempting to read or set any data")
            return 0

        elif self.team_id=="":
            messagebox.showerror(title=self.appname, message="You must first select a team from the list box")
            return 0
        try:
            team_id:int = self.lbox_teams.get(0, "end").index(self.lbox_teams.get(self.lbox_teams.curselection()))
            
            if 0 <= team_id < self.total_national:
                kit_list = self.national_kits
                kit_length = self.national_kit_length
                address_initial = self.nation_start_address
            elif self.total_national <= team_id < self.total_teams:
                team_id -= self.total_national
                kit_list = self.club_kits
                kit_length = self.clubes_kit_length
                address_initial = self.club_start_address
            kit_type = self.kit_combox.current()
            
            if kit_type == 0:
                variable = kit_list[team_id].GA

            elif kit_type == 1:
                variable = kit_list[team_id].PA

            elif kit_type == 2:
                variable = kit_list[team_id].GB
                
            elif kit_type == 3:
                variable = kit_list[team_id].PB

            variable.update_model_type(self.model_type_var.get())
            variable.update_license(self.license_type.get())
            variable.update_font_shirt(self.font_shirt_status.current())
            variable.update_y_position_font_shirt(self.y_position_font_shirt_var.get())
            variable.update_front_number(self.front_number_status.current())
            variable.update_shorts_number(self.shorts_number_status.current())
            variable.update_overlay_type(self.overlay_type_var.get())
            
            variable.update_y_position_long_sleeve_overlay(self.y_position_long_sleeve_overlay_var.get())
            variable.update_y_position_short_sleeve_overlay(self.y_position_short_sleeve_overlay_var.get())
            
            variable.update_font_curve(self.font_curve_type.current())
            variable.update_font_size(self.font_spb_size_var.get())
            variable.update_number_size_back(self.back_number_size_var.get())
            variable.update_shorts_number_size(self.short_number_size_var.get())
            variable.update_front_number_size(self.front_number_size_var.get())
            variable.update_y_position_back_number(self.y_position_number_back_var.get())
            variable.update_x_position_front_number(self.x_position_front_number_var.get())
            variable.update_y_position_front_number(self.y_position_front_number_var.get())
            variable.update_x_position_shorts_number(self.x_position_shorts_number_var.get())
            variable.update_y_position_shorts_number(self.y_position_shorts_number_var.get())
            
            variable.update_color_radar(self.colors_rgb_int_var.get())
            self.btn_radar.configure(bg=self.colors_rgb_int_var.get())
        
            kit_list[team_id].update_data()
            self.memory.write_bytes(address_initial + (team_id * kit_length), bytes(kit_list[team_id].data), kit_length)

        except (TclError, ValueError) as e:
            messagebox.showerror(title=self.appname, message=e)

    def youtube(self):     
        webbrowser.open_new('https://www.youtube.com/channel/UCzHGN5DBIXVviZQypFH_ieg')
        
    def about(self):
        messagebox.showinfo(f'{self.appname} {self.version}', f'Developed by {self.author}')

    def donate(self):     
        webbrowser.open_new('https://www.paypal.com/paypalme/gerardocj11')
        
    def on_closing(self):
        if messagebox.askokcancel("Exit", "Do you want to exit the program?"):
            self.destroy()

    def start(self):
        self.bind("<KeyPress>", self.scroll_to_match)
        self.mainloop()