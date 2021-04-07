def vision(request):
    import re
    from sep_blob_bucket import regex_
    from gcp_cloud_vision import gcp_vision
    from storage_upload import upload_blob
    from bigquery_ import writeToBQ
    import uuid
    from datetime import datetime
    now = str(datetime.now())


    uuid=str(uuid.uuid1())
    print(uuid)
    request_json=request.get_json()
    if request_json:
        source_url=request_json['source_url']
    link=regex_(source_url)

    bucket_and_blob=re.split('[+]',link)
    bucket_name=bucket_and_blob[0]#bucket name in gcs
    blob_name=bucket_and_blob[1]#blob name in gcs

    
    exact_file_name_list = re.split("/", blob_name)

    exact_file_name=exact_file_name_list[-1]

    json_=gcp_vision(source_url,exact_file_name)

    destination_json_link="Image/Processed_"+uuid+'_vision_json.json'

    json_link=upload_blob('context_primary',destination_json_link,json_)
    print(json_link)

    document_entities={'time_stamp':now,'file_name':exact_file_name,'vision_json':json_link}

    writeToBQ(document_entities,"elaborate-howl-285701.context.vision_json")







    return json_link