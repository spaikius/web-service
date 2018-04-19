Adresas: http://193.219.91.103:8067
Darbą atliko Dovilė Patiejūnaitė ir Paulius Matijošaitis
Web servisas tv programa, pasiekiamas 80 portu.
Paleisti web servisą, reikia įsirašyti docker ir docker-compose.
Paleidimo komandos:
docker-compose build
docker-compose up -d

Paleisti terminale galima šias užklausas, naudojant curl:

1.GET metodas. Parodyti visą TV programą:
#curl -i http://localhost:80/tv_programs

2.GET metodas. Parodyti programą pagal pasirinktą id:
#curl -i http://localhost:80/tv_programs/<id>

3.POST metodas. Patalpinti dar vieną įrašą, rodomą per tv:
#curl -i -H "Content-Type: application/json" - X POST -d '{"title":"<>", "television":"<>","start_time":"<>", etc <optional>}' https://localhost:80/tv_programs

4.PUT metodas. Atnaujinti įrašą, rodomą per tv, pagal įrašo id:
#curl -i -H "Content-Type: application/json" - X PUT -d '{"<>":"<>"}' https://localhost:80/tv_programs/<element_id>

5.DELETE metodas. Ištrinti įrašą, rodomą per tv, pagal id:
#curl -i -H "Content-Type: application/json" -X DELETE http://localhost:80/tv_programs/<element_id>

