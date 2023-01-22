from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess

@csrf_exempt
def webhook(request):
    secret = request.headers.get('X-Hub-Signature')
    if secret != 'QWERTY123456':
        return JsonResponse({'error': 'Invalid secret'}, status=401)

    subprocess.run(['/deploy.sh'])

    return JsonResponse({'status': 'success'})
