# measure.py - YouTube AdBlock (adBlock Plus)
from playwright.sync_api import sync_playwright
import time
import subprocess

def phase_start(name):
    """Signal à GMT que la phase commence"""
    subprocess.run(["echo", f"[PHASE: {name}]"])

def phase_end(name):
    """Signal à GMT que la phase se termine"""
    subprocess.run(["echo", f"[PHASE-END: {name}]"])

def watch_video(page, url, duration, phase_name):
    page.goto(url, timeout=60000, wait_until="domcontentloaded")
    
    # Accepter les cookies si nécessaire (hors phase mesurée)
    for text in ['Accept all', 'Aceptar todo', 'Tout accepter']:
        try:
            page.click(f"button:has-text('{text}')", timeout=3000)
            break
        except:
            pass
    
    # Attendre que la vidéo démarre vraiment
    time.sleep(3)
    
    # ---- DÉBUT DE LA PHASE MESURÉE ----
    phase_start(phase_name)
    time.sleep(duration)
    phase_end(phase_name)
    # ---- FIN DE LA PHASE MESURÉE ----

def run():
    with sync_playwright() as p:
        # Since GMT copies the files to /app in the Docker container,
        # the path will be this one:

        path_to_extension = "/app/adblockplus"


        # Launch Chromium using a persistent context
        # so that the extension can be injected
        
        context = p.chromium.launch_persistent_context(
            user_data_dir="/tmp/playwright-user-data", # Temporary folder required
            headless=True,
            args=[
                f"--disable-extensions-except={path_to_extension}",
                f"--load-extension={path_to_extension}",
                "--headless=new"
            ]
        )

        # In a persistent context, the browser already opens one page by default
        page = context.pages[0]


        watch_video(page, 
                    "https://youtu.be/8YxQLBRBpJI?si=WqOA2tSgWDM5BMKB", 
                    161, "video1")
        
        watch_video(page, 
                    "https://youtu.be/cX24KlL8klY?si=havUAEjKDooz68T_", 
                    186, "video2")
        
        watch_video(page, 
                    "https://youtu.be/Y4J_NYAQQEQ?si=BLcMRRYQMqy0-23l", 
                    181, "video3")

        context.close()

if __name__ == "__main__":
    run()