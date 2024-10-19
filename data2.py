import pandas as pd

# functie care converteste numerele de telefon la tipul de date int si care gestioneaza valorile NaN
def convert_to_int(value):
    if pd.isna(value):  # Dacă valoarea este NaN, o lăsăm neschimbată
        return value
    try:
        # convertim la int dacă este un număr valid
        return int(float(value))  # În cazul în care este float, eliminăm zecimalele
    except (ValueError, TypeError):
        return value  # Dacă nu poate fi convertit, returnăm valoarea originală

# pastrez valorile NaN și convertesc restul valorilor la `str`
def convert_to_str_preserve_nan(value):
    if pd.isna(value):
        return value  # Dacă este NaN, păstrăm valoarea
    return str(value)  # Convertim la str doar valorile non-NaN

# combinam coloanele cu sufixele _x si _y generate in urma imbinarii a doua dataframe-uri
def merge_x_y_columns(df, convert_func):
    for col in df.columns:
        if '_x' in col:
            base_col = col[:-2]  # eliminam  sufixul '_x'

            # convertim valorile din '_x' și '_y' folosind funcția de conversie
            df[col] = df[col].apply(convert_func)
            df[base_col + '_y'] = df[base_col + '_y'].apply(convert_func)

            # Combinam valorile din '_x' si '_y', pastrand valorile non-NaN
            df.loc[:, base_col] = df[col].combine_first(df[base_col + '_y'])

            # Comparăm valorile diferite din '_x' și '_y'
            mask_diff_values = (
                    df[col].notna() &
                    df[base_col + '_y'].notna() &
                    (df[col] != df[base_col + '_y'])
            )

            # Daca valorile sunt diferite, le concatenam
            df.loc[mask_diff_values, base_col] = (
                    df.loc[mask_diff_values, col].apply(convert_func).astype(str) + ' / ' +
                    df.loc[mask_diff_values, base_col + '_y'].apply(convert_func).astype(str)
            )

            # Eliminăm coloanele duplicate cu sufixele '_x' și '_y'
            df.drop(columns=[col, base_col + '_y'], inplace=True)

    return df

# Citim fișierele CSV
df1 = pd.read_csv(r"C:\Users\wirux\Desktop\datasets\facebook_dataset.csv", on_bad_lines='skip')
df2 = pd.read_csv(r"C:\Users\wirux\Desktop\datasets\google_dataset.csv", on_bad_lines='skip', low_memory=False)
df3 = pd.read_csv(r"C:\Users\wirux\Desktop\datasets\website_dataset.csv", sep=";")

# Renumim coloanele pentru a fi consistente
df3 = df3.rename(columns={'root_domain': 'domain', 'main_city': 'city', 'main_country':'country', 'legal_name': 'name', 'main_region':'region' , 's_category': 'category'})
df2 = df2.rename(columns={'country_name': 'country', 'region_name': 'region'})
df1 = df1.rename(columns={'country_name': 'country', 'region_name': 'region', 'categories': 'category'})

# imbinam dataframe-urile df1 și df2 pe baza coloanelor "domain" si "name" pastrand toate randurile din abmele dataframe-uri
first_merge = df2.merge(df1, on=['domain', 'name'], how='outer')

# definesc ordinea coloanelor pentru dataframe-ul nou generat in urma combinarii
new_column_order = ['name', 'domain', 'category_x', 'category_y','phone_x', 'phone_y', 'country_x', 'country_y', 'region_x', 'region_y' , 'city_x', 'city_y', 'address_x', 'address_y']
first_merge_reordered = first_merge[new_column_order]
first_merge_reordered_concatenated = first_merge_reordered.copy()

# gestionez coloanele din noul dataframe, cu sufixele _x si _y din df1 (facebook dataset) si df2 (google dataset)
# astfel combin datele din cele doua coloane  intr-o singura coloana si elimin duplicate (coloanele _x si _y)
first_merge_reordered_concatenated = merge_x_y_columns(first_merge_reordered_concatenated, convert_to_int)

# convertesc valorile din coloana 'phone' in tip de date str si pastrez valorile NaN
first_merge_reordered_concatenated['phone'] = first_merge_reordered_concatenated['phone'].apply(convert_to_str_preserve_nan)

# exportam
# first_merge_reordered_concatenated.to_csv('test9.csv', index=False)

# imbinam dataframe-urile df1 și df2 pe baza coloanelor "domain" si "name" prin metoda "outer join"
final_merge = first_merge_reordered_concatenated.merge(df3, on=['domain', 'name'], how='outer')

# definesc ordinea coloanelor pentru dataframe-ul nou generat in urma combinarii
new_column_order = ['name', 'domain', 'category_x', 'category_y','phone_x', 'phone_y', 'country_x', 'country_y', 'region_x', 'region_y' , 'city_x', 'city_y', 'address']
final_merge_reordered = final_merge[new_column_order]
final_merge_reordered_concatenated = final_merge_reordered.copy()

# gestionez coloanele cu sufixele _x si _y din dataframe-ul generat anterior (facebook + google dataset) si df3 (website dataset)
# astfel combin datele din cele doua coloane  intr-o singura coloana si elimin duplicate (coloanele _x si _y)
final_merge_reordered_concatenated = merge_x_y_columns(final_merge_reordered_concatenated, convert_to_int)

# final_merge_reordered_concatenated.to_csv('final_merge_reordered_concatenated(4).csv', index=False)

#Sortam dataframe-ul astfel incat randurile cu cele mai multe completate sa fie primele
#si eliminam duplicatele in raport cu coloanele "phone" si "domain" pastrand doar prima aparitie

# Adaugam o coloana care calculeaza cate campuri non-NaN sunt completate pe fiecare rand
final_merge_reordered_concatenated['non_null_count'] = final_merge_reordered_concatenated.notna().sum(axis=1)
# Sortam dataframe - ul astfel incat randurile cu cele mai multe campurile completate sa fie primele
df_sorted = final_merge_reordered_concatenated.sort_values(by='non_null_count', ascending=False)
# Eliminam duplicatele pe baza coloanelor  'phone' si 'domain;, pastrand randurile cu cele mai multe campuri completate.
df_cleaned = df_sorted.drop_duplicates(subset=['phone', 'domain'], keep='first')
# stergem coloana  'non_null_count'
df_cleaned.drop(columns=['non_null_count'], inplace=True)

df_cleaned.to_csv('cleaned.csv', index=False)
