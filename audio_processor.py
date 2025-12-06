import numpy as np

def apply_ild_itd(audio_chunk, sr, azimuth_deg, distance_m):
    # ILD
    ild = np.clip(azimuth_deg / 90.0, -1, 1)
    left_gain = 1 - max(ild, 0)
    right_gain = 1 + min(ild, 0)

    # ITD (very tiny delay)
    itd_sec = azimuth_deg * 1e-5
    itd_samples = int(itd_sec * sr)

    out = np.zeros_like(audio_chunk)
    if itd_samples >= 0:
        out[itd_samples:, 0] = audio_chunk[:-itd_samples, 0] * left_gain
        out[:, 1] = audio_chunk[:, 1] * right_gain
    else:
        delay = -itd_samples
        out[:, 0] = audio_chunk[:, 0] * left_gain
        out[delay:, 1] = audio_chunk[:-delay, 1] * right_gain

    return out
