# web-service
## build / run
```
docker-compose build
docker-compose up
```

## Antra uzduotis
```
web-server: https://github.com/DovilePatiejunaite/WebServices
```
Nuorodu saugojimas
```
"tv_programs": [
                {
                    "id": 1,
                    "url": "http://tv_programs:5000/tv_programs/1"
                },
                {
                    "id": 2,
                    "url": "http://tv_programs:5000/tv_programs/2"
                }
```

## Antros uzduotis metodai
'/tv_programs'
1) GET: Grazina visas tv programas

'/lists/< list_id >/tv_programs'
1) GET: Grazina visas tv programas priklausancias listui
2) POST: Sukuria nauja tv_programa
```JSON
{
	"television": "",
	"type": "",
	"title": "",
	"start_time": "",
	"description": "",
	"release_year": "",
	"legal_age": ""
}
```
'/lists/< list_id >/tv_programs/< program_id >'
1) GET: grazina tv programa pagal id
2) PUT: atnauja tv programos atributus
3) DELETE: pasalina tv programa is saraso


# Pirmas uzduotis
```JSON
{
        "id": 1,
        "name": "Pirmadienis",
        "done": true,
        "cart": "Alus, Medus",
        "tv_programs": [
            {
                "id": 3,
                "url": "http://tv_programs:5000/tv_programs/3"
            },
            {
                "id": 4,
                "url": "http://tv_programs:5000/tv_programs/4"
            }
        ]
}
```
## Methods
'/'
Avialable methods:
1) GET: greeting message

'/lists'  
Avialable methods:
1) GET: return all shopping lists
2) POST: add a new shopping list. 

'/lists/< list_id >'  
Avialable methods:
1) GET: Return shopping list by id
2) PUT: Update attributes
3) PATCH: Update partial attributes
4) DELETE: Delete list
