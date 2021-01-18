from toja.models.meta import Base


def init_db(request):
    Base.metadata.drop_all(request.dbsession.bind)
    Base.metadata.create_all(request.dbsession.bind)


fixtures = {}


def create(request):
    """Handles setting up the test fixtures"""
    init_db(request)
    # if 'setting' in request.params:
    #    for update_setting in request.params.getall('setting'):
    #        key, value = update_setting.split(':')
    #        setting = request.dbsession.query(Setting).filter(Setting.key == key).first()
    #        if setting:
    #            setting.value = value
    #    request.dbsession.flush()
    if 'obj' in request.params:
        for fixture in request.params.getall('fixture'):
            if fixture in fixtures:
                fixtures[fixture](request)
    return {}
