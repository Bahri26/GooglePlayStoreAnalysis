#Veri setimizi csv formatından DataFrame formatına getirerek verilere erişiyoruz.
import pandas as pd
apps_with_duplicates = pd.read_csv("datasets/apps.csv")

#Veri setin de tekrar eden satırları çıkarıyoruz.
apps = apps_with_duplicates.drop_duplicates()

#Toplam uygulama sayısı
print('Veri setindeki toplam uygulama sayısı = ',apps.sum())

#Veri setindeki kolonların hakkında bilgi sahibi oluyoruz.
print(apps.info())

#İlk beş satırı getiriyoruz.
print(apps.head())

"""-----------------------------------------------------------------------"""

# Karakterleri kaldırmak için bir liste oluşturulur.
chars_to_remove = ['+',',',"$"]
# Kolon isimlerini temizlemek için bir liste oluşturduk.
cols_to_clean = ['Installs', 'Price']

# Her bir kolon için döngü
for col in cols_to_clean:
    # Her bir karakter için döngü
    for char in chars_to_remove:
        # Kolonlardaki istemediğimiz karakterleri değiştiriyoruz.
        apps[col] = apps[col].apply(lambda x: x.replace(char, ''))
    # Kolonları obje tipinden float tipine döştürülüyor.
    apps[col] = apps[col].astype(float)       
    
"""-----------------------------------------------------------------------"""

#Verileri görselleştirmek için plotly kütüphanesini kullanıyoruz.
import plotly
plotly.offline.init_notebook_mode(connected=True)
import plotly.graph_objs as go

# Benzersiz kategorilerin toplam sayısı
num_categories = len(apps["Category"].unique())
print('Kategorilerin sayısı = ', num_categories)

# Her bir 'Category' uygulamaların sayısı . En fazla olan en az olana doğru yani en fazla uygulamaya sahip kategoriler
num_apps_in_category = apps['Category'].value_counts().sort_values(ascending=False)

data = [go.Bar(
        x = num_apps_in_category.index, # Kategori ismi
        y = num_apps_in_category.values, # Sayısı
)]

plotly.offline.iplot(data)

"""---------------------------------------------------------------------"""

# Ortalama uygulşama oranları
avg_app_rating = apps.mean()
print('Ortalama uygulama oranı = ', avg_app_rating)

# Oranlara göre uygulama dağılımları
data = [go.Histogram(
        x = apps['Rating']
)]

# Ortalama uygulama oranları göstermek için dikey çizgi çizlir. 
layout = {'shapes': [{
              'type' :'line',
              'x0': avg_app_rating,
              'y0': 0,
              'x1': avg_app_rating,
              'y1': 1000,
              'line': { 'dash': 'dashdot'}
          }]
          }

plotly.offline.iplot({'data': data, 'layout': layout})

"""----------------------------------------------------------------------"""
import seaborn as sns
sns.set_style("darkgrid")
import warnings
warnings.filterwarnings("ignore")

# Hem 'Rating' hem de 'Price' kolonlarının boş olmayan değerlerini getir.
apps_with_size_and_rating_present = apps[(~apps['Rating'].isnull()) & (~apps['Price'].isnull())]

# 250'den daha fazla uygulamaya sahip kategorileri oluşturma
large_categories = apps_with_size_and_rating_present.groupby("Category").filter(lambda x: len(x) >= 250)

# Boyuta karşı oranı görselleştirmek
plt1 = sns.jointplot(x = large_categories["Size"], y = large_categories["Rating"])

# Ödemeli uygulamaları çekmek
paid_apps = apps_with_size_and_rating_present[apps_with_size_and_rating_present["Type"]=="Paid"]

# Fiyata karşı oranı grafik haline getirmek
plt2 = sns.jointplot(x = paid_apps["Price"], y = paid_apps["Rating"])

"""-------------------------------------------------------------------------"""

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
fig.set_size_inches(15, 8)

# Birkaç populer kategori uygulamaları
popular_app_cats = apps[apps.Category.isin(['GAME', 'FAMILY', 'PHOTOGRAPHY',
                                            'MEDICAL', 'TOOLS', 'FINANCE',
                                            'LIFESTYLE','BUSINESS'])]

# Fiyata karşı kategorileri grafik yardımıyla fiyatları incelemek
ax = sns.stripplot(x = popular_app_cats['Price'], y = popular_app_cats['Category'], jitter=True, linewidth=1)
ax.set_title('App pricing trend across categories')

# Fiyatları 200 $ fazla olan uygulamaları getirmek
apps_above_200 = popular_app_cats[popular_app_cats['Price'] > 200]
apps_above_200[['Category', 'App', 'Price']]

"""-------------------------------------------------------------------------"""

# 100 $ altındaki paralı uygulamaları getirmek
apps_under_100 = popular_app_cats[popular_app_cats["Price"]<100]

fig, ax = plt.subplots()
fig.set_size_inches(15, 8)

# 100 $ altındaki uygulamaların kategorilerini fiyata karşı incelemek
ax = sns.stripplot(x ='Price',y = 'Category', data =apps_under_100, jitter = True, linewidth = 1)
ax.set_title('App pricing trend across categories after filtering for junk apps')

"""-------------------------------------------------------------------------"""

trace0 = go.Box(
    # Ödemeli uygulamalar
    y = apps[apps['Type'] == 'Paid']['Installs'],
    name = 'Paid'
)

trace1 = go.Box(
    # Ücretsiz uygulamalar
    y = apps[apps['Type'] == 'Free']['Installs'],
    name = 'Free'
)

layout = go.Layout(
    title = "Ücretli uygulamalara karşı ücretsiz uygulama indirme sayısı",
    yaxis = dict(title = "İndirme log sayısı",
                type = 'log',
                autorange = True)
)

# Grafiklerini inceleyelim.
data = [trace0, trace1]
plotly.offline.iplot({'data': data, 'layout': layout})

"""-------------------------------------------------------------------------"""

# user_reviews.csv dosyasını yükleniyor.
reviews_df = pd.read_csv('datasets/user_reviews.csv')

# apps ve reviews_df DataFrame birleştiriyoruz.
merged_df = apps.merge(reviews_df)

# Sentiment and Review kolonlarından NA olanları atıyoruz.
merged_df = merged_df.dropna(subset = ['Sentiment', 'Review'])

sns.set_style('ticks')
fig, ax = plt.subplots()
fig.set_size_inches(11, 8)

# Kullanıcıların ücretliye karşı ücretsiz uygulamaların verdiği duygusallık analizi
ax = sns.boxplot(x = 'Type',y = 'Sentiment_Polarity', data = merged_df)
ax.set_title('Duygusallık Popülerlik Dağılımı')