from fast_bitrix24 import Bitrix
from broker.settings import WEBHOOK


webhook = Bitrix(WEBHOOK)

def get_contact(phone):
    """Получаем клиента по номеру телефона"""
    method = 'crm.contact.list'
    params = {
        'filter': {'PHONE': phone},
        'select': [ "ID", "NAME", "LAST_NAME", "PHONE",]
    }
    contacts = webhook.get_all(method, params)
    return contacts


def add_contact(name, surname, phone, adress):
    """Создаем новый контакт"""
    method = 'crm.contact.add'
    params = {
        'fields': {
            "NAME": name,  
            "LAST_NAME": surname, 
            "PHONE": [ { "VALUE": phone,} ],
            "ADDRESS" : adress,
        }
    }
    contact = webhook.call(method, params)
    return contact


def get_deal(delivery_code):
    """Получаем сделку по delivery_code"""
    method = 'crm.deal.list'
    params = {
        'filter': {'UF_CRM_DELIVERY_CODE2': delivery_code},
        'select': [
            'ID',
            'TITLE',
            'UF_CRM_DELIVERY_CODE',
            'UF_CRM_DELIVERY_ADRESS',
            'UF_CRM_DELIVERY_DATE',
            'UF_CRM_DESCRIPTION'
            ]
    }
    contacts = webhook.get_all(method, params)
    return contacts


def add_deal(
    title,
    description,
    contact,
    delivery_adress,
    delivery_date,
    delivery_code
    ):
    """Создаем новую сделку"""
    method = 'crm.deal.add'
    params = {
        'fields': {
            "TITLE": title,  
            "UF_CRM_DESCRIPTION": description, 
            "CONTACT_ID": contact,
            "UF_CRM_DELIVERY_ADRESS": delivery_adress,
            "UF_CRM_DELIVERY_DATE": delivery_date,
            "UF_CRM_DELIVERY_CODE": delivery_code,
        }
    }
    contact = webhook.call(method, params)
    return contact


def update_deal(id, title, description, delivery_adress, delivery_date):
    method = 'crm.deal.update'
    params = {
        'id': id,
        'fields': {
            "TITLE": title,
            "UF_CRM_DESCRIPTION": description,
            "UF_CRM_DELIVERY_ADRESS": delivery_adress,
            "UF_CRM_DELIVERY_DATE": delivery_date,
        }
    }
    return webhook.call(method, params)


def add_field(field_name, tupe_field):
    """"Создает пользовательское поле в сделке"""
    method = 'crm.deal.userfield.add'
    params = {
        'fields': {
            "FIELD_NAME": field_name,
            "USER_TYPE_ID": tupe_field
        }
    }
    try:
        webhook.call(method, params)
    except RuntimeError:
        return False
    return True


def get_userfield_list(field_name):
    """Получает список пользовательских полей"""
    method = 'crm.deal.userfield.list'
    params = {
        'filter': {'FIELD_NAME': f"UF_CRM_{field_name}"},
        'select': ['ID', 'FIELD_NAME',]
    }
    if len(webhook.get_all(method, params)) ==  0:
        return False
    return True
