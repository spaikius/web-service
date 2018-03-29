# web-service
## build / run
```
docker-compose build
docker-compose up
```
## Routing and available methods

ROOT -> '/shopping'
Avialable methods:
    GET: return all shopping lists or by name
    POST: add a new shopping list (Attribute 'buy' is set to empty list if no list provided)
```JSON
[
    {
        'id': 0,
        'name': 'Pirmadienis',
        'done': False,
        'list': [
            {
                'product': 'Pienas',
                'quantity': 1
            },
        	...
        ]
```

shopping inner child -> '/shopping/<id>'
Avialable methods:
    GET: Return inner child of shopping_list by id
    PUT: Update attributes
    DELETE: Delete child
