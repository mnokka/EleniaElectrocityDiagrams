import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import locale


locale.setlocale(locale.LC_TIME, 'fi_FI.UTF-8')
df_2022 = pd.read_csv('2022.csv', sep=';', decimal=',', parse_dates=['Aika'])
df_2023 = pd.read_csv('2023.csv', sep=';', decimal=',', parse_dates=['Aika'])

# Yhdistetään molemmat DataFrame:t
df = pd.concat([df_2022, df_2023])

# Järjestetään aikajärjestykseen
df = df.sort_values(by='Aika')

# Muutetaan 'Aika' sarake datetime-muotoon ja asetetaan indeksiksi
df['Aika'] = pd.to_datetime(df['Aika'], utc=True)
df.set_index('Aika', inplace=True)

# Lisää vuosi-sarake
df['Year'] = df.index.year

# Summataan kuukausittain
df_monthly = df.resample('ME').sum()

# Erotellaan vuodet
df_2022 = df_monthly[df_monthly.index.year == 2022]
df_2023 = df_monthly[df_monthly.index.year == 2023]

# Varmistetaan, että molemmilla vuosilla on 12 kuukautta
assert len(df_2022) == len(df_2023) == 12, "Kuukausitietoja ei ole tasan 12"

# Lasketaan kuukausittainen keskilämpötila
df_2022_monthly_temp = df[df.index.year == 2022].resample('ME')['Vuorokauden keskilämpötila'].mean()
df_2023_monthly_temp = df[df.index.year == 2023].resample('ME')['Vuorokauden keskilämpötila'].mean()

# Luodaan x-akseli kuukausille
x_labels = df_2022.index.strftime('%b')  # Kuukausien nimet
x = np.arange(len(df_2022))  # 0-11 kuukausille
bar_width = 0.4  # Palkkien leveys

# Luodaan kuvaaja
fig, ax1 = plt.subplots(figsize=(12, 6))

# Piirretään 2022 ja 2023 kulutus ja tuotanto
ax1.bar(x - bar_width / 2, df_2022['Kulutus (netotettu) kWh'], color='blue', width=bar_width, alpha=0.6, label='Kulutus 2022')
ax1.bar(x - bar_width / 2, -df_2022['Tuotanto (netotettu) kWh'], color='green', width=bar_width, alpha=0.6, label='Tuotanto 2022')

ax1.bar(x + bar_width / 2, df_2023['Kulutus (netotettu) kWh'], color='red', width=bar_width, alpha=0.6, label='Kulutus 2023')
ax1.bar(x + bar_width / 2, -df_2023['Tuotanto (netotettu) kWh'], color='orange', width=bar_width, alpha=0.6, label='Tuotanto 2023')

# Lämpötila (käytetään kuukausittaista dataa)
ax2 = ax1.twinx()  # Luo toinen y-akseli lämpötilalle

# 2022 lämpötilan piirtäminen
x_2022 = np.array(df_2022_monthly_temp.index)
y_2022 = np.array(df_2022_monthly_temp)
ax2.plot(x, df_2022_monthly_temp.values, color='blue', marker='', linestyle='-', linewidth=2, label='Lämpötila 2022 (°C)')

# 2023 lämpötilan piirtäminen
x_2023 = np.array(df_2023_monthly_temp.index)
y_2023 = np.array(df_2023_monthly_temp)
ax2.plot(x, df_2023_monthly_temp.values, color='pink', marker='', linestyle='-', linewidth=2, label='Lämpötila 2023 (°C)')

ax2.legend(loc='upper right')


# Akselit ja otsikot
#ax1.set_xlabel('Kuukausi')
ax1.set_ylabel('Kulutus ja tuotanto (kWh)')
ax1.set_xticks(x)
ax1.set_xticklabels(x_labels)
ax1.legend(loc='upper left')
fig.tight_layout()

# Näytetään kuvaaja
plt.title('Sähkönkulutus ja tuotanto 2022 vs 2023')
plt.show()
