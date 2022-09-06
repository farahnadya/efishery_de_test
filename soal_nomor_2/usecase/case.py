#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np


def main():
    data = get_data()
    komoditas = get_komoditas(data)
    komoditas.to_csv('komoditas.csv')
    list_komoditas = get_list_komoditas(data)
    unique_table = get_unique_table(data)
    group_1, group_2, group_3, group_4_3, group_5, group_6, group_7_4 = group(data)
    total_1 = total_satu(list_komoditas, group_1, group_2, group_3, group_5, group_6)
    total_2 = total_dua(group_4_3, group_7_4)
    total_all_data = total_all(total_1, total_2)
    print(total_all_data)

def get_data():
    path = "soal-2.json"
    data_init = pd.read_json(path)
    data = data_init.copy()
    data['komoditas'] = data['komoditas'].str.lower().str.replace('ikan', '').str.replace(' ', ',')
    data['berat'] = data['berat'].str.lower().str.replace('kg', '').str.replace(',', ' ').str.replace('-', ' ')
    return data

def get_komoditas(data):
    # get komoditas value#
    komoditas_init = data['komoditas']
    komoditas = pd.DataFrame(
        komoditas_init.str.split(',').apply(lambda x: pd.Series(x).value_counts()).sum()).reset_index().sort_values(
        by='index').reset_index(drop=True)
    return komoditas


def get_list_komoditas(data):
    # create komoditas columns #
    def create_columns(kom):
        x = pd.DataFrame()
        x[kom] = np.where(data.komoditas.str.contains(kom), 1, 0)
        return x[kom]

    # cleansing komoditas #
    data['komoditas'] = data['komoditas'].str.replace('gurami', 'gurame')
    data['komoditas'] = data['komoditas'].str.replace('majaer|muajir', 'mujaer')
    data['komoditas'] = data['komoditas'].str.replace('kerpu|krapu', 'kerapu')
    data['komoditas'] = data['komoditas'].str.replace('lelw', 'lele')
    data['komoditas'] = data['komoditas'].str.replace('nilem|nilaa', 'nila')
    data['komoditas'] = data['komoditas'].str.replace('salam', 'salem')
    data['komoditas'] = data['komoditas'].str.replace('tingkol|tngkol', 'tongkol')

    list = ['ayam', 'babat', 'bandeng', 'bebek', 'bawal', 'cakalang', 'cumi', 'mas', 'gurame', 'mujaer',
            'kakap', 'kembung', 'kepiting', 'kerang', 'kerapu', 'lele', 'nila', 'patin', 'salem', 'tongkol', 'udang']
    list_komoditas = pd.DataFrame()
    for i in list:
        list_komoditas[i] = create_columns(i)
    return list_komoditas

def get_unique_table(data):
    # define unique data['berat'] #
    unique_table = pd.DataFrame(data.berat.unique())
    return unique_table

def group(data):
    # group 1 #
    words_1 = ['rata', 'masing', 'kurang', 'kadang']
    pattern_1 = '|'.join(words_1)
    group_1 = data[(data.berat.str.contains(pattern_1, case=False)) & ~data.berat.str.contains('kecuali')]
    group_1['berat'] = group_1['berat'].str.replace('rata2|masing2|kadang2', '')
    group_1['berat'] = group_1['berat'].str.replace(r'([a-z,-]+)', '')
    group_1['berat'] = group_1['berat'].str.replace(r'\s', '')
    group_1['berat'] = group_1['berat'].fillna(value=1)

    # group 2#
    group_2 = data[(data.berat.str.contains(pattern_1, case=False)) & data.berat.str.contains('kecuali')]
    group_2['berat'] = group_2['berat'].str.replace('rata2|masing2|kadang2', '')
    group_2['berat'] = group_2['berat'].str.replace(r'([a-z,-]+)', '')
    group_2['berat'] = group_2['berat'].str.replace(r'\s', '')
    group_2['berat'] = group_2['berat'].fillna(1)

    # group 3#
    group_3 = data[(~data.berat.str.contains(pattern_1, case=False)) & data.berat.str.isnumeric()]

    list = ['ayam', 'babat', 'bandeng', 'bebek', 'bawal', 'cakalang', 'cumi', 'mas', 'gurame', 'mujaer',
            'kakap', 'kembung', 'kepiting', 'kerang', 'kerapu', 'lele', 'nila', 'patin', 'salem', 'tongkol', 'udang']
    pattern_2 = '|'.join(list)

    # group 5#
    group_5 = data[(~data.berat.str.contains(pattern_1, case=False)) & (
                ~data.berat.str.isnumeric() & ~data.berat.str.contains(pattern_2) & data.berat.str.contains(r'[a-z]'))]
    group_5['berat'] = group_5['berat'].str.replace(r'[a-z]', '')
    group_5['berat'] = group_5['berat'].str[0]

    group_6 = data[(~data.berat.str.contains(pattern_1, case=False)) & (
                ~data.berat.str.isnumeric() & ~data.berat.str.contains(pattern_2) & ~data.berat.str.contains(r'[a-z]'))]
    group_6['berat'] = group_6['berat'].str.replace(' ', ',').str.rstrip(',')
    group_6 = group_6[group_6['berat'].str.len() == 1]

    group_4 = data[(~data.berat.str.contains(pattern_1, case=False)) & (
                ~data.berat.str.isnumeric() & data.berat.str.contains(pattern_2))]
    group_4['komoditas'] = group_4['komoditas'].str.replace(r',,', ',')
    group_4['komoditas'] = group_4['komoditas'].str.replace(r',,', ',')

    group_4_1 = group_4.assign(komoditas=group_4['komoditas'].str.split(r',')).explode('komoditas')

    group_4_3 = pd.DataFrame([])
    for index, row in group_4_1.iterrows():
        # group_4_2 = pd.DataFrame()
        # group_4_2['komoditas'] = row['komoditas']
        string = row['berat']
        komoditas = row['komoditas']
        i = string.find(komoditas) + len(komoditas) + 1
        if string[i].isdigit():
            berat = string[i]
        else:
            berat = 0
        group_4_3 = group_4_3.append(pd.DataFrame({'komoditas': komoditas, 'berat': berat}, index=[0]), ignore_index=True)
        # group_4_2['komoditas'] = string[i]

    group_4_3 = group_4_3[group_4_3['komoditas'].isin(list)]

    group_7 = data[(~data.berat.str.contains(pattern_1, case=False)) & (
                ~data.berat.str.isnumeric() & ~data.berat.str.contains(pattern_2) & ~data.berat.str.contains(r'[a-z]'))]
    group_7['berat'] = group_7['berat'].str.replace(' ', ',').str.rstrip(',')
    group_7 = group_7[group_7['berat'].str.len() != 1]

    group_7['komoditas'] = group_7['komoditas'].str.replace(r',,', ',')
    group_7['komoditas'] = group_7['komoditas'].str.replace(r',,', ',')

    group_7_1 = group_7.copy()

    # indexing on komoditas
    group_7_2 = group_7_1.assign(komoditas=group_7_1['komoditas'].str.split(r',')).explode('komoditas')
    group_7_2 = group_7_2[['komoditas']]
    group_7_2 = group_7_2.reset_index()
    group_7_2['idx_grp'] = group_7_2.groupby(['index']).cumcount() + 1

    # indexing on berat
    group_7_3 = group_7_1.assign(berat=group_7_1['berat'].str.split(r',')).explode('berat')
    group_7_3 = group_7_3[['berat']]
    group_7_3 = group_7_3.reset_index()
    group_7_3['idx_grp'] = group_7_3.groupby(['index']).cumcount() + 1

    # join the dataframe
    group_7_4 = pd.merge(group_7_2, group_7_3, how='inner', left_on=['index', 'idx_grp'], right_on=['index', 'idx_grp'])

    group_7_4 = group_7_4[['komoditas', 'berat']]

    group_7_4 = group_7_4[group_7_4['komoditas'].isin(list)]

    group_7_4 = group_7_4[pd.to_numeric(group_7_4['berat'],errors='coerce').notnull()]
    return group_1, group_2, group_3, group_4_3, group_5, group_6, group_7_4

def total_satu(list_komoditas, group_1, group_2, group_3, group_5, group_6):
    pdList = [group_1, group_2, group_3, group_5, group_6]  # List of your dataframes
    set_group_1 = pd.concat(pdList)
    set_group_1 = set_group_1['berat']

    list_komoditas_group = list_komoditas.merge(set_group_1, left_index=True, right_index=True)

    # create komoditas columns #
    def sum_weight(x, kom):
        x[kom] = x[kom] * x['berat']
        return x[kom]

    list = ['ayam', 'babat', 'bandeng', 'bebek', 'bawal', 'cakalang', 'cumi', 'mas', 'gurame', 'mujaer',
            'kakap', 'kembung', 'kepiting', 'kerang', 'kerapu', 'lele', 'nila', 'patin', 'salem', 'tongkol', 'udang']
    list_komoditas_multiple = pd.DataFrame()
    for i in list:
        list_komoditas_multiple[i] = sum_weight(list_komoditas_group, i)

    total_1 = list_komoditas_multiple.stack().reset_index()
    total_1[0] = np.where((total_1[0] == '') | (total_1[0] == ' '), 0, total_1[0])
    total_1[0] = total_1[0].str.replace(',', '.')
    total_1[0] = total_1[0].astype(float)
    total_1[0] = total_1[0].fillna(0)
    total_1 = total_1.groupby('level_1').agg({0: 'sum'}).reset_index()
    total_1 = total_1.rename(columns={'level_1': 'komoditas', 0: 'berat'})
    return total_1

def total_dua(group_4_3, group_7_4):
    total_2 = pd.concat([group_4_3, group_7_4])

    # final cleansing for summary
    total_2['berat'] = total_2['berat'].str.replace('1/2', '0.5')
    total_2['berat'] = total_2['berat'].str.replace('', '0')
    total_2['berat'] = np.where(total_2['berat'] == '0+0', 0, total_2['berat'])
    total_2['berat'] = total_2['berat'].astype(float)
    total_2 = total_2.groupby('komoditas').agg({'berat': 'sum'}).reset_index()
    return total_2

def total_all(total_1, total_2):
    total_all = pd.concat([total_1, total_2]).reset_index(drop=True)
    total_all = total_all.groupby('komoditas').agg({'berat': 'sum'}).sort_values(by='berat', ascending=False).reset_index()
    return total_all