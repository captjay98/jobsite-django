from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    SeekerProfileSerializer,
    EmployerProfileSerializer,
    JobSerializer,
    ApplicationSerializer,
)
from .models import EmployerProfile, Job, Application
from seekers.models import SeekerProfile


class EmployerProfileView(APIView):
    def get(self, request, format=None):
        user = self.request.user
        if not user.is_employer:
            return Response(
                {"unauthorized": "Only Employers can access this page"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            employerProfile = EmployerProfile.objects.get(user=user)
            employerProfile = EmployerProfileSerializer(employerProfile)
            return Response(
                {"employer": employerProfile.data},
                status=status.HTTP_200_OK,
            )

        except EmployerProfile.DoesNotExist:
            return Response(
                {"error": "Employer profile does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def put(self, request):
        user = self.request.user
        if not user.is_employer:
            return Response(
                {"unauthorized": "Only Employers can access this page"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            employer_profile = EmployerProfile.objects.get(user=user)
            serializer = EmployerProfileSerializer(
                employer_profile,
                data=request.data,
            )
            if serializer.is_valid():
                serializer.save(partial=True)
                serializer.save()

                return Response(
                    {"success": serializer.data},
                    status=status.HTTP_200_OK,
                )

        except EmployerProfile.DoesNotExist:
            return Response(
                {"error": serializer.errors},
                status=status._404_NOT_FOUND,
            )


class SeekerProfilesView(APIView):
    def get(self, request, *args, **kwargs):
        print(kwargs)
        user = self.request.user
        if not user.is_employer:
            return Response(
                {"unauthorized": "Only Employers can access this page"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if "id" in kwargs:
            id = kwargs["id"]
            try:
                profile = SeekerProfile.objects.get(id=id)
                serializer = SeekerProfileSerializer(profile)
                return Response(serializer.data)
            except SeekerProfile.DoesNotExist:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            profiles = SeekerProfile.objects.all()
            serializer = SeekerProfileSerializer(profiles, many=True)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )


class SeekerProfileDetailsView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        user = self.request.user
        if not user.is_employer:
            return Response(
                {"unauthorized": "Only Employers can access this page"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if "id" in kwargs:
            try:
                id = kwargs["id"]
                seeker = SeekerProfile.objects.get(id=id)
                serializer = SeekerProfileSerializer(seeker)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except SeekerProfile.DoesNotExist:
                return Response(
                    {"error": "No user with that ID found"},
                    status=status.HTTP_404_NOT_FOUND,
                )


class JobsView(APIView):
    def get(self, request):
        user = self.request.user
        if not user.is_employer:
            return Response(
                {"unauthorized": "Only Employers can access this page"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            recruiter = EmployerProfile.objects.get(user=user)
            jobs = Job.objects.filter(recruiter=recruiter)
            serializer = JobSerializer(jobs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            return Response(
                {"error": "Profile Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def post(self, request):
        user = request.user
        if not user.is_employer:
            return Response(
                {"unauthorized": "Only employers can create jobs"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            recruiter = EmployerProfile.objects.get(user=user)
        except EmployerProfile.DoesNotExist:
            return Response(
                {"error": "Employer profile does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            job = serializer.save(recruiter=recruiter)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class JobView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        user = self.request.user
        id = kwargs["id"]
        if not user.is_employer:
            return Response(
                {"unauthorized": "Only Employers can access this page"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            recruiter = EmployerProfile.objects.get(user=user)
            jobs = Job.objects.filter(recruiter=recruiter, id=id)
            serializer = JobSerializer(jobs, many=True)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        except Job.DoesNotExist:
            return Response(
                {"error": "Job Not Found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def put(self, request, id):
        user = self.request.user
        if not user.is_employer:
            return Response(
                {"unauthorized": "Only Employers can access this page"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            job = Job.objects.get(id=id, recruiter__user=user)
        except Job.DoesNotExist:
            return Response(
                {"error": "Job not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class ApplicationsView(APIView):
    def get(self, request):
        user = self.request.user

        if not user.is_employer:
            return Response("")

        try:
            applications = Application.objects.filter(employer=user)
            serializer = ApplicationSerializer(applications, many=True)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        except Application.DoesNotExist:
            return Response(
                "Application does Not Exist",
                status=status.HTTP_400_BAD_REQUEST,
            )
