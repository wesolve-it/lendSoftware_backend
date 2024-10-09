import os
from django.http import FileResponse, Http404
from django.views.decorators.http import require_GET
from django.conf import settings

@require_GET
def serve_image(request, path):
    # Baue den vollständigen Pfad zur Bilddatei zusammen
    image_path = os.path.join(settings.MEDIA_ROOT, path)

    # Überprüfe, ob die Datei existiert
    if not os.path.exists(image_path):
        raise Http404("Bild nicht gefunden")

    # Bestimme den Content-Type basierend auf der Dateiendung
    if path.endswith('.png'):
        content_type = 'image/png'
    elif path.endswith('.jpg') or path.endswith('.jpeg'):
        content_type = 'image/jpeg'
    else:
        content_type = 'application/octet-stream' # Standard für unbekannte Typen

    #Erstelle die Antwort mit den CORS-Headern
    response = FileResponse(open(image_path, 'rb'), content_type=content_type)
    response['Access-Control-Allow-Origin'] = '*' # Erlaube alle Ursprünge
    response['Access-Control-Allow-Methods'] = '*' # Erlaube alle Methoden
    response['Access-Control-Allow-Headers'] = '*' # Erlaube alle Header

    return response
