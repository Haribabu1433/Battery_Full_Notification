from tkinter import *
import time
import psutil
import sys
from plyer import notification
import threading
from threading import Thread
from tkinter import messagebox


root = Tk()
root.title('BATTERY HEALTH MONITOR')

root.iconbitmap("batteryfull_1429.ico")
root.geometry("500x300")

is_on = False

# Define Our Images

on = PhotoImage(file = "on.png")
off = PhotoImage(file = "off.png")
charging = PhotoImage(file = "final_charge_icon.png")
discharging = PhotoImage(file = "final_discharge_icon.png")
low_battery = PhotoImage(file = "final_battery_low_icon.png")
full_battery = PhotoImage(file = "final_full_battery.png")

my_label = Label(root,
                 text = "Toggle button to Start",
                 fg = "green",
                 font = ("helvetica",25))
my_label.pack(pady = 5)

battery_status_label = Label(root,
                 text = "",
                 fg = "green",
                 font = ("helvetica",10))
battery_status_label.pack(pady = 5)

battery_percentage_label = Label(root,
                 text = "",
                 fg = "green",
                 font = ("helvetica",10))
battery_percentage_label.pack(pady = 5)


def battery_alert():
    #print("battery_alert function")
    while(True):
        #print("monitoring..")
        global is_on
        battery = psutil.sensors_battery()
        if int(battery.percent) >= 90 and battery.power_plugged: # edit percentage here
            #print("battery full")
            notification.notify(title = f"BATTERY IS ALMOST FULL - {battery.percent}%",
                    message="UNPLUG THE CHARGER",
                    app_name = "BatteryHealth",
                    app_icon = "batteryfull_1429.ico",
                    # displaying time
                    timeout=1
                    )
            time.sleep(120)
        elif int(battery.percent) <= 30 and not battery.power_plugged: # edit percentage here 
            #print("battery low")
            notification.notify(
                    title = f"BATTERY is Low - {battery.percent}%",
                    message="PLUG IN THE CHARGER",
                    app_name = "BatteryHealth",
                    app_icon = "lowbattery_114254.ico",
                    # displaying time
                    timeout=1,
                    ticker="",
                    toast=False
                    )
            time.sleep(120)
        if not is_on:
            #print("monitoring stopped")
            break
        time.sleep(2)

# Define our switch function
def switch():
    global is_on
    # Determine is on or off
    if is_on:
        on_button.config(image = off)
        my_label.config(text = "Monitoring OFF",
                        fg = "grey")
        print("Monitoring off")
        is_on = False
        time.sleep(0.5)
    else:
        on_button.config(image = on)
        my_label.config(text = "Monitoring ON", fg = "green")
        print("Monitoring on")
        is_on = True
        time.sleep(0.5)
        thread2 = Thread(target=battery_alert, daemon=True).start()
        
def charing_indicator():
    while(True):
        battery = psutil.sensors_battery()
        if battery.power_plugged:
            battery_status_label.config(image = charging)
            battery_percentage_label.config(text = str(battery.percent) + "%" , fg = "green")
            time.sleep(1)
        elif not battery.power_plugged and battery.percent<=30:
            battery_status_label.config(image = low_battery)
            battery_percentage_label.config(text = str(battery.percent) + "%" , fg = "red")
            time.sleep(1)
        elif battery.power_plugged and battery.percent>=90:
            battery_status_label.config(image = full_battery)
            battery_percentage_label.config(text = str(battery.percent) + "%" , fg = "red")
            time.sleep(1)
        else:
            battery_status_label.config(image = discharging)
            battery_percentage_label.config(text = str(battery.percent) + "%" , fg = "brown")
            time.sleep(1)


def on_closing():
    if is_on:
        messagebox.showwarning("Warning!", "Turn OFF monitor before closing window")
    else:
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
            sys.exit()

root.protocol("WM_DELETE_WINDOW", on_closing)


if __name__ == "__main__":
    thread1 = Thread(target=charing_indicator, daemon=True).start()
    on_button = Button(root, image = off, bd = 0,
                   command = switch)
    on_button.pack(pady = 20)
# Execute Tkinter
root.mainloop()
