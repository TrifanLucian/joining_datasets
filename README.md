# joining_datasets

<pre>Pentru rezolvarea problemei voi folosi limbajul de programare Python si biblioteca Pandas datorita functiilor de analiza, curatare si de manipulare a datelor. Biblioteca Pandas poate fi folosita pentru seturi mari de date.
Incarc datele CSV prin metoda read_csv pentru a explora structura datelor si pentru a genera metadate.
Ma folosesc de metodele  .info(), isna() sin unique() pentru afisarea informatiile generale despre dataseturi, numar de valori lipsa pe fiecare coloanal, si cate valori unica sunt in fiecare coloana.</pre>

![image](https://github.com/user-attachments/assets/9ebe2836-88f3-4d8c-a937-910df765e3d5)

<pre>Pentru setul de date Facebook:
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
<pre>Aproape toate datele din coloana “Domain” din setul de date facebook si website se regasesc in setul de date google. La fel si pentru facebook in raport cu website.
Folosim metodele series.apply(type).unique() pentru a afla tipurile de date din fiecare coloane. Toate datele sunt Float si Str. Pentru coloana Phone, voi face conversii catre int iar apoi in str.</pre>
```
Coloana 'domain' are următoarele tipuri de date: [<class 'str'>]
Coloana 'address' are următoarele tipuri de date: [<class 'str'> <class 'float'>]
Coloana 'phone' are următoarele tipuri de date: [<class 'float'>]
………………………………………………………………………………………………………
```
Luand in considerare aceste informatii, voi folosi combinatia Domain + Name , care devine un identificator bun pentru companie.

