# web-service
## build / run
```
docker-compose build
docker-compose up
```
## Rout
```JSON
ROOT -> '/'
Avialable methods:
    GET: return all shopping lists
    POST: add a new shopping list (Attribute 'buy' is set to empty list if no list provided)
    DELETE: remove shopping list by id

[
    {
        "buy": [
            "Duonos",
            "Pieno",
            "Kavos",
            "Arbatos"
        ],
        "done": false,
        "id": 0
    },
    ...
]
```
```
ROOT inner child -> '/<id>'
Avialable methods:
    GET: Return inner child of shopping_list by id
    PUT: Update attribute 'done'
    POST: Append new 'list item' to attribute 'buy'
{
    "buy": [
        "Pieno",
        "Medaus",
        "Kakavos"
    ],
    "done": false,
    "id": 1
 },
```
```
Attributes 'buy' list element -> '/<id>/<list_index>'
Avialable methods:
    GET: get product by product_id (list index)
    PUT: update product by product_id (list index)
    DELETE: delete product from list by product_id (list index)
            
 "Medaus"
```
