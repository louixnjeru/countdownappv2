from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.template.context_processors import csrf 
from .common.apiAccess.apiAccess import API

interface = API()

def main(request):
    template = loader.get_template('index.html')
    context = {
        'locationAvailable': False,
        }
    context.update(csrf(request))
    
    return HttpResponse(template.render(context, request))

def search(request):
    query = request.GET.get('q', None)
    if not query: return redirect('main')
    
    matches, stops = interface.getStopNames(query)
    
    context = {
        'searchTerm': query,
        'matches': matches,
        'stopList': stops
        }
    template = loader.get_template('search.html')
    return HttpResponse(template.render(context, request))
    

def arrivals(request,id):
    arrivalsList = interface.getArrivalsForStop(id)
    return HttpResponse(arrivalsList)
    
def station(request,id):
    response = interface.getStopsById(id)
    if not response: return redirect('404')
    name, stops = response
    template = loader.get_template('station.html')
    context = {
        'name': name,
        'stops': stops,
        }
    context.update(csrf(request))
    return HttpResponse(template.render(context, request))

def stop(request,id):
    if request.method != "POST":
        return redirect('main')
                
    context = {
        'name': request.POST['name'],
        'stopLetter': request.POST['stopLetter'],
        'waypoint': request.POST['waypoint'],
        'arrivals': interface.getArrivalsForStop(id),
        }
    context.update(csrf(request))
    
    template = loader.get_template('stop.html')
    
    return HttpResponse(template.render(context, request))

def nearby(request):
    context = {
        'stops': interface.getNearestBusStops(request.POST['currLat'], request.POST['currLon'])
        }
    
    return JsonResponse(context)

def vehicle(request):
    context = {
        'stops': interface.getVehicleInfo(request.POST['vehicleId'], request.POST['destination']),
        }
    
    return JsonResponse(context)
        