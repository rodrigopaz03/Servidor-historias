import re
from django.http import JsonResponse

class SQLInjectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Lista de patrones de inyección SQL comunes
        sql_patterns = [
            r"'.*--",         # Comentarios SQL
            r"SELECT.*FROM",  # Comienzo de un SELECT
            r"UNION.*SELECT", # Unión de consultas
            r"OR 1=1",        # Inyecciones de verdadero
            r"DROP TABLE",    # Intento de eliminar tablas
            r"EXEC",          # Ejecución de comandos
            r"INSERT INTO",   # Intento de inserción
            r"UPDATE.*SET",   # Intento de actualización
        ]

        # Buscar en los parámetros de la URL
        for param in request.GET.values():
            if any(re.search(pattern, param, re.IGNORECASE) for pattern in sql_patterns):
                return JsonResponse({"error": "SQL Injection detected"}, status=400)

        # Buscar en los parámetros del cuerpo de la solicitud (si es POST o PUT)
        if request.method in ['POST', 'PUT']:
            for param in request.POST.values():
                if any(re.search(pattern, param, re.IGNORECASE) for pattern in sql_patterns):
                    return JsonResponse({"error": "SQL Injection detected"}, status=400)

        # Continuar con la solicitud si no hay coincidencias
        return self.get_response(request)
