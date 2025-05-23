# Hurtful Words: Quantifying Biases in Clinical Contextual Word Embeddings

This page describes the steps that we executed to reproduce the paper "Hurtful Words: Quantifying Biases in Clinical Contextual Word Embeddings".

Original publication: https://dl.acm.org/doi/abs/10.1145/3368555.3384448  

If you use this code in your research, please cite the following publication:

Haoran Zhang, Amy X. Lu, Mohamed Abdalla, Matthew McDermott, and Marzyeh Ghassemi. 2020.
Hurtful words: quantifying biases in clinical contextual word embeddings.
In Proceedings of the ACM Conference on Health, Inference, and Learning (CHIL ’20).
Association for Computing Machinery, New York, NY, USA, 110–120.
A publically available version of this paper is also on arXiv.

A publically available version of this paper is also on arXiv-> https://arxiv.org/abs/2003.11515  

We referred to the links: 
https://github.com/MLforHealth/HurtfulWords  
and   
https://github.com/YerevaNN/mimic3-benchmarks  


In this paper, we have tried to reproduce and prove that contextual word embeddings can create bias to favor certain demographic groups over others. We have used the pretrained baseline and adversarial debiased models from the original paper first to capture the embeddings using masked real clinical notes and letting the model fill the masked blanks, and eventually create a log probability bias score quantification. Secondly, use the same models to read the real preprocessed clinical notes to predict the 25 phenotype labels and compare them against the truth labels, come up with fairness metrics of recall, parity, and specificity, and compare these performance metrics against different demographic subgroups. As an extra step, we also fine-tuned the pretrained baseline model with one set of data and then evaluated the same model on another dataset, and later created quantification of the same performance gaps across intersectional demographics (extension to the paper, the original paper did not explore intersectional demographic performance gaps). <br>

Please note that we ran all the steps on Google Colab and thus have also given the steps to run on Google Colab. For other environments, please change them accordingly. <br><br>
**Pretrained Models**
The pretrained BERT models used in our experiments are available to download here:
- [Baseline_Clinical_BERT](https://www.cs.toronto.edu/pub/haoran/hurtfulwords/baseline_clinical_BERT_1_epoch_512.tar.gz)
- [Adversarially_Debiased_Clinical_BERT (Gender)](https://www.cs.toronto.edu/pub/haoran/hurtfulwords/adv_clinical_BERT_1_epoch_512.tar.gz) <br><br>

**Reproducibility**
  You can follow the steps on ```python DLH-Project-Reproduce-HurtfulWords/test_hurtful_words.ipynb ```<br><br>
Here are the Steps in details: <br><br>
**Step 0: Environment and Prerequisites**

- Run the following commands to clone this repo and install the dependencies.

```python
git clone https://github.com/zelal-Eizaldeen/DLH-Project-Reproduce-HurtfulWords.git
cd DLH-Project-Reproduce-HurtfulWords/
pip install -r requirements.txt
```
**Step 1: Data Downloads and Decompress**

- **i.** Download the MIMIC-III data from [physionet.org](https://physionet.org/), provided you've completed the required training:   

  ```python
  !wget -r -N -c -np --user userID --ask-password https://physionet.org/files/mimiciii/1.4/
  ```


- **ii.** And unzip them:  

  ```
  !unzip <input_location>/mimic-iii-clinical-database-1.4.zip -d <output_location>
  ```

**Step 2: Dataset Preprocessing**  

Run DLH-Project-Reproduce-HurtfulWords/preprocessing_dataset.ipynb cells. 

`preprocessing_dataset.ipynb`  
  


<br><br>  

Now we tried reproducing two parts of the paper:

1. We identified dangerous latent relationships that are captured by the contextual word embeddings using a fill-in-the-blank method with text from real clinical notes and a log probability bias score quantification.
2. We evaluated performance gaps across different definitions of fairness on several downstream clinical prediction tasks, including the detection of acute and chronic conditions.


To reproduce the first point, follow steps 3 and 4 as given below:

**Step 3: Filtering and Tokenizing notes**  

Run the below script to limit notes(obtained from step 2) to the types: "Nursing", "Nursing/other", "Physician", and "Discharge summary". Next, concatenate note subsequences starting from the end of each patient’s period of interest, working backwards, until we reach a limit of 30 subsequences. Then restrict notes within the first 48 hours of ICU stay. Deidentify the PII information and drop outpatient notes.

  `filtering_tokenizing_notes.ipynb`

**Step 4: Masking Gender terms and Comparing Log Probability Bias Scores**  


Run the below script to MASK tokens in place of gender terms, calculate the log probability for males and females using the pretrained clinical base line model, compare the log probabilities and derive a bias score:  

 `fill_in_the_blank.ipynb`


To reproduce the second point, follow steps 5, 6, and 7 as given below:  

**Step 5: Create the MIMIC3 BENCHMARK directory structure** 
This step creates the "mimic3-benchmarks" folder structure and "phenotyping folder" within, using the downloaded files- D ICD DIAGNOSES, DIAGNOSES ICD, ICUSTAYS, PATIENTS, and ADMISSIONS and used joins between each of them to relate each subject to the diagnosis labels, across all admissions. We have followed all the steps 1-5 from this Github page:  [MIMIC-benchmarks repository](https://github.com/YerevaNN/mimic3-benchmarks) to create the "mimic3-benchmarks" folder structure. 

Run our script below on Google Colab to clone their Github and run all steps. Just please note that you would need to use our extract_subjects.py from DLH-Project-Reproduce-HurtfulWords/mimic3-benchmarks/mimic3benchmark/scripts path and our requirements.txt from DLH-Project-Reproduce-HurtfulWords/mimic3-benchmarks path.

`mimic3_benchmark_preprocessing.ipynb`  


**Step 6: Evaluate the pretrained models to calculate the performance gaps**  


This step is using the output from step 5- dataset files (mainly listfile.csv) from phenotyping folder within mimic3-benchmarks/data folder, and the output from step 5 above which is demographic file with cleaned and filtered notes. These two sources are joined to get the 25 phenotype labels per subject with their demographic data and notes. In this script, we tokenize the notes using BertTokenizer, create dataset and use our dataset to evaluate the pretrained baseline clinical model. Then we calculate fairness metrics to report the count of tasks that show statistically significant differences within each subgroup (Male vs. Female, or English vs. Other, etc.), and also calculate percentage of significant tasks which favor a subgroup. We also repeat the process with the Pretrained Adversarially Debiased model to report the similar metrics and compare the gender performance gaps between baseline and Debiased.

Run the below script:  

`fairness_metric_recreation_using_pretrained_model_withadversarial.ipynb`



**Step 7: Fine-tune the pretrained baseline model and evaluate on another dataset, and then calculate the performance gaps**  


This step is using the same sources as step 6 is using. In this script, we tokenize both the train dataset and test dataset notes using BertTokenizer, create datasets, fine-tune the pretrained baseline model with the train dataset, and evaluate the model on our test dataset. Then we calculate same fairness metrics as described above in step 7. As an extension to the project, we also find the same fairness metrics across inter-sectional demographic groups, like Gender x Ethnicity.

Run the below script:  

`fairness_metric_recreation_after_finetuning_of_preatrained_model_&_evaluation_with_extension.ipynb`



