import threading
import plotly.graph_objs as go
import plotly.express as px
import plotly.offline as offline
from queue import Queue

plot_queue = Queue()  

def plot_fuel_consumption():
    started = False
    while True:
        data = plot_queue.get()  
        data = [x / 1000 for x in data]  # convert fuel consumption to liters
        fig = px.line(x=range(len(data)), y=data)  
        fig.update_layout(xaxis_title='Time Step', yaxis_title='Fuel Consumption (L)')  
        offline.plot(fig, auto_open=(not started), filename='simulation-output/fuel-consumption.html')
        started = True

def plot_speed():
    started = False
    while True:
        data = plot_queue.get()  
        data = [x * 3.6 for x in data]  # convert m/s to km/h
        fig = px.line(x=range(len(data)), y=data)  
        fig.update_layout(xaxis_title='Time Step', yaxis_title='Speed (km/h)')  
        offline.plot(fig, auto_open=(not started), filename='simulation-output/speed.html')
        started = True
    