import subprocess
import os
import psutil
import threading
import tkinter as tk

server_process = None

def run_npm_dev(file_path_raw, delete_button):
    file_path = file_path_raw.cget("text")
    global server_process
    try:
            print(f"Running npm run dev in folder: {file_path}")
            if os.path.exists(file_path):

                def target():
                    global server_process
                    server_process = subprocess.Popen(
                        ["npm run dev"],
                        cwd=file_path,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    delete_button.config(state=tk.DISABLED)
                    
                    for line in server_process.stdout:
                        print(line, end="") 
            
                    for line in server_process.stderr:
                        print(f"Error: {line}", end="")
                

                
                thread = threading.Thread(target=target)
                thread.start()

            else:
                print(f"Folder can't be found: {file_path}")
    except Exception as e:
            print(f"Error in npm run dev: {e}")


def kill_process_tree(pid):
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        for child in children:
            child.terminate() 
        parent.terminate() 
        
        gone, alive = psutil.wait_procs(children, timeout=3)
        for p in alive:
            p.kill()
        parent.kill()
        print("Server and child processes killed.")
    except psutil.NoSuchProcess:
        print("Process can't be found.")
    except Exception as e:
        print(f"Error in killing process: {e}")


def stop_npm_dev(delete_button):
    global server_process
    if server_process:
        try:
            print("Trying to shut down...")
            kill_process_tree(server_process.pid)
            server_process = None
            delete_button.config(state=tk.NORMAL)
        except Exception as e:
            print(f"Error in shut down: {e}")
    else:
        print("Server not active.")


def open_code_editor(file_path):
    file_path = file_path.cget("text")
    global server_process
    try:
            print(f"Opening code editor in folder: {file_path}")
            if os.path.exists(file_path):

                def target():
                    global server_process
                    server_process = subprocess.Popen(
                        ["code ."],
                        cwd=file_path,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    
                    for line in server_process.stdout:
                        print(line, end="") 
            
                    for line in server_process.stderr:
                        print(f"Error: {line}", end="")
                

                
                thread = threading.Thread(target=target)
                thread.start()

            else:
                print(f"Folder can't be found: {file_path}")
    except Exception as e:
            print(f"Error in code .: {e}")