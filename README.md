# say-it-with-DNA
This command-line Python 3 application eases the access to use one of the most exciting data storage technologies of our time by providing rapid-prototyping-enabling access to established en- and decoding algorithms based on the library [Chamaeleo](https://github.com/ntpz870817/Chamaeleo). This contributes to further understanding of the algorithms’ strengths and weaknesses, and allows using various parameters.

### How to
#### Requirements: 
   * [Python 3](https://www.python.org/downloads/) installation
   * Download sayitwithDNA.py


#### Options
Five different algorithms are available for en- and decoding via the implemented library Chamaeleo: 
[Simple Code](https://www.researchgate.net/profile/George_Church/publication/230698422_Next-Generation_Digital_Information_Storage_in_DNA/links/550c03e60cf2b2450b4e5103/Next-Generation-Digital-Information-Storage-in-DNA.pdf), [Goldman Code](https://www.nature.com/articles/nature11875), [Grass Code](https://www.researchgate.net/publication/272029638_Robust_Chemical_Preservation_of_Digital_Information_on_DNA_in_Silica_with_Error-Correcting_Codes), [Fountain Code](https://www.biorxiv.org/content/10.1101/074237v4.full.pdf), [Yin-Yang Code](https://www.biorxiv.org/content/biorxiv/early/2020/02/20/829721.full.pdf). 
In addition, a Reed-Solomon or Hamming Correction can be added to each process.

#### Example

The program can be used from the terminal. Here is a simple example of how to encode and decode a file using the Goldman code.

<samp>$ python sayitwithDNA.py --mode encode --algorithm GoldmanCode --input_path /Users/name/file.gif --output_path /Users/name/file.dna

<samp>$ python sayitwithDNA.py --mode decode --algorithm GoldmanCode --input_path /Users/name/file.dna --output_path /Users/name/file.gif


See "[Command Line Arguments.pdf](https://github.com/DNA-project/say-it-with-DNA/blob/master/Command%20Line%20Arguments.pdf)" for a detailed listing of all possible command line arguments and options.



If this repo helps or being used in your research, please refer to it.

