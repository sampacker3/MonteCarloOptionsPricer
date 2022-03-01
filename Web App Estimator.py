from time import time
from math import exp, sqrt, log
from random import gauss, seed

from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
from pywebio.session import hold, go_app
from math import sqrt

seed(20000)
initial_time = time()

initial_value = 'a'
Strike_Price = 'b'
Maturity = 'c'
risk = 'd'
volatility = 'e'
Time_Steps = 'f'
num_paths = 'g'

data = input_group("Data", [input("Initial Value", type=FLOAT, name='a'),
                            input("Strike Price", type=FLOAT, name='b'),
                            input("Maturity", type=FLOAT, name='c'),
                            input("Risk", type=FLOAT, name='d'),
                            input("Volatility", type=FLOAT, name='e'),
                            input("Time Steps", type=FLOAT, name='f')])

Maturityflt = float(Maturity)
Time_Stepsflt = float(Time_Steps)

dt = Maturityflt / Time_Stepsflt

def quad():
    put_markdown("""
Solving a Quadratic Equation

## [Sam Packer](https://www.sam-packer.co.uk)

Here, we solve a quadratic equation (a.x<sup>2</sup>+b.x+c=0) using Python including the math library

    """, strip_indent=4)

Sim = []
for i in range(num_paths):
    Simpath = []
    for t in range(Time_Steps + 1):
        if t == 0:
            Simpath.append(initial_value)
        else:
            z = gauss(0.0, 1.0)
            Simt = Simpath[t - 1] * exp((risk - 0.5 * volatility ** 2) * dt
                                        + volatility * sqrt(dt) * z)
            Simpath.append(Simt)
    Sim.append(Simpath)

Option_Value = exp(-risk * Maturity) * sum([max(path[-1] - Strike_Price, 0) for path in Sim]) / num_paths

time_taken = time() - initial_time
print(" Option Value %7.3f" % Option_Value)
print("Duration in Seconds   %7.3f" % time_taken)

put_markdown("""## Option Value""")
put_text(f'The Option Value is {round(Option_Value, 3)}')

if __name__ == '__main__':
    start_server(quad, port=9999, debug=True, cdn=False)

