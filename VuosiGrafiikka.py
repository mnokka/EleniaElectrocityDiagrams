import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Lue CSV-tiedosto
df = pd.read_csv('2022.csv', sep=';', decimal=',', parse_dates=['Aika'])

df = df.sort_values(by='Aika')  # Järjestetään aikajärjestykseen

#print(df.columns)
#print(df.head())
print ("WORKING HARD....")

# Luodaan kuvaaja
fig, ax1 = plt.subplots(figsize=(20, 10))
fig.canvas.manager.set_window_title('2022')


# Pylväsdiagrammi kulutukselle
ax1.bar(df['Aika'], df['Kulutus (netotettu) kWh'], color='blue', alpha=0.6, label='Kulutus (kWh)')
#ax1.set_xlabel('Aika')
#ax1.set_ylabel('Kulutus (netotettu) kWh', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

#tuotanto pylvädiagrammina alaspäin 
ax1.bar(df['Aika'], -df['Tuotanto (netotettu) kWh'], color='green', alpha=0.6, label='Kulutus (kWh)')
#ax1.set_xlabel('Aika')
ax1.set_ylabel('Kultuus ja tuotanto (netotettu) kWh', color='green')
ax1.tick_params(axis='y', labelcolor='green')

# Lämpötila 
x = np.array(df['Aika'])
y = np.array(df['Vuorokauden keskilämpötila'])
plt.plot(x, y, color='pink', marker='', linestyle='-')
sc = plt.scatter(x, y, c=y, cmap='coolwarm', marker='', label='Lämpötila')

# Lisätään väriasteikko (colorbar)
cbar = plt.colorbar(sc, ax=ax1, label='Lämpötila (°C)')

# Lisätään otsikko ja legendaa
plt.title('Sähkönkulutus, tuotanto ja lämpötila 2021 TUNNEITTAIN')
fig.autofmt_xdate()  # Aikaleimojen muotoilu
fig.tight_layout()
plt.show()