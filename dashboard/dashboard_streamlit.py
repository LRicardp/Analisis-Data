import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import altair as alt
import numpy as np

sns.set(style='dark')
#Load dataset
merge_df = pd.read_csv("dashboard\merge_data.csv")

st.title('Bike Sharing Dashboard')
#Visualisasi Nomor 1
st.subheader('Kapan penyewaan sepeda mengalami peningkatan dan penurunan?')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='mnth_day', y='total_day', data=merge_df, hue='year_day')
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Pengguna")
ax.set_title("Penggunaan Sepeda Harian dalam Satu Tahun")

st.pyplot(fig)
#Visualisasi Nomor 2
st.subheader('Bagaimana hubungan antara banyaknya penyewaan dengan cuaca?')
fig, ax = plt.subplots(figsize=(10,6))
kelompok_cuaca = merge_df.groupby('weathersit_hour')['total_hour'].mean().reset_index().sort_values("weathersit_hour")
sns.barplot(x='total_hour', y='weathersit_hour', data=kelompok_cuaca)
ax.set_xlabel("Rata-Rata Pengguna Per Jam")
ax.set_ylabel("Keadaan Cuaca")
ax.set_title("Penggunaan Sepeda Per Jam berdasarkan Cuaca")

st.pyplot(fig)
#Visualisasi Nomor 3
st.subheader('Bagaimana hubungan antara banyaknya penyewaan dengan hari libur?')
fig, ax = plt.subplots(figsize=(10,6))
kelompok_holiday = merge_df.groupby('holiday_day')['total_day'].mean().reset_index().sort_values("total_day")
sns.barplot(x='holiday_day', y='total_day', data=kelompok_holiday)
ax.set_xlabel("Hari")
ax.set_ylabel("Rata-Rata Pengguna Harian")
ax.set_xticks([0,1], ['Tidak Libur', 'Libur'])
ax.set_title("Rata-Rata Pengguna Harian antara Hari Libur dan Hari Kerja")
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10,6))
kelompok_jam = merge_df.groupby('hr')['total_hour'].mean().reset_index()
sns.lineplot(x='hr', y='total_hour', data=kelompok_jam, color='red')
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-Rata Pengguna Per Jam")
ax.set_title("Rata-Rata Pengguna Harian antara Hari Libur dan Hari Kerja")
st.pyplot(fig)

#Visualisasi Nomor 4
st.subheader('Bagaimana hubungan antara banyaknya penyewaan dengan musim?')
fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(x='season_day', y='total_day', data=merge_df, hue='year_day')
ax.legend(title="Tahun")
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Pengguna")
ax.set_title("Penggunaan Sepeda Harian per Musim")
st.pyplot(fig)

#Visualisasi Nomor 5
st.subheader('Bagaimana hubungan antara penyewaan dengan suhu, kelembapan, dan kecepatan angin?')
fig, ax = plt.subplots(figsize=(10, 6))  # Menentukan ukuran figure
variabel_day = merge_df[['season_day', 'temperature_day', 'humidity_day', 'windspeed_day', 'total_day']]
corr_matrix_day = variabel_day.corr(method='spearman')
sns.heatmap(corr_matrix_day, annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
st.pyplot(fig)
#Membuat regresi suhu dan total penyewaan sepeda
slope, intercept = np.polyfit(merge_df['temperature_day'], merge_df['total_day'], 1)
#Membuat scatterplot
scatter_chart = alt.Chart(merge_df).mark_circle().encode(
    x='temperature_day:Q',
    y='total_day:Q'
).properties(
    width=600,
    height=400
)
#Membuat garis regresi
regression_line = scatter_chart.transform_regression(
    'temperature_day', 'total_day', method='linear'
).mark_line(color='red')

# Menggabungkan scatterplot dengan garis regresi
chart = (scatter_chart + regression_line).properties(
    title='Regresi Suhu dengan Penyewaan Sepeda Harian',
)
#Membuat penamaan grafik regresi
text = alt.Chart(merge_df).mark_text(
    align='left',
    baseline='middle',
    dx=5, 
).encode(
    x=alt.value(600),  
    y='total_day',
    text=alt.value('Regression Equation: y = {:.2f}x + {:.2f}'.format(slope, intercept)),
)
#Menampilkan regresi
st.altair_chart(chart+text, use_container_width=True)
