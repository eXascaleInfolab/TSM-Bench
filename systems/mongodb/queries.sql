{"find" : {"id_station": {"$in": <stid>}, "time": {"$gt": "<timestamp_from>", "$lt": "<timestamp>" }} }
{ "find" : {"id_station": {"$in": <stid>}, "time": {"$gt": "<timestamp_from>", "$lt": "<timestamp>" }, "<sid1>": {"$gt": 0.95}} }
{ "aggregate" : [ { "$match": { "time" : { "$gt": "<timestamp_from>" ,  "$lt": "<timestamp>" }, "id_station" : { "$in": <stid> } } }, { "$group": { "_id": "$id_station",  <avg_sid> } }] }
{ "aggregate" :  [ {  "$match" : { "id_station": { "$in": <stid> }, "time": { "$gte": "<timestamp_from>", "$lt":  "<timestamp>" } } }, { "$group": {  "_id": { "st_id": "$st_id", "year": { "$year" : "$time" }, "month" : { "$month": "$time" }, "day": { "$dayOfMonth" : "$time" },  "hour" : { "$hour" : "$time" } } , <avg_sid> }} ]  }
EMPTY
{ "aggregate": [ { "$match": { "time" : { "$gt": "<timestamp_from>" ,  "$lt": "<timestamp>" }, "id_station" : { "$in": <stid> } } },  { "$addFields": { "avg": {  "$avg": ["$s1", "$s2"] } }  }   ,   {  "$project": { "_id":0, "time":1, "id_station": 1,  "s1": 1,  "s2": 1 , "avg" :1  }  }  ] }

