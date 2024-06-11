from lava.proc.lif.process import LIF
from lava.proc.monitor.process import Monitor
from lava.proc.dense.process import Dense
from lava.magma.core.run_conditions import RunContinuous, RunSteps
from lava.magma.core.run_configs import Loihi1SimCfg
import numpy as np
from matplotlib import pyplot as plt
import matplotlib


def function():
    # Create processes
    lif1 = LIF(shape=(3, ),                         # Number and topological layout of units in the process
               vth=10.,                             # Membrane threshold
               dv=0.1,                              # Inverse membrane time-constant
               du=0.1,                              # Inverse synaptic time-constant
               bias_mant=(1.1, 1.2, 1.3),           # Bias added to the membrane voltage in every timestep
               name="lif1")
    
    dense = Dense(weights=np.random.rand(2, 3),     # Initial value of the weights, chosen randomly
                  name='dense')
    
    lif2 = LIF(shape=(2, ),                         # Number and topological layout of units in the process
               vth=10.,                             # Membrane threshold
               dv=0.1,                              # Inverse membrane time-constant
               du=0.1,                              # Inverse synaptic time-constant
               bias_mant=0.,                        # Bias added to the membrane voltage in every timestep
               name='lif2')
    
    
    # Connect the OutPort of lif1 to the InPort of dense
    lif1.s_out.connect(dense.s_in)
    
    # Connect the OutPort of dense to the InPort of lif2
    dense.a_out.connect(lif2.a_in)
    
    variable = dense.weights.get()
    
    
    monitor_lif1 = Monitor()
    monitor_lif2 = Monitor()
    
    num_steps = 100
    
    monitor_lif1.probe(lif1.v, num_steps)
    monitor_lif2.probe(lif2.v, num_steps)
    
    run_condition = RunSteps(num_steps=num_steps)
    
    
    run_cfg = Loihi1SimCfg()
    
    lif2.run(condition=run_condition, run_cfg=run_cfg)
    
    data_lif1 = monitor_lif1.get_data()
    data_lif2 = monitor_lif2.get_data()
    
    
    # Create a subplot for each monitor
    fig = plt.figure(figsize=(16, 5))
    ax0 = fig.add_subplot(121)
    ax1 = fig.add_subplot(122)
    
    # Plot the recorded data
    monitor_lif1.plot(ax0, lif1.v)
    monitor_lif2.plot(ax1, lif2.v)

function()

