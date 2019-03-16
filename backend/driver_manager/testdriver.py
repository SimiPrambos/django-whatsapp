import os
from django.conf import settings
from .webwhatsapi import WhatsAPIDriver, WhatsAPIDriverStatus
from background_task import background

@background()
class Driver():
    
    instance = None

    def __init__(self, id):
        self.id = id
    
    def start():
        profile_path = settings.CHROME_CACHE_PATH + str(self.id)
        if not os.path.exists(profile_path):
            os.makedirs(profile_path)

        chrome_options = [
            'window-size=' + settings.CHROME_WINDOW_SIZE,
            '--user-agent=' + settings.USER_AGENT
        ]

        if settings.CHROME_IS_HEADLESS:
            chrome_options.append('--headless')
        if settings.CHROME_DISABLE_SANDBOX:
            chrome_options.append('--no-sandbox')
        if settings.CHROME_DISABLE_GPU:
            chrome_options.append('--disable-gpu')
        
        self.instance = WhatsAPIDriver(
            username=self.id, 
            profile=profile_path, 
            client='chrome', 
            chrome_options=chrome_options
        )

    def stop(self):
        if self.instance:
            self.instance.quit()

    def get_instance(self):
        return self.instance