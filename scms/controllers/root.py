from pecan import expose, redirect
from webob.exc import status_map

from scms.controllers.api import chain
from scms.controllers.api import chainlink
from scms.controllers.api import image
from scms.controllers.api import service


class RootController(object):
    chain = chain.ChainController()
    service = service.ServiceController()
    image = image.ImageController()
    chainlink = chainlink.ChainLinkController()

    @expose(generic=True, template='index.html')
    def index(self):
        return dict()

    @index.when(method='POST')
    def index_post(self, q):
        redirect('https://pecan.readthedocs.io/en/latest/search.html?q=%s' % q)

    @expose('error.html')
    def error(self, status):
        try:
            status = int(status)
        except ValueError:  # pragma: no cover
            status = 500
        message = getattr(status_map.get(status), 'explanation', '')
        return dict(status=status, message=message)
