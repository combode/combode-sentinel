"""
    Set up defaults and read sentinel.conf
"""
import sys
import os
from combode_config import CombodeConfig

default_sentinel_config = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '../sentinel.conf')
)
sentinel_config_file = os.environ.get('SENTINEL_CONFIG', default_sentinel_config)
sentinel_cfg = CombodeConfig.tokenize(sentinel_config_file)
sentinel_version = "1.2.1"
min_comboded_proto_version_with_sentinel_ping = 70207


def get_combode_conf():
    if sys.platform == 'win32':
        combode_conf = os.path.join(os.getenv('APPDATA'), "CombodeCore/combode.conf")
    else:
        home = os.environ.get('HOME')

        combode_conf = os.path.join(home, ".combodecore/combode.conf")
        if sys.platform == 'darwin':
            combode_conf = os.path.join(home, "Library/Application Support/CombodeCore/combode.conf")

    combode_conf = sentinel_cfg.get('combode_conf', combode_conf)

    return combode_conf


def get_network():
    return sentinel_cfg.get('network', 'mainnet')


def get_rpchost():
    return sentinel_cfg.get('rpchost', '127.0.0.1')


def sqlite_test_db_name(sqlite_file_path):
    (root, ext) = os.path.splitext(sqlite_file_path)
    test_sqlite_file_path = root + '_test' + ext
    return test_sqlite_file_path


def get_db_conn():
    import peewee
    env = os.environ.get('SENTINEL_ENV', 'production')

    # default values should be used unless you need a different config for development
    db_host = sentinel_cfg.get('db_host', '127.0.0.1')
    db_port = sentinel_cfg.get('db_port', None)
    db_name = sentinel_cfg.get('db_name', 'sentinel')
    db_user = sentinel_cfg.get('db_user', 'sentinel')
    db_password = sentinel_cfg.get('db_password', 'sentinel')
    db_charset = sentinel_cfg.get('db_charset', 'utf8mb4')
    db_driver = sentinel_cfg.get('db_driver', 'sqlite')

    if (env == 'test'):
        if db_driver == 'sqlite':
            db_name = sqlite_test_db_name(db_name)
        else:
            db_name = "%s_test" % db_name

    peewee_drivers = {
        'mysql': peewee.MySQLDatabase,
        'postgres': peewee.PostgresqlDatabase,
        'sqlite': peewee.SqliteDatabase,
    }
    driver = peewee_drivers.get(db_driver)

    dbpfn = 'passwd' if db_driver == 'mysql' else 'password'
    db_conn = {
        'host': db_host,
        'user': db_user,
        dbpfn: db_password,
    }
    if db_port:
        db_conn['port'] = int(db_port)

    if driver == peewee.SqliteDatabase:
        db_conn = {}

    db = driver(db_name, **db_conn)

    return db


combode_conf = get_combode_conf()
network = get_network()
rpc_host = get_rpchost()
db = get_db_conn()
