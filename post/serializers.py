from rest_framework import serializers
from .models import Company, JobPost, JobPostSkillSet
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["company_name", "business_area"]
class JobPostSerializer(serializers.ModelSerializer):
    position_type = serializers.SerializerMethodField()
    def get_position_type(self, obj):
        return obj.job_type.job_type
    class Meta:
        model = JobPost
        fields = ["position_type", "company", "job_description","salary"]
class JobPostSkillSetSerializer(serializers.ModelSerializer):
    job_post = JobPostSerializer()
    skill_set = serializers.SerializerMethodField()
    def get_skill_set(self, obj):
        return [skill_set.name for skill_set in obj.skill_set.all()]
    class Meta:
        model = JobPostSkillSet
        fields = ["skill_set", "job_post"]