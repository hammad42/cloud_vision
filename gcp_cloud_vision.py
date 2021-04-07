def gcp_vision(uri,file_name):    
    from google.cloud import vision
    import os
    from google.protobuf.json_format import MessageToJson
    import proto
    from datetime import datetime
    from bigquery_ import writeToBQ
    now = str(datetime.now())


    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:\gcp_credentials\elaborate-howl-285701-105c2e8355a8.json"

    client = vision.ImageAnnotatorClient()

    image = vision.Image()
    #uri="gs://context_primary/Nike-ZoomX-Vaporfly-NEXT-el-calzado-utilizado-por-Eliud-Kipchogue.jpg"

    image.source.image_uri = uri

    #response = client.logo_detection(image=image)

    response = client.annotate_image({
        'image': {'source': {'image_uri': uri}},
        'features': [{'type_': vision.Feature.Type.LOGO_DETECTION},{'type_': vision.Feature.Type.LANDMARK_DETECTION},{'type_': vision.Feature.Type.TEXT_DETECTION},{'type_': vision.Feature.Type.FACE_DETECTION},{'type_': vision.Feature.Type.OBJECT_LOCALIZATION}],
    })

    json_string = proto.Message.to_json(response)

    ############logos
    logos=response.logo_annotations

    if not logos:
        logo_={'time_stamp':now,'file_name':file_name,'description':'empty','score':'0.0',"input_uri":uri}
        writeToBQ(logo_,"elaborate-howl-285701.context.image_logo")
        
    else:
        for logo in logos:
            desc=logo.description
            print(desc)
            score=str(logo.score)
            print(score)
            logo_={'time_stamp':now,'file_name':file_name,'description':desc,'score':score,"input_uri":uri}
            writeToBQ(logo_,"elaborate-howl-285701.context.image_logo")

    ##############landmarks
    landmarks = response.landmark_annotations
    
    if not landmarks:
        landmarks_={'time_stamp':now,'file_name':file_name,'description':'empty','score':'0.0','latitude':'empty','longitude':'empty',"input_uri":uri}
        writeToBQ(landmarks_,"elaborate-howl-285701.context.image_landmark")
            
        
    else:


        for landmark in landmarks:
            desc=landmark.description
            latitude=str(landmark.locations[0].lat_lng.latitude) 
            longitude=str(landmark.locations[0].lat_lng.longitude)
            score=str(landmark.score)

            print(desc)
            print(latitude)
            print(longitude)
            print(score)
            landmarks_={'time_stamp':now,'file_name':file_name,'description':desc,'score':score,'latitude':latitude,'longitude':longitude,"input_uri":uri}
            writeToBQ(landmarks_,"elaborate-howl-285701.context.image_landmark")

    ###########text

            








    return json_string
#gcp_vision("gs://context_primary/Nike-ZoomX-Vaporfly-NEXT-el-calzado-utilizado-por-Eliud-Kipchogue.jpg")

