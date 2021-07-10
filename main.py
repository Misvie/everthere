import datetime

import entities


def execute():

    #is deleted
    e1 = entities.Event(start_date=datetime.date.today(), name="event1", link="link1")
    e1.is_deleted = True
    e2 = entities.Event(start_date=datetime.date.today(), name="event2", link="link2")
    str_type_event = str(entities.ENTITY_TYPES[0])
    put_input(e1, e2, str_type_event)

    #entity deleted
    c1 = entities.Company(employees_min=1,employees_max=20,name='everthere', link='link')
    str_type_event = str(entities.ENTITY_TYPES[1])
    put_input(c1, None, str_type_event)

    #new entity
    w1 = entities.Webinar(start_date=datetime.date.today(),name='some webinar', link='link')
    str_type_event = str(entities.ENTITY_TYPES[2])
    put_input(None, w1, str_type_event)

    #is blacklist
    cfe1 = entities.CompanyForEvent(event=e1,company=c1,is_deleted=False,is_blacklisted=False)
    cfe2 = entities.CompanyForEvent(event=e1,company=c1,is_deleted=False,is_blacklisted=True)
    str_type_event = str(entities.ENTITY_TYPES[4])
    put_input(cfe1, cfe2, str_type_event)

    #crawler status change
    ci1 = entities.ContentItem(company=c1,name='content 1', link='link3')
    ci1.crawling_status = entities.CRAWLING_STATUSES.AWAITING_CRAWL
    ci2 = entities.ContentItem(company=c1,name='content 2', link='link4')
    ci2.crawling_status = entities.CRAWLING_STATUSES.TEXT_ANALYZED
    str_type_event = str(entities.ENTITY_TYPES[3])
    put_input(ci1, ci2, str_type_event)

    #David - new entity.
    d1 = entities.David(company=c1,name='David Obviously', link='link5')
    str_type_event = str(entities.ENTITY_TYPES[7])
    put_input(None, d1, str_type_event)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

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
    if old and new:
        return old.is_deleted != new.is_deleted
    return False

# check if there is a change of the field "is_blacklisted"
def is_blacklisted(old,new) :
    if old and new:
        return old.is_blacklisted != new.is_blacklisted
    return False

# check if there is an update at the crawler status
def is_crawler_status_changed(old,new) :
    if old and new:
        return new.crawling_status == entities.CRAWLING_STATUSES.TEXT_ANALYZED or new.crawling_status == entities.CRAWLING_STATUSES.TEXT_UPLOADED
    return False

def get_notify_type(original_entity_obj, entity_obj, string_type):
    entity = entity_obj
    if not entity :
        entity = original_entity_obj
    if notify_on()[string_type] == "self":
        return entity.name
    if notify_on()[string_type] == "company":
        return '(company) ' + entity.company.name
    if notify_on()[string_type] == "event":
        return '(event) ' + entity.event.name
    if notify_on()[string_type] == "webinar":
        return '(webinar) ' + entity.webinar.name



def put_input(original_entity_obj, entity_obj, string_type):
    rule_list = rules()[string_type]
    should_notify = False
    for func in rule_list:
        if func(original_entity_obj, entity_obj) :
            should_notify = True
    if should_notify:
        print('notifying on ' + get_notify_type(original_entity_obj, entity_obj, string_type))


#### list of notification functions for each entity
company_notifications_list = [is_object_delete,is_object_new,is_deleted,is_crawler_status_changed]
event_notifications_list = [is_object_delete,is_object_new,is_deleted,is_blacklisted,is_crawler_status_changed]
webinar_notification_list = [is_object_delete,is_object_new,is_deleted,is_blacklisted,is_crawler_status_changed]
content_item_notification_list = [is_object_delete,is_object_new,is_deleted,is_blacklisted,is_crawler_status_changed]
company_for_event_notification_list = [is_object_delete,is_object_new,is_deleted,is_blacklisted]
company_for_webinar_notification_list = [is_object_delete,is_object_new,is_deleted,is_blacklisted]
company_competitor_notification_list = [is_object_delete,is_object_new,is_deleted]
# let's add notification rules for David
david_notification_list = [is_object_delete,is_object_new,is_deleted]


## the string type input would suggest which event type will trigger a set of specific rules.
def rules() :
    return {
        'Company': company_notifications_list,
        'Event': event_notifications_list,
        'Webinar': webinar_notification_list,
        'ContentItem': content_item_notification_list,
        'CompanyForEvent': company_for_event_notification_list,
        'CompanyForWebinar': company_for_webinar_notification_list,
        'CompanyCompatitor': company_competitor_notification_list,
        'David':david_notification_list
    }

## who should be notified, if self then the type of the object itself.
def notify_on():
    return {
        'Company': 'self',
        'Event': 'self',
        'Webinar': 'self',
        'ContentItem': 'company',
        'CompanyForEvent': 'event',
        'CompanyForWebinar': 'company',
        'CompanyCompatitor': 'webinar',
        'David': 'company'
    }

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    execute()

