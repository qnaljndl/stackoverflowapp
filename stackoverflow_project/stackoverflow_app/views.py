import math
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import BadRequest
from rest_framework import status
from stackoverflow_app.serializers import SearchSerializer, RequestSerializer
from datetime import datetime, timezone, timedelta
from django.db import connection


output_dict = {}


@api_view(['POST'])
def search(request, format=None):
    requestObject = create_request_object(request)

    validate_user_search_limit(request.data.get('user_id'))
    validate_request(requestObject)

    params = create_params(requestObject)
    dict_key_string = create_dic_key(requestObject, 'default')

    save_search_request(request, dict_key_string)

    total_num_of_elements = get_total_elements(requestObject)

    data = cache_data_check(dict_key_string)
    if data is None:
        data = requests.get('https://api.stackexchange.com/2.3/search?', params=params).json()
        output_dict[dict_key_string] = data

    search_response = {
        'items': data.get('items'),
        'pagesize': requestObject.pagesize,
        'page': requestObject.page,
        'totalpages': math.ceil(total_num_of_elements/int(requestObject.pagesize))
    }
    return Response(search_response, status=status.HTTP_200_OK)


def validate_request(request):

    sort_list = ['activity', 'creation', 'votes', 'relevance']
    order_list = ['desc', 'asc']

    if request.tagged is None and request.intitle is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.nottagged is not None and request.tagged is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.sort not in sort_list and request.order not in order_list:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def convert_date_to_timestamp(date):
    date_time = datetime.strptime(date, '%Y/%m/%d')
    return int(date_time.replace(tzinfo=timezone.utc).timestamp())


def create_params(request):

    value_fromdate = None
    if request.fromdate is not None:
        value_fromdate = convert_date_to_timestamp(request.fromdate)

    value_todate = None
    if request.todate is not None:
        value_todate = convert_date_to_timestamp(request.todate)

    params = {
        'site': 'stackoverflow',
        'intitle': request.intitle,
        'nottagged': request.nottagged,
        'tagged': request.tagged,
        'sort': request.sort,
        'order': request.order,
        'todate': value_todate,
        'fromdate': value_fromdate,
        'pagesize': request.pagesize,
        'page': request.page
    }

    return params


def create_dic_key(request, filter):
    return str(request.fromdate) + '|' + str(request.todate) + '|' + str(request.order) + '|' + \
           str(request.sort) + '|' + str(request.tagged) + '|' + str(request.nottagged) + '|' + \
           str(request.intitle) + '|' + str(filter) + '|' + str(request.pagesize) + '|' + str(request.page) +\
           '|' + 'stackoverflow'


def create_request_object(request):
    serializer = RequestSerializer(data=request.data)
    return serializer.create(request.data)


def save_search_request(request, query):
    serializer_dict = {'user_id': request.data.get('user_id'), 'query': query}
    serializer = SearchSerializer(data=serializer_dict)
    if serializer.is_valid():
        serializer.save()
    else:
        raise BadRequest('Invalid request.')


def get_search_count(user_id, date):
    query = 'select * from stackoverflow_app_search where search_time>%s AND user_id = %s'
    with connection.cursor() as cursor:
        count = cursor.execute(query, [date, user_id])
        return count


def validate_user_search_limit(user_id):
    minute_limit = (datetime.utcnow() - timedelta(minutes=5)).strftime("%Y-%m-%d, %H:%M:%S")
    daily_limit = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d, %H:%M:%S")

    user_queries_in_X_minutes = get_search_count(user_id, minute_limit)
    user_queries_in_X_days = get_search_count(user_id, daily_limit)

    if user_queries_in_X_minutes <= 5 and user_queries_in_X_days <= 100:
        return True
    else:
        raise BadRequest('Limit Reached, Please after try sometime!!!!')


def cache_data_check(string):
    if string in output_dict:
        return output_dict[string]
    else:
        None


def get_total_elements(search_request):
    params = create_params(search_request)
    params['filter'] = 'total'
    cache_key = create_dic_key(search_request, 'total')
    if cache_key in output_dict:
        return output_dict[cache_key]
    else:
        response = requests.get('https://api.stackexchange.com/2.3/search?', params=params)
        output_dict[cache_key] = response.json().get('total')
        return output_dict[cache_key]















