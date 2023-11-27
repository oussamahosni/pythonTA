build the app

    docker compose -up --build

check the if data was correclty inserted into mongodb

    docker exec -it mongodb bash 
    mongosh
    show dbs
    use ScrapingDB
    db.PageLyceena.find()

"# pythonTA" 
