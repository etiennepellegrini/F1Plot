import fastf1
from fastf1 import plotting
import matplotlib.pylab as plt
# import numpy as np
# import pandas as pd

cache_dir = ".cache"

# Enable Cache
fastf1.Cache.enable_cache(cache_dir)

# ======================================================================
# Classes
# ======================================================================

# ======================================================================
class InputVars:

    def __init__(self, gp=None, year=None, ses=None, driver=None):
        self.grand_prix = gp or input(f'Which Grand Prix do you want to evaluate?  ("Imola", "Italy", etc.): \n')
        self.year = year or int(input(f'What year did the Grand Prix take place? ("2022", "2021", etc.): \n'))
        self.ses = ses or input(f'What is the session type? ("R","Sprint", "FP1", etc.): \n')
        self.driver = driver or input(f'Which driver do you want to evaluate? (ex. Abbreviation or Number): \n')


# ======================================================================
class SessionInfo:

    def __init__(self, gp=None, year=None, ses=None, driver=None):
        self.input_vars = InputVars(gp, year, ses, driver)

        self.session = fastf1.get_session(
            self.input_vars.year,
            self.input_vars.grand_prix,
            self.input_vars.ses,
        )
        self.session.load()
        self.results = self.session.results
        self.event_name = self.session.event['EventName']


# ======================================================================
class DriverInfo:
    session_info = SessionInfo()
    info = session_info.session.get_driver(session_info.input_vars.driver)
    ses = session_info.session.laps.pick_driver(session_info.input_vars.driver)
    fullname = info['FullName']
    team = info['TeamName']
    team_color = fastf1.plotting.team_color(team)
    print(f'Getting data for {fullname}...\n')

    lap_or_ses = input(f'Do you want to evaluate a specific lap? (Y/N/F for Fastest): \n')
    if lap_or_ses == 'Y':
        print(ses['LapNumber'])
        num = int(input(f'\nInput Lap Number (10, 20, 30, etc.): \n'))
        lap = f"Lap {num}"
        lap_n = ses[(ses['LapNumber'] == num)]
        lap_n_tel = lap_n.get_telemetry()
        data = lap_n_tel
        print(f"Getting lap {num} data...\n")

    elif lap_or_ses == 'F':
        f_lap = ses.pick_fastest()
        lap = f"Lap {f_lap['LapNumber']} (fastest)"
        fastest_lap = f_lap.get_telemetry()
        data = fastest_lap
        print(f"Getting fastest lap data...\n")

    else:
        data = ses
        lap = "Full session"
        print(f"Getting full session data...\n")


# ======================================================================
# Methods
# ======================================================================

# ----------------------------------------------------------------------
def define_data():
    var_list = list(DriverInfo.data)
    for number, var in enumerate(var_list):
        print(number, var)
    y = int(input(f'\nSelect Y AXIS data point to evaluate from list above (Int): \n'))
    req_dat_y = var_list[y]
    x = int(input(f'\nSelect X AXIS data point to evaluate from list above (Int): \n'))
    req_dat_x = var_list[x]
    return req_dat_y, req_dat_x


# ----------------------------------------------------------------------
def data():
    req_dat_y, req_dat_x = define_data()
    driver_xvar = DriverInfo.data[f'{req_dat_x}']
    driver_yvar = DriverInfo.data[f'{req_dat_y}']
    return driver_xvar, driver_yvar


# ----------------------------------------------------------------------
def data_plot():
    plt.rcParams["figure.autolayout"] = True

    driver_xvar, driver_yvar = data()
    x = driver_xvar
    y = driver_yvar
    xmin, xmax = x.min(), x.max()

    fig = plt.figure(1)
    speed = fig.subplots()
    speed.plot(x, y, color=DriverInfo.team_color, label=f"{y.name}")
    speed.set_ylabel(f"{y.name}")
    speed.set_xlabel(f"{x.name}")
    # speed.set_xlim(xmin, xmax)
    speed.grid(visible=True, axis='y', alpha=.5)
    title = f"{DriverInfo.fullname} - {DriverInfo.session_info.event_name} - {DriverInfo.lap}\n{y.name} Analysis"
    plt.suptitle(title)
    # Sanitize string
    title = title.replace("\n", "_").replace(" - ", "_").replace(" ", "-")

    # Save without asking...
    plot_title = f"{cache_dir}/save/{title}.png"
    plt.savefig(plot_title, dpi=300, transparent=True)

    plt.show()
    print("Plot saved as {plot_title}")
    return fig


# ----------------------------------------------------------------------
def save():
    s = input(f'Do you want to save telemetry data? (Y/N): \n')
    if s == 'Y':
        export = DriverInfo.data
        csv = f"{cache_dir}/{DriverInfo.fullname}_{DriverInfo.session_info.event_name}.csv"
        export.to_csv(csv.replace(" ", "-"))
        print("Data Saved.\n")
    if s == 'N':
        print("Nothing saved.\n")
        pass


# ----------------------------------------------------------------------
if __name__ == "__main__":
    i = 'Y'
    while i == 'Y':
        data_plot()
        # save()
        # i = input(f'Do you want to go again? (Y/N): \n')
    else:
        print("All good, thanks!")
