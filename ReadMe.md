# Reproducibility Study for : Reproducibility Project: Predictive Multi-level Patient Representations from Electronic Health Records 
Paper Link : [link](https://arxiv.org/pdf/1911.05698v1.pdf)
Presentation Link: [Youtube](https://youtu.be/U5M4hE0m1sM)
## Dependencies:
- Python 3.6
- Keras
- Theono
- TensorFlow
- Sickit-Learn
- [keras-tcn](https://github.com/philipperemy/keras-tcn)

And all the dependencies mentioned in repositories used to sections below.

## Data Download & Processing

1. Download MIMIC-III Data Set from physionet website after requesting access and acquiring access.
2. Use main [MIMIC Github Repository](https://github.com/MIT-LCP/mimic-code/tree/main/mimic-iii/benchmark) to load the downloaded .csvs to postgres. This [video](https://www.youtube.com/watch?v=5rg1p7sg2Qo) is very helpful in installation of postgres and building MIMIC Demo Dataset and can be used for whole as well.
3. Then use this [repository's](https://github.com/illidanlab/urgent-care-comparative) instruction for use section.
    - You will need to create Folder structure
      - .../local_mimic
      - .../local_mimic/views
      - .../local_mimic/tables
      - .../local_mimic/save
      - .../local_mimic/save/checkpoint/Mortality/Retain
      - .../local_mimic/save/checkpoint/PotassiumLabtest/Retain
    - Updated Sqls for required pivot related views and for potassium dataset for postgres run are available in SQL folder of this repository.
    - Updated code for preprocessing.py is available under Data Processing Folder of this repository.
4. Then use installation instruction section in this [repository](https://github.com/mp2893/retain). Updated Script available in Data Processing Folder in this repository. [process_mimic.py, process_potassium.py]

## Model Build and Evaluation
Notebooks folder contain:
- utilities.py which is used by other notebooks
- DeathSet.ipynb : Contains implementations, model training and validations for LR, SVM, LSTM, TCN, MRM for Mortality Dataset
- PotassiumAbnormalityDataset.ipynb : Contains implementations, model training and validations for LR, SVM, LSTM, TCN, MRM for Potassium Dataset
- retain.py (code for version python 3.6) referenced from [RETAIN Github] (https://github.com/mp2893/retain)
- retainPotassium.py (code for version python 3.6) referenced from [RETAIN Github] (https://github.com/mp2893/retain)
