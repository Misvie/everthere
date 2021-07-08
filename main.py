import datetime
import entities

def execute():
    # an example
    ce1 = entities.Event(start_date=datetime.date.today(), name="event1", link="link1")
    ce1.is_deleted = True
    ce2 = entities.Event(start_date=datetime.date.today(), name="event2", link="link2")
    put_input(ce1, ce2, "event")

# checks whether an object was deleted physically
def is_object_delete(old,new) :
    if new is None and old is not None:
        return True
    return False

# check if an object is new
def is_object_new(old,new) :
    if old is None and new is not None:
        return True
    return False

# check if there is a change of the field "is_deleted"
def is_deleted(old,new) :
    return old.is_deleted != new.is_deleted

# check if there is a change of the field "is_blacklisted"
def is_blacklisted(old,new) :
    return old.is_blacklisted != new.is_blacklisted

# check if there is an update at the crawler status
def is_crawler_status_changed(old,new) :
    return new.crawling_status == CRAWLING_STATUSES.TEXT_ANALYZED or new.crawling_status == CRAWLING_STATUSES.TEXT_UPLOADED

# the input function
def put_input(original_entity_obj, entity_obj, string_type):
    rule_list = rules()[string_type]
    for func in rule_list:
        if func(original_entity_obj, entity_obj) :
            if notify_on()[string_type] == "self" :
                print('at event : ' + func.__name__)

#### list of notification functions for each entity
company_notifications_list = [is_object_delete,is_object_new,is_deleted,is_crawler_status_changed]
event_notifications_list = [is_object_delete,is_object_new,is_deleted,is_blacklisted,is_crawler_status_changed]

## the string type input would suggest which event type will trigger a set of specific rules.
def rules() :
    return {
        "company" : company_notifications_list,
        "event" : event_notifications_list
    }

## who should be notified, if self then the type of the object itself.
def notify_on():
    return {
        "company": "self",
        "event": "self"
    }

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    execute()

