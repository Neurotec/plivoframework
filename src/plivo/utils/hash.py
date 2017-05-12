
# conn : freeswitch
def insert(conn, ctx, key, value):
    """insert key value into freeswitch hash"""
    
    conn.api("hash insert/%s/%s/%s" % (key, ctx, value))

# conn : freeswitch
def select(conn, ctx, key, default=''):
    """select key from freeswitch hash"""
    
    res = conn.api("hash select/%s/%s/" % (key, ctx)).get_body()
    if res != 'None':
        return res
    conn.bgapi("hash delete/%s/%s/" % (key, ctx))
    return default
