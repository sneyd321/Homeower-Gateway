from server.api.RequestManager import HomeownerManager, HouseGatewayManager, Zookeeper, RequestManager
from . import api
from flask import request, Response, jsonify, redirect
import requests, json




zookeeper = Zookeeper()

#############################################################

@api.route("/")
def get_homeowner_account():
    service = zookeeper.get_service("homeowner-service")
    if service:
        manager = RequestManager(request, service)
        return manager.get_html("/homeowner/v1/")
    return Response(response="Error: Zookeeper down", status=503)


@api.route("/", methods=["POST"])
def create_homeowner_account():
    service = zookeeper.get_service("homeowner-service")
    if service:
        manager = RequestManager(request, service)
        return manager.post_html("/homeowner/v1/")
    return Response(response="Error: Zookeeper down", status=503)
    


@api.route("Homeowner")
def get_homeowner():
    service = zookeeper.get_service("homeowner-service")
    if service:
        manager = RequestManager(request, service)
        homeownerId = manager.authenticate()
        if homeownerId:
            return manager.get("homeowner/v1/Homeowner")
        return Response(response="Not Authorized", status=401)
    return Response(response="Error: Zookeeper down", status=503)
    

@api.route("Login", methods=["GET"])
def login_homeowner():
    service = zookeeper.get_service("homeowner-service")
    if service:
        manager = RequestManager(request, service)
        return manager.post("homeowner/v1/login")
    return Response(response="Error: Zookeeper down", status=503)
   


#############################################################

@api.route("House")
def get_arrangement_form():
    homeownerService = zookeeper.get_service("homeowner-service")
    if homeownerService:
        homeownerManager = RequestManager(request, homeownerService)
        homeownerId = homeownerManager.authenticate()
        if homeownerId:
            houseService = zookeeper.get_service("house-service")
            if houseService:
                houseManager = RequestManager(request, houseService)
                return houseManager.get_html("/house/v1/House/" + str(homeownerId))
            return Response(response="Error: House Service Currently Unavailable", status=503)
        return Response(response="Not Authorized", status=401)
    return Response(response="Error: Homeowner Not Available", status=503)

  


@api.route("House", methods=["POST"])
def create_arrangement():
    homeownerService = zookeeper.get_service("homeowner-service")
    if homeownerService:
        headers = {"Authorization": "Bearer " + request.form.get("token") }
        homeownerManager = RequestManager(request, homeownerService)
        homeownerId = homeownerManager.authenticate(headers=headers)
        if homeownerId:
            houseService = zookeeper.get_service("house-service")
            if houseService:
                houseManager = RequestManager(request, houseService)
                return houseManager.post_html("/house/v1/House/" + str(homeownerId), headers=headers)
            return Response(response="Error: House Service Currently Unavailable", status=503)
        return Response(response="Not Authorized", status=401)
    return Response(response="Error: Homeowner Not Available", status=503)
    
    
    
    


@api.route("HomeownerLocation/<string:province>/<string:arrangement>/<int:homeownerId>/<int:houseId>")
def get_homeowner_location_form(province, arrangement, homeownerId, houseId):
    houseService = zookeeper.get_service("house-service")
    if houseService:
        houseManager = RequestManager(request, houseService)
        return houseManager.get_html("/house/v1/HomeownerLocation/" + province + "/" + arrangement + "/" + str(homeownerId) + "/" + str(houseId))
    return Response(response="Error: House Not Available", status=503)
   


@api.route("HomeownerLocation/<string:province>/<string:arrangement>/<int:homeownerId>/<int:houseId>", methods=["POST"])
def create_homeowner_location(province, arrangement, homeownerId, houseId):
    houseService = zookeeper.get_service("house-service")
    if houseService:
        houseManager = RequestManager(request, houseService)
        return houseManager.post_html("/house/v1/HomeownerLocation/" + province + "/" + arrangement + "/" + str(homeownerId) + "/" + str(houseId))
    return Response(response="Error: House Not Available", status=503)


@api.route("RentalUnitLocation/<string:province>/<int:houseId>")
def get_rental_unit_location_form(province,  houseId):
    houseService = zookeeper.get_service("house-service")
    if houseService:
        houseManager = RequestManager(request, houseService)
        return houseManager.get_html("/house/v1/RentalUnitLocation/" + province + "/" + str(houseId))
    return Response(response="Error: House Not Available", status=503)

   

@api.route("RentalUnitLocation/<string:province>/<int:houseId>", methods=["POST"])
def create_rental_unit_location(province, houseId):
    houseService = zookeeper.get_service("house-service")
    if houseService:
        houseManager = RequestManager(request, houseService)
        return houseManager.post_html("/house/v1/RentalUnitLocation/" + province + "/" + str(houseId))
    return Response(response="Error: House Not Available", status=503)
   


@api.route("HouseComplete/<int:houseId>", methods=["POST", "GET"])
def house_complete(houseId):
    houseService = zookeeper.get_service("house-service")
    if houseService:
        houseManager = RequestManager(request, houseService)
        return houseManager.post_html("/house/v1/HouseComplete/" + str(houseId))
    return Response(response="Error: House Service Currently Unavailable", status=503)

   
    
@api.route("FormComplete")
def form_complete():
    return Response(status=204)








@api.route("RentDetails/<string:province>/<int:houseId>")
def view_rent_details(province, houseId):
    homeownerService = zookeeper.get_service("homeowner-service")
    if homeownerService:
        homeownerManager = RequestManager(request, homeownerService)
        homeownerId = homeownerManager.authenticate()
        if homeownerId:
            leaseService = zookeeper.get_service("lease-service")
            if leaseService:
                leaseManager = RequestManager(request, leaseService)
                return leaseManager.get_html("/lease/v1/RentDetails/" + province + "/" + str(houseId))
            return Response(response="Error: House Service Currently Unavailable", status=503)
        return Response(response="Not Authorized", status=401)
    return Response(response="Error: Lease Not Available", status=503)


@api.route("RentDetails/<string:province>/<int:houseId>", methods=["POST"])
def create_rent_details(province, houseId):
    homeownerService = zookeeper.get_service("homeowner-service")
    if homeownerService:
        headers = {"Authorization": "Bearer " + request.form.get("token") }
        homeownerManager = RequestManager(request, homeownerService)
        homeownerId = homeownerManager.authenticate(headers=headers)
        if homeownerId:
            leaseService = zookeeper.get_service("lease-service")
            if leaseService:
                leaseManager = RequestManager(request, leaseService)
                return leaseManager.post_html("/lease/v1/RentDetails/" + province + "/" + str(houseId), headers=headers)
            return Response(response="Error: House Service Currently Unavailable", status=503)
        return Response(response="Not Authorized", status=401)
    return Response(response="Error: Lease Not Available", status=503)

    

@api.route("Amenities/<string:province>/<int:houseId>")
def view_amenities(province, houseId):
    leaseService = zookeeper.get_service("lease-service")
    if leaseService:
        leaseManager = RequestManager(request, leaseService)
        return leaseManager.get_html("/lease/v1/Amenities/" + province + "/" + str(houseId))
    return Response(response="Error: Lease Not Available", status=503)
    
   

@api.route("Amenities/<string:province>/<int:houseId>", methods=["POST"])
def create_amenities(province, houseId):
    leaseService = zookeeper.get_service("lease-service")
    if leaseService:
        leaseManager = RequestManager(request, leaseService)
        return leaseManager.post_html("/lease/v1/Amenities/" + province + "/" + str(houseId))
    return Response(response="Error: Lease Not Available", status=503)
    


@api.route("Utilities/<string:province>/<int:houseId>")
def view_utilites(province, houseId):
    leaseService = zookeeper.get_service("lease-service")
    if leaseService:
        leaseManager = RequestManager(request, leaseService)
        return leaseManager.get_html("/lease/v1/Utilities/" + province + "/" + str(houseId))
    return Response(response="Error: Lease Not Available", status=503)

   

    
@api.route("Utilities/<string:province>/<int:houseId>", methods=["POST"])
def create_utilites(province, houseId):
    leaseService = zookeeper.get_service("lease-service")
    if leaseService:
        leaseManager = RequestManager(request, leaseService)
        return leaseManager.post_html("/lease/v1/Utilities/" + province + "/" + str(houseId))
    return Response(response="Error: Lease Not Available", status=503)
    


@api.route("LeaseComplete/<string:province>/<int:houseId>")
def lease_complete(province, houseId):
    leaseService = zookeeper.get_service("lease-service")
    if leaseService:
        leaseManager = RequestManager(request, leaseService)
        return leaseManager.post_html("/lease/v1/LeaseComplete/" + province + "/" + str(houseId))
    return Response(response="Error: Lease Not Available", status=503)






















@api.route("Homeowner/House")
def get_houses():
    homeownerService = zookeeper.get_service("homeowner-service")
    if homeownerService:
        homeownerManager = RequestManager(request, homeownerService)
        homeownerId = homeownerManager.authenticate()
        if homeownerId:
            tenantService = zookeeper.get_service("house-service")
            if tenantService:
                tenantManager = RequestManager(request, tenantService)
                return tenantManager.get("house/v1/Homeowner/" + str(homeownerId) + "/House")
            return Response(response="Error: Tenant Not Available", status=503)
        return Response(response="Not Authorized", status=401)
    return Response(response="Error: Homeowner Not Available", status=503)


#############################################################


@api.route("House/<int:houseId>/Tenant")
def get_tenants_by_house_id(houseId):
    homeownerService = zookeeper.get_service("homeowner-service")
    if homeownerService:
        homeownerManager = RequestManager(request, homeownerService)
        homeownerId = homeownerManager.authenticate()
        if homeownerId:
            tenantService = zookeeper.get_service("tenant-service")
            if tenantService:
                tenantManager = RequestManager(request, tenantService)
                return tenantManager.get("tenant/v1/House/" + str(houseId) + "/Tenant")
            return Response(response="Error: Tenant Not Available", status=503)
        return Response(response="Not Authorized", status=401)
    return Response(response="Error: Homeowner Not Available", status=503)


@api.route("Tenant/<int:tenantId>/Approve", methods=["PUT"])
def update_tenant(tenantId):
    homeownerService = zookeeper.get_service("homeowner-service")
    if homeownerService:
        homeownerManager = RequestManager(request, homeownerService)
        homeownerId = homeownerManager.authenticate()
        if homeownerId:
            tenantService = zookeeper.get_service("tenant-service")
            if tenantService:
                tenantManager = RequestManager(request, tenantService)
                return tenantManager.put("tenant/v1/Tenant/" + str(tenantId) + "/Approve")
            return Response(response="Error: Tenant Not Available", status=503)
        return Response(response="Not Authorized", status=401)
    return Response(response="Error: Homeowner Not Available", status=503)
  

###################################################


@api.route("House/<int:houseId>/Problem")
def get_problems(houseId):
    homeownerService = zookeeper.get_service("homeowner-service")
    if homeownerService:
        homeownerManager = RequestManager(request, homeownerService)
        homeownerId = homeownerManager.authenticate()
        if homeownerId:
            problemService = zookeeper.get_service("problem-service")
            if problemService:
                problemManager = RequestManager(request, problemService)
                return problemManager.get("problem/v1/House/" + str(houseId) + "/Problem")
            return Response(response="Error: problem service Not Available", status=503)
        return Response(response="Not Authorized", status=401)
    return Response(response="Error: Homeowner Not Available", status=503)
  

@api.route("Problem/<int:problemId>")
def get_problem(problemId):
    homeownerService = zookeeper.get_service("homeowner-service")
    if homeownerService:
        homeownerManager = RequestManager(request, homeownerService)
        homeownerId = homeownerManager.authenticate()
        if homeownerId:
            tenantService = zookeeper.get_service("problem-service")
            if tenantService:
                tenantManager = RequestManager(request, tenantService)
                return tenantManager.get("problem/v1/Problem/" + str(problemId))
            return Response(response="Error: Tenant Not Available", status=503)
        return Response(response="Not Authorized", status=401)
    return Response(response="Error: Homeowner Not Available", status=503)
  


@api.route("Problem/<int:problemId>/Status", methods=["PUT"])
def put_problem(problemId):
    homeownerService = zookeeper.get_service("homeowner-service")
    if homeownerService:
        homeownerManager = RequestManager(request, homeownerService)
        homeownerId = homeownerManager.authenticate()
        if homeownerId:
            tenantService = zookeeper.get_service("problem-service")
            if tenantService:
                tenantManager = RequestManager(request, tenantService)
                return tenantManager.put("problem/v1/Problem/" + str(problemId) + "/Status")
            return Response(response="Error: Tenant Not Available", status=503)
        return Response(response="Not Authorized", status=401)
    return Response(response="Error: Homeowner Not Available", status=503)

@api.route("/Document/<int:houseId>")
def get_homeowner_documents(houseId):
    homeownerService = zookeeper.get_service("homeowner-service")
    if homeownerService:
        homeownerManager = RequestManager(request, homeownerService)
        homeownerId = homeownerManager.authenticate()
        if homeownerId:
            documentService = zookeeper.get_service("document-service")
            if documentService:
                documentManager = RequestManager(request, documentService)
                return documentManager.get("document/v1/Document/" + str(houseId))
            return Response(response="Error: Documents Not Available", status=503)
        return Response(response="Not Authorized", status=401)
    return Response(response="Error: Homeowner Not Available", status=503)