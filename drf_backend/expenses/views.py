from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Expense
from .serializers import ExpenseSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from drf_spectacular.utils import extend_schema


class ExpenseListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        expenses = Expense.objects.filter(
            user=request.user
        )

        category = request.query_params.get('category')

        date = request.query_params.get('date')

        if category:
            expenses = expenses.filter(category=category)

        if date:
            expenses = expenses.filter(date=date)

        serializer = ExpenseSerializer(expenses, many=True)

        return Response(serializer.data)
    
    @extend_schema(
        request=ExpenseSerializer,
        responses=ExpenseSerializer
    )

    def post(self, request):

        serializer = ExpenseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExpenseDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self,request,pk):
        try:
            return Expense.objects.get(pk = pk,user=request.user)
        except Expense.DoesNotExist:
            return None
        
    def get(self,request,pk):
        expense = self.get_object(request,pk)
        if not expense:
            return Response(
                {"Error: Response not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)

    @extend_schema(
        request=ExpenseSerializer,
        responses=ExpenseSerializer
    )
    def put(self,request,pk):
        expense = self.get_object(request,pk)
        if not expense:
            return Response(
                {"Error: Response not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serialiser = ExpenseSerializer(expense,data=request.data)

        if serialiser.is_valid():
            serialiser.save(user=request.user)
        return Response(serialiser.data)
    def delete(self,request,pk):
        expense = self.get_object(request,pk)
        if not expense:
            return Response(
                {"Error: Data not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        expense.delete()
        return Response(
            {"Message:Expense has been deleted"},
            status=status.HTTP_404_NOT_FOUND
        )
class ExpenseSummaryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        expenses = Expense.objects.filter(
            user=request.user
        )

        total_expense = expenses.aggregate(
            total=Sum('amount')
        )['total'] or 0

        category_summary = expenses.values(
            'category'
        ).annotate(
            total=Sum('amount')
        )

        return Response(
            {
                "total_expense": total_expense,
                "category_summary": category_summary
            }
        )
        
class MonthlyExpenseSummaryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        expenses = Expense.objects.filter(
            user=request.user
        )

        monthly_summary = expenses.annotate(
            month=ExtractMonth('date')
        ).values(
            'month'
        ).annotate(
            total=Sum('amount')
        ).order_by('month')

        return Response(monthly_summary)
        
    