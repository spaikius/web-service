# web-service
## build / run
```
docker-compose build
docker-compose up
```
## Structure
```JSON
[
    {
        "id": 0,
        "name": "Pirmadienis",
        "done": false,
        "list": [
            {
                "product_id": 0,
                "product": "Pienas",
                "quantity": 1
            },
        ]
    },
]
```

## Routing and available methods

'/shopping'  
Avialable methods:
1) GET: return all shopping lists
    OR retrun shopping list by attribute "name"
2) POST: add a new shopping list. 
Attribute "list" is set to (example below) if no list provided 
```JSON
[
    {
        "product_id": 0,
        "product": None,
        "quantity": None
    }
]
```

'/shopping/<  list_id  >'  
Avialable methods:
1) GET: Return shopping_list[list_id]
2) PUT: Update attributes
3) POST: Add a new list element
4) DELETE: Delete shopping_list[list_id]

'/shopping/<  list_id  >/<  product_id  >'
Avialable methods:
1) GET: Return shopping_list[list_id]  [product_id] 
2) PUT: Update attributes in shopping_list[list_id]  [product_id]
3) DELETE: Delete shopping_list[list_id]  [product_id]