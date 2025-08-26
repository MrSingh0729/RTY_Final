import requests
from datetime import datetime, timedelta
from config import Config

def get_token():
    payload = {"userCode": Config.USER_CODE, "password": Config.PASSWORD, "langCode": Config.LANG_CODE}
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    resp = requests.post(Config.LOGIN_URL, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return data["data"]

def get_project_list(token):
    today = datetime.now().strftime("%Y-%m-%d")
    headers = {"token": token, "lang-code": Config.LANG_CODE}
    params = {"stationType": "BE", "startDate": today, "endDate": today}
    resp = requests.get(Config.PROJECT_LIST_URL, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()["data"]

def get_fpy(token, projects):
    now = datetime.now()
    start = now.replace(hour=8, minute=0, second=0, microsecond=0)
    payload = {
        "startDate": start.strftime("%Y-%m-%d %H:%M:%S"),
        "endDate": now.strftime("%Y-%m-%d %H:%M:%S"),
        "projects": projects,
        "station": ["PCURR", "AUD", "ANTWBG", "RQC", "RQC2", "MMI", "MMI2_All"],
        "stationType": "BE",
        "current": 1,
        "size": 100
    }
    headers = {"Content-Type": "application/json", "token": token, "lang-code": Config.LANG_CODE}
    resp = requests.post(Config.FPY_URL, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()["data"]["records"]

def get_station_ntf_details(token, project, station):
    now = datetime.now()
    start = now.replace(hour=8, minute=0, second=0, microsecond=0)
    params = {
        "startDate": start.strftime("%Y-%m-%d %H:%M:%S"),
        "endDate": now.strftime("%Y-%m-%d %H:%M:%S"),
        "project": project,
        "stationName": station,
        "stationType": "BE",
        "workOrder": "",
        "lineName": "",
        "current": 1,
        "size": 1000
    }
    headers = {"token": token, "lang-code": Config.LANG_CODE}
    resp = requests.get(Config.NTF_DETAIL_URL, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()["data"]["records"]

def get_station_der_details(token, project, station):
    end_time = datetime.now()
    start_time = end_time - timedelta(days=1)
    params = {
        "startDate": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "endDate": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "project": project,
        "stationName": station,
        "stationType": "BE",
        "workOrder": "",
        "lineName": "",
        "current": 1,
        "size": 1000
    }
    headers = {"token": token, "lang-code": Config.LANG_CODE, "Accept": "application/json"}
    resp = requests.get(Config.DER_DETAIL_URL, params=params, headers=headers)
    resp.raise_for_status()
    return resp.json()["data"]["records"]



def get_fpy_by_model(token, model_name, station_type, start_date, end_date):
    payload = {
        "startDate": start_date,
        "endDate": end_date,
        "projects": [model_name],
        "station": ["PCURR", "AUD", "ANTWBG", "RQC", "RQC2", "MMI", "MMI2_All"],
        "stationType": station_type,
        "current": 1,
        "size": 100
    }
    headers = {"Content-Type": "application/json", "token": token, "lang-code": Config.LANG_CODE}
    resp = requests.post(Config.FPY_URL, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()["data"]["records"]

def get_station_ntf_details_by_model(token, model_name, station, station_type, start_date, end_date):
    params = {
        "startDate": start_date,
        "endDate": end_date,
        "project": model_name,
        "stationName": station,
        "stationType": station_type,
        "workOrder": "",
        "lineName": "",
        "current": 1,
        "size": 1000
    }
    headers = {"token": token, "lang-code": Config.LANG_CODE}
    resp = requests.get(Config.NTF_DETAIL_URL, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()["data"]["records"]

def get_station_der_details_by_model(token, model_name, station, station_type, start_date, end_date):
    params = {
        "startDate": start_date,
        "endDate": end_date,
        "project": model_name,
        "stationName": station,
        "stationType": station_type,
        "workOrder": "",
        "lineName": "",
        "current": 1,
        "size": 1000
    }
    headers = {"token": token, "lang-code": Config.LANG_CODE, "Accept": "application/json"}
    resp = requests.get(Config.DER_DETAIL_URL, params=params, headers=headers)
    resp.raise_for_status()
    return resp.json()["data"]["records"]


# utils/api.py

def get_fpy(token, projects, start_date=None, end_date=None):
    if start_date is None or end_date is None:
        # Default behavior (current day from 8AM to now)
        now = datetime.now()
        start = now.replace(hour=8, minute=0, second=0, microsecond=0)
        end = now
    else:
        # Use provided date range
        start = start_date
        end = end_date
        
    payload = {
        "startDate": start.strftime("%Y-%m-%d %H:%M:%S"),
        "endDate": end.strftime("%Y-%m-%d %H:%M:%S"),
        "projects": projects,
        "station": ["PCURR", "AUD", "ANTWBG", "RQC", "RQC2", "MMI", "MMI2_All"],
        "stationType": "BE",
        "current": 1,
        "size": 100
    }
    headers = {"Content-Type": "application/json", "token": token, "lang-code": Config.LANG_CODE}
    resp = requests.post(Config.FPY_URL, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()["data"]["records"]