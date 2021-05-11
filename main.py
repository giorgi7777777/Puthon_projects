import requests
import json
import sqlite3
my_key = "0b80a86883bc071c1173d50d7da704ac"

tbilisi_lat = 41.716667
tbilisi_lon = 44.783333

type = input("ამოირჩიეთ სასურველი ამ პასუხებიდან(current, minutely, hourly, daily და alerts): ")
# ამ ინფუთში შეგვიძლია ჩავწეროთ 5 პასუხი, ესენია: current, minutely, hourly, daily და alerts სხვა შემთხვევაში პროგრამა არ იმუშავებს.
url = f"https://api.openweathermap.org/data/2.5/onecall?lat={tbilisi_lat}&lon={tbilisi_lon}&exclude={type},dayly&appid={my_key}"

r = requests.get(url)
print(r.headers)
print(r.text)
print(r.status_code)
res = json.loads(r.text)
print(res)
wind_speed = res['current']['wind_speed']
print('ქარის სიჩქარე: ', wind_speed, 'მ/წმ')
clouds = res['current']['clouds']
print('ღრუბლიანობა: ', clouds, '%')
# print(json.dumps(res, indent=4))
# ეს დავაკომენტარე, რადგან დიდ ადგილს იკავებს.
with open('data.json', 'w') as f:
    json.dump(res, f, indent=4)


conn = sqlite3.connect('weather.sqlite')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE if not exists weather_forcst
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                wind_speed varchar(50),
                clouds varchar(100)
                )

''')

cursor.execute("INSERT INTO weather_forcst (wind_speed, clouds) VALUES (?, ?)", (wind_speed , clouds))
# weather_forcst ცხრილში დავამატე ორი სვეტი - wind_speed და clouds ხოლო პარამეტრებად გადავეცი ჯეისონ ფაილიდან წამოღებული ინფორმაცია.
conn.commit()
conn.close()


