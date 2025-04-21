import argparse
import yaml
import os

from mimic3benchmark.mimic3csv import *
from mimic3benchmark.preprocessing import add_hcup_ccs_2015_groups, make_phenotype_label_matrix
from mimic3benchmark.util import dataframe_from_csv

parser = argparse.ArgumentParser(description='Extract per-subject data from MIMIC-III CSV files.')
parser.add_argument('mimic3_path', type=str, help='Directory containing MIMIC-III CSV files.')
parser.add_argument('output_path', type=str, help='Directory where per-subject data should be written.')
parser.add_argument('--event_tables', '-e', type=str, nargs='+', help='Tables from which to read events.',
                    default=['CHARTEVENTS', 'LABEVENTS', 'OUTPUTEVENTS'])
parser.add_argument('--phenotype_definitions', '-p', type=str,
                    default=os.path.join(os.path.dirname(__file__), '../resources/hcup_ccs_2015_definitions.yaml'),
                    help='YAML file with phenotype definitions.')
parser.add_argument('--itemids_file', '-i', type=str, help='CSV containing list of ITEMIDs to keep.')
parser.add_argument('--verbose', '-v', dest='verbose', action='store_true', help='Verbosity in output')
parser.add_argument('--quiet', '-q', dest='verbose', action='store_false', help='Suspend printing of details')
parser.set_defaults(verbose=True)
parser.add_argument('--test', action='store_true', help='TEST MODE: process only 1000 subjects, 1000000 events.')
args, _ = parser.parse_known_args()

try:
    os.makedirs(args.output_path)
except:
    pass

patients = read_patients_table(args.mimic3_path)
admits = read_admissions_table(args.mimic3_path)
stays = read_icustays_table(args.mimic3_path)
if args.verbose:
    print('START:\n\tICUSTAY_IDs: {}\n\tHADM_IDs: {}\n\tSUBJECT_IDs: {}'.format(stays.ICUSTAY_ID.unique().shape[0],
          stays.HADM_ID.unique().shape[0], stays.SUBJECT_ID.unique().shape[0]))

stays = remove_icustays_with_transfers(stays)
if args.verbose:
    print('REMOVE ICU TRANSFERS:\n\tICUSTAY_IDs: {}\n\tHADM_IDs: {}\n\tSUBJECT_IDs: {}'.format(stays.ICUSTAY_ID.unique().shape[0],
          stays.HADM_ID.unique().shape[0], stays.SUBJECT_ID.unique().shape[0]))

stays = merge_on_subject_admission(stays, admits)
stays = merge_on_subject(stays, patients)
stays = filter_admissions_on_nb_icustays(stays)
if args.verbose:
    print('REMOVE MULTIPLE STAYS PER ADMIT:\n\tICUSTAY_IDs: {}\n\tHADM_IDs: {}\n\tSUBJECT_IDs: {}'.format(stays.ICUSTAY_ID.unique().shape[0],
          stays.HADM_ID.unique().shape[0], stays.SUBJECT_ID.unique().shape[0]))

stays = add_age_to_icustays(stays)
stays = add_inunit_mortality_to_icustays(stays)
stays = add_inhospital_mortality_to_icustays(stays)
stays = filter_icustays_on_age(stays)
if args.verbose:
    print('REMOVE PATIENTS AGE < 18:\n\tICUSTAY_IDs: {}\n\tHADM_IDs: {}\n\tSUBJECT_IDs: {}'.format(stays.ICUSTAY_ID.unique().shape[0],
          stays.HADM_ID.unique().shape[0], stays.SUBJECT_ID.unique().shape[0]))

stays.to_csv(os.path.join(args.output_path, 'all_stays.csv'), index=False)
diagnoses = read_icd_diagnoses_table(args.mimic3_path)
diagnoses = filter_diagnoses_on_stays(diagnoses, stays)
diagnoses.to_csv(os.path.join(args.output_path, 'all_diagnoses.csv'), index=False)
count_icd_codes(diagnoses, output_path=os.path.join(args.output_path, 'diagnosis_counts.csv'))

phenotypes = add_hcup_ccs_2015_groups(diagnoses, yaml.safe_load(open(args.phenotype_definitions, 'r')))

make_phenotype_label_matrix(phenotypes, stays).to_csv(os.path.join(args.output_path, 'phenotype_labels.csv'),
                                                      index=False, quoting=csv.QUOTE_NONNUMERIC)

# Select a consistent subset of 3,300 patients
custom_subjects_df = pd.read_csv('/content/drive/MyDrive/Payel-DLH-related/DataFiles/cleaned_data/data.csv')  # Replace with actual path
selected_subjects = custom_subjects_df['subject_id'].drop_duplicates()

# Filter all relevant dataframes to keep only selected patients
patients = patients[patients.SUBJECT_ID.isin(selected_subjects)]
stays = stays[stays.SUBJECT_ID.isin(selected_subjects)]
diagnoses = diagnoses[diagnoses.SUBJECT_ID.isin(selected_subjects)]
phenotypes = phenotypes[phenotypes.SUBJECT_ID.isin(selected_subjects)]

print(f'Using only {stays.shape[0]} ICU stays and {selected_subjects.nunique()} unique patients.')

output_dir = '/content/drive/MyDrive/Payel-DLH-related/DataFiles/WiderSampledFiles/'

# Save filtered tables as CSV files
patients.to_csv(os.path.join(output_dir, 'filtered_patients.csv'), index=False)
stays.to_csv(os.path.join(output_dir, 'filtered_stays.csv'), index=False)
diagnoses.to_csv(os.path.join(output_dir, 'filtered_diagnoses.csv'), index=False)
phenotypes.to_csv(os.path.join(output_dir, 'filtered_phenotypes.csv'), index=False)

# Process stays and diagnoses for selected patients
break_up_stays_by_subject(stays, args.output_path, subjects=selected_subjects)
break_up_diagnoses_by_subject(phenotypes, args.output_path, subjects=selected_subjects)

# Handle event tables while ensuring consistency
items_to_keep = set(
    [int(itemid) for itemid in dataframe_from_csv(args.itemids_file)['ITEMID'].unique()]
) if args.itemids_file else None

for table in args.event_tables:
    read_events_table_and_break_up_by_subject(
        args.mimic3_path, table, args.output_path,
        items_to_keep=items_to_keep,
        subjects_to_keep=selected_subjects  # Ensures only selected patients are included
    )
