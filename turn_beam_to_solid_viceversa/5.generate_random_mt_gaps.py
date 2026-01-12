import numpy as np
from scipy.stats import skewnorm
import matplotlib.pyplot as plt

def generate_beams_with_gaps(mt_num, total_len, mean_len, std_len, skew, gap_len, forbidden_fraction=0.1, seed=None):
    """
    Generate gaps for beams using skew-normal segments, independent per beam,
    avoiding the first and last `forbidden_fraction` of the beam.
    """
    if seed is not None:
        np.random.seed(seed)

    allowed_start = forbidden_fraction * total_len
    allowed_end = (1 - forbidden_fraction) * total_len
    allowed_width = allowed_end - allowed_start

    all_gaps = []

    for _ in range(mt_num):
        segments = []
        cum_length = 0.0

        while True:
            seg = skewnorm.rvs(a=skew, loc=mean_len, scale=std_len)
            seg = max(seg, 0.0)  # ensure positive

            if cum_length + seg + gap_len > allowed_width:
                break

            segments.append(seg)
            cum_length += seg + gap_len

        if not segments:
            all_gaps.append([])
            continue

        # Convert segments to gap positions
        gaps = []
        x = 0.0
        for seg in segments:
            x += seg
            gaps.append((x, x + gap_len))
            x += gap_len

        # Random shift inside allowed window
        last_gap_end = gaps[-1][1]
        max_shift = allowed_width - last_gap_end
        shift = np.random.uniform(0, max_shift)
        gaps = [(g0 + allowed_start + shift, g1 + allowed_start + shift) for (g0, g1) in gaps]

        all_gaps.append(gaps)

    return all_gaps

# -----------------------
# Parameters
# -----------------------
mt_num = 19
total_len = 8.0       # beam length
mean_len = 4.0        # segment mean
std_len = 2.0         # segment std
skew = 1              # positive skew
gap_len = 0.15
forbidden_fraction = 0.1

gaps = generate_beams_with_gaps(mt_num, total_len, mean_len, std_len, skew, gap_len, forbidden_fraction, seed=42)

# Print gaps
for i, beam_gaps in enumerate(gaps):
    print(f"Beam {i+1} gaps:", beam_gaps)

# Plot beams
fig, ax = plt.subplots(figsize=(8, 2))
for i, beam_gaps in enumerate(gaps):
    y = i * 1.0
    x = 0
    for gap_start, gap_end in beam_gaps:
        plt.hlines(y, x, gap_start, color='black', linewidth=4)
        x = gap_end
    if x < total_len:
        plt.hlines(y, x, total_len, color='black', linewidth=4)

ax.set_xlim(0, total_len)
ax.set_ylim(-1, mt_num)
ax.axis('off')
plt.show()
