# This script processes MIMIC-III dataset and builds longitudinal diagnosis records for patients with at least two visits.
# The output data are cPickled, and suitable for training Doctor AI or RETAIN
# Written by Edward Choi (mp2893@gatech.edu)
# Usage: Put this script to the foler where MIMIC-III CSV files are located. Then execute the below command.
# python process_mimic.py ADMISSIONS.csv DIAGNOSES_ICD.csv PATIENTS.csv <output file> 

# Output files
# <output file>.pids: List of unique Patient IDs. Used for intermediate processing
# <output file>.PotAbnFlgs: List of binary values indicating the mortality of each patient
# <output file>.dates: List of List of Python datetime objects. The outer List is for each patient. The inner List is for each visit made by each patient
# <output file>.seqs: List of List of List of integer diagnosis codes. The outer List is for each patient. The middle List contains visits made by each patient. The inner List contains the integer diagnosis codes that occurred in each visit
# <output file>.types: Python dictionary that maps string diagnosis codes to integer diagnosis codes.

import sys
import pickle
from datetime import datetime

def convert_to_icd9(dxStr):
    if dxStr.startswith('E'):
        if len(dxStr) > 4: return dxStr[:4] + '.' + dxStr[4:]
        else: return dxStr
    else:
        if len(dxStr) > 3: return dxStr[:3] + '.' + dxStr[3:]
        else: return dxStr
	
def convert_to_3digit_icd9(dxStr):
    if dxStr.startswith('E'):
        if len(dxStr) > 4: return dxStr[:4]
        else: return dxStr
    else:
        if len(dxStr) > 3: return dxStr[:3]
        else: return dxStr

if __name__ == '__main__':
    admissionFile = 'local_mimic/tables/admissions.csv'
    diagnosisFile = 'local_mimic/tables/diagnoses_icd.csv'
    patientsFile = 'local_mimic/tables/PATIENTS.csv'
    potassiumAbnFile = 'local_mimic/views/labtest_dataset.csv'
    outFile = 'local_mimic/save/'
    
    print('Collecting mortality information')
    pidPotAbnMap = {}
    infd = open(potassiumAbnFile, 'r')
    infd.readline()
    for line in infd:
        tokens = line.strip().split(',')
        pid = int(tokens[0])
        PotAbn = tokens[30]
        if len(PotAbn) > 0:
            pidPotAbnMap[pid] = 1
        else:
            pidPotAbnMap[pid] = 0
    infd.close()
    
    print( 'Building pid-admission mapping, admission-date mapping')
    pidAdmMap = {}
    infd = open(potassiumAbnFile, 'r')
    infd.readline()
    for line in infd:
        tokens = line.strip().split(',')
        pid = int(tokens[0])
        admId = int(tokens[1])
        if pid in pidAdmMap: pidAdmMap[pid].append(admId)
        else: pidAdmMap[pid] = [admId]
    infd.close()
    
    
    print( 'Building admission-dxList mapping')
    admDxMap = {}
    admDxMap_3digit = {}
    infd = open(diagnosisFile, 'r')
    infd.readline()
    for line in infd:
        tokens = line.strip().split(',')
        admId = int(tokens[2])
        dxStr = 'D_' + convert_to_icd9(tokens[4][1:-1]) ############## Uncomment this line and comment the line below, if you want to use the entire ICD9 digits.
        dxStr_3digit = 'D_' + convert_to_3digit_icd9(tokens[4][1:-1])
        
        if admId in admDxMap:
            admDxMap[admId].append(dxStr)
        else: 
            admDxMap[admId] = [dxStr]
        
        if admId in admDxMap_3digit: 
            admDxMap_3digit[admId].append(dxStr_3digit)
        else: 
            admDxMap_3digit[admId] = [dxStr_3digit]
    infd.close()
    
    print( 'Building pid-sortedVisits mapping')
    pidSeqMap = {}
    pidSeqMap_3digit = {}
    for pid, admIdList in pidAdmMap.items():
        print(len(admIdList))
        if len(admIdList) < 2: continue
        
        sortedList = sorted([ admDxMap[admId] for admId in admIdList])
        pidSeqMap[pid] = sortedList
        
        sortedList_3digit = sorted([admDxMap_3digit[admId] for admId in admIdList])
        pidSeqMap_3digit[pid] = sortedList_3digit  
    
    print ('Building pids, dates, mortality_labels, strSeqs')
    pids = []
    PotAbnSeqs = []
    PotAbnFlgs = []
    for pid, visits in pidSeqMap.items():
        pids.append(pid)
        PotAbnFlgs.append(pidPotAbnMap[pid])
        seq = []
        for visit in visits:
            seq.append(visit[0])
        PotAbnSeqs.append(seq)
    
    print('Building pids, dates, strSeqs for 3digit ICD9 code')
    PotAbnSeqs_3digit = []
    for pid, visits in pidSeqMap_3digit.items():
        seq = []
        for visit in visits:
            seq.append(visit[0])
        PotAbnSeqs_3digit.append(seq)
    
    print('Converting strSeqs to intSeqs, and making types')
    types = {}
    PotAbnNewSeqs = []
    for patient in PotAbnSeqs:
        newPatient = []
        for visit in patient:
            newVisit = []
            for code in visit:
                if code in types:
                    newVisit.append(types[code])
                else:
                    types[code] = len(types)
                    newVisit.append(types[code])
            newPatient.append(newVisit)
        PotAbnNewSeqs.append(newPatient)
    
    
    print('Converting strSeqs to intSeqs, and making types for 3digit ICD9 code')
    PotAbnTypes_3digit = {}
    PotAbnNewSeqs_3digit = []
    for patient in PotAbnSeqs_3digit:
        newPatient = []
        for visit in patient:
            newVisit = []
            for code in set(visit):
                if code in PotAbnTypes_3digit:
                    newVisit.append(PotAbnTypes_3digit[code])
                else:
                    PotAbnTypes_3digit[code] = len(PotAbnTypes_3digit)
                    newVisit.append(PotAbnTypes_3digit[code])
            newPatient.append(newVisit)
        PotAbnNewSeqs_3digit.append(newPatient)
    
    pickle.dump(pids, open(outFile+'potpids', 'wb'), -1)
    pickle.dump(PotAbnFlgs, open(outFile+'PotAbnFlgs', 'wb'), -1)
    pickle.dump(PotAbnSeqs, open(outFile+'PotAbnSeqs', 'wb'), -1)
    pickle.dump(types, open(outFile+'pottypes', 'wb'), -1)
    pickle.dump(PotAbnNewSeqs_3digit, open(outFile+'pot3digitICD9.seqs', 'wb'), -1)
    pickle.dump(PotAbnTypes_3digit, open(outFile+'pot3digitICD9.types', 'wb'), -1)
 
 
