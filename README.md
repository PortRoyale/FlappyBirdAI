Lean how to program an AI to play the game of flappy bird using python and the module neat python. We will start by building a version of flappy bird using pygame and end by implementing the evolutionary neat algorithm to play the game. 

REFERENCES: 
Tech With Tim Flappy AI tutorials: https://www.youtube.com/playlist?list=PLzMcBGfZo4-lwGZWXz5Qgta_YNX3_vLS2
Tech With Time Flappy AI Overview: https://www.youtube.com/watch?v=OGHA-elMrxI
NEAT-Python algorithm home page: https://github.com/CodeReclaimers/neat-python
NEAT simple explanation paper: http://nn.cs.utexas.edu/downloads/papers/stanley.cec02.pdf
		
>>Why is NEAT good? (Granted, this algorithm was born in early 2000/2001, we still use it today)
"We identify three major challenges for
TWEANNs and presentsolutions to each of them: (1) Is there
a genetic representation that allows disparate topologies to
crossover in a meaningful way? Our solution is to use historical markings to line up genes with the same origin. (2)
How can topological innovation that needs a few generations
to optimize be protected so that it does not disappear from the
population prematurely? Our solution is to separate each innovation into a different species. (3) How can topologies be
minimized throughout evolution without the need for a specially contrived fitness function that measures complexity?
Our solution is to start from a minimal structure and grow
only when necessary. This paper establishes that each of our
solutions is necessary by showing that NE performance significantly declines with the ablation of any of the major solution components. Working together in NEAT these components constitute a promising new approach to difficult reinforcement learning tasks."

>>Flappy bird is simple. That's why it works.
from wiki: "On simple control tasks, the NEAT algorithm often arrives at effective networks more quickly than other contemporary neuro-evolutionary techniques and reinforcement learning methods.[1][2]"