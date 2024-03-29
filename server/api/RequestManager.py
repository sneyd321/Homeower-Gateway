import requests
from flask import Response, jsonify, redirect
from server import app, zk


class Zookeeper:

    def __init__(self):
        self._zookeeper = zk

    def get_service(self, service):
        if self._zookeeper.exists("/RoomR/Services/" + service):
            data, stat = self._zookeeper.get("/RoomR/Services/" + service)
            return data.decode("utf-8")
        return None


class RequestManager:

    def __init__(self, request, service):
        self.request = request
        self.service = service

    def get_public_ip(self):
        return "34.107.132.144"


    def post(self, resource):
        try:
            response = requests.post("http://" + self.service + "/" + resource, json=self.request.get_json(), headers=self.request.headers)
            return Response(response=response.text, status=response.status_code)
        except requests.exceptions.ConnectionError:
            return Response(response="Error: Page Failed to Load", status=503)

    def put(self, resource):
        try: 
            response = requests.put("http://" + self.service + "/" + resource, json=self.request.get_json(), headers=self.request.headers)
            return Response(response=response.text, status=response.status_code)
        except requests.exceptions.ConnectionError:
            return Response(response="Error: Page Failed to Load", status=503)


    def get(self, resource):
        try:
            response = requests.get("http://" + self.service + "/" + resource, headers=self.request.headers)
            if response.ok:
                return jsonify(response.json())
            return Response(response=response.text, status=response.status_code)
        except requests.exceptions.ConnectionError:
            return Response(response="Error: Page Failed to Load", status=503)


    
    def authenticate(self, **kwargs):
        headers = kwargs.get("headers", self.request.headers)
        try:
            response = requests.get("http://" + self.service + "/homeowner/v1/Verify", headers=headers)
            if response.ok:
                homeownerData = response.json()
                return homeownerData["homeownerId"]
            return None
        except requests.exceptions.ConnectionError:
            return None
   


    def get_html(self, resource):
        try:
            response = requests.get("http://" + self.service + resource, headers=self.request.headers)
            if response.ok:
                return response.text
            return Response(response=response.text, status=response.status_code)
        except requests.exceptions.ConnectionError:
            return Response(response="Error: Page Failed to Load", status=503)



    def post_html(self, resource, **kwargs):
        headers = kwargs.get("headers", self.request.headers)
        try:

            


            response = requests.post("http://" + self.service + resource, data=self.request.form, headers=headers)
            print("http://" + self.get_public_ip() + "/homeowner-gateway/v1/" + response.text)
            if response.status_code == 201:
                return redirect("http://" + self.get_public_ip() + "/homeowner-gateway/v1/" + response.text)
            return Response(response=response.text, status=response.status_code)
        except requests.exceptions.ConnectionError:
            
            return Response(response="Error: Page Failed to Load", status=503)


    def post_profile(self, homeownerId):
        if not self.request.files or "image" not in self.request.files:
            return Response(response="Error: Bad request data", status=400)

        image = self.request.files["image"] 
        files = {"image": (image.filename, image.read(), "image/jpg")}
        try:
            response = requests.post("http://" + self.service  + "/image/v1/Homeowner/" + str(homeownerId) + "/Profile", files=files)
            return Response(response=response.text, status=response.status_code)
        except requests.exceptions.ConnectionError:
            return Response(response="Error: Page Failed to Load", status=503)

    def post_lease(self, resource, **kwargs):
        headers = kwargs.get("headers", self.request.headers)
        try:
            response = requests.post("http://" + self.service + resource, data=self.request.form, headers=headers)
            if response.status_code == 201:
                return redirect("http://" + self.get_public_ip() + "/homeowner-gateway/v1/FormComplete")
            return Response(response=response.text, status=response.status_code)
        except requests.exceptions.ConnectionError:
            return Response(response="Error: Page Failed to Load", status=503)
