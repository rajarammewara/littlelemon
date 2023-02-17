from .serializer import CategorySerializer, MovieSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Movie
from .data import data
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
from rest_framework import generics


from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view, throttle_classes
from rest_framework.throttling import AnonRateThrottle 
from .throttle import ThreeCallsPerMinute

# Create your views here.


# def index(request):
 
#     return render(request, "index.html")


# @api_view(["GET"])
# def category(request):
#     all_categories = Category.objects.all()
#     serializer = CategorySerializer(all_categories, many=True)
#     return Response(serializer.data, 200)


class CategoryList(APIView):


    def get(self, request):

# create and update =======================================================

        for x in data:
            categories = Category.objects.get(category_name= x['category'])
            print(x, categories)
            Movie.objects.update_or_create(title = x['title'], image = x['image'], description = x['description'], release = x['release'], rating = x['rating'], category = categories)


        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data, 200)

    def post(self, request):
        return Response({"request": "Value"}, 200)

class MovieList(APIView, IsAuthenticated):

    serializer_class = MovieSerializer


# search order pagination =====================================================================

    def get(self, request):
        all_movies = Movie.objects.all()
        
        search_query = request.query_params.get('search')  
        order_query = request.query_params.get('ordering')

        perpage = request.query_params.get('perpage')
        page = request.query_params.get('page')

        if search_query:
            all_movies = Movie.objects.filter(Q(title__icontains=search_query) | Q(release__icontains=search_query))
        
        if order_query:
            all_movies = Movie.objects.order_by(order_query)
        
        if perpage:
            paginator = Paginator(all_movies, per_page=perpage)
        
            try:
                all_movies = paginator.page(number=page)
            except EmptyPage:
                all_movies = []

        serializer = MovieSerializer(all_movies, many=True)
        return Response(serializer.data, 200)


# post ==============================================================================

    def post(self, request):
        if request.user.groups.filter(name='Manager').exists():
            serializer = MovieSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, 200)

        else:
            return Response({"message": "You are not authorized to view this"}, 403)

# put update ==================================================================================

class SingleMovieView(generics.RetrieveUpdateAPIView, IsAuthenticated):
    
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def put(self, request, pk):
        if request.user.groups.filter(name='Manager').exists() == False:
            return Response({"message": "You are not authorized to update."}, 403)

# token ======================================================================================

@api_view()
@permission_classes([IsAuthenticated])
def userauth(request):
    return Response({"message": "hii"})



# user roles ===================================================================================

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message": "Only manager should see this7"})
    else:
        return Response({"message": "You are not authorized to view this"}, 403)


# throttle =======================================================================

@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message": "Successful"})


# user throttle ===================================================================================

@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([ThreeCallsPerMinute])
def throttle_check_auth(request):
    return Response({"message": "Message for the logged in user"})
