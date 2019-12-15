import numpy as np
import gym
import town
import time

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, BatchNormalization
from keras.optimizers import Adam

from rl.agents.cem import CEMAgent
from rl.memory import EpisodeParameterMemory

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


cem.load_weights('cem_{}_params.h5f'.format("citizen-0"))

for move in range(100):
    action = cem.forward(env.citizens[0].vision)
    print(action)
    env.step(action)
    print(env.citizens[0].score)
    time.sleep(0.05)
    print(env)

