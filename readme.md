# Elevator System
Control a system with n cabinets, to serve m floors (application's parameters).
On each floor there will be one panel (client) for customers to send their requests to backend.

- [Elevator System](#elevator-system)
  - [Acknowledgement](#acknowledgement)
  - [RESTful API](#restful-api)
    - [GET](#get)
      - [`/system`](#system)
      - [`/cabin`](#cabin)
    - [POST](#post)
      - [`/order`](#order)
      - [`/servant`](#servant)
  - [References](#references)
  - [License](#license)

## Acknowledgement
Big thanks to VNG Tech Fresher 2022 and trainers, buddies in ZaloPay.

## RESTful API
> http://35.241.110.157:8000/`endpoint`
> 
> **Content-type:** application/json
> 
> **Web-server framework:** Flask
>
> **WSGI:** gunicorn
> 
> **VPS**: Google Cloud Platform

### GET
#### `/system`

**All information about system**

> **GET** http://35.241.110.157:8000/system

```JSON
    {
        "model": "Campus Elevator System",
        "version": "v1.0.0",
        "builder": "datnh2",
        "owner": "VNG Campus",
        "timestamp": "06/15/2022 21:04:14",
        "status": "ACTIVE",
        "cabinets": 4,
        "floors": 40,
        "requests": 0,
        "queue": [],
        "detail": [
            {
                "index": 0,
                "floor": 40,
                "status": "MOVEUP",
                "destinationCount": 0
            },
            {
                "index": 1,
                "floor": 12,
                "status": "ACTIVE",
                "destinationCount": 0
            },
            {
                "index": 2,
                "floor": 1,
                "status": "ACTIVE",
                "destinationCount": 0
            },
            {
                "index": 3,
                "floor": 1,
                "status": "ACTIVE",
                "destinationCount": 0
            }
        ]
    }
```

| Field     | Description                            |
| --------- | -------------------------------------- |
| model     | Model name of elevator system          |
| version   | Version of system                      |
| builder   | Builder of system                      |
| owner     | Owner of system                        |
| timestamp | Local time of system                   |
| status    | Status of system (`ACTIVE`/`INACTIVE`) |
| cabinets  | Number of cabinets                     |
| floors    | Number of floors                       |
| requests  | Number of requests in queue            |
| queue     | Queue of request IDs                   |
| detail    | Summarization of each cabinet          |

#### `/cabin`
**Get information about specified cabinet**

| Required | Value                                 |
| -------- | ------------------------------------- |
| id       | Valid floor (from 1 to highest floor) |

> **GET** http://35.241.110.157:8000/cabin?id=1

```json
    {
        "index": 1,
        "floor": 12,
        "status": "ACTIVE",
        "destinationCount": 0,
        "destination": []
    }   
```
</br>

> **GET** http://35.241.110.157:8000/cabin

```json
    {
        "status": 400,
        "message": "The request could not be understood by the server 
                    due to incorrect syntax."
    }
```

| Field            | Description                      |
| ---------------- | -------------------------------- |
| index            | Index of cabinet                 |
| floor            | Current floor of cabinet         |
| status           | Status of cabinet                |
| destinationCount | Number of requested destinations |
| destination      | List of destinations             |

### POST
#### `/order`
**Post new order from any exist floor with associated direction**

| Required  | Value                                 |
| --------- | ------------------------------------- |
| from      | Valid floor (from 1 to highest floor) |
| direction | 0 - `Move down` / 1 - `Move up`       |

> **POST** http://35.241.110.157:8000/order?from=10&direction=0

```json
    {
        "index": 12,
        "key": "07eee4959aaf1bceaeef259d08e968e7",
        "timestamp": "06/15/2022 21:34:59"
    }
```

| Field     | Description                              |
| --------- | ---------------------------------------- |
| index     | Index of order                           |
| key       | Secret key for future action             |
| timestamp | Local time of system when received order |

#### `/servant`
**Post new request to servant of a specified client (order) which is authorized by index and secret key**

| Required    | Value                                                                                                                               |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| id          | Order ID                                                                                                                            |
| key         | Secret key associated with order ID                                                                                                 |
| destination | *Valid* destination *(Valid destination means that you cannot request a floor with the opposite direction from the original order)* |

> **POST** http://35.241.110.157:8000/servant?id=3&key=e65e1a87d075409983fc9dc81a594493&destination=20

```json
    {
        "status": true,
        "message": "OK!"
    }
```

## References

[Example project dockerization](https://github.com/vimentor-com/pythonbackenddemo/tree/6-gunicorn-flask)

## License
MIT