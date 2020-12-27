from . import api
from flask import request, Response, jsonify
import requests, uuid, pika, json

def get_homeowner_service():
    return "http://192.168.0.115:8081/homeowner/v1/"

def get_house_service():
    return "http://192.168.0.115:8082/house/v1/"
   

def handle_post(url, request):
    try:
        response = requests.post(url, json=request.get_json(), headers=request.headers)
        return Response(response=response.text, status=response.status_code)
    except requests.exceptions.ConnectionError:
        return Response(response="Error: Service currently unavailable.", status=503)

def handle_put(url, request):
    try: 
        response = requests.put(url, json=request.get_json(), headers=request.headers)
        return Response(response=response.text, status=response.status_code)
    except requests.exceptions.ConnectionError:
        return Response(response="Error: Service currently unavailable.", status=503)


def handle_get(url, request):
    try:
        response = requests.get(url, headers=request.headers)
        if response.ok:
            return jsonify(response.json())
        return Response(response=response.text, status=response.status_code)
    except requests.exceptions.ConnectionError:
        return Response(response="Error: Service currently unavailable.", status=503)

def authenticate_homeowner(request):
    try:
        response = requests.get(get_homeowner_service() + "verifyHomeowner", headers=request.headers)
        if response.ok:
            return response.json()
        return None
    except requests.exceptions.ConnectionError:
        return None
   


#############################################################
@api.route("/", methods=["GET"])
def create_homeowner_account():
    return get_homeowner_service() + "SignUp"

@api.route("Homeowner")
def get_homeowner():
    homeownerData = authenticate_homeowner(request)
    if homeownerData:
        url = get_homeowner_service() + "Homeowner"
        return handle_get(url, request)
    return Response(response="Not Authorized", status=401)
#############################################################

@api.route("House", methods=["POST"])
def create_house():
    homeownerData = authenticate_homeowner(request)
    if homeownerData:
        try:
            houseData = request.get_json()
            houseData["homeownerId"] = homeownerData["homeownerId"]
            response = requests.post(url = get_house_service() + "House", json=request.get_json(), headers=request.headers)
            return Response(response=response.text, status=response.status_code)
        except requests.exceptions.ConnectionError:
            return Response(response="Error: Service currently unavailable.", status=503)
    return Response(response="Not Authenticated", status=401)
        
        
@api.route("Homeowner/House")
def get_houses():
    homeownerData = authenticate_homeowner(request)
    if homeownerData:
        url = get_house_service() + "Homeowner/" + str(homeownerData["homeownerId"]) + "/House"
        return handle_get(url, request)
    return Response(response="Not Authorized", status=401)



#############################################################
@api.route("House/<int:houseId>/Tenant")
def get_tenants_by_house_id(houseId):
    homeownerData = authenticate_homeowner(request)
    if homeownerData:
        url = get_house_service() + "House/" + str(houseId) + "/Tenant"
        return handle_get(url, request)
    return Response(response="Not Authorized", status=401)

@api.route("Tenant/<int:tenantId>/Approve", methods=["PUT"])
def update_tenant(tenantId):
    homeownerData = authenticate_homeowner(request)
    if homeownerData:
        url = get_house_service() + "Tenant/" + str(tenantId) + "/Approve"
        return handle_put(url, request)
    return Response(response="Not Authorized", status=401)

##########################################################
@api.route("Login", methods=["GET"])
def login_homeowner():
    url = get_homeowner_service() + "login"
    return handle_post(url, request)

####################################################

@api.route("Lease", methods=["POST"])
def upload_lease_agreement():
    homeownerData = authenticate_homeowner(request)
    if homeownerData:
        homeowner = handle_get(get_homeowner_service() + "Homeowner", request)
        leaseData = request.get_json()
        leaseData["homeowner"] = homeowner.json
        try:
            response = requests.post(get_house_service() + "Lease", json=leaseData, headers=request.headers)
            return Response(response=response.text, status=response.status_code)
        except requests.exceptions.ConnectionError:
            return Response(response="Error: Service currently unavailable.", status=503)
    return Response(response="Not Authorized", status=401)
    
###################################################


@api.route("House/<int:houseId>/Problem")
def get_problems(houseId):
    homeownerData = authenticate_homeowner(request)
    if homeownerData:
        url = get_house_service() + "House/" + str(houseId) + "/Problem"
        return handle_get(url, request)
    return Response(response="Not Authorized", status=401)

@api.route("Problem/<int:problemId>")
def get_problem(problemId):
    homeownerData = authenticate_homeowner(request)
    if homeownerData:
        url = get_house_service() + "Problem/" + str(problemId)
        return handle_get(url, request)
    return Response(response="Not Authorized", status=401)

@api.route("Problem/<int:problemId>/Status", methods=["PUT"])
def put_problem(problemId):
    homeownerData = authenticate_homeowner(request)
    if homeownerData:
        url = get_house_service() + "Problem/" + str(problemId) + "/Status"
        return handle_put(url, request)
    return Response(response="Not Authorized", status=401)