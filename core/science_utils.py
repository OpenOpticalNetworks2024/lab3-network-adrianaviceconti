# Use this file to define all your scientific functions (as SNR or BER evaluations)

from core.math_utils import lin2db
import numpy as np

def snr(signal_power, noise_power):
    return signal_power / noise_power

def snr_db(signal_power, noise_power):
    return 10 * np.log10(signal_power / noise_power)