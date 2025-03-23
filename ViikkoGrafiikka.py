import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
#import locale


#locale.setlocale(locale.LC_TIME, 'fi_FI.UTF-8')

# Lue CSV-tiedosto
df = pd.read_csv('2022.csv', sep=';', decimal=',', parse_dates=['Aika'])
df = df.sort_values(by='Aika')  # Järjestetään aikajärjestykseen

#print(df.columns)
#print(df.head())
print ("WORKING HARD....")


# Muutetaan 'Aika' sarake datetime-muotoon ja määritetään UTC aikavyöhyke
df['Aika'] = pd.to_datetime(df['Aika'], utc=True)

# Asetetaan Aika sarake indeksiksi
df.set_index('Aika', inplace=True)

# Ryhmitellään data päivittäin ja lasketaan kulutus yhteen, lämpötiloista keskiarvo
weekly_data = df.resample('W').sum()
weekly_data ['Vuorokauden keskilämpötila'] = df['Vuorokauden keskilämpötila'].resample('W').mean()
#print(daily_data)

# Luodaan kuvaaja
fig, ax1 = plt.subplots(figsize=(20, 10))
fig.canvas.manager.set_window_title('2022')

ax1.xaxis.set_major_formatter(mdates.DateFormatter('Vko %W'))  # Viikon numero

#ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))  # Lyhyet nimet: Tam, Hel, Maa...
# ax1.xaxis.set_major_formatter(mdates.DateFormatter('%B'))  # Täydet nimet: Tammikuu, Helmikuu...

# Pylväsdiagrammi kulutukselle (käytetään päivittäistä dataa)
ax1.bar(weekly_data .index, weekly_data ['Kulutus (netotettu) kWh'], color='blue', alpha=0.6, label='Kulutus (kWh)',width=5)
#jax1.set_xlabel('Päivämäärä')
ax1.set_ylabel('Kulutus (netotettu) kWh', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Tuotanto pylvädiagrammina alaspäin (käytetään päivittäistä dataa)
ax1.bar(weekly_data .index, -weekly_data ['Tuotanto (netotettu) kWh'], color='green', alpha=0.6, label='Tuotanto (kWh)',width=5)
ax1.set_ylabel('Kulutus ja tuotanto (netotettu) kWh', color='green')
ax1.tick_params(axis='y', labelcolor='green')

# Lämpötila (käytetään päivittäistä dataa)
x = np.array(weekly_data .index)
y = np.array(weekly_data ['Vuorokauden keskilämpötila'])
ax2 = ax1.twinx()  # Luo toinen y-akseli lämpötilalle
ax2.plot(x, y, color='pink', marker='', linestyle='-', label='Lämpötila')
sc = ax2.scatter(x, y, c=y, cmap='coolwarm', marker='', label='Lämpötila')
# Lisätään väriasteikko (colorbar)
cbar = plt.colorbar(sc, ax=ax2, label='Lämpötila (°C)')

# Lisätään otsikko ja legendaa
plt.title('Sähkönkulutus, tuotanto ja lämpötila 2021 VIIKOITTAIN')
fig.autofmt_xdate()  # Aikaleimojen muotoilu
fig.tight_layout()
plt.show()
