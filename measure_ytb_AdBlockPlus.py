# measure.py - YouTube AdBlock (adBlock Plus)
from playwright.sync_api import sync_playwright
import time

def timestamp_us():
    """Returns the current timestamp in microseconds"""
    return int(time.time() * 1_000_000)

def note(msg):
    """Prints in the format expected by GMT"""
    print(f"{timestamp_us()} {msg}", flush=True)

def watch_video(page, url, duration, label):
    page.goto(url, timeout=60000, wait_until="domcontentloaded")
    
    # Accept cookies if necessary (outside the measured phase)
    for text in ['Accept all', 'Aceptar todo', 'Tout accepter']:
        try:
            page.click(f"button:has-text('{text}')", timeout=3000)
            break
        except:
            pass
    
    # Wait for the video to actually start
    time.sleep(3)
    
    note(f"START {label}")   # GMT records this timestamp
    time.sleep(duration)
    note(f"END {label}")     # GMT records this timestamp

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

        # Manually load cookies from the json file
        with open("/app/free_state.json") as f:
            state = json.load(f)
            context.add_cookies(state["cookies"])

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
        time.sleep(5)  # let powermetrics finish properly


if __name__ == "__main__":
    run()