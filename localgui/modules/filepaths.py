from modules.querys import *
import tkinter as tk
from tkinter import filedialog, Toplevel

server_process = None

def main_filepaths():
    conn = db_start('database.db')
    create_tables(conn)


def get_all_filepaths():
    conn = db_start('database.db')
    filepath_names = get_filepaths_from_db(conn)
    conn.close()

    print(filepath_names)
    return filepath_names


def add_filepath(inputName, inputUrl, listbox):
    name = inputName.get()
    url = inputUrl.get()

    conn = db_start('database.db')
    add_filepath_to_db(conn, name, url)

    listbox.delete(0, tk.END)
    filepaths = get_filepaths_from_db(conn)
    for file in filepaths:
        listbox.insert(tk.END, file)
    conn.close()


def remove_selected_path(right_listbox, file_name, file_path):
    try:
        selected_index = right_listbox.curselection()
        if selected_index:
            selected_path = right_listbox.get(selected_index)
            right_listbox.delete(selected_index)
            file_name.config(text="")
            file_path.config(text="")  
            
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM filepaths WHERE name=?", (selected_path,))
            conn.commit()
            conn.close()
            
            print(f"Polku '{selected_path}' poistettu onnistuneesti.")
        else:
            print("Valitse poistettava polku.")
    except Exception as e:
        print(f"Virhe polun poistamisessa: {e}")


def update_filepath(inputPathId, inputPathName, inputPathUrl, inputPathDesc):
    conn = db_start('database.db')
    update_filepath_in_db(conn, inputPathName, inputPathUrl, inputPathId, inputPathDesc)
    get_all_filepaths()
    conn.close()

    
def browse_and_add_path(listbox):
    folder_selected = filedialog.askdirectory()
    
    if folder_selected: 
        top = Toplevel()
        top.title("Uusi kansiopolku")
        
        entry_name = tk.Entry(top)
        entry_desc = tk.Entry(top)
        tk.Label(top, text="Nimi:").pack(pady=10)
        entry_name.pack(pady=10)
        tk.Label(top, text="Kuvaus:").pack(pady=10)
        entry_desc.pack(pady=10)

        
        def save_name():
            name = entry_name.get()
            desc = entry_desc.get()
            conn = db_start('database.db')
            add_filepath_to_db(conn, name, folder_selected, desc)
            
            
            listbox.delete(0, tk.END) 
            filepaths = get_filepaths_from_db(conn)  
            for file in filepaths:
                listbox.insert(tk.END, file)  

            conn.close()
            top.destroy() 
            
        
        save_button = tk.Button(top, text="Tallenna", command=save_name)
        save_button.pack(pady=10)


def on_listbox_select(event, file_name, file_path, file_desc):
    
    selection = event.widget.curselection()
    if selection:  
        index = selection[0]
        selected_name = event.widget.get(index)
        
        
        conn = db_start('database.db')
        details = get_filepath_details(conn, selected_name)
        conn.close()

        if details:
            name, url, desc = details
            
            file_name.config(text="") 
            file_path.config(text="") 
            file_desc.config(text="")
            file_name.insert(tk.END, f"Nimi: {name}")
            file_path.insert(tk.END, f"Sijainti: {url}")
            file_desc.insert(tk.END, f"{desc}")


def update_file_details(right_listbox, file_name_label, file_path_label, file_desc):
    selected_index = right_listbox.curselection()
    if selected_index:
        selected_item = right_listbox.get(selected_index)
        
        conn = db_start('database.db')
        details = get_filepath_details(conn, selected_item)
        conn.close()
        
        name, url, desc = details
        file_name_label.config(text=f"{name}")
        file_path_label.config(text=f"{url}")
        file_desc.config(text=f"{desc}")
    else:
        print("Valitse tiedosto listasta.")
