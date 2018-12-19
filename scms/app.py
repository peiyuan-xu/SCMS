from pecan import make_app
from scms.db import common
from scms.db import models


def setup_app(config):

    models.ModelBase.metadata.create_all(common.get_engine())
    app_conf = dict(config.app)

    return make_app(
        app_conf.pop('root'),
        logging=getattr(config, 'logging', {}),
        **app_conf
    )
