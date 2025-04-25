# Hurtful Words: Quantifying Biases in Clinical Contextual Word Embeddings

This page describes the steps that we executed to reproduce the paper "Hurtful Words: Quantifying Biases in Clinical Contextual Word Embeddings".

Original publication: [here](https://https://dl.acm.org/doi/abs/10.1145/3368555.3384448) 

In this paper, we have tried to reproduce and prove that contextual word embeddings can create bias to favor certain demographic groups over others. We have used the pretrained baseline and adversarial debiased models from the original paper first to capture the embeddings using masked real clinical notes and letting the model fill the masked blanks, and eventually create a log probability bias score quantification. Secondly, use the same models to read the real preprocessed clinical notes to predict the 25 phenotype labels and compare them against the truth labels, come up with fairness metrics of recall, parity, and specificity, and compare these performance metrics against different demographic subgroups. As an extra step, we also fine-tuned the pretrained baseline model with one set of data and then evaluated another dataset using the same model, and later created quantification of the same performance gaps across intersectional demographics.

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

**Step 2: Download the MIMIC files**  

Run the below script that uses these downloaded files PATIENTS, ADMISSIONS, DIAGNOSES ICD, ICUSTAYS, and NOTEEVENTS and joins them and does some processing of some of its fields.  
`preprocessing_dataset.ipynb`

**Step 3: Create the MIMIC3 BENCHMARK directory structure** 
This step creates the mimicbenchmark folder structure and "phenotyping folder" within, using the downloaded files- D ICD DIAGNOSES, DIAGNOSES ICD, ICUSTAYS, PATIENTS, and ADMISSIONS and used joins between each of them to relate each subject to the diagnosis labels, across all admissions. You can either follow the instructions on [this GitHub link](https://github.com/YerevaNN/mimic3-benchmarks) to create the "mimic3-benchmark" folder structure and the files within, by going through the below steps, or run our notebook directly on Google Colab which runs all these steps at one place. Whichever method you follow, please note that `extract_subjects.py` and `requirements.txt` would have to be downloaded from this GitHub page within "mimic3-benchmark/mimicbenchmark" folder.

- **i.** Clone the GitHub Repository:
  
  ```python
  !git clone https://github.com/YerevaNN/mimic3-benchmarks/
  %cd '<your_location>/mimic3-benchmarks/
  ```

- **ii.** Install the requirements with  the below command (The requirements.txt file that comes within the cloned repository states outdated versions. We used latest versions while running on Google Colab, and those are listed in the requirements.txt on this GitHub page within "mimic3-benchmark/mimicbenchmark" folder.

  ```python
  !pip install -r requirements.txt
  ```

- iii. Follow all 5 steps under "Building the benchmark". Please note that to reproduce our code and results, you will have to download the extract_subject.py from our folder "mimic3-benchmark/mimicbenchmark/scripts" where we process and proceed with subjects that we have gathered notes data for.

**OR** run the below script cell by cell on Google Colab:

`mimic3_benchmark_preprocessing.ipynb`  

**Step 4: Download the Pre-trained models**  

Download the Pretrained models from the original paper https://github.com/MLforHealth/HurtfulWords :

1. Baseline_Clinical_BERT
2. Adversarially_Debiased_Clinical_BERT (Gender)


Now we tried reproducing two parts of the paper:

1. We identified dangerous latent relationships that are captured by the contextual word embeddings using a fill-in-the-blank method with text from real clinical notes and a log probability bias score quantification.
2. We evaluated performance gaps across different definitions of fairness on several downstream clinical prediction tasks, including the detection of acute and chronic conditions.


To reproduce the first one, follow steps 5 and 6 as given below:

**Step 5: Filtering and Tokenizing notes**  

Run the below script to limit notes(obtained from step 2) to the types: "Nursing", "Nursing/other", "Physician", and "Discharge summary". Next, concatenate note subsequences starting from the end of each patient’s period of interest, working backwards, until we reach a limit of 30 subsequences. Then restrict notes within the first 48 hours of ICU stay. Deidentify the PII information and drop outpatient notes.

  `filtering_tokenizing_notes.ipynb`

**Step 6: Masking Gender terms and Comparing Log Probability Bias Scores**  


Run the below script to MASK tokens in place of gender terms, calculate the log probability for males and females using the pretrained clinical base line model, compare the log probabilities and derive a bias score:  

 `Final_ResultsLogP_Gender.ipynb`


To reproduce the second part, follow steps 7 and 8 as given below:  

**Step 7: Evaluate the pretrained models to calculate the performance gaps**  


This step is using the output from step 3- dataset files (mainly listfile.csv) from phenotyping folder within mimic3-benchmark/mimicbenchmark/data folder, and the outpu from step 5 above which is demographic file with cleaned and filtered notes. These two sources are joined to get the 25 phenotype labels per subject with their demographic data and notes. In this script, we tokenize the notes using BertTokenizer, create dataset and evaluate our dataset using the pretrained baseline clinical model. Then we calculate fairness metrics to report the count of tasks that show statistically significant differences within each subgroup (Male vs. Female, or English vs. Other, etc.), and also calculate percentage of significant tasks which favor a subgroup. We also repeat the process with the Pretrained Adversarially Debiased model to report the similar metrics and compare the gender performance gaps between baseline and Debiased.

Run the below script:  

`Fairness metric_recreation_using pretrained_model_withadversarial.ipynb`


**Step 8: Fine-tune the pretrained baseline model and evaluate on another dataset, and then calculate the performance gaps**  


This step is using the same sources as step 7 is using. In this script, we tokenize both the train dataset and test dataset notes using BertTokenizer, create datasets, fine-tune the pretrained baseline midel with the train dataset, and evaluate our test dataset using the model. Then we calculate same fairness metrics as described above in step 7. As an extension to the project, we also find the same fairness metrics across inter-sectional demographic groups, like Gender x Ethnicity.

Run the below script:  

`Fairness metric_recreation_after_finetuning_of_preatrained_model&_evaluation_with_extension.ipynb`


