import numpy as np
import scipy.signal as sig


def short_time_fourier_transform(signal: np.ndarray, win_size: int, hop_size: int) -> np.ndarray:
    """ Функция, которая производит коротковременное преобразования """
    window = sig.windows.hann(win_size, sym=False)
    frames = np.array([np.fft.fft(window * signal[i:i + win_size]) for i in range(0, len(signal) - win_size, hop_size)])
    return frames


def inverse_short_time_fourier_transform(frames: np.ndarray, win_size: int, hop_size: int) -> np.ndarray:
    """ Функция, которая производит обратное коротковременное преобразования """
    window = sig.windows.hann(win_size, sym=False)
    signal = np.zeros(len(frames) * hop_size + win_size)
    window_sum = np.zeros(len(frames * hop_size + win_size))
    for n, i in enumerate(range(0, len(signal) - win_size, hop_size)):
        signal[i:i + win_size] += np.real(np.fft.ifft(frames[n])) * window
        window_sum[i:i + win_size] += window ** 2
    return signal / window_sum


def phase_vocoder(signal: np.ndarray, ratio: float, win_size: int = 2048, hop_size: int = None) -> np.ndarray:
    """ Сам алгоритм """
    if hop_size is None:
        hop_size = int(win_size / 4)
    frames = short_time_fourier_transform(signal, win_size, hop_size)
    n_fft_bins, n_frames = frames.shape
    t_scale = np.arange(n_fft_bins) * ratio
    ph = np.zeros(n_fft_bins)
    transformed_frames = np.zeros((n_fft_bins, n_frames), dtype=np.complex)
    for i in range(n_frames):
        transformed_frames[:, i] = np.abs(frames[:, i]) * np.exp(1j * ph)
        ph += 2 * np.pi * t_scale / n_fft_bins
        frames[:, i] *= np.exp(1j * ph)
    transformed_signal = inverse_short_time_fourier_transform(frames, win_size, hop_size)
    return transformed_signal
