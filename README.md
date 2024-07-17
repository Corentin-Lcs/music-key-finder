<h1 align="center">Music Key Finder</h1>

The "Music Key Finder" GitHub project is designed to help musicians, analysts, and enthusiasts identify the musical key of any given audio file. Using advanced algorithm and signal processing techniques, this tool analyzes the harmonic content of the audio and determines its key, making it easier for users to understand and work with music.

<p align="center">
  <img src="https://github.com/Corentin-Lcs/music-key-finder/blob/main/The_Fourth_Art.png" alt="The_Fourth_Art.png"/>
</p>

## Installation

To install the `librosa` module from the command prompt, run the following command:

```
pip install librosa
```

> To learn more about the features of the module, here is a useful link:
> 
> https://librosa.org/doc/latest/index.html [EN]

## Krumhansl-Schmuckler Key-Finding Algorithm

### Overview

The Krumhansl-Schmuckler key-finding algorithm is a widely-used computational model designed to analyze musical pieces and determine their key. Developed by Carol Krumhansl and Edward Schmuckler, this algorithm is based on the concept of tonal hierarchies, which posits that certain tones are perceived as more stable or central within a given key. The algorithm leverages these tonal hierarchies to compute the most likely key of a piece of music by comparing the distribution of pitch classes in the music to pre-defined key profiles.

### How It Works

The Krumhansl-Schmuckler key-finding algorithm operates through the following steps:

1. **Pitch Class Profile (PCP) Calculation**:
   - The musical piece is analyzed to extract the frequencies or durations of each pitch class (e.g., C, C#, D, etc.).
   - These values are aggregated to form a PCP, a vector representing the distribution of pitch classes in the piece.

2. **Correlation With Key Profiles**:
   - The PCP is compared against pre-defined key profiles for all major and minor keys. These key profiles represent the ideal distribution of pitch classes for each key.
   - The comparison involves calculating a correlation coefficient between the PCP and each key profile, resulting in a set of correlation values.

3. **Key Determination**:
   - The key with the highest correlation value is identified as the most likely key of the musical piece.

## Implementation Details

During the development of this project, particular attention was given to implementing the Krumhansl-Schmuckler key-finding algorithm efficiently and accurately. Here’s a detailed outline of the steps and considerations involved.

### General Formula For Pearson Correlation Coefficient

The core of the Krumhansl-Schmuckler algorithm relies on calculating the Pearson correlation coefficient between the pitch profile $`P`$ of the musical passage and the key profile $`K`$. This formula, applicable to any number of notes $`N`$, ensures robust key detection:

<p align="center">
  <img src="https://github.com/Corentin-Lcs/music-key-finder/blob/main/Formula A.png" alt="Formula A.png"/>
</p>

where:
- $`P_i`$ is the frequency of the $`i`$-th note in the musical passage.
- $`K_i`$ is the value of the $`i`$-th element in the key profile.
- $`\bar{P}`$ is the mean of the values in $`P`$.
- $`\bar{K}`$ is the mean of the values in $`K`$.

### Detailed Formula Application

To compute $`\bar{P}`$ and $`\bar{K}`$:

```math
\bar{P} = \frac{1}{n} \sum_{i=1}^{n} P_i
```

```math
\bar{K} = \frac{1}{n} \sum_{i=1}^{n} K_i
```

These means are essential for normalizing the data and ensuring the correlation calculation reflects the relative contributions of each note or pitch class.

### Calculation Of Means

The detailed implementation involves substituting the means into the correlation formula:

<p align="center">
  <img src="https://github.com/Corentin-Lcs/music-key-finder/blob/main/Formula B.png" alt="Formula B.png"/>
</p>

This approach ensures that the algorithm is adaptable to different musical systems, accommodating various numbers of notes or pitch classes beyond the traditional 12-tone chromatic scale.

### Integration Into The Algorithm

For each potential key $`T`$, the algorithm computes $`R(P, K_T)`$, where $`K_T`$ represents the key profile for key $`T`$. The key with the highest correlation value $`R(P, K_T)`$ is identified as the most probable key of the musical passage:

```math
T_{\text{optimal}} = \arg\max_{T} \left( R(P, K_T) \right)
```

By following these steps, the Krumhansl-Schmuckler key-finding algorithm achieves a systematic and empirical approach to key detection. Its reliance on tonal hierarchies and statistical correlation ensures a high level of accuracy and robustness across different musical genres and styles, making it a versatile and preferred method in the field of computational music analysis for musicians and analysts alike.

## Further Information

Two annexed documents are attached to the project:

- A pedagogical music theory lesson (simplified, discovery) on the major notions of music, written by me [[FR]](https://github.com/Corentin-Lcs/music-key-finder/blob/main/L%E2%80%99Art%20de%20la%20Musique%20-%20Music%20Theory%20Lessons.pdf)
- An article, a very interesting study on the Krumhansl-Schmuckler Key-Finding algorithm [[EN]](https://github.com/Corentin-Lcs/music-key-finder/blob/main/Krumhansl-Schmuckler%20Key-Finding%20Algorithm%20-%20Article.pdf)

> [!TIP]
> If you have a curious profile, reading these two documents is a good thing.

## Project's Structure

```
music-key-finder/
├─ README.md
├─ LICENSE
├─ Formula A.png
├─ Formula B.png
├─ The_Fourth_Art.png
├─ L’Art de la Musique - Music Theory Lessons.pdf
├─ Krumhansl-Schmuckler Key-Finding Algorithm - Article.pdf
└─ src/
   ├─ script.py
   └─ Miroirs No. 3, Une Barque Sur L'Océan (Maurice Ravel).mp3
```

## Meta

Created by [@Corentin-Lcs](https://github.com/Corentin-Lcs). Feel free to contact me !

Distributed under the GNU GPLv3 license. See [LICENSE](https://github.com/Corentin-Lcs/music-key-finder/blob/main/LICENSE) for more information.
