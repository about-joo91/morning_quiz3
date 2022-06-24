from rest_framework import serializers
from .models import Company, JobPost, JobPostSkillSet, JobType, SkillSet

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "company_name"]
class JobPostSerializer(serializers.ModelSerializer):
    def validate(self, data):
        request_data = self.context.get('request', {}).data
        job_type = request_data.get("job_type", None)
        company_name = request_data.get("company_name", None)
        skillset = request_data.get('skillsets', None)
        if not job_type:
            raise serializers.ValidationError(
                detail= {
                    "error": "직업 유형이 비어있습니다."
                }
            )
        if not company_name:
            raise serializers.ValidationError(
                detail= {
                    "error": "회사 이름이 비어있습니다."
                }
            )
        if not skillset:
            raise serializers.ValidationError(
                detail= {
                    "error": "기술 스택이 비어있습니다."
                }
            )
        job_type= int(job_type)
        if not JobType.objects.filter(id=job_type).exists():
            raise serializers.ValidationError(
                detail= {
                    "error": "없는 직업유형입니다."
                }
            )
        return data
    def create(self, validated_data):
        request_data = self.context.get('request').data
        job_type = request_data.get("job_type")
        company_name = request_data.get("company_name")
        skillsets = list(map(int,request_data.get('skillsets')))
        job_post = JobPost.objects.create(**validated_data)
        job_post.job_type = JobType.objects.get(id= job_type)
        company_obj, _ = Company.objects.get_or_create(company_name = company_name)
        job_post.company = company_obj
        job_post.skillset_set.add(*skillsets)
        job_post.save()
        return job_post

    position_type = serializers.SerializerMethodField(read_only=True)
    company = CompanySerializer(read_only=True)
    skillsets = serializers.SerializerMethodField(read_only=True)
    def get_skillsets(self, obj):
        return [skill_set.name for skill_set in obj.skillset_set.all()]
    def get_position_type(self, obj):
        return obj.job_type.job_type
    class Meta:
        model = JobPost
        fields = ["id","position_type", "company", "job_description","salary", "skillsets"]
class JobPostSkillSetSerializer(serializers.ModelSerializer):
    job_post = JobPostSerializer()
    class Meta:
        model = JobPostSkillSet
        fields = ["job_post"]