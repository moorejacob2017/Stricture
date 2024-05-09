# `Schedule` Class
- [About](#about)
- [Attributes](#attributes)
  - [`timezone: str`](#timezone-str)
  - [`start_time: datetime.time`](#start_time-datetimetime)
  - [`stop_time: datetime.time`](#stop_time-datetimetime)
  - [`unrestricted_days: list[str]`](#unrestricted_days-liststr)
  - [`restricted_days: list[str]`](#restricted_days-liststr)
  - [`prohibited_days: list[str]`](#prohibited_days-liststr)
  - [`specific_dates: list[dict]`](#specific_dates-listdict)
  - [`assume: str`](#assume-str)
- [Methods](#methods)
  - [`check_schedule`](#check_schedule)
  - [`test_schedule`](#test_schedule)
  - [`from_dict`](#from_dict)
  - [`from_json`](#from_json)
  - [`from_yaml`](#from_yaml)
  - [`from_json_file`](#from_json_file)
  - [`from_yaml_file`](#from_yaml_file)
  - [`to_str`](#to_str)
  - [`to_dict`](#to_dict)
- [Timezones](#timezones)


## About
The `Schedule` class is used to check if the current date and time falls within a defined schedule. By instantiating and initializing a `Schedule` object and running the `check_schedule` method, return `True` if the current date and time is in the schedule and `False` if outside the schedule. It includes several options for instantiation and can be defined with broad and granular attributes. 

__NOTE:__  All attibutes (minus the lists and dictionary portions) can be instantiated as strings. However, the `start_time`, `stop_time`, and `timezone` attributes get initialized and stored as different types. For this reason, modifying `Schedule` attributes manually is not recommend unless you know what you are doing.


##### Example 1
A simple `Schedule` used to check if it is currently between 9:30am and 5:00pm for any given everyday.
```python
from stricture import Schedule

my_schedule = Schedule(
    start_time='09:30',
    stop_time='17:00',
)

if my_schedule.check_schedule():
    print('Currently time between 9:30am and 5:00pm')
else:
    print('Current time outside of 9:30am and 5:00pm')

```

##### Example 2
A complex `Schedule` used for fine-tuned control.
```python
from stricture import Schedule

# Schedule:
#   9:00am-5:00pm on Monday-Friday
#   All day on Saturdays
#   Never on Sundays
#   All day from December 12-23, 2024
#   Never from December 24-26, 2024
#   6:00pm-8:30am from December 27-31, 2024

my_schedule = Schedule(
    timezone='US/Central',
    start_time='09:30',
    stop_time='17:00',
    restricted_days=[
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
    ],
    unrestricted_days=[
        'Saturday',
    ],
    prohibited_days=[
        'Sunday',
    ],
    specific_dates=[
        {
            'mode': 'unrestricted',
            'start_date': '2024-12-12',
            'stop_date': '2024-12-23',
        },
        {
            'mode': 'prohibited',
            'start_date': '2024-12-24',
            'stop_date': '2024-12-26',
        },
        {
            'mode': 'restricted',
            'start_date': '2024-12-27',
            'stop_date': '2024-12-31',
            'start_time': '18:00',
            'stop_time': '08:30',
        },
    ],
    assume='restricted',
)

if my_schedule.check_schedule():
    print('Current date and time is in schecule')
else:
    print('Current date and time is out of schecule')

```

## Attributes
- [`timezone: str`](#timezone-str)
- [`start_time: datetime.time`](#start_time-datetimetime)
- [`stop_time: datetime.time`](#stop_time-datetimetime)
- [`unrestricted_days: list[str]`](#unrestricted_days-liststr)
- [`restricted_days: list[str]`](#restricted_days-liststr)
- [`prohibited_days: list[str]`](#prohibited_days-liststr)
- [`specific_dates: list[dict]`](#specific_dates-listdict)
- [`assume: str`](#assume-str)


### `timezone: str`
Specifies the timezone to use when checking the schedule. Default value is the local timezone (according to the system). Takes [Olson Timezone Identifiers](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) associated with the `pytz` package. See [Timezones](#timezones) for a complete list.

##### Example
```python
# 9:30am-5:00pm everyday according to the US/Central timezone
schedule_1 = Schedule(
    timezone='US/Central',
    start_time='09:30',
    stop_time='17:00',
)

# 9:30am-5:00pm everyday according to the Europe/London timezone
schedule_2 = Schedule(
    timezone='Europe/London',
    start_time='09:30',
    stop_time='17:00',
)
```


### `start_time: datetime.time`
Specifies when the schedule time range "starts" for restricted days. Is stored as a `datetime.time`, but can be instantiated as a string in 24-hour `%H:%M` format.

##### Example
```python
# 9:30am-5:00pm everyday
schedule_1 = Schedule(
    start_time='09:30',
    stop_time='17:00',
)

# 2:37pm-5:00pm everyday
schedule_2 = Schedule(
    start_time='14:37',
    stop_time='17:00',
)

# 5:00pm-9:30am everyday
schedule_3 = Schedule(
    start_time='17:00',
    stop_time='09:30',
)
```


### `stop_time: datetime.time`
Specifies when the schedule time range "stops" for restricted days. Is stored as a `datetime.time`, but can be instantiated as a string in 24-hour `%H:%M` format.

##### Example
```python
# 9:30am-5:00pm everyday
schedule_1 = Schedule(
    start_time='09:30',
    stop_time='17:00',
)

# 9:30am-11:13pm everyday
schedule_2 = Schedule(
    start_time='09:30',
    stop_time='11:13',
)
```


### `restricted_days: list[str]`
A `list` of week days that will have the `start_time` and `stop_time` applied to. When no days are supplied to `restricted_days`, the default value is a list of days that are NOT include in `unrestricted_days` and `prohibited_days`.

##### Example
```python
# 9:30am-5:00pm Monday-Wednesday
schedule_1 = Schedule(
    start_time='09:30',
    stop_time='17:00',
    restricted_days=[
        'Monday',
        'Tuesday',
        'Wednesday'
    ]
)

# 9:30am-5:00pm Thursday-Saturday
schedule_2 = Schedule(
    start_time='09:30',
    stop_time='17:00',
    restricted_days=[
        'Thursday',
        'Friday',
        'Saturday'
    ]
)

# 9:30am-5:00pm Monday-Wednesday
# All day Thursday-Saturday
# Never on Sunday
schedule_3 = Schedule(
    start_time='09:30',
    stop_time='17:00',
    unrestricted_days=[
        'Thursday',
        'Friday',
        'Saturday'
    ]
    prohibited_days=[
        'Sunday',
    ]
)
```

### `unrestricted_days: list[str]`
A `list` of week days that are considered "in schedule" for all 24 hours.

##### Example
```python
# All day Monday-Wednesday
schedule_1 = Schedule(
    unrestricted_days=[
        'Monday',
        'Tuesday',
        'Wednesday'
    ]
)

# 9:30am-5:00pm Monday-Wednesday
# All day Thursday-Saturday
schedule_2 = Schedule(
    start_time='09:30',
    stop_time='17:00',
    restricted_days=[
        'Monday',
        'Tuesday',
        'Wednesday'
    ],
    unrestricted_days=[
        'Thursday',
        'Friday',
        'Saturday'
    ]
)
```


### `prohibited_days: list[str]`
A `list` of week days that are considered "out of schedule" for all 24 hours.

##### Example
```python
# 9:30am-5:00pm Monday-Wednesday
# All day Thursday-Friday
schedule_1 = Schedule(
    start_time='09:30',
    stop_time='17:00',
    restricted_days=[
        'Monday',
        'Tuesday',
        'Wednesday'
    ],
    prohibited_days=[
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday'
    ]
)
```

### `specific_dates: list[dict]`
A `list` of `dict{str,*}` used to set the schedule behavior for specific date ranges (overrides `restricted_days`, `unrestricted_days`, and `prohibited_days`). Each `dict` can have 3-5 key:value pairs that affect schedule behavior.
- `mode: str` - A `str` specifying what mode to use for the date range. Required. Must be 1 of 3 values:
  - `restricted` - Date range is treated as restricted. Requires `start_time` and `stop_time` for date range.
  - `unrestricted` - Date range is treated as unrestricted.
  - `prohibited` - Date range is treated as prohibited.
- `start_date: str` - The start of the date range. Required. Must be in `%Y-%m-%d %H:%M` format.
- `stop_date: str` - The end of the date range (inclusive). Required. Must be in `%Y-%m-%d %H:%M` format.
- `start_time: datetime.time` - Start time for date range. Required for `restricted` mode. Is stored as a `datetime.time`, but can be instantiated as a string in 24-hour `%H:%M` format.
- `stop_time: datetime.time` - Stop time for date range. Required for `restricted` mode. Is stored as a `datetime.time`, but can be instantiated as a string in 24-hour `%H:%M` format.






##### Example
```python
# 9:30am-5:00pm every day
# 6:00pm-8:30am from December 27-31, 2024
schedule_1 = Schedule(
    start_time='09:30',
    stop_time='17:00',
    specific_dates=[
        {
            'mode': 'restricted',
            'start_date': '2024-12-27',
            'stop_date': '2024-12-31',
            'start_time': '18:00',
            'stop_time': '08:30',
        },
    ]
)

# 9:30am-5:00pm every day
# All day from December 12-23, 2024
schedule_2 = Schedule(
    start_time='09:30',
    stop_time='17:00',
    specific_dates=[
        {
            'mode': 'unrestricted',
            'start_date': '2024-12-12',
            'stop_date': '2024-12-23',
        },
    ]
)

# 9:30am-5:00pm every day
# Never from December 24-26, 2024
schedule_3 = Schedule(
    start_time='09:30',
    stop_time='17:00',
    specific_dates=[
        {
            'mode': 'prohibited',
            'start_date': '2024-12-24',
            'stop_date': '2024-12-26',
        },
    ]
)

```

### `assume: str`
A `str` that specifies how unlisted days should be handled. Must be 1 of 3 values (Default value is `restricted`):
- `restricted` - Unlisted days are treated as restricted.
- `unrestricted` - Unlisted days are treated as unrestricted.
- `prohibited` - Unlisted days are treated as prohibited.

##### Example
```python
# Never on Monday-Friday
# 9:30am-5:00pm on Saturday and Sunday
schedule_1 = Schedule(
    assume='restricted',
    start_time='09:30',
    stop_time='17:00',
    prohibited_days=[
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
    ],
)

# 9:30am-5:00pm on Monday-Friday
# All day on Saturday and Sunday
schedule_2 = Schedule(
    assume='unrestricted',
    start_time='09:30',
    stop_time='17:00',
    restricted_days=[
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
    ],
)

# 9:30am-5:00pm on Monday-Friday
# Never on Saturday and Sunday
schedule_3 = Schedule(
    assume='prohibited',
    start_time='09:30',
    stop_time='17:00',
    restricted_days=[
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
    ],
)

```

## Methods
- [`check_schedule`](#check_schedule)
- [`test_schedule`](#test_schedule)
- [`from_dict`](#from_dict)
- [`from_json`](#from_json)
- [`from_yaml`](#from_yaml)
- [`from_json_file`](#from_json_file)
- [`from_yaml_file`](#from_yaml_file)
- [`to_str`](#to_str)
- [`to_dict`](#to_dict)

### `check_schedule`
Returns `True` or `False` based on whether the current time and date (according to the system) is within the schedule's given time and date ranges.

##### Example
```python
if my_schedule.check_schedule():
    print('Currently in schecule')
else:
    print('Currently out of schecule')
```

### `test_schedule`
Returns `True` or `False` based on whether the provided time and date is within the schedule's given time and date ranges. Provided date must be a `str` in the format of `%Y-%m-%d %H:%M %Z` with the `%Z` timezone being optional. When no timezone is provided, the local timezone (according to the system) is used. Useful for testing and debugging purposes.

##### Example
```python
date1 = "2024-05-05 17:35"
date2 = "2024-08-20 22:47 US/Central"

if my_schedule.test_schedule(date1):
    print(date1, ' in schecule')
else:
    print(date1, ' out of schecule')

if my_schedule.test_schedule(date2):
    print(date2, ' in schecule')
else:
    print(date2, ' out of schecule')
```

### `from_dict`
Instantiates a `Schedule` object and initializes based on a provided `dict`.

##### Example
```python
schedule_dict = {
    'timezone':'US/Central',
    'start_time':'09:30',
    'stop_time':'17:00',
    'restricted_days':[
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
    ],
    'unrestricted_days':[
        'Saturday',
    ],
    'prohibited_days':[
        'Sunday',
    ],
    'specific_dates':[
        {
            'mode': 'unrestricted',
            'start_date': '2024-12-12',
            'stop_date': '2024-12-23',
        },
        {
            'mode': 'prohibited',
            'start_date': '2024-12-24',
            'stop_date': '2024-12-26',
        },
        {
            'mode': 'restricted',
            'start_date': '2024-12-27',
            'stop_date': '2024-12-31',
            'start_time': '18:00',
            'stop_time': '08:30',
        },
    ],
    'assume':'restricted',
}

my_schedule = Schedule.from_dict(schedule_dict)
```

### `from_json`
Instantiates a `Schedule` object and initializes based on a provided `str` in json format.

##### Example
```python
schedule_json = '''
{
    'timezone':'US/Central',
    'start_time':'09:30',
    'stop_time':'17:00',
    'restricted_days':[
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
    ],
    'unrestricted_days':[
        'Saturday',
    ],
    'prohibited_days':[
        'Sunday',
    ],
    'specific_dates':[
        {
            'mode': 'unrestricted',
            'start_date': '2024-12-12',
            'stop_date': '2024-12-23',
        },
        {
            'mode': 'prohibited',
            'start_date': '2024-12-24',
            'stop_date': '2024-12-26',
        },
        {
            'mode': 'restricted',
            'start_date': '2024-12-27',
            'stop_date': '2024-12-31',
            'start_time': '18:00',
            'stop_time': '08:30',
        },
    ],
    'assume':'restricted',
}
'''

my_schedule = Schedule.from_json(schedule_json)
```

### `from_yaml`
Instantiates a `Schedule` object and initializes based on a provided `str` in yaml format.

##### Example
```python
schedule_yaml = '''
timezone: "US/Central"
start_time: "09:30"
stop_time: "17:00"
restricted_days:
  - "Monday"
  - "Tuesday"
  - "Wednesday"
  - "Thursday"
  - "Friday"
unrestricted_days:
  - "Saturday"  
prohibited_days:
  - "Sunday"
specific_dates:
  - mode: "unrestricted"
    start_date: "2024-12-12"
    stop_date: "2024-12-23"
  - mode: "prohibited"
    start_date: "2024-12-24"
    stop_date: "2024-12-26"
  - mode: "restricted"
    start_date: "2024-12-27"
    stop_date: "2024-12-31"
    start_time: "18:00"
    stop_time: "08:30"
assume: "restricted"
'''

my_schedule = Schedule.from_yaml(schedule_yaml)
```

### `from_json_file`
Instantiates a `Schedule` object and initializes based on a provided json file.

##### Example
```python
my_schedule = Schedule.from_json_file('./my_schedule.json')
```

### `from_yaml_file`
Instantiates a `Schedule` object and initializes based on a provided yaml file.

##### Example
```python
my_schedule = Schedule.from_yaml_file('./my_schedule.yml')
```

### `to_dict`
Returns the schedule in `dict` format.

##### Example
```python
schedule_dict = my_schedule.to_dict()
```

### `to_str`
Returns the schedule in `str` format. Is a synonym for `__str__`. Can be printed directly without needing to call `to_str`.

##### Example
```python
schedule_str = my_schedule.to_str()
schedule_str = my_schedule.__str__()
print(my_schedule) 
```


## Timezones
The `Schedule` class uses the `pytz` package to handle timezones, which takes [Olson Timezone Identifiers](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).

<details>
<summary>A complete list of acceptable timezones is as follows:</summary>
<pre><code>Africa/Abidjan
Africa/Accra
Africa/Addis_Ababa
Africa/Algiers
Africa/Asmara
Africa/Asmera
Africa/Bamako
Africa/Bangui
Africa/Banjul
Africa/Bissau
Africa/Blantyre
Africa/Brazzaville
Africa/Bujumbura
Africa/Cairo
Africa/Casablanca
Africa/Ceuta
Africa/Conakry
Africa/Dakar
Africa/Dar_es_Salaam
Africa/Djibouti
Africa/Douala
Africa/El_Aaiun
Africa/Freetown
Africa/Gaborone
Africa/Harare
Africa/Johannesburg
Africa/Juba
Africa/Kampala
Africa/Khartoum
Africa/Kigali
Africa/Kinshasa
Africa/Lagos
Africa/Libreville
Africa/Lome
Africa/Luanda
Africa/Lubumbashi
Africa/Lusaka
Africa/Malabo
Africa/Maputo
Africa/Maseru
Africa/Mbabane
Africa/Mogadishu
Africa/Monrovia
Africa/Nairobi
Africa/Ndjamena
Africa/Niamey
Africa/Nouakchott
Africa/Ouagadougou
Africa/Porto-Novo
Africa/Sao_Tome
Africa/Timbuktu
Africa/Tripoli
Africa/Tunis
Africa/Windhoek
America/Adak
America/Anchorage
America/Anguilla
America/Antigua
America/Araguaina
America/Argentina/Buenos_Aires
America/Argentina/Catamarca
America/Argentina/ComodRivadavia
America/Argentina/Cordoba
America/Argentina/Jujuy
America/Argentina/La_Rioja
America/Argentina/Mendoza
America/Argentina/Rio_Gallegos
America/Argentina/Salta
America/Argentina/San_Juan
America/Argentina/San_Luis
America/Argentina/Tucuman
America/Argentina/Ushuaia
America/Aruba
America/Asuncion
America/Atikokan
America/Atka
America/Bahia
America/Bahia_Banderas
America/Barbados
America/Belem
America/Belize
America/Blanc-Sablon
America/Boa_Vista
America/Bogota
America/Boise
America/Buenos_Aires
America/Cambridge_Bay
America/Campo_Grande
America/Cancun
America/Caracas
America/Catamarca
America/Cayenne
America/Cayman
America/Chicago
America/Chihuahua
America/Coral_Harbour
America/Cordoba
America/Costa_Rica
America/Creston
America/Cuiaba
America/Curacao
America/Danmarkshavn
America/Dawson
America/Dawson_Creek
America/Denver
America/Detroit
America/Dominica
America/Edmonton
America/Eirunepe
America/El_Salvador
America/Ensenada
America/Fort_Nelson
America/Fort_Wayne
America/Fortaleza
America/Glace_Bay
America/Godthab
America/Goose_Bay
America/Grand_Turk
America/Grenada
America/Guadeloupe
America/Guatemala
America/Guayaquil
America/Guyana
America/Halifax
America/Havana
America/Hermosillo
America/Indiana/Indianapolis
America/Indiana/Knox
America/Indiana/Marengo
America/Indiana/Petersburg
America/Indiana/Tell_City
America/Indiana/Vevay
America/Indiana/Vincennes
America/Indiana/Winamac
America/Indianapolis
America/Inuvik
America/Iqaluit
America/Jamaica
America/Jujuy
America/Juneau
America/Kentucky/Louisville
America/Kentucky/Monticello
America/Knox_IN
America/Kralendijk
America/La_Paz
America/Lima
America/Los_Angeles
America/Louisville
America/Lower_Princes
America/Maceio
America/Managua
America/Manaus
America/Marigot
America/Martinique
America/Matamoros
America/Mazatlan
America/Mendoza
America/Menominee
America/Merida
America/Metlakatla
America/Mexico_City
America/Miquelon
America/Moncton
America/Monterrey
America/Montevideo
America/Montreal
America/Montserrat
America/Nassau
America/New_York
America/Nipigon
America/Nome
America/Noronha
America/North_Dakota/Beulah
America/North_Dakota/Center
America/North_Dakota/New_Salem
America/Ojinaga
America/Panama
America/Pangnirtung
America/Paramaribo
America/Phoenix
America/Port-au-Prince
America/Port_of_Spain
America/Porto_Acre
America/Porto_Velho
America/Puerto_Rico
America/Rainy_River
America/Rankin_Inlet
America/Recife
America/Regina
America/Resolute
America/Rio_Branco
America/Rosario
America/Santa_Isabel
America/Santarem
America/Santiago
America/Santo_Domingo
America/Sao_Paulo
America/Scoresbysund
America/Shiprock
America/Sitka
America/St_Barthelemy
America/St_Johns
America/St_Kitts
America/St_Lucia
America/St_Thomas
America/St_Vincent
America/Swift_Current
America/Tegucigalpa
America/Thule
America/Thunder_Bay
America/Tijuana
America/Toronto
America/Tortola
America/Vancouver
America/Virgin
America/Whitehorse
America/Winnipeg
America/Yakutat
America/Yellowknife
Antarctica/Casey
Antarctica/Davis
Antarctica/DumontDUrville
Antarctica/Macquarie
Antarctica/Mawson
Antarctica/McMurdo
Antarctica/Palmer
Antarctica/Rothera
Antarctica/South_Pole
Antarctica/Syowa
Antarctica/Troll
Antarctica/Vostok
Arctic/Longyearbyen
Asia/Aden
Asia/Almaty
Asia/Amman
Asia/Anadyr
Asia/Aqtau
Asia/Aqtobe
Asia/Ashgabat
Asia/Ashkhabad
Asia/Baghdad
Asia/Bahrain
Asia/Baku
Asia/Bangkok
Asia/Barnaul
Asia/Beirut
Asia/Bishkek
Asia/Brunei
Asia/Calcutta
Asia/Chita
Asia/Choibalsan
Asia/Chongqing
Asia/Chungking
Asia/Colombo
Asia/Dacca
Asia/Damascus
Asia/Dhaka
Asia/Dili
Asia/Dubai
Asia/Dushanbe
Asia/Gaza
Asia/Harbin
Asia/Hebron
Asia/Ho_Chi_Minh
Asia/Hong_Kong
Asia/Hovd
Asia/Irkutsk
Asia/Istanbul
Asia/Jakarta
Asia/Jayapura
Asia/Jerusalem
Asia/Kabul
Asia/Kamchatka
Asia/Karachi
Asia/Kashgar
Asia/Kathmandu
Asia/Katmandu
Asia/Khandyga
Asia/Kolkata
Asia/Krasnoyarsk
Asia/Kuala_Lumpur
Asia/Kuching
Asia/Kuwait
Asia/Macao
Asia/Macau
Asia/Magadan
Asia/Makassar
Asia/Manila
Asia/Muscat
Asia/Nicosia
Asia/Novokuznetsk
Asia/Novosibirsk
Asia/Omsk
Asia/Oral
Asia/Phnom_Penh
Asia/Pontianak
Asia/Pyongyang
Asia/Qatar
Asia/Qyzylorda
Asia/Rangoon
Asia/Riyadh
Asia/Saigon
Asia/Sakhalin
Asia/Samarkand
Asia/Seoul
Asia/Shanghai
Asia/Singapore
Asia/Srednekolymsk
Asia/Taipei
Asia/Tashkent
Asia/Tbilisi
Asia/Tehran
Asia/Tel_Aviv
Asia/Thimbu
Asia/Thimphu
Asia/Tokyo
Asia/Tomsk
Asia/Ujung_Pandang
Asia/Ulaanbaatar
Asia/Ulan_Bator
Asia/Urumqi
Asia/Ust-Nera
Asia/Vientiane
Asia/Vladivostok
Asia/Yakutsk
Asia/Yekaterinburg
Asia/Yerevan
Atlantic/Azores
Atlantic/Bermuda
Atlantic/Canary
Atlantic/Cape_Verde
Atlantic/Faeroe
Atlantic/Faroe
Atlantic/Jan_Mayen
Atlantic/Madeira
Atlantic/Reykjavik
Atlantic/South_Georgia
Atlantic/St_Helena
Atlantic/Stanley
Australia/ACT
Australia/Adelaide
Australia/Brisbane
Australia/Broken_Hill
Australia/Canberra
Australia/Currie
Australia/Darwin
Australia/Eucla
Australia/Hobart
Australia/LHI
Australia/Lindeman
Australia/Lord_Howe
Australia/Melbourne
Australia/NSW
Australia/North
Australia/Perth
Australia/Queensland
Australia/South
Australia/Sydney
Australia/Tasmania
Australia/Victoria
Australia/West
Australia/Yancowinna
Brazil/Acre
Brazil/DeNoronha
Brazil/East
Brazil/West
CET
CST6CDT
Canada/Atlantic
Canada/Central
Canada/East-Saskatchewan
Canada/Eastern
Canada/Mountain
Canada/Newfoundland
Canada/Pacific
Canada/Saskatchewan
Canada/Yukon
Chile/Continental
Chile/EasterIsland
Cuba
EET
EST
EST5EDT
Egypt
Eire
Etc/GMT
Etc/GMT+0
Etc/GMT+1
Etc/GMT+10
Etc/GMT+11
Etc/GMT+12
Etc/GMT+2
Etc/GMT+3
Etc/GMT+4
Etc/GMT+5
Etc/GMT+6
Etc/GMT+7
Etc/GMT+8
Etc/GMT+9
Etc/GMT-0
Etc/GMT-1
Etc/GMT-10
Etc/GMT-11
Etc/GMT-12
Etc/GMT-13
Etc/GMT-14
Etc/GMT-2
Etc/GMT-3
Etc/GMT-4
Etc/GMT-5
Etc/GMT-6
Etc/GMT-7
Etc/GMT-8
Etc/GMT-9
Etc/GMT0
Etc/Greenwich
Etc/UCT
Etc/UTC
Etc/Universal
Etc/Zulu
Europe/Amsterdam
Europe/Andorra
Europe/Astrakhan
Europe/Athens
Europe/Belfast
Europe/Belgrade
Europe/Berlin
Europe/Bratislava
Europe/Brussels
Europe/Bucharest
Europe/Budapest
Europe/Busingen
Europe/Chisinau
Europe/Copenhagen
Europe/Dublin
Europe/Gibraltar
Europe/Guernsey
Europe/Helsinki
Europe/Isle_of_Man
Europe/Istanbul
Europe/Jersey
Europe/Kaliningrad
Europe/Kiev
Europe/Kirov
Europe/Lisbon
Europe/Ljubljana
Europe/London
Europe/Luxembourg
Europe/Madrid
Europe/Malta
Europe/Mariehamn
Europe/Minsk
Europe/Monaco
Europe/Moscow
Europe/Nicosia
Europe/Oslo
Europe/Paris
Europe/Podgorica
Europe/Prague
Europe/Riga
Europe/Rome
Europe/Samara
Europe/San_Marino
Europe/Sarajevo
Europe/Simferopol
Europe/Skopje
Europe/Sofia
Europe/Stockholm
Europe/Tallinn
Europe/Tirane
Europe/Tiraspol
Europe/Ulyanovsk
Europe/Uzhgorod
Europe/Vaduz
Europe/Vatican
Europe/Vienna
Europe/Vilnius
Europe/Volgograd
Europe/Warsaw
Europe/Zagreb
Europe/Zaporozhye
Europe/Zurich
GB
GB-Eire
GMT
GMT+0
GMT-0
GMT0
Greenwich
HST
Hongkong
Iceland
Indian/Antananarivo
Indian/Chagos
Indian/Christmas
Indian/Cocos
Indian/Comoro
Indian/Kerguelen
Indian/Mahe
Indian/Maldives
Indian/Mauritius
Indian/Mayotte
Indian/Reunion
Iran
Israel
Jamaica
Japan
Kwajalein
Libya
MET
MST
MST7MDT
Mexico/BajaNorte
Mexico/BajaSur
Mexico/General
NZ
NZ-CHAT
Navajo
PRC
PST8PDT
Pacific/Apia
Pacific/Auckland
Pacific/Bougainville
Pacific/Chatham
Pacific/Chuuk
Pacific/Easter
Pacific/Efate
Pacific/Enderbury
Pacific/Fakaofo
Pacific/Fiji
Pacific/Funafuti
Pacific/Galapagos
Pacific/Gambier
Pacific/Guadalcanal
Pacific/Guam
Pacific/Honolulu
Pacific/Johnston
Pacific/Kiritimati
Pacific/Kosrae
Pacific/Kwajalein
Pacific/Majuro
Pacific/Marquesas
Pacific/Midway
Pacific/Nauru
Pacific/Niue
Pacific/Norfolk
Pacific/Noumea
Pacific/Pago_Pago
Pacific/Palau
Pacific/Pitcairn
Pacific/Pohnpei
Pacific/Ponape
Pacific/Port_Moresby
Pacific/Rarotonga
Pacific/Saipan
Pacific/Samoa
Pacific/Tahiti
Pacific/Tarawa
Pacific/Tongatapu
Pacific/Truk
Pacific/Wake
Pacific/Wallis
Pacific/Yap
Poland
Portugal
ROC
ROK
Singapore
Turkey
UCT
US/Alaska
US/Aleutian
US/Arizona
US/Central
US/East-Indiana
US/Eastern
US/Hawaii
US/Indiana-Starke
US/Michigan
US/Mountain
US/Pacific
US/Pacific-New
US/Samoa
UTC
Universal
W-SU
WET
Zulu
</code></pre>
</details>