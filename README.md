# web-service
## build / run
```
docker-compose build
docker-compose up
```
## Routing and available methods

ROOT -> '/shopping'  
Avialable methods:
1) GET: return all shopping lists or by name
2) POST: add a new shopping list (Attribute 'buy' is set to empty list if no list provided)
```JSON
[
    {
        "id": 0,
        "name": "Pirmadienis",
        "done": false,
        "list": [
            {
                "product": "Pienas",
                "quantity": 1
            },
        ]
    },
]
```

shopping inner child -> '/shopping/<id>'  
Avialable methods:
1) GET: Return inner child of shopping_list by id
2) PUT: Update attributes
3) DELETE: Delete child
