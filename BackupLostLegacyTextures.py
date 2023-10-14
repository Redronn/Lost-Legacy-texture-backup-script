import os
import time
import zipfile


# ANSI escape codes for colors
class Colors:
    LIGHTRED_EX = '\033[91m'
    LIGHTGREEN_EX = '\033[92m'
    LIGHTCYAN_EX = '\033[96m'
    RESET = '\033[0m'


# Custom progress bar
def progress_bar(iteration, total, prefix='', length=50, fill='█'):
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '•' * (length - filled_length)
    print('\r%s |%s| %s%% [%s/%s files]' % (Colors.LIGHTCYAN_EX + prefix, bar, percent, iteration, str(total))
          + Colors.RESET, end='\r')

    if iteration == total:
        print()


# What it do?
print("This script is for backing up landscape and exterior architecture textures for the purpose of\n"
      "downsizing them with 'Cathedral Assets Optimizer' to get better performance/less stutters in\n"
      "Skyrim Lost Legacy. If performance options in MO2 don't work well enoough for you, then\n"
      "downsizing these textures might help as it reduces RAM & VRAM usage.\n\n"

      "Made for Lost Legacy version 1.2.0\n")

# Check if the script and 'texturelist.txt' are in the same directory as 'Lost Legacy'
if not os.path.exists('Lost Legacy'):
    print(
        Colors.LIGHTRED_EX + "Error: The script is not in the same directory as the 'Lost Legacy' folder."
        + Colors.RESET)
    input(Colors.LIGHTGREEN_EX + "Press enter to exit..." + Colors.RESET)
    quit()
elif not os.path.exists('texturelist.txt'):
    print(Colors.LIGHTRED_EX + "Error: 'texturelist.txt' is not in the same directory as the script." + Colors.RESET)
    input(Colors.LIGHTGREEN_EX + "Press enter to exit..." + Colors.RESET)
    quit()

# Ask for user confirmation
run_script = input(Colors.LIGHTCYAN_EX + "Run script? (y/n): " + Colors.RESET)
if run_script.lower() == 'y':
    # Open the file in read mode
    with open('texturelist.txt', 'r') as f:
        # Read lines from the file
        lines = f.readlines()
else:
    quit()

# Ask user which lists to archive
archive_landscape = input(Colors.LIGHTCYAN_EX + "Backup landscape textures? (y/n): " + Colors.RESET)
archive_architecture = input(Colors.LIGHTCYAN_EX + "Backup architecture textures? (y/n): " + Colors.RESET)

if archive_landscape.lower() != 'y' and archive_architecture.lower() != 'y':
    print(Colors.LIGHTRED_EX + "No lists selected for archiving. Exiting..." + Colors.RESET)
    time.sleep(10)
    quit()

# Separate lines into landscape and architecture lists
landscape_lines = []
architecture_lines = []
current_list = None

for line in lines:
    line = line.strip()
    if "Landscape textures:" in line:
        current_list = landscape_lines
    elif "Architecture textures:" in line:
        current_list = architecture_lines
    elif line == "":
        current_list = None
    elif current_list is not None:
        current_list.append(line)

if not os.path.exists('LostLegacy Textures'):
    os.makedirs('LostLegacy Textures')

# Create a ZipFile object
with zipfile.ZipFile('LostLegacy Textures/LostLegacy_textures_backup.zip', 'w') as zipf:
    # Combine selected lists and archive with a single progress bar
    combined_lines = []
    if archive_landscape.lower() == 'y':
        combined_lines.extend(landscape_lines)
    if archive_architecture.lower() == 'y':
        combined_lines.extend(architecture_lines)

    total_files = len(combined_lines)

    for i, line in enumerate(combined_lines):
        if os.path.isfile(line):
            zipf.write(line)
            progress_bar(i + 1, total_files, prefix="Creating 'LostLegacy_textures_backup.zip':",
                         length=40)

input(Colors.LIGHTGREEN_EX + "Done! 'LostLegacy_textures_backup.zip' created in 'LostLegacy Textures' folder. Press "
                             "enter to exit..." + Colors.RESET)

# Open the directory in the default file explorer
os.startfile('LostLegacy Textures')
