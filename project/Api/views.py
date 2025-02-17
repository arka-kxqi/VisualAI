from django.shortcuts import get_object_or_404
from .models import Profile
import random
from django.shortcuts import render, get_object_or_404
from .models import Appointment
from django.http import JsonResponse
from .models import Appointment
from .models import Appointment, Profile
from django.utils import timezone
from .models import LabReport
from collections import defaultdict
from .models import *
from django.contrib.auth.models import User
from .serializers import ProfileSerializer, AppointmentSerializer
from .models import Profile, Appointment
from rest_framework import generics
import requests
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from .models import LabReport, LabReportImage
import json
from .ml_recog import *




# Step 1: AspireResponseView
class AspireResponseView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data.get('user_id')
            user = User.objects.get(id=user_id)

            image_file = request.FILES['file']

            receipt_ocr_endpoint = 'https://ocr.asprise.com/api/v1/receipt'
            r = requests.post(receipt_ocr_endpoint, data={
                'api_key': 'TEST',  # Use 'TEST' for testing purpose
                'recognizer': 'auto',  # can be 'US', 'CA', 'JP', 'SG' or 'auto'
                'ref_no': 'ocr_python_123',  # optional caller provided ref code
            }, files={"file": image_file})

            data = r.json()
            print(f" line 40  {data}")
            extracted_data = []
            for receipt in data.get('receipts', []):
                date = receipt.get('date')
                time = receipt.get('time')
                ocr_text = receipt.get('ocr_text')
                ocr_confidence = receipt.get('ocr_confidence')
                merchant_address = receipt.get('merchant_address')
                success = data.get('success')

                extracted_data.append({
                    'date': date,
                    'time': str(time),
                    'ocr_text': ocr_text,
                    'ocr_confidence': ocr_confidence,
                    'merchant_address': merchant_address,
                    'success': str(success),
                })

            # Save to TemporaryLabReport
            temp_report = TemporaryLabReport.objects.create(
                user=user,
                ocr_text=extracted_data[0]['ocr_text'],
                original_report_date=extracted_data[0]['date'],
                ocr_confidence=extracted_data[0]['ocr_confidence'],
                address_of_hospital=extracted_data[0]['merchant_address'],
                image=image_file
            )
            print(f"line 69 extracted data :    {extracted_data}")
            print(f"Temporary  id  :    {temp_report.id}")

            return JsonResponse({'temporary_report_id': temp_report.id}, safe=False)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


# Helper function for Gemini API call


def gemini_response(prompt):
    API_KEY = 'AIzaSyBP2PuxTxEG07iLzj4hQuvftwbCb6r08hI'
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    response_text = response.json(
    )['candidates'][0]['content']['parts'][0]['text']
    return response_text

# Step 2: GeminiStep1APIView


class GeminiStep1APIView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data.get('user_id')
            temp_report_id = request.data.get('temporary_report_id')
            temp_report = TemporaryLabReport.objects.get(
                id=temp_report_id, user_id=user_id)

            prompt1 = '''I have some text from a lab report obtained through OCR. It's a bit messy, and I'd like to clean it up and organize the data nicely in text.
            Present the information in plain text, don't use tables.

            Here is the OCR text: 

            ''' + temp_report.ocr_text

            gemini_result = gemini_response(prompt1)
            print(f"Line 118     {gemini_result}")

            # Save cleaned text to TemporaryLabReport
            temp_report.gemini_prompt1_response = gemini_result
            temp_report.save()

            return JsonResponse({'temporary_report_id': temp_report.id}, safe=False)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

# Step 3: GeminiStep2APIView


class GeminiStep2APIView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data.get('user_id')
            temp_report_id = request.data.get('temporary_report_id')
            temp_report = TemporaryLabReport.objects.get(
                id=temp_report_id, user_id=user_id)

            prompt2 = (
                "I have an OCR-extracted text from a medical lab report. "
                "I need to transform this text into a well-structured JSON format that can be easily stored in a database and displayed on a frontend. "
                "The JSON should include detailed test results with appropriate keys for descriptions, results, reference ranges, and units. "
                "No need to give the information of the patient, only provide the test results.\n\n"
                f"Here's the OCR-extracted text: \n\n{temp_report.gemini_prompt1_response}\n\n"
                "Transform the text into the following JSON structure:\n\n"
                "[\n"
                '    {"test_name": "Complete Blood Count (CBC)"}\n'
                '    {"sample": "Blood"}\n'
                '    {"description": "Haemoglobin", "result": "15", "ref_range": "13-17", "unit": "g/dL"},\n'
                '    {"description": "Total Leucocyte Count", "result": "5000", "ref_range": "4000-10000", "unit": "/cumm"},\n'
                '    {"description": "Neutrophils", "result": "50", "ref_range": "40-80", "unit": "%"},\n'
                '    {"description": "Lymphocytes", "result": "40", "ref_range": "20-40", "unit": "%"},\n'
                '    {"description": "Eosinophils", "result": "", "ref_range": "1-6", "unit": "%"},\n'
                '    {"description": "Basophils", "result": "0.00", "ref_range": "0-1", "unit": "%"},\n'
                '    {"description": "Absolute Neutrophils", "result": "2500.00", "ref_range": "2000-7000", "unit": "/cumm"},\n'
                '    {"description": "Absolute Lymphocytes", "result": "2000.00", "ref_range": "1000-3000", "unit": "/cumm"},\n'
                '    {"description": "Absolute Eosinophils", "result": "50.00", "ref_range": "20-500", "unit": "/cumm"},\n'
                '    {"description": "Absolute Monocytes", "result": "450.00", "ref_range": "200-1000", "unit": "/cumm"},\n'
                '    {"description": "RBC Count", "result": "5", "ref_range": "4.5-5.5", "unit": "million/cumm"},\n'
                "\n please provide json response only as the given structured no need to give extra explanatory text just give the json response as you are API "
                "]"
            )

            gemini_json_final = gemini_response(prompt2)
            data_for_clean = gemini_response(prompt2)
            data_ = data_for_clean.strip()
            cleaned_data = data_.replace(
                '```json', '').replace('```', '').strip()

            if cleaned_data:
                # Decode the JSON data
                report_data_list = json.loads(cleaned_data)

                # Initialize variables for test_name and sample
                test_name = None
                sample = None

                # Separate test_name and sample from the main data
                for item in report_data_list:
                    if 'test_name' in item:
                        test_name = item['test_name']
                        break
                for item in report_data_list:
                    if 'sample' in item:
                        sample = item['sample']
                        break

                # Check if the test_name already exists in the Test model
                test_instance, created = Test.objects.get_or_create(
                    user=temp_report.user,
                    name=test_name
                )

                # Create LabReport instance
                lab_report = LabReport.objects.create(
                    user=temp_report.user,
                    test_name=test_instance,
                    sample=sample,
                    report_data=gemini_json_final,
                    report_date=temp_report.original_report_date,
                    uploaded_at=timezone.now(),
                    ocr_conf=temp_report.ocr_confidence,
                    hospital_address=temp_report.address_of_hospital
                )

            # Create LabReportImage instance
            LabReportImage.objects.create(
                lab_report=lab_report,
                image=temp_report.image,
                size=temp_report.image.size
            )

            return JsonResponse(gemini_json_final, safe=False)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class DatasetAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        try:
            user = request.user

            if not user.is_authenticated:
                return Response({"error": "User not authenticated"}, status=401)

            user_id = user.id
            image_file = request.FILES['file']

            # Step 1: Make a POST request to AspireResponseView
            aspire_url = 'http://localhost:8000/ocr'  # Adjust URL as needed
            response = requests.post(
                aspire_url, files={'file': image_file}, data={'user_id': user_id})
            response_data = response.json()
            temporary_report_id = response_data['temporary_report_id']

            # Step 2: Make a POST request to GeminiStep1APIView
            gemini_prompt1_url = 'http://localhost:8000/gemini_prompt1'  # Adjust URL as needed
            response = requests.post(gemini_prompt1_url, data={
                                     'temporary_report_id': temporary_report_id, 'user_id': user_id})
            response_data = response.json()
            temporary_report_id = response_data['temporary_report_id']

            # Step 3: Make a POST request to GeminiStep2APIView
            gemini_prompt2_url = 'http://localhost:8000/gemini_prompt2'  # Adjust URL as needed
            response = requests.post(gemini_prompt2_url, data={
                                     'temporary_report_id': temporary_report_id, 'user_id': user_id})
            gemini_json_final = response.json()

            # Return the final JSON response
            return JsonResponse(gemini_json_final, safe=False)

        except Exception as e:
            original_exception = e.__cause__
            error_message = f"Original error: {str(original_exception)}" if original_exception else str(
                e)
            return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def data_representation(request, id, test_name):
      # Get user id to fetch the data
    
    test_instance = Test.objects.get(user=id, name=test_name)

# Get the id of the test_instance
    test_id = test_instance.id

    # Fetch reports for the user and the specific test name
    reports = LabReport.objects.filter(user=id, test_name=test_id)
    

    combined_report_data = defaultdict(lambda: {"description": "", "result": [
    ], "ref_range": "", "unit": ""})  # initiazing the structure of the response
    for report in reports:
        print(f"Processing report ID: {report.id}")
        print(f"Report Data: {report.report_data}")
        # Clean and prepare the JSON data for decoding
        cleaned_data = report.report_data.strip()
        cleaned_data = cleaned_data.replace('```json', '').replace('```', '')
        cleaned_data = cleaned_data.strip()
        if cleaned_data:
            try:
                # Decode the JSON data
                report_data_list = json.loads(cleaned_data)
                print(f"Decoded JSON: {report_data_list}")
                for item in report_data_list:
                    description = item.get("description")
                    if description:
                        if description not in combined_report_data:
                            combined_report_data[description]["description"] = item.get(
                                "description", "")
                            combined_report_data[description]["ref_range"] = item.get(
                                "ref_range", "")
                            combined_report_data[description]["unit"] = item.get(
                                "unit", "")
                        # Append result if it exists
                        result = item.get("result")
                        if result:
                            combined_report_data[description]["result"].append(
                                {report.report_date.strftime('%Y-%m-%d'): result})
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON for report {report.id}: {e}")
                continue  # Skip this report if there's a decoding error
        else:
            print(f"Empty or invalid report_data for report {report.id}")
    # Prepare final result data
    result_data = list(combined_report_data.values())
    print(f"Final Result Data: {result_data}")
    return JsonResponse(result_data, safe=False)


def report_names_get(request):
    user_id = request.user.id
    reports = Test.objects.filter(user_id=user_id)
    # Extracting only the test_name field as a list
    names = reports.values_list('name', flat=True)

    return JsonResponse(list(names), safe=False)


def report_images(request, id, name):

    # Get the test ID based on the test name
    test = get_object_or_404(Test, name=name)
    test_id = test.id

    # Filter reports based on test ID and user ID
    reports = LabReport.objects.filter(test_name=test_id, user_id=id)
    report_data = []

    for report in reports:
        try:
            image = LabReportImage.objects.get(lab_report=report)
            image_url = image.image.url
        except LabReportImage.DoesNotExist:
            image_url = None

        report_data.append({

            'id': report.id,
            'name': str(report.test_name),
            'date': report.report_date,  # assuming there's a date field
            'sample': report.sample,     # assuming there's a sample field
            'image_url': image_url,
        })

    # Return the report data as a JSON response
    return JsonResponse({'report_data': report_data})


# appointments logic


def appointment(request):
    user_profile = Profile.objects.get(user=request.user)

    if user_profile.role == 'doctor':
        appointments = Appointment.objects.filter(doctor=request.user)
    else:
        appointments = Appointment.objects.filter(patient=request.user)

    # Convert each appointment to a dictionary
    appointments_data = [
        {
            "id": appointment.id,
            "doctor": appointment.doctor.username,
            "doctor_id": appointment.doctor.id,
            "patient": appointment.patient.username,
            "patient_id": appointment.patient.id,
            "appointment_date": appointment.appointment_date,
            "apointment_time": appointment.apointment_time,
            "status": appointment.status,
            "zoom_meeting_id": appointment.meeting_id,
            "zoom_join_link": appointment.join_link,
        }
        for appointment in appointments
    ]

    return JsonResponse(appointments_data, safe=False)


def accept_appointment(request, id):
    # Get the appointment object
    appointment = get_object_or_404(Appointment, id=id)

    # Update appointment status to 'confirmed'
    appointment.status = 'confirmed'

    # Generate a unique meeting ID
    meeting_id = f"room_{random.randint(1000, 9999)}"

    # Construct the call link using the meeting ID
    join_link = f"http://127.0.0.1:8000/join-call?roomID={meeting_id}"

    # Save meeting ID and join link to the appointment
    appointment.meeting_id = meeting_id
    appointment.join_link = join_link
    appointment.save()

    # Optionally, you can return a JSON response (for debugging or front-end integration)
    return JsonResponse({
        'message': 'Appointment accepted and call link generated.',
        'meeting_id': meeting_id,
        'join_link': join_link
    })


def impersonate_report_names_get(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    request.user = target_user
    return report_names_get(request)

#ml connecting part




class ProfileListCreateView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class AppointmentListCreateView(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class AppointmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


# templates rendering views
def appointment_render(request):
    return render(request, 'appointment.html')


from django.http import JsonResponse
from django.shortcuts import render
from .models import Profile

from django.shortcuts import render
from django.http import JsonResponse
from .models import Profile

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from .models import Profile
# from .ai_model import recommend_doctor  # Import your AI recommendation function
import json
def exm(request):
    problem="i have cough and heart problem"
    a=recommend_doctor(problem)
    return print(a)


from django.http import JsonResponse
from .models import Profile
 # Adjust import based on your project structure

def recommend_specialization(request, problem):
    recommended_specialization = recommend_doctor(problem)
    print(recommended_specialization)
    doctors = Profile.objects.filter(role__icontains="Doctor", specialization=recommended_specialization)

    data = [
        {
            "id": doctor.id,
            "doctor": doctor.user.username,  # Access the username of the related User model
            "specialization": doctor.specialization,
        }
        for doctor in doctors
    ]

    return JsonResponse({"doctors": data})




def index(request):
    doctor = Profile.objects.filter(role__icontains="Doctor")
    context = {
        "doctors": doctor,
    }
    return render(request, 'index.html', context)

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Appointment, Profile
from django.utils.dateparse import parse_date, parse_time

@login_required
def book_appointment(request):
    if request.method == "POST":
        patient = request.user
        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        problem = request.POST.get('problem')
        
        try:
            # Fetch the Profile object for the selected doctor
            doctor_profile = Profile.objects.get(id=doctor_id)
            doctor = doctor_profile.user  # Get the associated User object
        except Profile.DoesNotExist:
            return HttpResponse("Doctor not found", status=404)

        try:
            appointment_date = parse_date(appointment_date)
            appointment_time = parse_time(appointment_time)
        except (ValueError, TypeError):
            return HttpResponse("Invalid date or time format", status=400)
        
        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=appointment_date,
            apointment_time=appointment_time,  # Corrected the typo
            status='pending'
        )
        
        return redirect('index')  # Redirect to the index page or wherever you want

    return HttpResponse("Invalid request method", status=405)


def chat_with_doctor(request):
    return render(request, 'chat_with_doctor.html')


def profile(request):
    return render(request, 'profile.html')

def chart(request):
    return render(request, 'chart.html')


def image(request):
    return render(request, 'image_view.html')


def join_call(request):
    return render(request, 'video_call.html', {"name": request.user})

def doct(request, id):
    return render(request, "doct_repo_view.html", {"userid": id})


def upload(request):
    return render(request, 'upload_image.html')