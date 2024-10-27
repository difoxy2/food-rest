from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from . import serializers, permissions, models, serializers
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Sum
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.decorators import throttle_classes


# Create your views here.
@api_view(['POST','GET'])
@permission_classes([permissions.IsManager])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def manager_list(request):
    if(request.method=='GET'):
        managers = User.objects.all().filter(groups__name__in=['Manager'])
        serialized_managers = serializers.UserSerializer(managers,many=True)
        return Response( serialized_managers.data )
    elif(request.method=='POST'):
        try:
            username=request.data['username']
        except:
            return Response( {'message':'HTTP_400_BAD_REQUEST'}, status=status.HTTP_400_BAD_REQUEST)
        user=get_object_or_404(User,username=username)
        managers=Group.objects.get(name='Manager')
        managers.user_set.add(user)
        return Response( {'message':'created'}, status=status.HTTP_201_CREATED )
            


@api_view(["DELETE"])
@permission_classes([permissions.IsManager])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def manager_list_remove(request, pk):
    username=request.data['username']
    if(username):
        user=get_object_or_404(User,pk=pk)
        if(user.groups.filter(name='Manager').exists()):
            managers=Group.objects.get(name='Manager')
            managers.user_set.remove(user)
            return Response( {'message':'removed'}, status.HTTP_200_OK )
        else:
            return Response( {'message':'this user is not Manager'}, status=status.HTTP_200_OK )
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST','GET'])
@permission_classes([permissions.IsManager])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def deliverycrew_list(request):
    if(request.method=='GET'):
        deliverycrews = User.objects.all().filter(groups__name__in=['Deliverycrew'])
        serialized_deliverycrews = serializers.UserSerializer(deliverycrews,many=True)
        return Response( serialized_deliverycrews.data )
    elif(request.method=='POST'):
        try:
            username=request.data['username']
        except:
            return Response( {'message':'HTTP_400_BAD_REQUEST'}, status=status.HTTP_400_BAD_REQUEST)
        user=get_object_or_404(User,username=username)
        deliverycrews=Group.objects.get(name='Deliverycrew')
        deliverycrews.user_set.add(user)
        return Response( {'message':'created'}, status=status.HTTP_201_CREATED )



@api_view(["DELETE"])
@permission_classes([permissions.IsManager])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def deliverycrew_list_remove(request, pk):
    username=request.data['username']
    if(username):
        user=get_object_or_404(User,pk=pk)
        if(user.groups.filter(name='Deliverycrew').exists()):
            deliverycrews=Group.objects.get(name='Deliverycrew')
            deliverycrews.user_set.remove(user)
            return Response( {'message':'removed'}, status.HTTP_200_OK )
        else:
            return Response( {'message':'this user is not Deliverycrew'}, status=status.HTTP_200_OK )
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

class Catagory(generics.ListCreateAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAdminUser]
    throttle_classes = [AnonRateThrottle,UserRateThrottle]


class MenuItem(generics.ListCreateAPIView):
    queryset = models.MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializer
    throttle_classes = [AnonRateThrottle,UserRateThrottle]

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [permissions.IsManager]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        items=models.MenuItem.objects.select_related('category').all()
        
        #seach menu item title
        search=self.request.query_params.get('search')
        if(search):
            items=items.filter(title__icontains=search)

        #filter by ?category=main ?max_price=6 ?min_price=4
        category_name=self.request.query_params.get('category')
        max_price=self.request.query_params.get('max_price')
        min_price=self.request.query_params.get('min_price')
        if(category_name):
            items=items.filter(category__title=category_name)
        if(max_price):
            items=items.filter(price__lte=max_price)
        if(min_price):
            items=items.filter(price__gte=min_price)

        #orderby ?orderby=
        orderby=self.request.query_params.get('orderby')
        if(orderby):
            items=items.order_by(orderby)

        #paginate ?perpage= & page=
        perpage=self.request.query_params.get('perpage',default=100)
        page=self.request.query_params.get('page',default=1)
        paginator=Paginator(items,per_page=perpage)
        try:
            items=paginator.page(number=page)
        except EmptyPage:
            items=[]

        return items
    

class SingleMenuItem(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializer
    throttle_classes = [AnonRateThrottle,UserRateThrottle]

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [permissions.IsManager]
        return [permission() for permission in permission_classes]
    


@api_view(['GET','POST','DELETE'])
@permission_classes([permissions.IsCustomer])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def cart(request):
    try:
        if(request.method=="POST"):
            checkrecord=models.Cart.objects.all().filter(menuitem=request.data['menuitem_id']).filter(user=request.user)
            if(checkrecord.exists()):
                new_quantity = checkrecord[0].quantity + int(request.data['quantity'])
                if(new_quantity<0):
                    return Response({'message':'new quantity < 0'},status=status.HTTP_400_BAD_REQUEST)
                new_totalprice = new_quantity * checkrecord[0].unit_price
                checkrecord.update(quantity = new_quantity)
                checkrecord.update(price = new_totalprice)
                checkrecord[0].save()
                return Response({'message':'quantity updated'}, status=status.HTTP_200_OK)      
            else:
                i=request.data.copy()
                i['user']=request.user.pk
                item = get_object_or_404(models.MenuItem,id=i['menuitem_id'])
                i['unit_price'] = item.price
                i['price'] = item.price * int(i['quantity'])
                serialized_items = serializers.CartSerializer(data=i)
                serialized_items.is_valid(raise_exception=True)
                serialized_items.save()
                return Response({'message': 'item added to cart'},status=status.HTTP_201_CREATED)
    except:
        return Response({'message':'bad request'},status=status.HTTP_400_BAD_REQUEST)

    if(request.method=="GET"):
        queryset=models.Cart.objects.all().filter(user=request.user.pk)
        serialized_items=serializers.CartSerializer(queryset,many=True)
        return Response(serialized_items.data)
    
    if(request.method=="DELETE"):
        queryset=models.Cart.objects.all().filter(user=request.user.pk)
        queryset.delete()
        return Response({'message':'this user"s cart is emptyed'})
    

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def Orders(request):
    if(request.method=="GET"):
        queryset=models.Order.objects.all()
        

        if(request.user.is_superuser or request.user.groups.filter(name='Manager').exists()):
            queryset = queryset
        elif((not request.user.groups.exists())):
            queryset = queryset.filter(user=request.user.id)
        elif(request.user.groups.filter(name='Deliverycrew').exists()):
            queryset = queryset.filter(delivery_crew=request.user.id)
        else:
            return Response({'message':'bad request'},status=status.HTTP_400_BAD_REQUEST)
        
        if(request.query_params.get('status')):
            queryset=queryset.filter(status=request.query_params.get('status'))

        serialized_queryset=serializers.OrderSerializer(queryset,many=True)
        return Response(serialized_queryset.data)
    
    if(request.method=="POST"):
        if(request.user.is_superuser or (not request.user.groups.exists())):
            cartitems=models.Cart.objects.select_related('user').filter(user=request.user)
            order={}
            order['user_id']=request.user.id
            order['total']=cartitems.aggregate(Sum('price'))['price__sum']
            serialized_order=serializers.OrderSerializer(data=order)
            serialized_order.is_valid(raise_exception=True)
            orderid=int(serialized_order.save().id)

            orderitems=cartitems.values()
            for i in orderitems:
                    i['order']=orderid
                    print(type(i))
                    print(i['menuitem_id'])

            serialized_orderitems = serializers.OrderItemSerializer(data=list(orderitems),many=True)
            serialized_orderitems.is_valid(raise_exception=True)
            serialized_orderitems.save()
            cartitems.delete()

            return Response( {'message':'Order record created and Cart emptied'},status=status.HTTP_201_CREATED )
        
        else:
            return Response( {'message':'Only Customer can POST this api end point'},status=status.HTTP_403_FORBIDDEN )





@api_view(['GET','PUT','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def SingleOrder(request, pk):
    order_query=get_object_or_404(models.Order,id=pk)

    if(request.method=='GET'):
        if(request.user.is_superuser or (not request.user.groups.exists())):
            if(order_query.user==request.user or request.user.is_superuser):
                order_items=models.OrderItems.objects.select_related('order').all().filter(order=pk)
                serialized_order_items=serializers.OrderItemSerializer(order_items,many=True)
                return Response( serialized_order_items.data )
            else:
                return Response( {'message':'This order not belong to this User'},status=status.HTTP_403_FORBIDDEN )
        else:
            return Response( {'message':'Only Customer can GET this api end point'},status=status.HTTP_403_FORBIDDEN )
        
    if(request.method=='DELETE'):
        if(request.user.is_superuser or request.user.groups.filter(name='Manager').exists()):
            order_query.delete()
            return Response( {'message':'Order Deleted'},status=status.HTTP_200_OK )
        else:
            return Response( {'message':'Only Manager can DELETE this api end point'},status=status.HTTP_403_FORBIDDEN )


    if(request.method=='PATCH'):
    
        if(request.user.is_superuser or request.user.groups.filter(name='Manager').exists()):
            if 'status' in request.POST:
                order_query.status=request.data['status']
            if 'delivery_crew' in request.POST:
                order_query.delivery_crew=get_object_or_404(User,username=request.data['delivery_crew'])
            order_query.save()
            return Response( {'message':'PATCHED by manager','order':serializers.OrderSerializer(order_query).data} ,status=status.HTTP_200_OK )
        elif(request.user.groups.filter(name='Deliverycrew').exists() and order_query.delivery_crew==request.user):
            if 'status' in request.POST:
                order_query.status=request.data['status']
            order_query.save()
            return Response( {'message':'PATCHED by deliverycrew','order':serializers.OrderSerializer(order_query).data} , status=status.HTTP_200_OK )
        else:
            return Response( {'message':'no patch'},status=status.HTTP_400_BAD_REQUEST )

        
    if(request.method=='PUT'):
        '''
        if(request.user.is_superuser or request.user.groups.filter(name='Manager').exists()):
            serialized_order=serializers.OrderPUTSerializer(order_query, data=request.data)
            serialized_order.is_valid(raise_exception=True)
            serialized_order.save()
            return Response( {'message':'Order PUT-ted','order':serializers.OrderSerializer(order_query).data},status=status.HTTP_200_OK )
        else:
        '''
        return Response( {'message':'The developer dont want to implement PUT, use PATCH instead'},status=status.HTTP_400_BAD_REQUEST )