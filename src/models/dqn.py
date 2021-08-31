import numpy as np

from models.base import BaseModel

###

GAMMA = 0.95

BATCH_SIZE = 5

###


class DQN(BaseModel):
    def __train(self):
        if self.memory.nb_entries < BATCH_SIZE + 2:
            return False

        # return number of {BATCH_SIZE} samples in random order.
        samples = self.memory.sample(BATCH_SIZE)

        for sample in samples:
            observation, action, reward, done, _ = sample
            observation = np.array(observation)

            target = self.target_network.predict(observation)

            if done is True:
                target[0][action] = reward
            else:
                q_future_value = max(self.target_network.predict(observation)[0])
                target[0][action] = reward + q_future_value * GAMMA

            self.network.fit([observation], target, epochs=1, verbose=0)

        return True