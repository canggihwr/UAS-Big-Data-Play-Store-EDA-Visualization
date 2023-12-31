# -*- coding: utf-8 -*-
"""uas_big_data-ps.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VOFvGP5y39Oc5-SEDWQTk8lAsy8myWHj

<div class="alert alert-block alert-success" style="text-align: center;">
    <h1 align="center">Tubes UAS Big Data ISKB381355</h1>
    <h3 align="center">Perbandingan kualitas dan popularitas aplikasi di Google Play Store: Berdasarkan rating, jumlah unduhan, tren, kategori, dan preferensi pengguna</h3>
</div>

<center>
  <img src = "http://res.heraldm.com/content/image/2021/02/21/20210221000044_0.jpg" width=40%>
</center>

<div>
    <h5>Kelompok 8 :</h5>
    <ul>
        <li>Alfi Atqia Rinjani (2201010280)</li>
        <li>Andrian (2201010289)</li>
        <li>Canggih Wahyu Rinaldi (2201010290)</li>
    </ul>
</div>

---

# **Pendahuluan:**

Disini kita menggunakan dataset playstore.csv yang berisi tentang bla bla bla

**Import library.**
"""

# Commented out IPython magic to ensure Python compatibility.
#import library
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

"""**Mount drive dan import dataset.**"""

from google.colab import drive
drive.mount('/content/drive')

# Import file csv dari drive

# dataset = '/content/drive/Colab Notebooks/big_data/googleplaystore.csv'
dataset = 'googleplaystore.csv'

ps_data = pd.read_csv(dataset)

# Mengecek 5 data teratas dalam dataset (head)
ps_data.head(10)

# Mengecek 5 data terakhir dalam dataset (tail)
ps_data.tail(5)

# Jumlah/shape dataset
ps_data.shape

# Atribut dalam dataset
ps_data.columns

"""**Adapun keterangan informasi yang terdapat dalam setiap kolom atribut dalam dataset ini :**

* `App`: Berisi nama aplikasi dengan deskripsi singkat (opsional).
* `Category`: kategori aplikasi.
* `Rating`: Berisi nilai rata-rata yang diberikan oleh pengguna untuk aplikasi tersebut.
* `Reviews`: Berisi jumlah pengguna yang memberikan ulasan untuk aplikasi tersebut.
* `Size`: Menyatakan ruang disk yang dibutuhkan untuk menginstal aplikasi tersebut/besar ukuran aplikasi.
* `Installs`: Berisi angka bulat untuk jumlah aplikasi tersebut diunduh.
* `Type`: Menyatakan apakah aplikasi tersebut gratis atau berbayar.
* `Price`: Berisi harga yang harus dibayar untuk menginstal aplikasi. Untuk aplikasi tipe gratis, harganya nol.
* `Content rating`: Menyatakan apakah aplikasi tersebut cocok untuk semua kelompok usia atau tidak.
* `Genres`: Menyatakan termasuk genre mana aplikasi tersebut.
* `Last updated`: Menyatakan tanggal update terakhir dirilis.
* `Current Ver`: Berisi versi terkini dari aplikasi tersebut.
* `Android Ver`: Berisi versi Android dari aplikasi tersebut.

# **Preprocessing dataset:**

**Data Duplikat.**
"""

# Mengecek data-data duplikat dalam dataset.
ps_data.duplicated().sum()

# Drop duplikat value pada dataset.
ps_data= ps_data.drop_duplicates()

ps_data.duplicated().sum()

# Jumlah/shape dataset
ps_data.shape

"""**Data Missing value.**"""

# Cek data missing values
ps_data.isnull().sum()

"""Disini kita harus menghitung persentase jumlah data missing value dalam dataset."""

total_miss = sum([True for id,row in ps_data.iterrows() if any(row.isnull())])

persentase = round(total_miss/10358*100, 2)

print(f'Jadi, ada total {total_miss} ({persentase}%) baris data yang memiliki setidaknya 1 missing value.')

"""Sehingga, jika menghapus semua data missing maka bisa berpengaruh ke hasil analisanya. Jadi untuk atribut yang jumlah missing valuenya sedikit akan dihapus sedangkan missing value pada atribut `rating` akan kita sispkan data baru berdasarkan nilai mean/median per tiap kategori"""

ps_data = ps_data[ps_data['Type'].notna()]
ps_data = ps_data[ps_data['Content Rating'].notna()]
ps_data = ps_data[ps_data['Current Ver'].notna()]
ps_data = ps_data[ps_data['Android Ver'].notna()]

# Cek data missing values
ps_data.isnull().sum()

# Mencari nilai mean dan median dalam atribut Rating dengan mengecualikan data missing valuenya.

nilai_mean = round(ps_data[~ps_data['Rating'].isnull()]['Rating'].mean(),1)

nilai_median = ps_data[~ps_data['Rating'].isnull()]['Rating'].median()

[nilai_mean, nilai_median]

"""Visualisasi nilainya dengan boxplot and a distplot."""

# Boxplot
sns.boxplot(data = ps_data['Rating'],x = ps_data['Rating']);

# Distplot
sns.histplot(ps_data['Rating'], kde=True)
plt.ylabel('Jumlah')

# Menambhkan nilai median ke dalam missing value'Rating'
ps_data['Rating'].fillna(value=nilai_median, inplace=True)

# Cek data missing values
ps_data.isnull().sum()

"""**Mengubah tipe data atribut `Price` dari string ke float.**




"""

ps_data['Price'].value_counts()

"""Untuk mengubah nilainya dari string menjadi float, pertama-tama kita harus menghilangkan simbol $ dari semua nilainya."""

# Membuat fungsi drop-dollar
def drop_dollar(val):
  if '$' in val:
    return float(val[1:])
  else:
    return float(val)

ps_data['Price'] = ps_data['Price'].apply(lambda x: drop_dollar(x))
ps_data['Price'].value_counts()

"""**Mengubah tipe data atribut `Installs` dari string ke integer.**"""

ps_data['Installs'].value_counts()

"""Untuk mengubah nilainya dari string menjadi int, kita harus menghilangkan simbol + dan , dari semua nilainya seperti $ pada langkah sebelumnya."""

def drop_plus(val):
  if '+' and ',' in val:
    new = int(val[:-1].replace(',',''))
    return new
  elif '+' in val:
    new1 = int(val[:-1])
    return new1
  else:
    return int(val)

ps_data['Installs'] = ps_data['Installs'].apply(lambda x: drop_plus(x))
ps_data.sample()

"""**Terakhir mengubah tipe data value atr `Reviews` dari string ke int.**"""

ps_data['Reviews'] = ps_data['Reviews'].astype(int)
ps_data.sample()

"""# **Visualisasi EDA:**

Setelah melakukan preprocessing. Sekarang kita dapat melakukan eksplorasi dan visualisasi data untuk mendapatkan beberapa insight dari dataset kita.

**1. Korelasi dan distribusi antar atribut**
"""

# Mengetahui korelasi antara atribut-atribut dalam play store dataset
ps_data.corr()

# Tampilan dengan Correlation heatmap
plt.figure(figsize=(10, 7))
sns.heatmap(ps_data.corr(), annot=True, cmap='coolwarm')
plt.title('Korelasi Heatmap ')
plt.show()

"""* Terdapat korelasi positif yang kuat antara kolom `Review` dan `Install`. Hal ini cukup jelas. Semakin tinggi jumlah Install, semakin tinggi pula basis pengguna, dan semakin tinggi pula jumlah ulasan yang diberikan oleh pengguna.
* `Harga` sedikit berkorelasi negatif dengan `Rating`, `Review`, dan `Install`. Ini berarti bahwa ketika harga aplikasi meningkat, peringkat rata-rata, jumlah total ulasan, dan Install akan turun sedikit.
* `Rating` sedikit berkorelasi positif dengan kolom `Installs` dan `Reviews`. Hal ini menunjukkan bahwa seiring dengan meningkatnya rating rata-rata pengguna, Install aplikasi dan jumlah ulasan juga meningkat.

Adapun Visualisasi distribusi atribut `Harga`, `Rating`, `Review`, dan `Install`
"""

plt.figure(figsize=(20, 10))

# Plot 1: Distribusi Rating
plt.subplot(2, 2, 1)
plt.xlabel("Rating")
plt.ylabel("Frekuensi")
sns.kdeplot(ps_data["Rating"], color="green", fill=True)
plt.title('Distribusi Rating', size=15)

# Plot 2: Distribusi Jumlah Review
plt.subplot(2, 2, 2)
plt.xlabel("Jumlah Review")
plt.ylabel("Frekuensi")
sns.kdeplot(ps_data["Reviews"], color="blue", fill=True)
plt.title('Distribusi Jumlah Review', size=15)

# Plot 3: Distribusi Jumlah Instalasi
plt.subplot(2, 2, 3)
plt.xlabel("Jumlah Instalasi")
plt.ylabel("Frekuensi")
sns.kdeplot(ps_data["Installs"], color="red", fill=True)
plt.title('Distribusi Jumlah Instalasi', size=15)

# Plot 4: Distribusi Harga
plt.subplot(2, 2, 4)
plt.xlabel("Harga ($)")
plt.ylabel("Frekuensi")
sns.kdeplot(ps_data["Price"], color="black", fill=True)
plt.title('Distribusi Harga', size=15)

plt.subplots_adjust(left=0.2, bottom=0.2, right=0.9, top=0.9, wspace=0.2, hspace=0.4)
plt.show()

"""**2. Persentase jumlah tipe aplikasi berbayar dan gratis (`free` dan `paid`)**"""

plt.figure(figsize=(12, 12))

# Plot 1 - Pie Chart: Persentase aplikasi gratis dan berbayar
plt.subplot(2, 2, 1)
ps_data['Type'].value_counts().plot.pie(autopct='%1.1f%%')
plt.title("Persentase Tipe Aplikasi")
plt.legend()

# Plot 2 - KDE Plot: Distribusi rating berdasarkan tipe aplikasi
plt.subplot(2, 2, 2)
sns.kdeplot(data=ps_data, x="Rating", hue='Type', fill=True)
plt.title("Distribusi Rating berdasarkan Tipe Aplikasi")

# Plot 3 - Bar Plot: Jumlah Tipe Aplikasi
plt.subplot(2, 2, 3)
sns.countplot(data=ps_data, x='Type')
plt.title("Jumlah Tipe Aplikasi")

# Plot 4 - Box Plot: Distribusi rating berdasarkan tipe aplikasi
plt.subplot(2, 2, 4)
sns.boxplot(data=ps_data, x='Type', y='Rating')
plt.title("Distribusi Rating berdasarkan Tipe Aplikasi")

plt.tight_layout()
plt.show()

"""Disini bisa kita simpulkan bahwa kebanyakan app di play store itu gratis (92.6% free). Dan berbayar dan tidaknya aplikasi ternyata tidak terlalu mempengaruhi rating.

**3. Eksplorasi Content-rating (Batasan usia)**
"""

plt.figure(figsize=(12, 12))

# Plot 1 - Pie Chart: Persentase berdasarkan batasan tingkatan usia
plt.subplot(2, 2, 1)
ps_data['Content Rating'].value_counts().plot.pie(autopct='%1.1f%%')
plt.title("Persentase Batasan Tingkatan Usia")
plt.legend()

# Plot 2 - Bar Plot: Jumlah Batasan Tingkatan Usia
plt.subplot(2, 2, 2)
sns.countplot(data=ps_data, x='Content Rating')
plt.setp(plt.gca().get_xticklabels(), rotation=45, ha="right")
plt.title("Jumlah Batasan Tingkatan Usia")


plt.tight_layout()
plt.show()

"""Rata-rata app di play store bisa digunakan semua orang tanpa batasan usia (81.8%). Sisanya ada batasan usia tertentu untuk menggunakannya.

**4. Jumlah aplikasi ditiap kategori aplikasi.**
"""

ps_data['Category'].value_counts().plot.barh(figsize=(10,10)).invert_yaxis()
plt.ylabel('Kategori')
plt.xlabel('Jumlah app')
plt.title('Jumlah app per kategori')
plt.legend()

"""Dari visualisasi ini kita bisa tau seberapa kompetitif kategori tertentu di play store. Kategori `Family`, `Game`, dan `Tools` memiliki jumlah aplikasi terbanyak dibandingkan dengan kategori lainnya.

**5. Kategori Populer berdasarkan app installs (Jumlah unduhan)**
"""

popular_categories = ps_data.groupby('Category')['Installs'].sum().sort_values(ascending=False)[:10]
colors = plt.cm.viridis(np.linspace(0, 1, len(popular_categories)))
popular_categories.plot.barh(figsize=(10, 10), color=colors)
plt.gca().invert_yaxis()
plt.xlabel('Jumlah Unduhan')
plt.title('Top 10 Kategori Populer berdasarkan Jumlah Unduhan')

"""Disini menunjukkan bahwa kategori aplikasi `Game`, `Communication` dan `Tools` memiliki jumlah penginstalan tertinggi (paling populer) dibandingkan dengan kategori aplikasi lainnya.

**6. Eksplorasi rata-rata rating aplikasi**
"""

plt.figure(figsize=(10, 15))

# Plot 1 - Histogram: Distribusi rata-rata rating aplikasi
plt.subplot(3, 1, 1)
ps_data['Rating'].plot.hist(bins=20, edgecolor='black')
plt.xlabel('Rata-rata Rating')
plt.ylabel('Jumlah Aplikasi')
plt.title('Distribusi Rata-rata Rating Aplikasi')

# Plot 2 - Box Plot: Distribusi rata-rata rating berdasarkan kategori
plt.subplot(3, 1, 2)
sns.boxplot(data=ps_data, x='Category', y='Rating')
plt.xlabel('Kategori')
plt.ylabel('Rating')
plt.title('Distribusi Rata-rata Rating berdasarkan Kategori')
plt.xticks(rotation=90, ha='right')

# Plot 3 - Violin Plot: Distribusi rata-rata rating berdasarkan tipe aplikasi
plt.subplot(3, 1, 3)
sns.violinplot(data=ps_data, x='Type', y='Rating')
plt.xlabel('Tipe Aplikasi')
plt.ylabel('Rating')
plt.title('Distribusi Rata-rata Rating berdasarkan Tipe Aplikasi')

plt.tight_layout()
plt.show()

"""**7. Representasi rata rata rating**

Kita dapat merepresentasikan rating dengan cara yang lebih baik jika kita mengelompokkan rating diantara interval tertentu. Di sini, kita coba mengelompokkan rating sebagai berikut:

* `4-5`: Rating tinggi
* `3-4`: Diatas rata-rata
* `2-3`: Rata-rata
* `1-2`: Dibawah rata-rata

Pertama buat dulu atribut baru dengan nama `Rating group` ke dataset.
"""

def rata_rata_rating(val):
  if val>=4:
    return 'Rating tinggi'
  elif val>=3 and val<4:
    return 'Diatas rata-rata'
  elif val>=2 and val<3:
    return 'Rata-rata'
  else:
    return 'Dibawah rata-rata'

# Panggil fungsi
ps_data['Rating Group'] = ps_data['Rating'].apply(lambda x: rata_rata_rating(x))

"""**Visualisasi Rating Grup**"""

plt.figure(figsize=(12, 12))

# Plot 1 - Bar Plot: Jumlah Aplikasi berdasarkan Rating Group
plt.subplot(2, 2, 1)
sns.countplot(data=ps_data, x='Rating Group', palette='RdYlGn')
plt.xlabel('Rating Group')
plt.ylabel('Jumlah Aplikasi')
plt.title('Jumlah Aplikasi berdasarkan Rating Group')

# Plot 2 - Pie Chart: Persentase Rating Group
plt.subplot(2, 2, 2)
ps_data['Rating Group'].value_counts().plot.pie(autopct='%1.1f%%', colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
plt.title('Persentase Rating Group')
plt.legend(title='Rating Group')
plt.tight_layout()

# Plot 2 - scatter plot
plt.figure(figsize=(8, 6))
sns.scatterplot(data=ps_data, x='Category', y='Rating', hue='Rating Group', palette='viridis')
plt.xlabel('Kategori')
plt.ylabel('Rating')
plt.title('Distribusi Rating dalam Setiap Kategori')
plt.xticks(rotation=90, ha='right')
plt.legend(title='Rating Group')
plt.tight_layout()


plt.show()

"""**8. Top 15 aplikasi dengan jumlah review dan unduhan terbanyak**"""

plt.figure(figsize=(10, 8))

# Top 15 App yang Paling Banyak Direiew
ps_data.groupby('App')[['Reviews','App']].sum().nlargest(15,['Reviews']).plot.barh(figsize = (10,5), color = 'pink').invert_yaxis()
plt.xlabel('Jumlah Review')
plt.title('Top 15 Aplikasi dengan Jumlah Review Terbanyak')

# Top 15 App yang Paling Banyak DiDownload
ps_data.groupby('App')[['Installs','App']].sum().nlargest(15,['Installs']).plot.barh(figsize = (10,5), color = 'purple').invert_yaxis()
plt.xlabel('Jumlah Review')
plt.title('Top 15 Aplikasi dengan Jumlah Download Terbanyak')

plt.tight_layout()
plt.show()

"""Bisa dikatakan bahwa aplikasi dengan jumlah download dan review pengguna terbanyak adalah aplikasi terpopuler di play store.

**9. Top 15 aplikasi berbayar paling mahal**
"""

plt.figure(figsize=(10, 8))

# Mengurutkan berdasarkan harga dari yang paling mahal dan mengambil 15 teratas
top_15_expensive_apps = ps_data[ps_data['Type'] == 'Paid'].nlargest(15, 'Price')

sns.barplot(data=top_15_expensive_apps, x='Price', y='App', palette='viridis')
plt.xlabel('Harga')
plt.ylabel('Nama Aplikasi')
plt.title('Top 15 Aplikasi Berbayar Paling Mahal')

plt.show()

"""**10. Aplikasi dengan penghasilan terbanyak**"""

#Aplikasi berdasarkan Pendapatan yang Dihasilkan
app_berbayar = ps_data[ps_data['Type'] == 'Paid']
app_berbayar['Pendapatan'] = app_berbayar['Installs']*app_berbayar['Price']
total_pendapatan = app_berbayar.nlargest(20, 'Pendapatan')
total_pendapatan.groupby('App')['Pendapatan'].mean().sort_values().plot.barh(figsize=(10,5), color='orange')
plt.xlabel('Pendapatan yang Dihasilkan (USD)')
plt.title('Aplikasi Teratas berdasarkan Pendapatan yang Dihasilkan melalui Biaya Instalasi')
plt.legend()

"""Aplikasi dengan penghasilan paling banyak adalah game `Minecraft`.

**11. Pairwise Plot**
"""

Rating = ps_data['Rating']
Size = ps_data['Size']
Installs = ps_data['Installs']
Type = ps_data['Type']
Price = ps_data['Price']

df_pairplot = sns.pairplot(pd.DataFrame(list(zip(Rating, Size, np.log(Installs), Price, Type)),
                        columns=['Rating','Size', 'Installs', 'Price','Type']), hue='Type')
df_pairplot.fig.suptitle("Pairwise Plot - Rating, Size, Installs, Price",x=0.5, y=1.0, fontsize=16)

"""#**Kesimpulan:**

* **~92.6%** aplikasi di play store gratis. Dan berbayar atau tidaknya aplikasi ternyata tidak terlalu mempengaruhi rating.
* Rata-rata aplikasi di play store bisa digunakan semua orang tanpa batasan usia **(81.8%)**
* Kategori **Family, Game,** dan **Tools** memiliki jumlah aplikasi terbanyak dibandingkan dengan kategori lainnya.
* kategori **Game, Communication** dan Tools memiliki jumlah penginstalan tertinggi (paling populer) dibandingkan dengan kategori aplikasi lainnya.
* Rata rata rating di play store adalah **4.2.**
* Persentasi aplikasi dengan Rating tinggi adalah **~76%**
* Aplikasi paling populer dengan jumlah review paling tinggi adalah aplikasi sosial media seperti **instagram** dan **facebook**
* **Minecraft** adalah aplikasi dengan revenue pendapatan paling tinggi di play store.
"""