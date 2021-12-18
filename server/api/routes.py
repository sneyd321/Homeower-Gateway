from server.api.RequestManager import  Zookeeper, RequestManager
from . import api
from flask import request, Response, jsonify, redirect, abort
import requests, json, time
from server import app




zookeeper = Zookeeper()

#############################################################

@api.route("/")
def get_homeowner_account():
    service = zookeeper.get_service("homeowner-service")
    if not service:
        return Response(response="Error: Homeowner Service Not Available", status=503)
    manager = RequestManager(request, service)
    return manager.get_html("/homeowner/v1/")


@api.route("/", methods=["POST"])
def create_homeowner_account():
    service = zookeeper.get_service("homeowner-service")
    if not service:
        return Response(response="Error: Homeowner Service Not Available", status=503)
    manager = RequestManager(request, service)
    return manager.post_html("/homeowner/v1/")
   


@api.route("HomeownerLocation/<int:homeownerId>")
def get_homeowner_location_form(homeownerId):
    homeownerService = zookeeper.get_service("homeowner-service")
    if not homeownerService:
        return Response(response="Error: Homeowner Service Not Available", status=503)

    homeownerManager = RequestManager(request, homeownerService)
    return homeownerManager.get_html("/homeowner/v1/HomeownerLocation/" + str(homeownerId))



@api.route("HomeownerLocation/<int:homeownerId>", methods=["POST"])
def create_homeowner_location(homeownerId):
    homeownerService = zookeeper.get_service("homeowner-service")
    if not homeownerService:
        return Response(response="Error: House Service Not Available", status=503)

    homeownerManager = RequestManager(request, homeownerService)
    return homeownerManager.post_html("/homeowner/v1/HomeownerLocation/" + str(homeownerId))
   

@api.route("HomeownerComplete/<int:homeownerId>", methods=["POST", "GET"])
def homeowner_complete(homeownerId):
    homeownerService = zookeeper.get_service("homeowner-service")
    if not homeownerService:
        return Response(response="Error: House Service Currently Unavailable", status=503)
    homeownerManager = RequestManager(request, homeownerService)
    return homeownerManager.post_html("/homeowner/v1/HomeownerComplete/" + str(homeownerId))



    


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
    if not service:
        return Response(response="Error: Service Currently Unavailable", status=503)
    manager = RequestManager(request, service)
    return manager.post("homeowner/v1/Login")
   
   








#############################################################

@api.route("House")
def get_arrangement_form():
    homeownerService = zookeeper.get_service("homeowner-service")
    if not homeownerService:
        return Response(response="Error: Homeowner Not Available", status=503)

    homeownerManager = RequestManager(request, homeownerService)
    homeownerId = homeownerManager.authenticate()
    if not homeownerId:
        return Response(response="Not Authorized", status=401)

    houseService = zookeeper.get_service("house-service")
    if not houseService:
        return Response(response="Error: House Service Currently Unavailable", status=503)
        
    houseManager = RequestManager(request, houseService)
    return houseManager.get_html("/house/v1/House/" + str(homeownerId))
    
    
    

  


@api.route("House/<int:homeownerId>", methods=["POST"])
def create_arrangement(homeownerId):
    homeownerService = zookeeper.get_service("homeowner-service")
    if not homeownerService:
        return Response(response="Error: Homeowner Not Available", status=503)
  

    houseService = zookeeper.get_service("house-service")
    if not houseService:
        return Response(response="Error: House Service Currently Unavailable", status=503)

    houseManager = RequestManager(request, houseService)
    return houseManager.post_html("/house/v1/House/" + str(homeownerId))

    
    
    
    
    



@api.route("RentalUnitLocation/<string:province>/<string:rentalType>/<int:houseId>")
def get_rental_unit_location_form(province, rentalType, houseId):
    houseService = zookeeper.get_service("house-service")
    if not houseService:
        return Response(response="Error: House Not Available", status=503)

    houseManager = RequestManager(request, houseService)
    return houseManager.get_html("/house/v1/RentalUnitLocation/" + province + "/" + rentalType + "/" + str(houseId))
   

   

@api.route("RentalUnitLocation/<string:province>/<string:rentalType>/<int:houseId>", methods=["POST"])
def create_rental_unit_location(province, rentalType, houseId):
    houseService = zookeeper.get_service("house-service")
    if not houseService:
        return Response(response="Error: House Not Available", status=503)

    houseManager = RequestManager(request, houseService)
    return houseManager.post_html("/house/v1/RentalUnitLocation/" + province + "/" + rentalType + "/" + str(houseId))
   


@api.route("HouseComplete/<int:houseId>", methods=["POST", "GET"])
def house_complete(houseId):
    houseService = zookeeper.get_service("house-service")
    if not houseService:
        return Response(response="Error: House Service Currently Unavailable", status=503)
    houseManager = RequestManager(request, houseService)
    return houseManager.post_html("/house/v1/HouseComplete/" + str(houseId))

   
    
@api.route("FormComplete")
def form_complete():
    return Response(status=204)








@api.route("RentDetails/<string:province>/<int:houseId>")
def view_rent_details(province, houseId):
    leaseService = zookeeper.get_service("lease-service")
    if not leaseService:
        return Response(response="Error: Lease Service Currently Unavailable", status=503)
        
    imageUploadService = zookeeper.get_service("image-upload-service")
    if not imageUploadService:
        return Response(response="Error: Upload Service Currently Unavailable", status=503)

    leaseManager = RequestManager(request, leaseService)
    return leaseManager.get_html("/lease/v1/RentDetails/" + province + "/" + str(houseId))
    
       


@api.route("RentDetails/<string:province>/<int:houseId>", methods=["POST"])
def create_rent_details(province, houseId):
    leaseService = zookeeper.get_service("lease-service")
    if not leaseService:
        return Response(response="Error: Lease Service Currently Unavailable", status=503)
    leaseManager = RequestManager(request, leaseService)
    return leaseManager.post_html("/lease/v1/RentDetails/" + province + "/" + str(houseId))


    
    

@api.route("Amenities/<string:province>/<int:houseId>")
def view_amenities(province, houseId):
    leaseService = zookeeper.get_service("lease-service")
    if not leaseService:
        return Response(response="Error: Lease Service Currently Unavailable", status=503)
    leaseManager = RequestManager(request, leaseService)
    return leaseManager.get_html("/lease/v1/Amenities/" + province + "/" + str(houseId))
    
   

@api.route("Amenities/<string:province>/<int:houseId>", methods=["POST"])
def create_amenities(province, houseId):
    leaseService = zookeeper.get_service("lease-service")
    if not leaseService:
        return Response(response="Error: Lease Service Currently Unavailable", status=503)
    leaseManager = RequestManager(request, leaseService)
    return leaseManager.post_html("/lease/v1/Amenities/" + province + "/" + str(houseId))
    
    


@api.route("Utilities/<string:province>/<int:houseId>")
def view_utilites(province, houseId):
    leaseService = zookeeper.get_service("lease-service")
    if not leaseService:
        return Response(response="Error: Lease Service Currently Unavailable", status=503)
    leaseManager = RequestManager(request, leaseService)
    return leaseManager.get_html("/lease/v1/Utilities/" + province + "/" + str(houseId))
   

    
@api.route("Utilities/<string:province>/<int:houseId>", methods=["POST"])
def create_utilites(province, houseId):
    leaseService = zookeeper.get_service("lease-service")
    if not leaseService:
        return Response(response="Error: Lease Service Currently Unavailable", status=503)
    leaseManager = RequestManager(request, leaseService)
    return leaseManager.post_html("/lease/v1/Utilities/" + province + "/" + str(houseId))
    


@api.route("LeaseComplete/<string:province>/<int:houseId>")
def lease_complete(province, houseId):
    leaseService = zookeeper.get_service("lease-service")
    if not leaseService:
        return Response(response="Error: Lease Service Currently Unavailable", status=503)
    leaseManager = RequestManager(request, leaseService)
    return leaseManager.post_lease("/lease/v1/LeaseComplete/" + province + "/" + str(houseId))


@api.route("Homeowner/Profile", methods=["POST"])
def homeownerProfile():
    homeownerService = zookeeper.get_service("homeowner-service")
    if not homeownerService:
        return Response(response="Error: Homeowner Service Not Available", status=503)

    homeownerManager = RequestManager(request, homeownerService)
    homeownerId = homeownerManager.authenticate()
    if not homeownerId:
        return Response(response="Not Authorized", status=401)

    imageUploadService = zookeeper.get_service("image-upload-service")
    if not imageUploadService:
        time.sleep(3.5) #Resolves broken pipe error on android. Fix is to convert to base64 image.
        return Response(response="Error: Image Upload Service Not Available", status=503)

    imageUploadManager = RequestManager(request, imageUploadService)
    return imageUploadManager.post_profile(homeownerId)
   
    

@api.route("Image/Task/<string:taskid>", methods=["POST"])
def pollTaskId(taskId):
    imageUploadService = zookeeper.get_service("image-upload-service")
    if not imageUploadService:
        return Response(response="Error: Image Upload Service Not Available", status=503)

    imageUploadManager = RequestManager(request, imageUploadService)
    return imageUploadManager.get("image/v1/Task/" + taskId)




@api.route("Homeowner/House")
def get_houses():
    homeownerService = zookeeper.get_service("homeowner-service")
    if not homeownerService:
        return Response(response="Error: Homeowner Service Not Available", status=503)

    homeownerManager = RequestManager(request, homeownerService)
    homeownerId = homeownerManager.authenticate()
    if not homeownerId:
        return Response(response="Not Authorized", status=401)
    
    houseService = zookeeper.get_service("house-service")
    if not houseService:
        return Response(response="Error: House Service Currently Not Available", status=503)

    houseManager = RequestManager(request, houseService)
    return houseManager.get("house/v1/Homeowner/" + str(homeownerId) + "/House")

    

#############################################################


@api.route("House/<int:houseId>/Tenant")
def get_tenants_by_house_id(houseId):
    homeownerService = zookeeper.get_service("homeowner-service")
    if not homeownerService:
        return Response(response="Error: Homeowner Service Not Available", status=503)

    homeownerManager = RequestManager(request, homeownerService)
    homeownerId = homeownerManager.authenticate()
    if not homeownerId:
        return Response(response="Not Authorized", status=401)

    tenantService = zookeeper.get_service("tenant-service")
    if not tenantService:
        return Response(response="Error: Tenant Service Not Available", status=503)

    tenantManager = RequestManager(request, tenantService)
    return tenantManager.get("tenant/v1/House/" + str(houseId) + "/Tenant")



@api.route("Tenant/<int:tenantId>/Approve", methods=["PUT"])
def update_tenant(tenantId):
    homeownerService = zookeeper.get_service("homeowner-service")
    if not homeownerService:
        return Response(response="Error: Homeowner Not Available", status=503)
    homeownerManager = RequestManager(request, homeownerService)
    homeownerId = homeownerManager.authenticate()
    if not homeownerId:
        return Response(response="Not Authorized", status=401)

    tenantService = zookeeper.get_service("tenant-service")
    if not tenantService:
        return Response(response="Error: Tenant Not Available", status=503)

    tenantManager = RequestManager(request, tenantService)
    return tenantManager.put("tenant/v1/Tenant/" + str(tenantId) + "/Approve")
    
   

  

###################################################


@api.route("House/<int:houseId>/Problem")
def get_problems(houseId):
    homeownerService = zookeeper.get_service("homeowner-service")
    if not homeownerService:
        return Response(response="Error: Homeowner Not Available", status=503)
    homeownerManager = RequestManager(request, homeownerService)
    homeownerId = homeownerManager.authenticate()
    if not homeownerId:
        return Response(response="Not Authorized", status=401)

    problemService = zookeeper.get_service("problem-service")
    if not problemService:
        return Response(response="Error: problem service Not Available", status=503)

    problemManager = RequestManager(request, problemService)
    return problemManager.get("problem/v1/House/" + str(houseId) + "/Problem")
    

    
  

@api.route("Problem/<int:problemId>")
def get_problem(problemId):
    homeownerService = zookeeper.get_service("homeowner-service")
    if not homeownerService:
        return Response(response="Error: Homeowner Not Available", status=503)
  
    homeownerManager = RequestManager(request, homeownerService)
    homeownerId = homeownerManager.authenticate()
    if not homeownerId:
        return Response(response="Not Authorized", status=401)

    tenantService = zookeeper.get_service("problem-service")
    if not tenantService:
        return Response(response="Error: Tenant Not Available", status=503)

    tenantManager = RequestManager(request, tenantService)
    return tenantManager.get("problem/v1/Problem/" + str(problemId))

    
    


@api.route("Problem/<int:problemId>/Status", methods=["PUT"])
def put_problem(problemId):
    homeownerService = zookeeper.get_service("homeowner-service")
    if not homeownerService:
        return Response(response="Error: Homeowner Not Available", status=503)
    homeownerManager = RequestManager(request, homeownerService)

    homeownerId = homeownerManager.authenticate()
    if not homeownerId:
        return Response(response="Not Authorized", status=401)

    tenantService = zookeeper.get_service("problem-service")
    if not tenantService:
        return Response(response="Error: Tenant Not Available", status=503)

    tenantManager = RequestManager(request, tenantService)
    return tenantManager.put("problem/v1/Problem/" + str(problemId) + "/Status")

    
   

@api.route("/Document/<int:houseId>")
def get_homeowner_documents(houseId):
    homeownerService = zookeeper.get_service("homeowner-service")
    if not homeownerService:
        return Response(response="Error: Document Service Not Available", status=503)

    homeownerManager = RequestManager(request, homeownerService)
    homeownerId = homeownerManager.authenticate()
    if not homeownerId:
        return Response(response="Not Authorized", status=401)
    
    documentService = zookeeper.get_service("document-service")
    if not documentService:
        return Response(response="Error: Documents Not Available", status=503)
   
    documentManager = RequestManager(request, documentService)
    return documentManager.get("document/v1/Document/" + str(houseId))
