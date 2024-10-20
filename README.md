# joining_datasets

Pentru rezolvarea problemei am folosit Python si biblioteca Pandas datorita functiilor de analiza, curatare si de manipulare a datelor. <br>
Incarc datele CSV prin metoda read_csv pentru a explora structura datelor si pentru a genera metadate. Totodata redenumesc coloanele pentru consistenta si pentru a le urmari mai usor.<br>
Ma folosesc de metodele  .info(), isna() si unique() pentru afisarea informatiile generale despre dataseturi, numar de valori lipsa pe fiecare coloana si cate valori unica sunt in fiecare coloana.<br>

![image](https://github.com/user-attachments/assets/9ebe2836-88f3-4d8c-a937-910df765e3d5)

Pentru setul de date Facebook:
-	Pe coloanele  ‘name’ si pe ‘domain’ avem cele mai multe valori unice
-	Pe aeleasi coloane ‘name’ si ‘domain’ nu sunt valori NA.
Pentru setul de date Google:
-	Cele mai multe valori unice avem pe coloanele ‘name’, ‘phone’, ‘text’
-	Cele mai putini valori NA sunt pe coloanele ‘name’ si ‘domain’
Pentru Website: 
-	Cele mai multe valori unice sunt pe coloanele ‘domain’ si ‘phone’
-	Cele mai putine valori NA sunt pe coloanal ‘domain’
Din aceste informatii , pot lua in considerare coloana ‘domain’ pentru imbinarea seturilor de date. Totodata observ ca in setul de date Google, sunt multe adrese care se repeta in coloana ‘domain’. Sunt 70109 adrese unice din 346925 inregistrari , raportat la doar doua campuri necompletate ( valoare NA).
Comparam datele din coloanele commune alte dataseturilor: </pre>
```
>>>df1['domain'].isin(df2['domain']).sum()
np.int64(69296)
>>>df1['domain'].isin(df3['domain']).sum()
np.int64(71162)
>>>df3['domain'].isin(df2['domain']).sum()
np.int64(70105)
```
Aproape toate datele din coloana “Domain” din setul de date facebook si website se regasesc in setul de date google. La fel si pentru facebook in raport cu website.<br>
Folosim metodele series.apply(type).unique() pentru a afla tipurile de date din fiecare coloane. Toate datele sunt Float si Str. Pentru coloana Phone, voi face conversii catre int iar apoi in str.<br>
```
Coloana 'domain' are următoarele tipuri de date: [<class 'str'>]
Coloana 'address' are următoarele tipuri de date: [<class 'str'> <class 'float'>]
Coloana 'phone' are următoarele tipuri de date: [<class 'float'>]
………………………………………………………………………………………………………
```
Luand in considerare aceste informatii, voi folosi combinatia Domain + Name , care devine un identificator bun pentru companie.
Am decis sa curat datele dupa imbinarea seturilor pentru a nu pierde date care pot fi relevante sau folosite in setul final.
Voi incepe prima oara prin imbinarea seturilor Facebook si Google pentru care voi folosi combinatia Domain + Name care devine un identificator potrivit pentru companie. Am folosit un join extern pentru a pastra toate datele posibile. 
Valorile din coloanele duplicate cu sufixele _x si _y din dataframe-ul generat, se vor combina intr-o noua coloana astfel incat sa se pastreze valorile non-lipsa sau acolo unde exista diferente ( ex: doua numere de telefon diferite ) sa se concateneze sirurile de caractere astfel incat sa se pastreze ambele date. Ulterior operatiei de concatenare se vor sterge coloanele _x si _y. Acolo unde diferentele in tipurile de date pun probleme in prelucrare, se va face conversia valorilor, ( de exemplu valorile de tip “float” se vor transforma in “int” apoi in “str”, fara modificarea valorilor NaN.
Mai departe voi imbina dataframe-ul rezultat cu dataframe-ul din setul Website. In acest caz voi folosi la operatia de imbinare (join extern)  tot coloanele Domain + Name. Am ales asa pentru a pastra aceeasi varianta de imbinare, valorile din “Domain” fiind toate unice, si “name” in loc de “phone” pentru ca in “phone” am campuri cu cate doua numere de telefon, rezultate in urma combinarii coloanelor _x si _y.
Pentru a curata dataframe-ul din a doua imbinare, am ales sa elimin duplicatele pe baza colanelor “phone” si “domain” pastrand inregistrarile cu cele mai multe campuri completate. Acest lucru il voi face sortand dataframe-ul astfel incat randurile cu cele mai multe campuri completate sa fie primele astfel, in urma operatiunii de eliminare a duplicatelor se va pastra primul rand, adica cel cu cele mai multe campuri completate.
Ultima operatie va fi de a salva dataframe-ul intr-un fisier csv.

Alte variante de rezolvare:
-	Alte variante de rezolvare ar putea fi folosirea altor biblioteci precum pyspark sau fuzzywuzzy
-	Prin fuzzywuzzy se pot identifica valori approximative (prin scoruri de similaritate) si se pot compara valori precum “Google Inc.", "Google LLC” care inseamna aceeasi companie.


