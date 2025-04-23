# DLH-Project-Reproduce-HurtfulWords
This page describes the steps that we executed to reproduce the paper "Hurtful Words: Quantifying Biases in Clinical Contextual Word Embeddings".
Original publication: [here](https://https://dl.acm.org/doi/abs/10.1145/3368555.3384448) 
Step1: Download the MIMIC3 data from the physionet.org site, you ca use the below command, provided you have gone through the training:
!wget -r -N -c -np --user userID --ask-password https://physionet.org/files/mimiciii/1.4/

And unzip them:
!unzip <input_location>/mimic-iii-clinical-database-1.4.zip -d <output_location>
