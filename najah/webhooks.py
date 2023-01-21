from django.http import JsonResponse
import subprocess

def webhook(request):
    secret = request.headers.get('X-Hub-Signature')
    if secret != 'QWERTY123456':
        return JsonResponse({'error': 'Invalid secret'}, status=401)

    subprocess.run(['/deploy.sh'])

    return JsonResponse({'status': 'success'})
