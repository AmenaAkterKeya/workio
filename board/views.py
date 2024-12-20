from rest_framework import viewsets,status,permissions,generics,filters
from .models import Board, List, Card,Member
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .serializers import BoardSerializer,BoarddSerializer, ListSerializer,CarddSerializer, CardSerializer, AddMemberSerializer,MemberDetailSerializer,MemberAllSerializer
from django.http import Http404
from rest_framework.exceptions import ValidationError
from collections import defaultdict
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
class BoardCreateView(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get the logged-in user's custom user instance
        user = self.request.user
        custom_user = user.customuser if hasattr(user, 'customuser') else None

        # Return only the boards owned by the logged-in user's CustomUser
        if custom_user:
            query_set = Board.objects.filter(owner=custom_user)
        else:
            query_set = Board.objects.none()  # Return an empty queryset if custom_user is None

        # Apply sorting if specified in the query params
        sort_order = self.request.query_params.get('sort', 'asc')
        if sort_order == 'asc':
            query_set = query_set.order_by('name')
        elif sort_order == 'desc':
            query_set = query_set.order_by('-name')

        return query_set

    def perform_create(self, serializer):
        # Check if the number of members exceeds 10
        members_num = serializer.validated_data.get('members_num', 0)
        if members_num  > 10:
            raise ValidationError('You cannot add more than 10 members to a board.')

        serializer.save(owner=self.request.user.customuser)
class BoarddViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoarddSerializer

    def perform_create(self, serializer):
        members_data = self.request.data.get('members', [])
        serializer_context = {
            'request': self.request,
            'members': members_data,
        }
        serializer = self.get_serializer(data=self.request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

class AddBoardMemberView(generics.GenericAPIView):
    serializer_class = AddMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return None 

    def post(self, request, pk):
        try:
            board = Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            raise ValidationError("Board does not exist.")

        if request.user.customuser != board.owner and not Member.objects.filter(board=board, member=request.user.customuser).exists():
            raise ValidationError("You do not have permission to add members to this board.")

        serializer = self.get_serializer(data=request.data, context={'board': board})
        serializer.is_valid(raise_exception=True)
        member = serializer.save()  

        user_email = member.member.user.email 

        email_subject = "You've been added to a Board!"
        email_body = render_to_string('invited_email.html', {'board_name': board.name})  

        email = EmailMultiAlternatives(email_subject, '', to=[user_email])
        email.attach_alternative(email_body, "text/html") 
        email.send()        
        return Response({"message": "Member added successfully!"})



class MemberDetailView(generics.GenericAPIView):
    serializer_class = MemberDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            member = Member.objects.get(pk=pk)
        except Member.DoesNotExist:
            raise NotFound("Member does not exist.")

      
        if request.user.customuser != member and not request.user.is_staff:
            raise permissions.PermissionDenied("You do not have permission to view this member.")

        serializer = self.get_serializer(member)
        return Response(serializer.data)
class ListCreateView(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['board__id']
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def create(self, request, *args, **kwargs):
        print("Request Data:", request.data)
        return super().create(request, *args, **kwargs)


class ListUpdateDeleteView(APIView):
    
    def get_object(self, board_id, list_id):
        try:
            board = Board.objects.get(id=board_id)
            list_item = List.objects.get(id=list_id, board=board)
            return board, list_item
        except Board.DoesNotExist:
            raise Response({'detail': 'Board not found.'}, status=status.HTTP_404_NOT_FOUND)
        except List.DoesNotExist:
            raise Response({'detail': 'List not found in this board.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, board_id, list_id):
        board, list_item = self.get_object(board_id, list_id)
        user = request.user

        # Check if the user is the owner of the board
        if not user.is_authenticated or board.owner != user.customuser:
            return Response({'detail': 'You are not authorized to modify this list.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ListSerializer(list_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, board_id, list_id):
        board, list_item = self.get_object(board_id, list_id)
        user = request.user

        # Check if the user is the owner of the board
        if not user.is_authenticated or board.owner != user.customuser:
            return Response({'detail': 'You are not authorized to delete this list.'}, status=status.HTTP_403_FORBIDDEN)

        list_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CardCreateView(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['list__id']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def create(self, request, *args, **kwargs):
        user = request.user
        custom_user = user.customuser
        list_id = request.data.get('list')
        
        if not list_id:
            raise ValidationError("List ID is required.")
        
        list_instance = List.objects.get(id=list_id)
        board = list_instance.board

        # Check if the user is the board owner or a member of the board
        if board.owner != custom_user:
            is_member = Member.objects.filter(board=board, member=custom_user).exists()
            if not is_member:
                raise ValidationError("You are not authorized to add a card to this board.")

        return super().create(request, *args, **kwargs)


class CardView(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CarddSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['list__id']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def create(self, request, *args, **kwargs):
        user = request.user
        custom_user = user.customuser
        list_id = request.data.get('list')
        
        if not list_id:
            raise ValidationError("List ID is required.")
        
        list_instance = List.objects.get(id=list_id)
        board = list_instance.board

        # Check if the user is the board owner or a member of the board
        if board.owner != custom_user:
            is_member = Member.objects.filter(board=board, member=custom_user).exists()
            if not is_member:
                raise ValidationError("You are not authorized to add a card to this board.")

        return super().create(request, *args, **kwargs)
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context  



class CardDetail(APIView):
    def get_object(self, pk):
        try:
            return Card.objects.get(pk=pk)
        except Card.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        card = self.get_object(pk)
        serializer = CarddSerializer(card)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        card = self.get_object(pk)
        list_instance = card.list
        board = list_instance.board

        
        custom_user = request.user.customuser

        is_owner = custom_user == board.owner

        is_assigned_member = card.assigned_members.filter(member=custom_user).exists()

        if not (is_owner or is_assigned_member):
            return Response({'detail': 'You do not have permission to edit this card.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = CardSerializer(card, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        card = self.get_object(pk)
        list = card.list
        board = list.board

        if not (request.user == board.owner or request.user in board.members.all()):
            return Response({'detail': 'You do not have permission to delete this card.'}, status=status.HTTP_403_FORBIDDEN)

        card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MemberListView(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberAllSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        member_id = self.request.query_params.get('member_id', None)
        customuser_id = self.request.query_params.get('customuser_id', None)

        if member_id:
            queryset = queryset.filter(id=member_id)
        
        if customuser_id:
            queryset = queryset.filter(member__id=customuser_id)

        return queryset
class CardCountView(APIView):
    def get(self, request, board_id, format=None):
        try:
            board = Board.objects.get(id=board_id)
            card_counts = board.get_card_counts()
            
            response_data = {
                "todo_count": card_counts.get("todo", 0),
                "in_progress_count": card_counts.get("in_progress", 0),
                "completed_count": card_counts.get("completed", 0),
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Board.DoesNotExist:
            return Response({'detail': 'Board not found.'}, status=status.HTTP_404_NOT_FOUND)
class BoardCountView(APIView):
    permission_classes = [permissions.IsAuthenticated] 

    def get(self, request, format=None):
        status_counts = defaultdict(int)

        user_boards = Board.objects.filter(owner=request.user.customuser)

        for board in user_boards:
            for list_instance in board.lists.all():
                for card in list_instance.cards.all():
                    status_counts[card.status] += 1

        response_data = {
            "todo_count": status_counts['todo'],
            "in_progress_count": status_counts['in_progress'],
            "completed_count": status_counts['completed']
        }

        return Response(response_data, status=status.HTTP_200_OK)
