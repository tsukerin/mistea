import re
import subprocess
from pyngrok import ngrok
import time

ngrok_tunnel = ngrok.connect(8001)

try:
    s='█'
    for i in range(101):
        time.sleep(0.03)
        print('\r','Загрузка',i*s,str(i),'%',end='')

    tunnel_info = ngrok.get_tunnels()[0]
    ngrok_url = tunnel_info.public_url

    print(f"\nNgrok-адрес: {ngrok_url}")

    manage_py_path = 'C:\projects\Mistea_project\mistea\manage.py'
    django_settings_path = 'C:\projects\Mistea_project\mistea\mistea\settings.py'
    with open(django_settings_path, 'r') as file:
        settings_content = file.read()

    csrf_trusted_origins_pattern = re.compile(r"CSRF_TRUSTED_ORIGINS\s*=\s*\[[^\]]*\]")
    updated_settings_content = csrf_trusted_origins_pattern.sub(
        f"CSRF_TRUSTED_ORIGINS = ['{ngrok_url}']", settings_content)

    with open(django_settings_path, 'w') as file:
        file.write(updated_settings_content)

    print(f"Адрес Ngrok успешно добавлен в CSRF_TRUSTED_ORIGINS: {ngrok_url}")

    django_process = subprocess.Popen(['python', manage_py_path, 'runserver', '8001'])
    django_process.wait()

except Exception as e:
    print(f"Произошла ошибка: {e}")

finally:
    ngrok.disconnect(ngrok_tunnel.public_url)
