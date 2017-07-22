import requests
import logging


logger = logging.getLogger('shipstation')


class ShipStationApiException(Exception):

    def __init__(self, message, code):
        self.message = message
        self.code = code

    def __str__(self):
        return '{0}: {1}'.format(self.code, self.message)


class SSApiResult(object):

    def __init__(self, endpoint, **kwargs):
        response = endpoint.service.do_get(endpoint, **kwargs)
        self._entities = response[endpoint.model]
        self.pages = int(response['pages'])
        self.total = int(response['total'])

    def __iter__(self):
        for entity in self._entities:
            yield entity

    def __len__(self):
        return len(self._entities)

    def __getitem__(self, ii):
        return self._entities[ii]


class SSEndpoint(object):

    def __init__(self, service, model):
        self.service = service
        self.model = model

    def page(self, filters, page_num=1, page_size=20):
        filters['page'] = page_num
        filters['pageSize'] = page_size
        return SSApiResult(self, filters=filters)

    def page_count(self, filters, page_size=20):
        return self.page(filters, page_num=1, page_size=page_size).pages

    def count(self, filters, page_size=20):
        return self.page(filters, page_num=1, page_size=page_size).total


class ShipStationApi(object):

    url_root = 'https://ssapi.shipstation.com/'

    MODELS = [
        'accounts'
        'carriers',
        'customers',
        'fulfillments',
        'orders',
        'products',
        'shipments',
        'stores',
        'users',
        'warehouses',
        'webhooks'
    ]

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

        for m in self.MODELS:
            setattr(self, m, SSEndpoint(self, m))

    @property
    def auth(self):
        return {'auth': (self.api_key, self.api_secret)}

    def _url_for(self, endpoint, filters=None):
        return '{0}{1}{2}{3}'.format(self.url_root,
                                     endpoint.model,
                                     '?' if filters else '',
                                     self._build_filters(filters))

    def _build_filters(self, filters):
        return '' if not filters else \
            '&'.join(['{0}={1}'.format(k, v) for k, v in filters.items()])

    def do_get(self, endpoint, filters=None):
        url = self._url_for(endpoint, filters=filters)
        logger.info('Shipstation API request to: {0}'.format(url))
        resp = requests.get(url, **self.auth)
        if resp.status_code == 200:
            return resp.json()
        raise ShipStationApiException(resp.content, resp.status_code)
