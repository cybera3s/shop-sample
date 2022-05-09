from bucket import bucket


# TODO: can be async
def all_bucket_objects_task():
    result = bucket.get_objects()
    return result


# def delete_bucket_object_task(obj_name):
#     bucket.del_object(obj_name)