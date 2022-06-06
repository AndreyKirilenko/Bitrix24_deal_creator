from .serializers import DealSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .utils import (
    webhook,
    get_contact,
    add_contact,
    get_deal,
    add_deal,
    update_deal,
    add_field,
    get_userfield_list,
    )


@api_view(['POST'])
def processor(request):
    if request.method == 'POST':
        serializer = DealSerializer(data=request.data)
        if serializer.is_valid():
            appl= serializer.save()
            # Получаем контакт с этим номером телефона
            messeges = []
            client = get_contact(appl.client.get('phone'))
            if len(client) > 1:
                messeges.append(f'Контактов с номером { appl.client.get("phone") } больше одного')
            # Если нет такого контакта
            elif len(client) == 0:
                # Создаем контакт
                contact_id = add_contact(
                    appl.client.get('name'),
                    appl.client.get('surname'),
                    appl.client.get('phone'), 
                    appl.client.get('adress'), 
                    )
                messeges.append(f"Новый контакт с номером {appl.client.get('phone') } создан")
                # Создаем сделку связав с этим контактом
                deal_id = add_deal(
                    appl.title,
                    appl.description,
                    contact_id,
                    appl.delivery_adress,
                    appl.delivery_date,
                    appl.delivery_code,
                    )
                print(deal_id)
                messeges.append(f"Сделка для этого контакта создана")
            else:  # Контакт существует
                messeges.append(f"Контакт с телефоном {appl.client.get('phone') } существует...")
                deals = get_deal(appl.delivery_code) # Получаем список сделок с этим delivery_code
                if len(deals) == 1:  # Если найдена единственная сделка
                    messeges.append(f'Найдена сделка с таким же delivery_code: { appl.delivery_code }...' )
                    accordance = {
                        "TITLE": appl.title,  
                        "UF_CRM_DESCRIPTION": appl.description,
                        "UF_CRM_DELIVERY_ADRESS": appl.delivery_adress,
                    }
                    for deal_field, application in accordance.items(): # Сравниваем с пришедшей заявкой
                        if deals[0].get(deal_field) != application: # Не совпадает?, обновляем
                            messeges.append(f'В сделках найдены различия: { deals[0].get(deal_field)} / {application }...' )
                            if update_deal(
                                deals[0].get('ID'),
                                appl.title, appl.description,
                                appl.delivery_adress,
                                appl.delivery_date,
                            ):
                                messeges.append(f'Сделка с delivery_code: { appl.delivery_code } обновлена' )
                            return Response(messeges, status=status.HTTP_200_OK)
                    messeges.append(f'Сделки идентичны. Ничего не делаем' )
                elif len(deals) == 0: # Если нет
                    messeges.append(f'Сделка с delivery_code: { appl.delivery_code } отсутствуют. Создаем...' )
                    if add_deal(
                        appl.title,
                        appl.description,
                        client[0].get('ID'),
                        appl.delivery_adress,
                        appl.delivery_date,
                        appl.delivery_code,
                        ):
                        messeges.append(f'Сделка создана' )
                else:  
                    messeges.append(f'Сделок с delivery_code: { appl.delivery_code } больше одной' )
            return Response(messeges, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def create_userfield(request):
    """Проверяем наличие пользовательских полей в сделке"""
    userfields = {
        "DESCRIPTION": 'string',
        "DELIVERY_ADRESS": 'string',
        "DELIVERY_DATE": 'datetime',
        "DELIVERY_CODE": 'string',
    }
    messeges = []
    for userfield, tupe_field in userfields.items():
        if get_userfield_list(userfield):
            messeges.append(f"UF_CRM_{userfield} is empty")
        else:
            if add_field(userfield, tupe_field):
                messeges.append(f"UF_CRM_{userfield} Created")
            else:
                messeges.append(f"ERROR: UF_CRM_{userfield} is not Created")
    return Response(messeges, status=status.HTTP_200_OK)
