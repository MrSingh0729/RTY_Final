import pandas as pd

def get_top_n_counts(df, col, n=3):
    if col not in df.columns or df.empty:
        return pd.DataFrame(columns=[col, "Count"])
    counts = df[col].value_counts().head(n).reset_index()
    counts.columns = [col, "Count"]
    return counts

def map_api_to_db(api_record):
    """Map API record to database model fields"""
    return {
        'project': api_record.get('project'),
        'station': api_record.get('station'),
        'inPut': int(api_record.get('inPut', 0)),
        'pass_qty': int(api_record.get('pass', 0)),  # Map 'pass' from API to 'pass_qty' in DB
        'fail': int(api_record.get('fail', 0)),
        'notFail': int(api_record.get('notFail', 0)),
        'der': float(api_record.get('der', 0).replace('%', '')) if api_record.get('der') else 0,
        'ntf': float(api_record.get('ntf', 0).replace('%', '')) if api_record.get('ntf') else 0,
        'rty': float(api_record.get('rty', 0).replace('%', '')) if api_record.get('rty') else 0,
        'py': float(api_record.get('py', 0).replace('%', '')) if api_record.get('py') else 0
    }

def map_db_to_api(db_record):
    """Map database model to API record format"""
    return {
        'project': db_record.project,
        'station': db_record.station,
        'inPut': db_record.inPut,
        'pass': db_record.pass_qty,  # Map 'pass_qty' from DB to 'pass' in API
        'fail': db_record.fail,
        'notFail': db_record.notFail,
        'der': f"{db_record.der}%",
        'ntf': f"{db_record.ntf}%",
        'rty': f"{db_record.rty}%",
        'py': f"{db_record.py}%"
    }