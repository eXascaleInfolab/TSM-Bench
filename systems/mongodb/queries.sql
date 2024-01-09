{"find" : {"id_station": {"$in": <stid>}, "time": {"$gt": "<timestamp_from>", "$lt": "<timestamp>" }} }
{ "find" : {"id_station": {"$in": <stid>}, "time": {"$gt": "<timestamp_from>", "$lt": "<timestamp>" }, "<sid1>": {"$gt": 0.95}} }
{ "aggregate" : [ { "$match": { "time" : { "$gt": "<timestamp_from>" ,  "$lt": "<timestamp>" }, "id_station" : { "$in": <stid> } } }, { "$group": { "_id": "$id_station",  <avg_sid> } }] }
{ "aggregate" :  [ {  "$match" : { "id_station": { "$in": <stid> }, "time": { "$gte": "<timestamp_from>", "$lt":  "<timestamp>" } } }, { "$group": {  "_id": { "st_id": "$st_id", "year": { "$year" : "$time" }, "month" : { "$month": "$time" }, "day": { "$dayOfMonth" : "$time" },  "hour" : { "$hour" : "$time" } } , <avg_sid> }} ]  }
EMPTY

