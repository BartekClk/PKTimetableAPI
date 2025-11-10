
# PKTimetable API

This project is a API for site with timetable for studens of Krakow University of Technology, Faculty of Mechanical Engineering.


## API Reference

#### Get all items

```http
  GET planzajecpk.app/api2/timetable/all
```

Returns all records in format `[{ "11K1":[{...}], "11K2":[{...}] }]`

#### Get filtered item

```http
  GET planzajecpk.app/api2/timetable/{group}?{variable1}={value}&{variable2}={value}&...&{variableN}={value}
```

| Parameter | Type     | Value |Description                       |
| :-------- | :------- | :--: |:-------------------------------- |
| `group`| `string` |1 / 2 |**Required**. Consecutively: 11K1, 11K2  |

| Variable | Type     | Value |Description                       |
| :-------- | :------- | :--: |:-------------------------------- |
| `day`| `string` |1 - 7 / auto|Day of the week / Returns records for current weekday|
| `lab`| `int` |1 - 5 |**Requred for ! variables to work** Lab group|
| `klab`| `int` |1 - 5 |**Requred for ! variables to work** Computer lab group |
| `week`| `string` |N / P / AutoExact / Auto |**Requred for ! variables to work** Consecutively: Odd, Even, Calculated week, calculated week but if called on sunday, will return records for next week|
|! `merge`| `bool` |True / False | If true it will return merged lessons|
|! `fill`| `bool` |True / False | If true it will fill return records filled with breaks between lessons|
|`changes`| `bool` |True / False | If true it will apply changes from database|

Example querry with all variables:
```http
  GET https://planzajecpk.app/api2/timetable/1?day=auto&lab=1&klab=1&week=auto&merge=true&fill=true&changes=true
```

#### Get week type

```http
  GET /api2/weektype?{variable}={value}
```

| Variable | Type     | Input |Description                       |
| :-------- | :------- | :--: |:-------------------------------- |
| `week`| `string` | Exact / Auto |Consecutively: Calculated week, calculated week but if called on sunday, will return records for next week|


## Authors

- [@BartekClk](https://www.github.com/bartekclk)

