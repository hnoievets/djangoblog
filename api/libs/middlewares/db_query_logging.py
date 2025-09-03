from django.db import connection

class DBQueryLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        total_queries = len(connection.queries)
        print(f"\n--- {total_queries} SQL queries during request ---")
        for q in connection.queries:
            print(q['sql'])
        print("--- end of SQL log ---\n")

        return response