from rest_framework import serializers
from .models import Board, List, Card,Member
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from account.models import CustomUser
from django.shortcuts import get_object_or_404
class AddMemberSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate_username(self, value):
        try:
            user = CustomUser.objects.get(user__username=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(f"User with username '{value}' does not exist.")
        return value

    def create(self, validated_data):
        board = self.context.get('board')
        username = validated_data.get('username')

        try:
            member_user = CustomUser.objects.get(user__username=username)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(f"User with username '{username}' does not exist.")

        # Check if the user is already a member
        if Member.objects.filter(board=board, member=member_user).exists():
            raise serializers.ValidationError(f"User '{username}' is already a member of this board.")

        # Add the member to the board
        Member.objects.create(board=board, member=member_user)

        # Update members_num field
        board.members_num = board.members.count()
        board.save()

        return validated_data

class MemberListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='member.user.username', read_only=True)
    first_name = serializers.CharField(source='member.user.first_name', read_only=True)
    last_name = serializers.CharField(source='member.user.last_name', read_only=True)
    email = serializers.EmailField(source='member.user.email', read_only=True)

    class Meta:
        model = Member
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class BoardSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.user.username')
    members = MemberListSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'name', 'owner', 'members_num', 'color', 'members']
        read_only_fields = ['owner']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        # Check if the user is authenticated
        if not user.is_authenticated:
            raise ValidationError("You must be logged in to create a board.")

        # Check if the CustomUser exists, if not, create it
        if not hasattr(user, 'customuser'):
            custom_user = CustomUser.objects.create(user=user)
        else:
            custom_user = user.customuser

        # Set the owner as the logged-in user's CustomUser instance
        validated_data['owner'] = custom_user
        return super().create(validated_data)
class MemberDetailSerializer(serializers.ModelSerializer):
    boards =BoardSerializer(many=True, read_only=True)  # Include boards

    class Meta:
        model = Member
        fields = ['id', 'email', 'name', 'boards'] 

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id', 'title', 'content', 'board']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        board = validated_data.get('board')

        if not board:
            board_id = request.query_params.get('board_id')
            if board_id:
                try:
                    board = Board.objects.get(id=board_id)
                except Board.DoesNotExist:
                    raise serializers.ValidationError("Board not found.")
            else:
                raise serializers.ValidationError("Board ID is required.")

        # Check if the user is the owner of the board
        if user.is_authenticated and board.owner != user.customuser:
            raise serializers.ValidationError("You are not authorized to add a list to this board.")

        validated_data['board'] = board

        return super().create(validated_data)

class ListBoardSerializer(serializers.ModelSerializer):
    board =BoardSerializer( read_only=True)

    class Meta:
        model = List
        fields = ['id', 'title', 'content','board']
        

  
        
# class CardSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Card
#         fields = ['id', 'title', 'content', 'board','list','priority','status']
#         read_only_fields = ['custom_user','member']

#     def create(self, validated_data):
#         request = self.context.get('request')
#         custom_user = request.user.customuser
#         validated_data['custom_user'] = custom_user
#         return super().create(validated_data)
class CardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Card
        fields = ['id', 'title', 'content', 'priority', 'status', 'list',]

    def create(self, validated_data):
        request = self.context.get('request')
        custom_user = request.user  # Get the logged-in user from the request

        # You may have logic to handle member if needed
        member_id = self.context.get('member_id')  # Get member ID from context or request
        
        # Additional logic for member_id validation or assignment
        if member_id:
            try:
                member = CustomUser.objects.get(id=member_id)
                # Optionally: Check if the member is part of the board or has any other valid context
                if not Member.objects.filter(board__members=member, board__owner=custom_user).exists():
                    raise serializers.ValidationError("You are not authorized to assign this member.")
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("Member does not exist.")
        
        # Create and return the Card instance
        return super().create(validated_data)

class MemberAllSerializer(serializers.ModelSerializer):
    boards = BoardSerializer(source='board', read_only=True)
    lists = serializers.SerializerMethodField()
    cards = serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = ['id', 'boards', 'lists', 'cards']

    def get_lists(self, obj):
        # Fetch all lists related to the member's board
        lists = List.objects.filter(board=obj.board)
        return ListSerializer(lists, many=True).data

    def get_cards(self, obj):
        # Fetch all cards related to the member's board
        cards = Card.objects.filter(list__board=obj.board)
        return CardSerializer(cards, many=True).data
