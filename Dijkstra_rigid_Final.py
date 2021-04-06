import numpy as np

obs_map = np.zeros((302, 402), dtype=int)
obs_map[0, :] = 1
obs_map[301, :] = 1
obs_map[:, 0] = 1
obs_map[:, 401] = 1