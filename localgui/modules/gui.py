import tkinter as tk
from tkinter import ttk
from modules.filepaths import *
from modules.servers import *

server_process = None

def main():
    #Master window
    root = tk.Tk()
    root.title('LocalGUI')

    ttk.Style().configure('button1.TButton', highlightbackground="white", foreground='black', background='#ffba0a')

    #Master window basic grid
    root.grid_columnconfigure(0, weight=1) 
    root.grid_columnconfigure(1, weight=1) 
    root.grid_columnconfigure(2, weight=1)
    root.grid_columnconfigure(3, weight=1)
    root.grid_rowconfigure(0, weight=2)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)

    frame1 = tk.Frame(root,  bg="white")
    frame2 = tk.Frame(root,  bg="white")
    frame3 = tk.Frame(root,  bg="white")
    frame4 = tk.Frame(root,  bg="white")

    frame1.grid(row=0, column=0, rowspan=4, padx=10, pady=10, sticky="nwes")
    frame2.grid(row=0, column=1, columnspan=2, rowspan=1, padx=10, pady=10, ipadx=20, ipady=20, sticky="nwse")
    frame3.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="wes")
    frame4.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="wes")

    #Widgets
    header_label = tk.Label(frame1, text="LocalGUI", font=('Helvetica', 30, 'bold'), bd=1, fg="black", bg="#ffba0a")
    header_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", ipady=10)

    file_listbox = tk.Listbox(frame1)
    file_listbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")  # Sijoitetaan myös gridillä

    file_name = tk.Label(frame2, fg="black", bg="white", text="", font=('Helvetica', 30, 'bold',), justify='left', anchor="w")
    file_path = tk.Label(frame2, fg="black", bg="white", text="", font=('Helvetica', 10), justify='left', anchor="w")
    file_desc = tk.Label(frame2, fg="black", bg="white", text="", font=('Helvetica', 15), justify='left', anchor="w")
    file_name.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")  # Sijoitetaan myös gridillä
    file_path.grid(row=1, column=1, columnspan=2, padx=10,  sticky="nsew")
    file_desc.grid(row=2, column=1, columnspan=2, padx=10, pady=10,  sticky="nsew")
    
    add_path_button = ttk.Button(frame1, style="button1.TButton", text="LISÄÄ KANSIO", command=lambda: browse_and_add_path(file_listbox))
    add_path_button.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    launch_server_button = tk.Button(frame3, highlightbackground='white', text="Käynnistä palvelin", command=lambda: run_npm_dev(file_path, delete_path_button))
    launch_server_button.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    delete_path_button = tk.Button(frame3, highlightbackground='white', text="Poista kansio", command=lambda:remove_selected_path(file_listbox, file_name, file_path))
    delete_path_button.grid(row=2, column=3, padx=10, pady=10, sticky="w")

    stop_button = tk.Button(frame3, highlightbackground='white', text="Sammuta Palvelin", command=lambda:stop_npm_dev(delete_path_button))
    stop_button.grid(row=2, column=2, pady=10, sticky="w")

    open_editor = tk.Button(frame4, highlightbackground='white', text="Avaa koodieditori", command=lambda:open_code_editor(file_path), anchor="center")
    open_editor.grid(row=3, column=3, pady=10, padx=10)


    #Function binds
    file_listbox.bind("<<ListboxSelect>>", lambda event: update_file_details(file_listbox, file_name, file_path, file_desc))


    conn = db_start('database.db')
    create_tables(conn)
    filepaths = get_filepaths_from_db(conn)
    for file in filepaths:
        file_listbox.insert(tk.END, file)
    conn.close()

    main_filepaths()
    root.mainloop()