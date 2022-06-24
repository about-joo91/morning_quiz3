from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from .serializers import CompanySerializer, JobPostSerializer, JobPostSkillSetSerializer
from .models import (
    JobPostSkillSet,
    JobType,
    JobPost,
    Company,
    SkillSet
)
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404
class SkillView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        skills = self.request.query_params.getlist('skills', '')
        print("skills = ", end=""), print(skills)
        data = JobPost.objects.filter(
            Q(skillset__name__in= skills)
            )
        if data.exists():
            serializer = JobPostSerializer(data, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(status= status.HTTP_400_BAD_REQUEST)


class JobView(APIView):
    def post(self, request):
        job_post_serializer = JobPostSerializer(data = request.data)
        if job_post_serializer.is_valid():
            job_type= int(request.data.get("job_type", None))
            company_name = request.data.get("company_name", None)
            job_type_intance = get_object_or_404(JobType, id= job_type)
            company_instane, _ = Company.objects.get_or_create(company_name = company_name)
            job_post_serializer.save(job_type = job_type_intance, company = company_instane)
            return Response(job_post_serializer.data, status=status.HTTP_200_OK)
        return Response(job_post_serializer.errors ,status = status.HTTP_400_BAD_REQUEST)

