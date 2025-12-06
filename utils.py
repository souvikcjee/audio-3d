def smooth(value_list, kernel=5):
    import numpy as np
    from scipy.signal import medfilt
    return medfilt(np.array(value_list), kernel_size=kernel)
