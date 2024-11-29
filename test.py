import pandas as pd

path = r"C:\Users\User\Downloads\NPS问卷 - Oct - Chinese Original.xlsx"
df_original = pd.read_excel(path, sheet_name = "原始问卷")
df_original.drop('国家',axis=1)

df_translation = pd.read_excel(path, sheet_name = "Translations")

en_dict = {}
pt_dict = {}

for column in df_translation.columns[1:]:
    en_dict[column] = df_translation.iloc[1][column]

for column in df_translation.columns[1:]:
    pt_dict[column] = df_translation.iloc[0][column]


pt_df = pd.DataFrame()
en_df = pd.DataFrame()

for column in df_translation.columns[1:]:

    # CHECK IF IT IS A VALUE OF A COLUMN NAME
    if column[0] == 'v' or column[0] == 'V':
        if column[-1] == "月":
            pt_df[current_column] = pt_df[current_column].str.replace('月','',regex=False)
        else:

            value = column[2:]
            pt_df[current_column].replace(value.split('.')[0],pt_dict[column],inplace=True)

    else:
        current_column = pt_dict[column]
        pt_df[current_column] = df_original[column]


for column in df_translation.columns[1:]:
    if column[0] == 'v' or column[0] == 'V':
        if column[-1] == "月":
            en_df[current_column] = en_df[current_column].str.replace('月','',regex=False)
        else:
            value = column[2:]
            if current_column == 'nation':
                print(en_df[current_column])
            en_df[current_column] = en_df[current_column].replace(value.split('.')[0],en_dict[column])

    else:
        current_column = en_dict[column]
        en_df[current_column] = df_original[column]