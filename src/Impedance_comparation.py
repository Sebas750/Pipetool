import matplotlib.pyplot as plt
from os.path import join
import os
import numpy as np

pipetool_path = join('src', 'Pipetool_result_impedances')
webtool_path = join('src', 'Webpage_result_impedances')

pipetool_names = [f for f in os.listdir(pipetool_path) if f.endswith('.txt') and os.path.isfile(os.path.join(pipetool_path, f))]
webtool_names = [f for f in os.listdir(webtool_path) if f.endswith('.csv') and os.path.isfile(os.path.join(webtool_path, f))]

files_comparation = []

for i in range(len(pipetool_names)):
    with open(join(pipetool_path, pipetool_names[i]), 'r') as file:
        pipe_tool_data_filtered = []
        pipetool_data = file.readlines()
        for line in pipetool_data:
            line = np.array(line.strip().split(' '))
            if '#' not in line[0]:
                pipe_tool_data_filtered.append(line)
        pipe_tool_data_filtered = np.array(pipe_tool_data_filtered)
    with open(join(webtool_path, webtool_names[i]), 'r') as file:
        web_tool_data_filtered = []
        webtool_data = file.readlines()
        for line in webtool_data:
            line = np.array(line.strip().split(' '))
            if '#' not in line[0]:
                web_tool_data_filtered.append(line)
        web_tool_data_filtered = np.array(web_tool_data_filtered)
    files_comparation.append([pipe_tool_data_filtered, web_tool_data_filtered])

print(len(files_comparation))

real_ERROR = []
imag_ERROR = []
for i in range(len(pipetool_names)):
    real_ERROR.append(np.abs(files_comparation[i][0][:, 1].astype(float) - files_comparation[i][1][:, 1].astype(float)))
    imag_ERROR.append(np.abs(files_comparation[i][0][:, 2].astype(float) - files_comparation[i][1][:, 2].astype(float)))

fig, ax = plt.subplots(2, 1, figsize=(8, 8))
for i in range(len(pipetool_names)):
    ax[0].plot(files_comparation[i][0][:, 0].astype(float), real_ERROR[i], label=pipetool_names[i])
    ax[1].plot(files_comparation[i][0][:, 0].astype(float), imag_ERROR[i], label=pipetool_names[i])
    ax[0].set_title('Real part error')
    ax[1].set_title('Imaginary part error')
    ax[1].set_xlabel('Frequency (Hz)')
    ax[0].set_ylabel('Error')
    ax[1].set_ylabel('Error')
    ax[0].legend()
    ax[1].legend()
    ax[0].grid()
    ax[1].grid()
    
plt.show()







