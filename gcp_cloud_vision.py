def gcp_vision(uri):    
    from google.cloud import vision
    import os
    from google.protobuf.json_format import MessageToJson
    import proto

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:\gcp_credentials\elaborate-howl-285701-105c2e8355a8.json"

    client = vision.ImageAnnotatorClient()

    image = vision.Image()

    image.source.image_uri = uri

    #response = client.logo_detection(image=image)

    response = client.annotate_image({
        'image': {'source': {'image_uri': uri}},
        'features': [{'type_': vision.Feature.Type.LOGO_DETECTION},{'type_': vision.Feature.Type.LANDMARK_DETECTION},{'type_': vision.Feature.Type.TEXT_DETECTION},{'type_': vision.Feature.Type.FACE_DETECTION},{'type_': vision.Feature.Type.OBJECT_LOCALIZATION}],
    })

    json_string = proto.Message.to_json(response)

    
    


    return json_string
#gcp_vision("gs://context_primary/Nike-ZoomX-Vaporfly-NEXT-el-calzado-utilizado-por-Eliud-Kipchogue.jpg")

