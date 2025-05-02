# dependencies 
import PySpice.Logging.Logging as Logging 
logger=Logging.setup_logging()

from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

import matplotlib.pyplot as pt
import numpy as np
import pandas as pd

from flask_socketio import SocketIO
from flask import Flask, render_template,request,Response
cxx=0;rr1=0;rr2=0;rr3=0;rr4=0;rr5=0;rr6=0;cd=0;

app=Flask(__name__)
socket=SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

        

@socket.on("message")
def cmessage(cm):
    #print(cm)
    cxx=cm['r1']
    rr1=float(cm['r2'])
    rr2=float(cm['r3'])
    rr3=float(cm['r4'])
    rr4=float(cm['r5'])
    rr5=float(cm['r6'])
    rr6=float(cm['r7'])
    #print(type(cxx))
    #circuit logic
    cx=float(cxx)
    r4=float(rr5*2000+rr4*1000+rr3*100+rr2*10+rr1*1)
    r3=float(rr6*1000)

    ckt=Circuit("desauty")
    ckt.SinusoidalVoltageSource('input','n1',ckt.gnd,amplitude=10@u_V,frequency=10000@u_Hz)
    ckt.C(2,'n1','n3',0.15@u_uF)
    ckt.C(1,'n1','n2',cx@u_uF)
    ckt.V(5,'n2','n3',0@u_V)
    ckt.R(3,'n2',ckt.gnd,r3@u_kOhm) #variable resistor r3
    ckt.R(4,'n3',ckt.gnd,r4@u_kOhm) #variable resistor r4
    #print(ckt)
    sim=ckt.simulator(temperature=25,nominal_temperature=25)
    sim.initial_condition(n1=0,n2=0,n3=0)
    analysis=sim.transient(step_time=1@u_us,end_time=0.1@u_ms)
    c=pd.DataFrame(analysis.branches.values())
    cv=float(c.iloc[1,:].max())
    socket.send(cv)

if __name__=='__main__':
    socket.run(
        app=app,
        host='127.0.0.1',
        debug=True, 
        port=5000)
    




#fig=pt.figure()
#pt.plot(c.iloc[0,:])
#pt.plot(c.iloc[1,:])
#pt.show()
#pt.close()
#v=float(input("enter value:"))
#t=v@u_uF
#print(type(t))
#print(t)


