# DLH-Project-Reproduce-HurtfulWords
This page describes the steps that we executed to reproduce the paper "Hurtful Words: Quantifying Biases in Clinical Contextual Word Embeddings".

Original publication: [here](https://https://dl.acm.org/doi/abs/10.1145/3368555.3384448) 


Please note that we ran all the steps on Google Colab and thus have also given the steps to run on Google Colab. For other environments, please change them accordingly.

**Step 1: Data Downloads and Decompress**

- **i.** Download the MIMIC-III data from [physionet.org](https://physionet.org/), provided you've completed the required training:   

  ```python
  !wget -r -N -c -np --user userID --ask-password https://physionet.org/files/mimiciii/1.4/
  ```


- **ii.** And unzip them:  

  ```
  !unzip <input_location>/mimic-iii-clinical-database-1.4.zip -d <output_location>
  ```

**Step 2: Create the MIMIC3 BENCHMARK directory structure** 
We did this step to be able to get the phenotyping label related file. You can either follow the instructions on [this GitHub link](https://github.com/YerevaNN/mimic3-benchmarks) to create the "mimic3-benchmark" folder structure and the files within, by going through the below steps, or run our notebook directly on Google Colab which runs all these steps at one pleace.

- **i.** Clone the GitHub Repository:
  
  ```python
  !git clone https://github.com/YerevaNN/mimic3-benchmarks/
  %cd '<your_location>/mimic3-benchmarks/
  ```

- **ii.** Install the requirements with  the below command (The requirements.txt file that comes within the cloned repository states outdated versions. We used latest versions while running on Google Colab, and those are listed in the requirements.txt on this GitHub page within "mimic3-benchmark/mimicbenchmark" folder.

  ```python
  pip install -r requirements.txt
  ```

- iii. Follow all 5 steps under "Building the benchmark". Please note that to reproduce our code and results, you will have to download the extract_subject.py from our folder "mimic3-benchmark/mimicbenchmark/scripts" where we process and proceed with subjects that we have gathered notes data for.

OR run the below script cell by cell on Google Colab:

mimic_benchmark_preprocessing.ipynb 

**Step 3: Download the MIMIC files**
  
