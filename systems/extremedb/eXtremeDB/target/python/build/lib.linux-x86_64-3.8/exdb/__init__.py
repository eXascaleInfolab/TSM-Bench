name = "exdb"

import os
import sys
#import ctypes
from inspect import isclass

apilevel = "2.0"
threadsafety = 1
paramstyle = "qmark"

_eXtremeDB = None
_eXtremeSQL = None
_eXtremeHA = None
_eXtremeCluster = None
_eXtremeIOT = None

_convert_py2value = None
_convert_value2py = None


#
# Dictionary description
#

class InvalidTypeException(Exception):
    pass

class ArgumentException(Exception):
    pass

class InvalidOperationException(Exception):
    pass

class Warning(Exception):
    pass

class Error(Exception):
    def __init__(self, code, msg, filename, line, text = None, info = None):
        self.code = code
        self.msg = msg
        self.file = "%s:%s" % (filename, line)
        self.text = text
        self.info = info

    def __str__(self):
        ret = " %s (%s)" % (self.code, self.msg)
        if not self.text is None:
            ret += " - '" + self.text + "'"
        if not self.info is None:
            ret += " " + str(self.info)

        ret += " at %s." % self.file
        return ret

class InterfaceError(Error):
    pass

class DatabaseError(Error):
    pass

class DataError(DatabaseError):
    pass

class OperationalError(DatabaseError):
    pass

class IntegrityError(DatabaseError):
    pass

class InternalError(DatabaseError):
    pass

class ProgrammingError(DatabaseError):
    pass

class NotSupportedError(DatabaseError):
    pass

class HACancelError(BaseException):
    pass

class StructDescriptor:
    def __init__(self):
        self.parent_class = None

class EventDescriptor:
    OnNew = 1
    OnFieldUpdate = 2
    OnDelete = 4
    OnDeleteAll  = 8
    OnCheckpoint = 16
    OnUpdate = 32

    def __init__(self):
        self.flags = 0


class eXtremeDBField(object):
    def __init__(self):
        self.struct = None
        self.event = None


class Int1Field(eXtremeDBField):
    def __init__(self, dimension=None):
        return


class Int2Field(eXtremeDBField):
    def __init__(self, dimension=None):
        return


class Int4Field(eXtremeDBField):
    def __init__(self, dimension=None):
        return


class Int8Field(eXtremeDBField):
    def __init__(self, dimension=None):
        return


class UInt1Field(eXtremeDBField):
    def __init__(self, dimension=None):
        return


class UInt2Field(eXtremeDBField):
    def __init__(self, dimension=None):
        return


class UInt4Field(eXtremeDBField):
    def __init__(self, dimension=None):
        return


class UInt8Field(eXtremeDBField):
    def __init__(self, dimension=None):
        return


class DateTimeField(eXtremeDBField):
    def __init__(self, dimension=None):
        return

class AutoIDField(eXtremeDBField):
    def __init__(self, dimension=None):
        return


class AutoOIDField(eXtremeDBField):
    def __init__(self, dimension=None):
        return


class RefField(eXtremeDBField):
    def __init__(self, dimension=None):
        return


class FloatField(eXtremeDBField):
    pass


class DoubleField(eXtremeDBField):
    pass


class CharField(eXtremeDBField):
    pass


class StringField(eXtremeDBField):
    pass


class BinaryField(eXtremeDBField):
    pass


class UnicodeCharsField(eXtremeDBField):
    pass


class UnicodeStringField(eXtremeDBField):
    pass


class BlobField(eXtremeDBField):
    pass


class StructField(eXtremeDBField):
    def __init__(self, base):
        self.base = base
        return


class DecimalField(eXtremeDBField):
    def __init__(self, base):
        self.base = base
        return


class SequenceField(eXtremeDBField):
    def __init__(self, base):
        if type(base) == type(type):
            self.base = base()
        elif not type(base) in [Int1Field, Int2Field, Int4Field, Int8Field,
                                UInt1Field, UInt2Field, UInt4Field, UInt8Field,
                                FloatField, DoubleField, CharField, DateTimeField]:
            raise InvalidTypeException("Invalid base %s of type %s" % (base, type(base)))
        self.base = base
        return


class VectorField(eXtremeDBField):
    def __init__(self, base):
        self.base = base
        return


class ArrayField(eXtremeDBField):
    def __init__(self, base, size):
        self.dimension = size
        self.base = base
        return


class TimeField(eXtremeDBField):
    pass


class DateField(eXtremeDBField):
    pass


class BooleanField(eXtremeDBField):
    pass


class IndexType:
    Hashtable = 0
    BTree = 1
    Patricia = 2
    RTree = 3
    Trigram = 4

    def __init__(self, kind=BTree):
        self.kind = kind


class SeqIteratorBoundary(object):
    MCO_SEQ_BOUNDARY_OPEN = 0
    MCO_SEQ_BOUNDARY_INCLUSIVE = 1
    MCO_SEQ_BOUNDARY_EXCLUSIVE = 2


class RuntimeOption(object):
    MCO_RT_OPTION_EXTHEAPS = 0
    MCO_RT_WINDOWS_SHM_OPT = 1
    MCO_RT_OPTION_MARK_LAST_OBJ = 2
    MCO_RT_OPTION_UNIX_SHM_MASK = 3
    MCO_RT_POSIX_SHM_OPT = 4
    MCO_RT_CRC_ALGORITHM = 5
    MCO_RT_MAX_PATRICIA_DEPTH = 6
    MCO_RT_MAX_DYNAMIC_PIPES = 7
    MCO_RT_OPTION_CLASS_LOAD_MERGE = 8
    MCO_RT_OPTION_DATETIME_PRECISION = 9    # Time resolution (precision): 1 - seconds, 1000 - milliseconds, 1000000 - microseconds,...

    MCO_RT_CRC32_NONE = 0  # do not calculate
    MCO_RT_CRC32 = 1  # block implementation
    MCO_RT_CRC32_FAST = 2  # calculate CRC only for firld and last 8-byte word of data
    MCO_RT_CRC32_OLD = 3  # implementation of CRC used prior release 12823 2013-01-28
    MCO_RT_CRC32C = 4  # CRC32C hardware&software implementations used after release 15523 2014-07-17


class McoSockDomain(object):
    InetDomain = 0
    LocalDomain = 1
    SDPDomain = 2


class SSLVerifyMode(object):
    VerifyNone = 0
    VerifyPeer = 1
    VerifyFailIfNoPeerCert = 2
    VerifyClientOnce = 4


class SSLOptions(object):
    # Disable SSL 2.
    NO_SSLV2 =   0x01

    # Disable SSL 3
    NO_SSLV3 = 0x02

    # Disable TLS 1.0.
    NO_TLSV1_0 = 0x04

    # Disable TLS 1.1.
    NO_TLSV1_1 = 0x08

    # Disable TLS 1.2.
    NO_TLSV1_2 = 0x10

    # Disable compression.
    OPT_NO_COMPRESSION = 0x20

    # Always create a new key when using ephemeral DH parameters
    SINGLE_DH_USE = 0x40


def init_runtime(disk=False, tmgr='mursiw', shm=False,
                 sync_library=None, memory_library=None, runtime_path=None,
                 debug=False, dptr=False,
                 cluster=False, ha=False, iot=False,
                 options=None,  DiskCompression=False,
                 UsePosixLibraries=False, UsePerfmon=False, skip_load=False, 
                 debug_load=False):
    """
    Initialize eXtremeDB runtime.
        disk, tmgr, shm, debug, cluster, ha, iot - select appropriate runtime library
        options - runtime option(s) to be set before call to mco_runtime_start. It can be either tuple (OPTION, VALUE) or a list of such tuples
    """
    global _eXtremeDB, _eXtremeSQL, _eXtremeHA, _eXtremeCluster, _eXtremeIOT

    suffix = '_py%s' % sys.version_info.major

    if debug:
        suffix += '_debug'

    if dptr:
        suffix += '_dptr'
        bin_so_dir = 'bin.dptr.so'
    else:
        suffix += '_offs'
        bin_so_dir = 'bin.so'

    modname = 'eXtremeDB' + suffix
    modname_sql = 'eXtremeSQL' + suffix
    modname_ha = 'eXtremeHA' + suffix
    modname_cluster = 'eXtremeCluster' + suffix
    modname_iot = 'eXtremeIOT' + suffix

    bin_so_path = None
    if runtime_path is None:
        if 'MCO_ROOT' in os.environ:
            bin_so_path = os.path.join(os.environ['MCO_ROOT'], 'target', bin_so_dir)
        else:
            bin_so_path = os.path.abspath(os.path.join(os.path.dirname(sys.executable), '..', bin_so_dir))

        runtime_path = os.environ.get('MCO_LIBRARY_PATH', None)

        if runtime_path is None:
            runtime_path = bin_so_path
            os.environ['MCO_LIBRARY_PATH'] = runtime_path

    eXtremeDB_load = None
    if sys.platform in ('win32',):
        pythonpath = os.path.dirname(sys.executable)
        python_root = os.path.abspath(os.path.join(pythonpath, ".."))

        if sys.version_info[0] == 3:
            pythonpath_a = bytes(pythonpath, "utf-8")
        else:
            pythonpath_a = pythonpath

        import ctypes
        res = ctypes.windll.kernel32.SetDllDirectoryA(pythonpath_a)
        if res == 0:
            raise Exception("SetDLLDirectoryA failed: LastError=%s, pythonpath=%s" %
                            (ctypes.windll.kernel32.GetLastError(), pythonpath_a))

        if bin_so_path:
            bin_so_path = os.path.abspath(bin_so_path)
            if sys.version_info[0] == 3:
                bin_so_path_a = bytes(bin_so_path, "utf-8")
            else:
                bin_so_path_a = bin_so_path

            res = ctypes.windll.kernel32.SetDllDirectoryA(bin_so_path_a)
            if res == 0:
                raise Exception("SetDLLDirectoryA failed: LastError=%s, bin_so_path=%s" %
                                (ctypes.windll.kernel32.GetLastError(), bin_so_path_a))
            os.environ['PATH'] += os.pathsep + bin_so_path
    else:
        if not sync_library or sync_library is True:
            if sys.platform == 'darwin':
                sync_library = 'mcosmacos'
            else:
                sync_library = 'mcoslnxp'
        if not memory_library:
            memory_library = ['mcomipc', 'mcomconv'][shm]

        if sys.version_info[0] == 2:
            import eXtremeDB_load_py2 as eXtremeDB_load
        else:
            import eXtremeDB_load_py3 as eXtremeDB_load
        sys.setdlopenflags(1)            

        if not skip_load:
            eXtremeDB_load._loadDependencies(disk, tmgr, shm, debug, cluster, ha, iot, DiskCompression,
                                             UsePosixLibraries, UsePerfmon)

    # Load modules
    _eXtremeDB = __import__(modname)
    _eXtremeDB.runtime_start(globals(), disk, tmgr.lower() == 'mvcc', shm,
                             sync_library, memory_library, runtime_path)

    # Optional modules
    try:
        if eXtremeDB_load and not skip_load:
            eXtremeDB_load._loadDependenciesSQL(debug)

        _eXtremeSQL = __import__(modname_sql)
        _eXtremeSQL.init(globals(), _eXtremeDB.__dict__)
        global _convert_py2value
        _convert_py2value = _eXtremeSQL._convert_py2value

        global _convert_value2py
        _convert_value2py = _eXtremeSQL._convert_value2py

    except:
        # SQL is not available on this system
        if debug_load:
            import traceback
            traceback.print_exc()
        pass

    if cluster and ha:    
        raise DatabaseError("Cluster runtime and HA runtime can not be used together")    

    if ha:
        try:
            _eXtremeHA = __import__(modname_ha)
            _eXtremeHA.init(globals(), _eXtremeDB.__dict__)
        except Exception as exc:
            # HA is not available on this system
            if debug_load:
                import traceback
                traceback.print_exc()
            pass

    if cluster:
        try:
            _eXtremeCluster = __import__(modname_cluster)
            _eXtremeCluster.init(globals(), _eXtremeDB.__dict__)
        except Exception as exc:
            # Cluster is not available on this system
            if debug_load:
                import traceback
                traceback.print_exc()
            pass

    if iot:
        try:
            _eXtremeIOT = __import__(modname_iot)
            _eXtremeIOT.init(globals(), _eXtremeDB.__dict__)
        except Exception as exc:
            # IOT is not available on this system
            if debug_load:
                import traceback
                traceback.print_exc()
            pass

    if options is not None:
        if type(options) == list:
            for opt in options:
                _eXtremeDB.runtime_setoption(opt[0], opt[1])
        elif type(options) == tuple:
            _eXtremeDB.runtime_setoption(options[0], options[1])

    if _eXtremeHA and "MasterConnection" in dir(_eXtremeHA):
        setattr(sys.modules[__name__], "MasterConnection", _eXtremeHA.MasterConnection)
        setattr(sys.modules[__name__], "ReplicaConnection", _eXtremeHA.ReplicaConnection)

    if "SequenceIterator" in dir(_eXtremeDB):
        setattr(sys.modules[__name__], "SequenceIterator", _eXtremeDB.SequenceIterator)

    if _eXtremeSQL and "SqlEngine" in dir(_eXtremeSQL):
        setattr(sys.modules[__name__], "SqlEngine", _eXtremeSQL.SqlEngine)
        setattr(sys.modules[__name__], "SqlServer", _eXtremeSQL.SqlServer)
        setattr(sys.modules[__name__], "SqlAggregator", _eXtremeSQL.SqlAggregator)
        setattr(sys.modules[__name__], "AggregatedConnection", _eXtremeSQL.AggregatedConnection)

    if _eXtremeIOT and "IoTCommunicator" in dir(_eXtremeIOT):
        setattr(sys.modules[__name__], "IoTCommunicator", _eXtremeIOT.IoTCommunicator)

    if _eXtremeIOT and "IoTReplicator" in dir(_eXtremeIOT):
        setattr(sys.modules[__name__], "IoTReplicator", _eXtremeIOT.IoTReplicator)


def stop_runtime():
    _eXtremeDB.runtime_stop()


def get_runtime_info():
    runtime_info = _eXtremeDB.get_runtime_info()
    return runtime_info


def get_net_capabilities():
    return _eXtremeDB.get_net_capabilities()


def get_registry():
    global _eXtremeDB
    return _eXtremeDB.get_registry()


class ReplicationType(object):
    SQL_REPLICATION = 0
    HA_REPLICATION  = 1


def runtime_setoption(option, value):
    global _eXtremeDB
    _eXtremeDB.runtime_setoption(option, value)


def runtime_getoption(option):
    global _eXtremeDB
    return _eXtremeDB.runtime_getoption(option)


MCO_TRACE_FATAL = 0
MCO_TRACE_ERROR = 1
MCO_TRACE_WARNING = 2
MCO_TRACE_NOTICE =3
MCO_TRACE_INFO = 4
MCO_TRACE_DEBUG = 5
MCO_TRACE_VERBOSE = 6


def trace(severity, msg):
    global _eXtremeDB
    _eXtremeDB.trace(severity, msg)


def fatal(msg):
    global _eXtremeDB
    _eXtremeDB.trace(MCO_TRACE_FATAL, msg)


def error(msg):
    global _eXtremeDB
    _eXtremeDB.trace(MCO_TRACE_ERROR, msg)


def warning(msg):
    global _eXtremeDB
    _eXtremeDB.trace(MCO_TRACE_WARNING, msg)


def notice(msg):
    global _eXtremeDB
    _eXtremeDB.trace(MCO_TRACE_NOTICE, msg)


def info(msg):
    global _eXtremeDB
    _eXtremeDB.trace(MCO_TRACE_INFO, msg)


def debug(msg):
    global _eXtremeDB
    _eXtremeDB.trace(MCO_TRACE_DEBUG, msg)


def connect(dbname=None, port=None, nodes=None, host=None,
            use_sql=None,
            nReplicas=1, replType=ReplicationType.SQL_REPLICATION,
            maxConnectAttempts=10, local=False,
            useConnectionPool=False, recover=False, txBufSize=64*1024,
            connectTimeout=2000, readTimeout=1200*1000,
            sql_login=None, sql_password=None, ssl_params=None, nWorkers=2, compressionLevel=0):
    """ Connect to existing database.
          To connect to existing database, either shared memory or in-proc use name parameter only. This will create
            Connection instance and will allow to use object-level API

          To connect to existing data, either shared memory or in-proc, use name parameter and apply use_sql=True.
          This will create SqlConnection object and will allow to use DB API SQL protocol

          By default it will create SqlConnection if eXtremeSQL module is loaded, and Connection if not.
          SqlConnection allows direct API operations.

          To connect to RSQL database and use DB API SQL protocol, use host and port parameters. This will create
          RemoteConnection object and will allow to use DB API SQL protocol

          To connect to Distributed SQL database use named parameters nodes and maxConnectAttempts. This will create
          DistributedConnection object and will allow to use DB API SQL protocol
    """

    global _eXtremeDB
    global _eXtremeSQL

    if nodes is None:

        if dbname and not port and ':' in dbname:
            host, port = dbname.split(':')
            port = int(port)
        elif host and not port and ':' in host:
            host, port = host.split(':')
            port = int(port)

        if host or (type(dbname) is str and port):
            # RSQL connection
            if dbname and not host:
                host = dbname

            conn = _eXtremeSQL.connect_remote(host=host, port=port, maxConnectAttempts=maxConnectAttempts,
                                              useConnectionPool=useConnectionPool,
                                              txBufSize=txBufSize, localDomain=local, connectTimeout=connectTimeout,
                                              readTimeout=readTimeout,sql_login=sql_login, sql_password=sql_password,
                                              ssl_params=ssl_params,
                                              compressionLevel=compressionLevel)
        else:
            if use_sql or (_eXtremeSQL and use_sql is None):
                # This is local SQL connection
                conn = _eXtremeSQL.connect(dbname=dbname)
            else:
                # This is local API connection
                conn = _eXtremeDB.connect(dbname=dbname)

                if recover and 'sniffer' in dir(conn):
                    conn.sniffer()
    else:
        # This is distributed connection to shards
        conn = _eXtremeSQL.connect_distributed(
            nodes=nodes, nReplicas=nReplicas, replType=replType,
            maxConnectAttempts=maxConnectAttempts, useConnectionPool=useConnectionPool,
            txBufSize=txBufSize, localDomain=local, connectTimeout=connectTimeout, readTimeout=readTimeout,
            sql_login=sql_login, sql_password=sql_password, ssl_params=ssl_params,
            compressionLevel=compressionLevel)

    return conn


b2i = {True: 1, False:0}


def load_dictionary(schema, nosort=True, dumpxml=False, genhpp=False, gencs=False, genjava=False,
                    outDir='.', csNamespace='eXtremeDB',
                    javaPackage='eXtremeDB', cmode1=False, genXmlMethods=False, genJsonMethods=False, genSql=False,
                    largeDatabase=False, wcharSize=2,
                    use_prefix=False, include_dir='.', compact=False, persistent=False, transient=False,
                    suppress_api=False, debug=False):
    global _eXtremeDB

    return _eXtremeDB.load_dictionary(
        schema,
        debug=b2i[debug], nosort=b2i[nosort],
        dumpxml=b2i[dumpxml], genhpp=b2i[genhpp], gencs=b2i[gencs], genjava=b2i[genjava],
        outDir=outDir, csNamespace=csNamespace, javaPackage=javaPackage,
        cmode1 = b2i[cmode1],
        genXmlMethods =b2i[genXmlMethods],
        genJsonMethods =b2i[genJsonMethods],
        genSql = b2i[genSql],
        largeDatabase = b2i[largeDatabase], wcharSize=wcharSize,
        use_prefix=b2i[use_prefix], include_dir=include_dir, compact=b2i[compact],
        persistent=b2i[persistent],
        transient=b2i[transient], suppress_api=b2i[suppress_api] )


def register_function(rettype, name, func, n_args):
    _eXtremeSQL.register_function(rettype, name, func, n_args)


def open_database(dbname, dictionary, is_disk = False,
                  db_segment_size = 128*1024*1024, cache_segment_size = 16*1024*1024,
                  mem_page_size=256, disk_page_size=4096, db_log_type="REDO_LOG",
                  log_params = None,
                  db_params_mode_mask = 0,
                  devices = None,
                  disk_max_database_size = 0, file_extension_quantum = 4096*1024,
                  db_max_connections = 100, databaseSnapshotFilePath = None,
                  clusterParams = None, max_classes = 100, max_indexes = 1000, maxDictionarySize = 32*1024,
                  backup_map_size = 0, backup_min_pages = 0, backup_max_passes = 10, backup_map_filename = None,
                  cipherKey=None,
                  compressionLevel=-1, compressionMask=4099, expectedCompressionRatio=20,
                  iot_agent_id=0,
                  ignore_ttl=False):
    """ 
        Create memory for database and open it.
    """

    if is_disk and not disk_page_size >= 8*mem_page_size:
        raise Exception("Disk page should be at least 8 times greater than memory page")

    if clusterParams:
        db = _eXtremeCluster.ClusterDatabase()
    else:
        db = _eXtremeDB.Database()

    db.prepare(
        dbname=dbname, dictionary=dictionary, is_disk=is_disk,
        db_segment_size=db_segment_size,
        cache_segment_size=cache_segment_size,
        mem_page_size=mem_page_size,
        disk_page_size=disk_page_size,
        db_log_type=db_log_type,
        disk_max_database_size=disk_max_database_size,
        log_params=log_params,
        params_mode_mask=db_params_mode_mask,
        devices=devices,
        file_extension_quantum=file_extension_quantum,
        db_max_connections=db_max_connections,
        max_classes=max_classes, max_indexes=max_indexes, maxDictionarySize=maxDictionarySize,
        backup_map_size=backup_map_size, backup_min_pages=backup_min_pages,
        backup_max_passes=backup_max_passes, backup_map_filename=backup_map_filename,
        cipherKey=cipherKey,
        compressionLevel=compressionLevel, compressionMask=compressionMask,
        expectedCompressionRatio=expectedCompressionRatio,
        iot_agent_id=iot_agent_id,
        ignore_ttl=ignore_ttl
    )

    if clusterParams:
        db.cluster_open(clusterParams)
    else:
        db.create(databaseSnapshotFilePath=databaseSnapshotFilePath)

    return db


def create_file_stream(filename):
    """ Create file stream for trans. iterator.
    """
    return _eXtremeDB.create_file_stream(filename=filename)


def create_socket_stream(hostname, port, listen = False, write_timeout = -1, buffer_size = -1, max_clients = -1, 
                                         connect_timeout = -1, connect_attempts = -1, connect_interval = -1, reconnect = -1, socket_domain = -1, compression_level = -1):
    """ Create socket stream for trans. iterator.
    """
    return _eXtremeDB.create_socket_stream(hostname = hostname, port = port, listen = listen, write_timeout = write_timeout, 
                                        buffer_size = buffer_size, max_clients = max_clients, connect_timeout = connect_timeout, 
                                        connect_attempts = connect_attempts, connect_interval = connect_interval, reconnect = reconnect, 
                                        socket_domain = socket_domain, compression_level = compression_level)


def create_tee_stream(stream_1, stream_2, any_ok = True):
    """ Duplicate output to both  stream_1 and stream_2.
    """
    return _eXtremeDB.create_tee_stream(stream_1, stream_2, any_ok)


def create_json_iterator(stream, compact = -1, ignore_stream_errors = -1):
    """ Create JSON or trans. iterator.
    """
    return _eXtremeDB.create_json_iterator(stream=stream, compact=compact, ignore_stream_errors=ignore_stream_errors)


def destroy_trans_iterator(iterator) :
    return _eXtremeDB.destroy_trans_iterator(iterator)


def destroy_stream(stream) :
    return _eXtremeDB.destroy_stream(stream)


def close_database(dbname):
    rc = _eXtremeDB.close_database(dbname)
    return  rc


def set_errhandler(fn):
    """
    Set fatal error handler
    """
    _eXtremeDB.set_errhandler(fn)


def ssl_init():
    """
    Initialize SSL layer
    """
    _eXtremeDB.ssl_init()


def ssl_load_verify_locations(ca_file, ca_path = None):
    _eXtremeDB.ssl_load_verify_locations(ca_file, ca_path)


def aio_start(max_queue_length, n_workers):
    _eXtremeDB.aio_start(max_queue_length, n_workers)


def aio_stop():
    _eXtremeDB.aio_stop()


class SequenceGroupIterator:
    def __init__(self, args):
        self.iters = args

    def __iter__(self):
        return self

    def next(self):
        return _eXtremeDB.seq_iterate(*self.iters)


def seq_iterate(*args):
    """
        Return iterator over a group of eXtremeDB sequence iterators
    """
    return SequenceGroupIterator(args)


def _attach_sql_session(session):
    return _eXtremeSQL._attach_sql_session(session)


class Database(object):
    MCO_DB_FT_NONE = 0
    MCO_DB_FT_UINT1 = 1
    MCO_DB_FT_UINT2 = 2
    MCO_DB_FT_UINT4 = 3
    MCO_DB_FT_INT1 = 4
    MCO_DB_FT_INT2 = 5
    MCO_DB_FT_INT4 = 6
    MCO_DB_FT_CHARS = 7
    MCO_DB_FT_STRING = 8
    MCO_DB_FT_REF = 9
    MCO_DB_FT_FLOAT = 10
    MCO_DB_FT_DOUBLE = 11
    MCO_DB_FT_UINT8 = 12
    MCO_DB_FT_INT8 = 13
    MCO_DB_FT_AUTOID = 14 # 8 byte
    MCO_DB_FT_OBJVERS = 15 # 2 byte
    MCO_DB_FT_DATE = 16
    MCO_DB_FT_TIME = 17
    MCO_DB_FT_AUTOOID = 18
    MCO_DB_FT_UNICODE_CHARS = 19
    MCO_DB_FT_UNICODE_STRING = 20
    MCO_DB_FT_WIDE_CHARS = 21
    MCO_DB_FT_WCHAR_STRING = 22
    MCO_DB_FT_BOOL = 23

    MCO_DB_FT_SEQUENCE_UINT1 =  30
    MCO_DB_FT_SEQUENCE_UINT2 =  31
    MCO_DB_FT_SEQUENCE_UINT4 =  32
    MCO_DB_FT_SEQUENCE_UINT8 =  33
    MCO_DB_FT_SEQUENCE_INT1	 =  34
    MCO_DB_FT_SEQUENCE_INT2  =	35
    MCO_DB_FT_SEQUENCE_INT4	 =  36
    MCO_DB_FT_SEQUENCE_INT8	 =  37
    MCO_DB_FT_SEQUENCE_FLOAT =  38
    MCO_DB_FT_SEQUENCE_DOUBLE=  39
    MCO_DB_FT_SEQUENCE_CHAR	 =  40

    MCO_DB_FT_STRUCT = 50
    MCO_DB_FT_BLOB = 51


class Event:
    NewEvent = 1
    DeleteEvent = 2
    UpdateEvent = 3
    CheckPointEvent = 4


class SyncEvent:
    NewEvent = 1    
    UpdateEvent = 2
    DeleteEvent = 4
    DeleteAllEvent = 8
    CheckPointEvent = 16
    ClassUpdateEvent = 32


class EventHandlingOrder:
    BeforeUpdate = 0
    AfterUpdate = 1


class Transaction(object):
    MCO_READ_ONLY = 0
    MCO_UPDATE = 1
    MCO_READ_WRITE = 2
    MCO_EXCLUSIVE = 3

    #MCO_TRANS_PRIORITY
    MCO_TRANS_IDLE       = -2
    MCO_TRANS_BACKGROUND = -1
    MCO_TRANS_FOREGROUND = 0
    MCO_TRANS_HIGH       = 1
    MCO_TRANS_ISR        = 2


class Operation(object):
    LessThan = 1
    LessOrEquals = 2
    Equals = 3
    GreaterOrEquals = 4
    GreaterThan = 5
    Overlaps = 6
    Contains = 7
    ExactMatch = 8
    BestMatch = 9
    PrefixMatch = 10
    NextMatch = 11
    Neighbourhood = 12
    StrictEquals = 13
    IsPrefixOf = 14


class Position(object):
    Unknown = 0
    Empty = 1
    First = 2
    Curr = 3
    DeleteNext = 4
    DeletePrev = 5


class Direction(object):
    Unknown = 0
    Forward = 1
    Backward= 2


class SortOrder(object):
    NoOrder = 0
    Ascending = 1
    Descending = 2


class CommitPolicy(object):
    SyncFlush = 0
    Buffered  = 1
    Delayed   = 2
    NoSync    = 3


class SnifferPolicy(object):
    InspectActiveConnections  = 0
    InspectActiveTransactions = 1
    InspectHangedTransactions = 2


class SnifferResult(object):
    Ok             =  0
    DeadConnection = 15


class DbParamsModeMask(object):
    MVCC_AUTO_VACUUM = 1
    SMART_INDEX_INSERT = 2
    OPEN_EXISTING  = 4
    USE_CRC_CHECK  = 8
    TRANSIENT      = 0x10
    LAZY_MEM_INITIALIZATION = 0x20
    MURSIW_DISK_COMMIT_OPTIMIZATION = 0x40
    BULK_WRITE_MODIFIED_PAGES = 0x80
    TRANS_LOG_FAST_CRC = 0x100
    INDEX_PRELOAD = 0x200
    DISABLE_NESTED_TRANSACTIONS = 0x0400
    DISABLE_IMPLICIT_ROLLBACK = 0x0800
    INMEMORY_PROTECTION = 0x1000
    INCLUSIVE_BTREE = 0x2000
    INMEMORY_COMPRESSION = 0x4000
    SEPARATE_BITMAP = 0x8000
    DISABLE_BTREE_REBALANCE_ON_DELETE = 0x10000
    AUTO_ROLLBACK_FIRST_PHASE = 0x20000
    MVCC_COMPATIBILITY_MODE = 0x40000
    DISABLE_PAGE_POOL_RESERVE = 0x80000
    REDO_LOG_OPTIMIZATION = 0x100000
    DISABLE_HOT_UPDATES = 0x200000
    SQL_AUTOCHECKPOINT = 0x400000
    MODE_READ_ONLY = 0x800000
    USE_AIO = 0x1000000
    INCREMENTAL_BACKUP = 0x2000000


class LogParams(object):

    MCO_COMMIT_SYNC_FLUSH = 0
    MCO_COMMIT_BUFFERED = 1
    MCO_COMMIT_DELAYED  = 2
    MCO_COMMIT_NO_SYNC  = 3

    def __init__(self, RedoLogLimit=None, DelayedCommitThreshold=None,
                 DefaultCommitPolicy=None, MaxDelayedTransactions=None,
                 MaxCommitDelay=None):
        self.RedoLogLimit = RedoLogLimit
        self.DelayedCommitThreshold = DelayedCommitThreshold
        self.DefaultCommitPolicy = DefaultCommitPolicy
        self.MaxDelayedTransactions = MaxDelayedTransactions
        self.MaxCommitDelay = MaxCommitDelay

    def __repr__(self, *args, **kwargs):
        return "<LogParams. RedoLogLimit=%s, DelayedCommitThreshold=%s, DefaultCommitPolicy=%s>" % (self.RedoLogLimit, self.DelayedCommitThreshold, self.DefaultCommitPolicy)


class Backup(object):
    MCO_BACKUP_TYPE_AUTO        = 0
    MCO_BACKUP_TYPE_SNAPSHOT    = 1
    MCO_BACKUP_TYPE_INCREMENTAL = 2

    MCO_BACKUP_FLAG_COMPRESSED  = 1
    MCO_BACKUP_FLAG_ENCRYPTED   = 2
    

###############################################################################
#  SQL definition
###############################################################################
class SqlOpenParameters(object):
    #        /* Allocate memory buffer of specified size for eXtremeDB database
    #     using malloc function (value of mapAddress parameter is ignored).
    #     If this flag is not set, specified value of mapAddress parameter is used.
    #     This flag is ignored for shared memory database, in which case mapAddress
    #     always specifies mapping address.
    ALLOCATE_MEMORY = 1
    SET_ERROR_HANDLER = 2         # Set McoSql specific error handler. */
    START_MCO_RUNTIME = 4         # Start MCO runtime.*/
    INITIALIZE_DATABASE = 16      # Initialize new database instance (call mco_db_open).*/
    PRESERVE_SHARED_DATABASE = 32 # Do not close database, keeping it in shared memory*/
    FOREIGN_CONNECTION = 64       # Connection was established outside SqlEngine: do not perform disconnect and database close */
    DEFAULT_OPEN_FLAGS = ALLOCATE_MEMORY | SET_ERROR_HANDLER | START_MCO_RUNTIME | INITIALIZE_DATABASE

    def __init__(self, databaseName, dictionary, mainMemoryDatabaseSize, mainMemoryPageSize, mainMemoryDatabaseAddress = 0,
                 maxClasses = 100, maxIndexes = 1000, maxDictionarySize = 64*1024,
                 diskDatabaseFile = None, diskDatabaseLogFile = None, diskCacheSize = 0, defaultCommitPolicy = CommitPolicy.SyncFlush,
                 flags = DEFAULT_OPEN_FLAGS,
                 backupMapSize = 0, backupMinPages = 0, backupMaxPasses = 10, backupMapFile = None):
        self.databaseName = databaseName
        self.dictionary = dictionary
        self.mainMemoryDatabaseSize = mainMemoryDatabaseSize
        self.mainMemoryPageSize = mainMemoryPageSize
        self.mainMemoryDatabaseAddress = mainMemoryDatabaseAddress
        self.maxClasses = maxClasses
        self.maxIndexes = maxIndexes
        self.maxDictionarySize = maxDictionarySize
        self.diskDatabaseFile = diskDatabaseFile
        self.diskDatabaseLogFile = diskDatabaseLogFile
        self.diskCacheSize = diskCacheSize
        self.defaultCommitPolicy = defaultCommitPolicy
        self.flags = flags
        self.backupMapSize = backupMapSize
        self.backupMinPages = backupMinPages
        self.backupMaxPasses = backupMaxPasses
        self.backupMapFile = backupMapFile


def set_sql_workspace_limit(limit):
    return _eXtremeSQL.set_workspace_limit(limit)


###############################################################################
#  Network definitions
###############################################################################

class SockDomain:
    InetDomain = 0  #IPv4 or IPv6
    InetV4Domain = 1 #IPv4 only
    InetV6Domain = 2 #IPv6 only
    LocalDomain = 3
    SDPDomain = 4


###############################################################################
#  Cluster definition
###############################################################################

class ClusterNodeParams(object):
    def __init__(self, addr, qrank = 1):
        self.addr = addr
        self.qrank = qrank


class ClusterNWParams(object):
    pass


class ClusterTCPParams(ClusterNWParams):
    def __init__(self, connectTimeout=5000, connectInterval=200, socketSendBuf=0, socketRecvBuf=0,
                 socketDomain=McoSockDomain.InetDomain, keepAliveTime=1000, keepAliveProbes = 10,
                 ssl_params = None, compressionLevel = 0):
        self.connectTimeout  = connectTimeout
        self.connectInterval = connectInterval
        self.socketSendBuf   = socketSendBuf
        self.socketRecvBuf   = socketRecvBuf
        self.socketDomain    = socketDomain
        self.keepAliveTime   = keepAliveTime
        self.keepAliveProbes = keepAliveProbes
        self.ssl_params      = ssl_params
        self.compressionLevel = compressionLevel


class ClusterMPIParams(ClusterNWParams):
    def __init__(self, flags):
        self.flags = flags


class ClusterWindow(object):
    def __init__(self, bsize = 0, length = 0, timeout = 1):
        self.bsize   = bsize
        self.length  = length
        self.timeout = timeout


class ClusterParams(object):
    def __init__(self, nodeId, nwtype, nodes=[], nwparams=None, MPICluster=False,
                 window = None, conn_pool_factor = 50, sync_msg_objects = 100, sync_msg_size = 0,
                 notifyCallback=None, quorumCallback = None,
                 clusterSendBuf=0, clusterRecvBuf=0, mode_mask=0):
        self.nodeId = nodeId
        self.type = nwtype
        self.nodes = nodes
        self.nwparams = nwparams
        self.MPICluster = MPICluster
        self.window = ClusterWindow() if window is None else window
        self.conn_pool_factor = conn_pool_factor
        self.sync_msg_objects = sync_msg_objects
        self.sync_msg_size = sync_msg_size
        self.clusterSendBuf = clusterSendBuf
        self.clusterRecvBuf = clusterRecvBuf
        self.quorumCallback = quorumCallback
        self.notifyCallback = notifyCallback
        self.mode_mask = mode_mask

    def __repr__(self, *args, **kwargs):
        return "<ClusterParams. nodeId=%s dir=%s>" % (self.nodeId, dir(self))


class ClusterNodeInfo(object):
    def __init__(self, addr, qrank, nodeId):
        self.addr = addr
        self.qrank = qrank
        self.nodeId = nodeId

    def __repr__(self, *args, **kwargs):
        return "<ClusterNodeInfo: addr=%s, qrank=%s, nodeId=%s>" %(self.addr, self.qrank, self.nodeId)


###########################################################################################################
#    HA
###########################################################################################################

# master modes
MCO_MASTER_MODE = 0x1
MCO_HAMODE_MULTIPROCESS_COMMIT = 0x2
MCO_HAMODE_ASYNCH = 0x4
MCO_HAMODE_MCAST = 0x8
MCO_HAMODE_MCAST_RELIABLE = 0x10
MCO_HAMODE_HOTSYNCH = 0x20
MCO_HAMODE_STATEFUL_REPLICATION = 0x40
MCO_HAMODE_BINEVOLUTION = 0x80

# replica modes
MCO_HAMODE_ALLOW_CANCEL = 0x2000
MCO_HAMODE_FORCE_MASTER = 0x4000
MCO_HAMODE_REPLICA_NOTIFICATION = 0x8000
MCO_HAMODE_FORCE_SYNC = 0x10000
MCO_HAMODE_SEND_RESTLIST = 0x20000
MCO_HAMODE_EXPLICIT_WRITE_ACCESS = 0x40000


class HANotifications(object):
    # "connected" notification
    MCO_REPL_NOTIFY_CONNECTED = 0

    # "connect failed" notification
    MCO_REPL_NOTIFY_CONNECT_FAILED = 1

    # "no need to load DB" notification
    MCO_REPL_NOTIFY_DB_EQUAL = 2

    # "begin loading DB" notification
    MCO_REPL_NOTIFY_DB_LOAD_BEGIN = 3

    # "loading failed" notification, "param1" of notification callback contains MCO_RET code
    MCO_REPL_NOTIFY_DB_LOAD_FAILED = 4

    # "succesful loading" notification, "param1" of notification callback contains MCO_E_HA_REPLICA_STOP_REASON code
    MCO_REPL_NOTIFY_DB_LOAD_OK = 5

    # "commit failed" notification, "param1" of notification callback contains MCO_RET code
    MCO_REPL_NOTIFY_COMMIT_FAILED = 6

    # "stopped" notification
    MCO_REPL_NOTIFY_REPLICA_STOPPED = 7

    # "database creation failed" notification, "param1" of notification callback contains MCO_RET code
    MCO_REPL_NOTIFY_DB_CREATION_FAILED = 8

    # "begining of hot synchronization" notification
    MCO_REPL_NOTIFY_HOTSYNC = 9

    # "end of hot synchronization" notification
    MCO_REPL_NOTIFY_EOHOTSYNC = 10

    # "begining of stateful replication" notification
    MCO_REPL_NOTIFY_STATEFUL_SYNC = 11

    # "end of stateful replication" notification
    MCO_REPL_NOTIFY_STATEFUL_SYNC_END = 12

    # master database was extended by mco_db_extend_dev() call
    MCO_REPL_NOTIFY_MASTER_DB_EXTENDED = 13

    #  master database was cleared by mco_db_clean() call
    MCO_REPL_NOTIFY_MASTER_DB_CLEANED = 14


class HAReplicaStopReason(object):
    MCO_HA_REPLICA_CONNECTION_ABORTED = 0
    MCO_HA_REPLICA_MASTER_REQUESTED_DISCONNECT = 1
    MCO_HA_REPLICA_HANDSHAKE_FAILED = 2
    MCO_HA_REPLICA_STOPPED_BY_LOCAL_REQUEST = 3
    MCO_HA_REPLICA_BECOMES_MASTER = 4


def MasterConnectionParameters(
        commitTimeout=None,
        initialTimeout=None,
        synchTimeout = None,
        detachTimeout = None,
        modeFlags = None,
        maxReplicas = None,
        quorum = None,
        transLogLength = None,
        asyncBuf = None,
        errorHandler = None,
        mcastPort = None,
        mcastAddr = None,
        hotsyncMsgObjects = None,
        hotsyncMsgSize = None,
        hotsyncDelay = None,
        compressionLevel = None):

    if not (_eXtremeHA and "MasterConnectionParameters" in dir(_eXtremeHA)):
        raise Exception ("HA not supported")

    ret = _eXtremeHA.MasterConnectionParameters()

    if not commitTimeout is None:
        ret.commitTimeout = commitTimeout

    if not initialTimeout is None:
        ret.initialTimeout = initialTimeout

    if not synchTimeout is None:
        ret.synchTimeout = synchTimeout

    if not detachTimeout is None:
        ret.detachTimeout = detachTimeout

    if not modeFlags is None:
        ret.modeFlags = modeFlags

    if not maxReplicas is None:
        ret.maxReplicas = maxReplicas

    if not quorum is None:
        ret.quorum = quorum

    if not transLogLength is None:
        ret.transLogLength = transLogLength

    if not asyncBuf is None:
        ret.asyncBuf = asyncBuf

    if not errorHandler is None:
        ret.errorHandler = errorHandler

    if not mcastPort is None:
        ret.mcastPort = mcastPort

    if not mcastAddr is None:
        ret.mcastAddr = mcastAddr

    if not hotsyncMsgObjects is None:
        ret.hotsyncMsgObjects = hotsyncMsgObjects

    if not hotsyncMsgSize is None:
        ret.hotsyncMsgSize = hotsyncMsgSize

    if not hotsyncDelay is None:
        ret.hotsyncDelay = hotsyncDelay

    if not compressionLevel is None:
        ret.compressionLevel = compressionLevel

    return ret


def ReplicaConnectionParameters(commitTimeout = None,
                                initialTimeout = None,
                                waitDataTimeout = None,
                                repeatCounter = None,
                                mcastPort = None,
                                mcastAddr = None,
                                initialCommitPolicy = None,
                                initialObjsInTrans = None,
                                modeFlags = None,
                                notifyCallback = None,
                                iterator = None,
                                cancelpointAddr = None,
                                batchCommitLength = None,
                                batchCommitBSize = None,
                                batchCommitPeriod = None,
                                compressionLevel = None):

    if not (_eXtremeHA and "ReplicaConnectionParameters" in dir(_eXtremeHA)):
        raise Exception ("HA not supported")

    ret = _eXtremeHA.ReplicaConnectionParameters()

    if not commitTimeout is None:
        ret.commitTimeout = commitTimeout

    if not initialTimeout is None:
        ret.initialTimeout = initialTimeout

    if not waitDataTimeout is None:
        ret.waitDataTimeout = waitDataTimeout

    if not repeatCounter is None:
        ret.repeatCounter = repeatCounter

    if not mcastPort is None:
        ret.mcastPort = mcastPort

    if not mcastAddr is None:
        ret.mcastAddr = mcastAddr

    if not initialCommitPolicy is None:
        ret.initialCommitPolicy = initialCommitPolicy

    if not initialObjsInTrans is None:
        ret.initialObjsInTrans = initialObjsInTrans

    if not batchCommitLength is None:
        ret.batchCommitLength = batchCommitLength

    if not batchCommitBSize is None:
        ret.batchCommitBSize = batchCommitBSize

    if not batchCommitPeriod is None:
        ret.batchCommitPeriod = batchCommitPeriod

    if not modeFlags is None:
        ret.modeFlags = modeFlags

    if not notifyCallback is None:
        ret.notifyCallback = notifyCallback

    if not iterator is None:
        ret.iterator = iterator

    if not cancelpointAddr is None:
        ret.cancelpointAddr = cancelpointAddr

    if not compressionLevel is None:
        ret.compressionLevel = compressionLevel

    return ret


def ReplicaConnection(*args):
    if not (_eXtremeHA and "ReplicaConnection" in dir(_eXtremeHA)):
        raise Exception ("HA not supported")

    return _eXtremeHA.ReplicaConnection(args)


def HACancel(cancelpoint_addr, timeout):
    return _eXtremeHA.HACancel(cancelpoint_addr, timeout)

###########################################################################################################
#    end of HA
###########################################################################################################


###########################################################################################################
#    IoT
###########################################################################################################


class IoT(object):
    ALL_AGENTS = 0
    MAX_AGENT_ID = 0xFFFFFFFFFFFFFFF0 #15 agent ID's reserved
    THIS_AGENT_ID = MAX_AGENT_ID + 1
    SERVER_AGENT_ID = MAX_AGENT_ID + 2
    INVALID_AGENT_ID = 0xFFFFFFFFFFFFFFFF

    SYNC_PUSH = 0x1      # Send data to other agent(s)
    SYNC_PULL = 0x2      # Request data from other agent(s)
    SYNC_NONBLOCK = 0x4  # Don't block on send() operation
    SYNC_WAIT = 0x8      # Wait for replication completion
    SYNC_BOTH = (SYNC_PUSH | SYNC_PULL)

    #Callback  return codes
    CALLBACK_OK =  0x0  # normal
    CALLBACK_FAIL  = 0x1  # error, disconnect the client
    CALLBACK_STOP  = 0x2  # error, don't call sebsequent callbacks in the chain


###########################################################################################################
#   end of IoT
###########################################################################################################


class Device(object):
    Data = 0
    DiskCache = 1
    TransactionLog = 2
    AsyncBuffer = 3
    PipeBuffer = 4

    def __init__(self, kind, flags=0):
        self.kind = kind
        self.flags = flags


class FileOpenFlags(object):
    Default = 0
    ReadOnly = 1
    Truncate = 2
    NoBuffering = 4
    OpenExisting = 8
    Temporary = 16
    FsyncFix = 32
    Subpartition = 64
    FsyncAIOBarrier = 128
    Compressed = 256
    OpenLock = 512
    NoReadBuffering = 1024


class privateMemoryDevice(Device):
    def __init__(self, kind, size):
        super(privateMemoryDevice, self).__init__(kind)
        self.size = int(size)


class sharedMemoryDevice(Device):
    def __init__(self, kind, name, size, hint = None):
        super(sharedMemoryDevice, self).__init__(kind)
        self.name = name
        self.size = int(size)
        self.hint = int(hint)


class fileDevice(Device):
    def __init__(self, kind, path, flags=FileOpenFlags.Default):
        super(fileDevice, self).__init__(kind, flags)
        self.path = path


class multiFileDevice(Device):
    def __init__(self, kind, path, size, flags=FileOpenFlags.Default):
        super(multiFileDevice, self).__init__(kind, flags)
        self.path = path
        self.size = int(size)


class raidDevice(Device):
    def __init__(self, kind, path, raidLevel, flags=FileOpenFlags.Default):
        super(raidDevice, self).__init__(kind, flags)
        self.path = path
        self.level = raidLevel


class NullableArray(object):
    def __init__(self, elemType, payload):
        self.elemType = elemType
        self.payload = payload

    def append(self, item):
        self.payload.append(item)


class Perfmon(object):

    TotalPages = 0
    FreePages = 1
    UsedPages = 2
    FileSize = 3
    LogFileSize = 4
    UsedFileSize = 5
    CacheHitCount = 6
    CacheMissCount = 7
    CachePagesAllocated = 8
    CachePagesUSed = 9
    CachePagesPinned = 10
    CachePagesModified = 11
    CachePagesDirty = 12
    CachePagesCopied = 13
    CachePagesWriteDelayed = 14

    DiskReadTime = 0
    DiskWriteTime = 1
    LogWriteTime = 2
    CommitTime = 3
    RollbackTime = 4
    SnapshotDuration = 5
    ClusterNetSendTime = 6
    ClusterNetRecvTime = 7

    @staticmethod
    def init(memsize=64 << 20):
        global _eXtremeDB
        return _eXtremeDB.perfmon_init(memsize)

    @staticmethod
    def close():
        global _eXtremeDB
        return _eXtremeDB.perfmon_close()

    @staticmethod
    def attach(db):
        global _eXtremeDB
        return _eXtremeDB.perfmon_attach(db)

    @staticmethod
    def detach(db):
        global _eXtremeDB
        return _eXtremeDB.perfmon_detach(db)

    @staticmethod
    def getDbName():
        global _eXtremeDB
        return _eXtremeDB.perfmon_get_db_name()

    @staticmethod
    def getOptions():
        global _eXtremeDB
        return _eXtremeDB.perfmon_get_options()

    @staticmethod
    def setOption(option, value):
        global _eXtremeDB
        return _eXtremeDB.perfmon_set_option(option, value)


class HV(object):
    """
    Wrapper over hv library - Hypeext Viewer. It has only 2 methods start() and stop()
    """
    def __init__(self):
        self.metadict = 0
        self.hv = 0

    def start(self, interfaces=None):
        """
        Start HV on specified interfaces.
        interfaces are optional and may be specified as [("1.1.1.1", 8080), ("2.3.4.5", 8081)]
        """
        global _eXtremeDB
        if interfaces:
            return _eXtremeDB.hv_start(self, interfaces)
        else:
            return _eXtremeDB.hv_start(self)

    def stop(self):
        global _eXtremeDB
        return _eXtremeDB.hv_stop(self)

