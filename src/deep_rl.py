import numpy as np
import gym
import town

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, BatchNormalization, LeakyReLU
from keras.optimizers import Adam

from rl.agents.cem import CEMAgent
from rl.memory import EpisodeParameterMemory



# Get the environment and extract the number of actions.
env = town.Town()
env.reset()

nb_actions = env.action_space.n
obs_dim = env.citizens[0].vision.shape[0]

model = Sequential()
model.add(Dense(128, input_shape=(8,)))
model.add(Activation('relu'))
model.add(BatchNormalization())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dense(32))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(nb_actions))
model.add(Activation('softmax'))

print(model.summary())

memory = EpisodeParameterMemory(limit=1000, window_length=1)

cem = CEMAgent(model=model, nb_actions=nb_actions, memory=memory,
               batch_size=50, nb_steps_warmup=2000, train_interval=50, elite_frac=0.05)
cem.compile()

cem.fit(env, nb_steps=100000, visualize=False, verbose=2)

cem.save_weights('cem_{}_params.h5f'.format("citizen-0"), overwrite=True)
