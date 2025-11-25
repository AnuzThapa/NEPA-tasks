Groq Chat Agent - Architecture
```
       +-----------------+
       |  User Input     |
       +--------+--------+
                |
                v
       +--------+--------+
       |  Save message   |
       |  (SQLite DB)    |
       +--------+--------+
                |
                v
       +--------+--------+
       | Load last N msgs|
       | from DB          |
       +--------+--------+
                |
                v
       +--------+--------+
       |  Groq Agent     |
       |  + Tools        |
       +--------+--------+
        |             |
        v             v
   get_weather()    get_crypto_price()
        |             |
        v             v
   Weather API      CoinGecko API
   (OpenWeather)    
        \             /
         \           /
          \         /
           +-------+
           | Response
           | (Assistant)
           +-------+
                |
                v
       +--------+--------+
       | Save response    |
       | to DB            |
       +-----------------+
```
