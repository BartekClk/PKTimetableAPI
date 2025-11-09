
# PKTimetable API

This project is a API for site with timetable for studens of Krakow University of Technology, Faculty of Mechanical Engineering.


## Documentation

### Getting timetable records for specific groups
https://pktimetable.app/api/timetable/{group} 

The variable group can take one of three possible values:
 - All - Return all available records
 - 1 - Return records for 11K1
 - 2 - Return records for 12K1    

### Available variables
 |Variable|Possible inputs|Description|
 |--------|--------------:|:----------|
 |`day`     |1 to 7         |Returns records from specific day|
 |`lab`     |1 to 5         |Returns records for specific lab group|
 |`klab`|1 to 5|Returns records for specific computer lab group|
 |`week`|N / P / autoExact / auto|Consecutively returns records with week: odd / even / calculated / calculated but if its called on sunday it will display next week|
 |`merge`|True / False| If true it will return merged lessons|
 |`fill`|True / False| If true it will fill return with breaks|

 Variables dont work if group is set to "All"
 
 Merge and Fill work only if lab, klab and week is set to any of provided inputs.
 



## API Reference

#### Get all items

```http
  GET /api/timetable/all
```

#### Get filtered item

```http
  GET /api/timetable/{group}?{variable1}={value}&{variable2}={value}&...&{variableN}={value}
```

| Parameter | Type     | Value |Description                       |
| :-------- | :------- | :--: |:-------------------------------- |
| `group`| `string` |1 / 2 |**Required**. Consecutively: 11K1, 11K2  |

| Variable | Type     | Value |Description                       |
| :-------- | :------- | :--: |:-------------------------------- |
| `day`| `int` |1 - 7 |Day of the week|
| `lab`| `int` |1 - 5 |**Requred for ! variables to work** Lab group|
| `klab`| `int` |1 - 5 |**Requred for ! variables to work** Computer lab group |
| `week`| `string` |N / P / AutoExact / Auto |**Requred for ! variables to work** Consecutively: Odd, Even, Calculated week, calculated week but if called on sunday, will return records for next week|
|! `merge`| `bool` |True / False | If true it will return merged lessons|
|! `fill`| `bool` |True / False | If true it will fill return with breaks|

#### Get week type

```http
  GET /api/weektype?{variable}={value}
```

| Variable | Type     | Input |Description                       |
| :-------- | :------- | :--: |:-------------------------------- |
| `week`| `string` | Exact / Auto |Consecutively: Calculated week, calculated week but if called on sunday, will return records for next week|


## Authors

- [@BartekClk](https://www.github.com/bartekclk)

