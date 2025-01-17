# -*- coding: utf-8 -*-
"""Statistics Spike Frequency.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1cycyYMO9n0lJ25z55pFs8NjtiI48XZRk
"""

from google.colab import drive
drive.mount('/content/drive')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# ----- Recording Duration -----
recording_duration = 60  # Duration of recordings in seconds

# ----- Spike Counts -----
# Replace these lists with your actual spike count data
wt_spike_counts = [7, 2, 16, 18, 12, 7, 8]  # Wild-Type group spike counts
ad_spike_counts = [35, 32, 22, 17, 19, 30, 45, 30]  # Mutant group spike counts (APP/PSEN1)

# ----- Calculate Spike Frequencies -----
wt_frequencies = [count / recording_duration for count in wt_spike_counts]
ad_frequencies = [count / recording_duration for count in ad_spike_counts]

# ----- Combine Data for Export -----
frequency_data = pd.DataFrame({
    'Group': ['WT AS2'] * len(wt_frequencies) + ['APP/PSEN1'] * len(ad_frequencies),
    'Spike Frequency (Hz)': wt_frequencies + ad_frequencies
})

# Save to CSV for GraphPad Prism or similar analysis tools
frequency_data.to_csv('frequency_data_for_prism.csv', index=False)

# ----- Statistical Analysis -----
# Perform an independent t-test
t_stat, p_value = ttest_ind(wt_frequencies, ad_frequencies, equal_var=False)

# Determine significance level
significance = (
    "***" if p_value < 0.001 else
    "**" if p_value < 0.01 else
    "*" if p_value < 0.05 else
    "ns"  # Not Significant
)

# ----- Visualization -----
plt.figure(figsize=(8, 6))
colors = ['green', 'purple']
labels = ['WT AS2', 'APP/PSEN1']

# Mean and SEM
mean_frequencies = [np.mean(wt_frequencies), np.mean(ad_frequencies)]
sem_frequencies = [
    np.std(wt_frequencies) / np.sqrt(len(wt_frequencies)),
    np.std(ad_frequencies) / np.sqrt(len(ad_frequencies))
]

# Plot Bar Chart with Error Bars and Data Points
for i, (freq_group, color, label) in enumerate(zip([wt_frequencies, ad_frequencies], colors, labels)):
    plt.bar(i, mean_frequencies[i], color=color, width=0.6, edgecolor='black', label=label)
    plt.errorbar(i, mean_frequencies[i], yerr=sem_frequencies[i], fmt='k_', capsize=5)
    plt.scatter(
        np.full(len(freq_group), i), freq_group,
        color=color, edgecolor='black', s=50, zorder=3
    )
    plt.text(i, mean_frequencies[i] + 0.05, f"n = {len(freq_group)}", ha='center', fontsize=10)

# Annotate Significance
x1, x2 = 0, 1
y, h, col = max(mean_frequencies) + 0.05, 0.02, 'black'
plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, color=col)
plt.text((x1 + x2) * 0.5, y + h, significance, ha='center', va='bottom', color=col, fontsize=12)

# Styling the Plot
plt.xticks([0, 1], labels, fontsize=12)
plt.ylabel('Spike Frequency (Hz)', fontsize=12)
plt.tight_layout()

# Save Plot
plt.savefig('frequency_plot_for_prism.svg', format='svg', bbox_inches='tight')
plt.savefig('frequency_plot_for_prism.pdf', format='pdf', bbox_inches='tight')
plt.show()

# ----- Summary Output -----
print("✅ Frequency data exported to 'frequency_data_for_prism.csv'")
print("✅ Frequency plot saved as 'frequency_plot_for_prism.svg' and 'frequency_plot_for_prism.pdf'")
print(f"WT Frequencies: {wt_frequencies}")
print(f"APP/PSEN1 Frequencies: {ad_frequencies}")
print(f"T-statistic: {t_stat:.4f}, P-value: {p_value:.4f} ({significance})")