import logging
import sys
import glob
import os
import json

sys.path.append(r"/Users/denism/work/sbb_challenge")
sys.path.append(r"/Users/denism/work/sbb_challenge/utils")

from simulator.simulator import Simulator
from simulator.simulator import BlockinException
from simulator.qtable import QTable
from simulator.event import humanize_time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

FORMAT = "[%(asctime)s %(filename)s:%(lineno)s - %(funcName)s ] %(message)s"
logging.basicConfig(format=FORMAT)

path = glob.glob(r"/Users/denism/work/train-schedule-optimisation-challenge-starter-kit/problem_instances/07*")[0]

qtable = QTable()

sim = Simulator(path=path, qtable=qtable)
sim.trains = sim.trains
sim.assign_limit()

i = 1

sim.wait_time = 30
sim.max_delta = 5 * 60
sim.n_state = 1
sim.with_connections = True

qtable.epsilon = 0.0
qtable.alpha = 0.8  # learning rate
qtable.gamma = 0.8  # discount factor
trains = list(sim.trains)

sim.initialize()
sim.match_trains()
sim.spiegel_anschlusse()

score = 200
j = 1

while i < 2:
    sim.initialize()
    sim.free_all_resources()
    i+=1
    while not sim.done:
        try:
            sim.initialize()
            sim.free_all_resources()
            j += 1
            sim.run()
        except BlockinException as e:
            logging.info("###########################")
            n = len(sim.trains)
            n2 = len([t for t in sim.trains if t.solution.done])
            #logging.info(e.train)
            logging.info("%s: %i/%i trains" % (humanize_time(sim.current_time), n2, n))
            #sim.go_back(e.back_time)

folder = r"/Users/denism/work/train-schedule-optimisation-challenge-starter-kit/solutions"
output_path = os.path.join(folder, sim.timetable.label + "_for_submission.json")
with open(output_path, 'w') as outfile:
    json.dump([sim.create_output()], outfile)