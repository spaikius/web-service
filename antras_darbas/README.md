# web-service
## build / run
```
docker-compose build
docker-compose up
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
