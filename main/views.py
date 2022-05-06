from utils.render_vue_page import render_vue_page


def index_view(request):
    if request.method == 'GET':
        todos = [
            {
                "id": 1,
                "title": "hello"
            },
            {
                "id": 2,
                "title": "world"
            }
        ]
        return render_vue_page(request, 'index', {'todos': todos})