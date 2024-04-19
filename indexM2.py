indexM2={
    "properties":{
        "Unnamed: 0":{
            "type":"long"
        },
        "Name":{
            "type":"text"
        },
        "college":{
            "type":"text"
        },
        "review":{
            "type":"text"
        },
        "rating":{
            "type":"long"
        }, 
        "DescriptionVectorV1":{
            "type":"dense_vector",
            "dims": 768,
            "index":True,
            "similarity": "l2_norm"
        }

    }
}