import librosa
import numpy as np
import os

# Key profiles for major and minor keys (Krumhansl-Schmuckler).
major_profile = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
minor_profile = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

# Key labels.
chroma_labels = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Key translation.
key_mapping = {'C': 'Do', 'C#': 'Do#', 'D': 'Ré', 'D#': 'Ré#', 'E': 'Mi', 'F': 'Fa', 'F#': 'Fa#', 'G': 'Sol', 'G#': 'Sol#', 'A': 'La', 'A#': 'La#', 'B': 'Si'}

# Key type translation.
key_type_mapping = {'Major': 'Majeur', 'Minor': 'Mineur'}

def list_mp3_files():
    """
    Lists all the MP3 files in the current directory.

    Returns:
    list: A list of MP3 file names.
    """
    return [f for f in os.listdir() if f.endswith('.mp3')]

def select_mp3_file(mp3_files):
    """
    Displays a list of MP3 files and prompts the user to select one.

    Parameters:
    mp3_files (list): List of MP3 file names.

    Returns:
    str: Selected MP3 file name.
    """
    print("\n|------------------------------[ Music Key Finder ]------------------------------|\n")
    print("Please select a file from the list below:\n")

    for i, file in enumerate(mp3_files, 1):
        print(f"{i}. {file}")
    
    while True:
        try:
            choice = int(input("\nEnter the number of the file you want to analyze: "))
            if 1 <= choice <= len(mp3_files):
                return mp3_files[choice - 1]
            else:
                print("Invalid number. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def detect_key(mp3_path):
    """
    Detects the key of a music file in terms of major and minor profiles.

    Parameters:
    mp3_path (str): Path to the MP3 file.

    Returns:
    tuple: Two arrays of correlations with major and minor key profiles.
    """
    y, sr = librosa.load(mp3_path, sr=None)

    # Trim silent segments.
    yt, _ = librosa.effects.trim(y)
    
    # Split into 10-second segments for more detailed analysis.
    segment_length = sr * 10
    num_segments = len(yt) // segment_length
    chroma_mean_total = np.zeros(12)

    for i in range(num_segments):
        start, end = i * segment_length, (i + 1) * segment_length
        segment = yt[start:end]

        # Chromogram calculation.
        # > Represents the intensity of each note in the audio signal at different time frames.
        # > It consists of chroma vectors, each a 12-dimensional array representing pitch classes (semitones of the chromatic scale).
        chroma_mean_total += np.mean(librosa.feature.chroma_cqt(y=segment, sr=sr), axis=1)
    
    # Average chromagram values across segments.
    chroma_mean_total /= num_segments

    # Normalize values for comparison with profiles.
    chroma_mean_total /= np.linalg.norm(chroma_mean_total)
    
    # Calculate correlations with major and minor key profiles.
    major_correlations = [np.corrcoef(np.roll(major_profile, i), chroma_mean_total)[0, 1] for i in range(12)]
    minor_correlations = [np.corrcoef(np.roll(minor_profile, i), chroma_mean_total)[0, 1] for i in range(12)]
    
    return major_correlations, minor_correlations

def determine_key(major_correlations, minor_correlations):
    """
    Determines the most likely key (major or minor) based on correlations.

    Parameters:
    major_correlations (list): Correlations with major key profiles.
    minor_correlations (list): Correlations with minor key profiles.

    Returns:
    tuple: Key label and type ('Major' or 'Minor').
    """
    major_key = np.argmax(major_correlations)
    minor_key = np.argmax(minor_correlations)

    if max(major_correlations) > max(minor_correlations):
        return chroma_labels[major_key], "Major"
    else:
        return chroma_labels[minor_key], "Minor"

def format_key_output(key, key_type):
    """
    Formats the detected key and type into a human-readable string.

    Parameters:
    key (str): Key label ('C', 'C#', etc.).
    key_type (str): Key type ('Major' or 'Minor').

    Returns:
    str: Formatted string of the key and type in French.
    """
    key_fr = key_mapping.get(key, "Unknown key")
    key_type_fr = key_type_mapping.get(key_type, "Unknown type")

    return f"{key} {key_type} ({key_fr} {key_type_fr})"

def print_correlations(correlations, key_type):
    """
    Prints the correlations of each key with the specified key type.

    Parameters:
    correlations (list): List of correlations.
    key_type (str): Key type ('Major' or 'Minor').
    """
    key_type_fr = key_type_mapping.get(key_type, "Unknown type")
    max_key_length = max(len(key) for key in chroma_labels)
    max_key_fr_length = max(len(key_mapping.get(key, "Unknown key")) for key in chroma_labels)
    max_type_length = max(len("Major"), len("Minor"))

    for key, correlation in zip(chroma_labels, correlations):
        key_fr = key_mapping.get(key, "Unknown key")
        key_padding = ' ' * (max_key_length - len(key) + 1)
        key_fr_padding = ' ' * (max_key_fr_length - len(key_fr) + 1)
        type_padding = ' ' * (max_type_length - len(key_type) + 1)

        # Add a space before positive correlations.
        correlation_str = f"{correlation:.3f}"
        if correlation >= 0:
            correlation_str = " " + correlation_str

        print(f"{key}{key_padding}{key_type}{type_padding}({key_fr}{key_fr_padding}{key_type_fr}) | {correlation_str}")

def select_analysis_type():
    """
    Prompts the user to select the type of analysis.

    Returns:
    int: Chosen analysis type (1 for standard, 2 for detailed).
    """
    print("\nPlease select the type of analysis you want to perform:\n")
    print("1. Standard analysis (dominant key)")
    print("2. Detailed analysis (key correlations)")

    while True:
        try:
            analysis_choice = int(input("\nEnter the number of your choice: "))
            if analysis_choice in [1, 2]:
                return analysis_choice
            else:
                print("Invalid choice. Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def analyze_music(mp3_path, analysis_choice):
    """
    Analyzes the music file based on the chosen analysis type.

    Parameters:
    mp3_path (str): Path to the MP3 file.
    analysis_choice (int): Chosen analysis type (1 for standard, 2 for detailed).
    """
    major_correlations, minor_correlations = detect_key(mp3_path)

    if analysis_choice == 1:
        key, key_type = determine_key(major_correlations, minor_correlations)
        print(f"\nThe key of the file is {format_key_output(key, key_type)}.")
    elif analysis_choice == 2:
        print("\nMajor key correlations:\n")
        print_correlations(major_correlations, "Major")
        print("\nMinor key correlations:\n")
        print_correlations(minor_correlations, "Minor")

def main():
    """Main function to orchestrate the music key detection process."""
    mp3_files = list_mp3_files()
    mp3_path = select_mp3_file(mp3_files)
    analysis_choice = select_analysis_type()
    analyze_music(mp3_path, analysis_choice)
    print("\n|----------------------------------------------------------------------------------|\n")

if __name__ == "__main__":
    main()