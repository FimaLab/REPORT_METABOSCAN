import subprocess
import time
import os
import signal
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import base64
import psutil
import threading
import queue
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class PDFGenerator:
    def __init__(self):
        self.message_queue = queue.Queue()
        self.driver = None
        self.flask_process = None
        self.shutdown_flag = threading.Event()
        
        # Windows-specific setup
        if os.name == 'nt':
            signal.signal(signal.SIGINT, self._handle_signal)
            signal.signal(signal.SIGTERM, self._handle_signal)

    def _handle_signal(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"Received signal {signum}, shutting down...")
        self.shutdown_flag.set()

    def _setup_chrome(self):
        """Configure Chrome WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

    def _start_flask_app(self):
        """Start Flask/Dash application"""
        process = subprocess.Popen(
            ['python', 'main.py'],
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
        )
        time.sleep(5)  # Wait for server to start
        return process

    def _kill_process_tree(self, pid):
        """Safely terminate process tree"""
        try:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)
            
            if os.name == 'nt':
                # Windows-specific graceful shutdown
                parent.send_signal(signal.CTRL_BREAK_EVENT)
                time.sleep(1)
            
            for child in children:
                try:
                    child.terminate()
                except psutil.NoSuchProcess:
                    continue
            
            gone, still_alive = psutil.wait_procs(children, timeout=5)
            parent.terminate()
            parent.wait(5)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
        except Exception as e:
            print(f"Process termination error: {e}")

    def _generate_pdf(self):
        """Generate PDF from current page"""
        print_settings = {
            "landscape": False,
            "paperWidth": 8.27,
            "paperHeight": 11.69,
            "marginTop": 0.4,
            "marginBottom": 0.4,
            "marginLeft": 0.4,
            "marginRight": 0.4,
            "printBackground": True,
            "scale": 1.0,
            "preferCSSPageSize": True
        }

        try:
            self.driver.get(f"http://localhost:8050?nocache={time.time()}")
            
            # Wait for page to stabilize
            time.sleep(2)
            
            # Set precise dimensions
            self.driver.execute_script("""
                document.body.style.width = '210mm';
                document.body.style.height = '297mm';
                document.body.style.margin = '0';
                document.body.style.padding = '0';
            """)
            
            # Additional stabilization time
            time.sleep(1)
            
            pdf_data = self.driver.execute_cdp_cmd("Page.printToPDF", print_settings)
            with open("output.pdf", "wb") as f:
                f.write(base64.b64decode(pdf_data["data"]))
            print("Successfully generated updated PDF")
            
        except Exception as e:
            print(f"PDF generation failed: {e}")

    def _monitor_files(self):
        """Watch for file changes"""
        class ChangeHandler(FileSystemEventHandler):
            def __init__(self, callback):
                self.callback = callback
            
            def on_modified(self, event):
                if event.src_path.endswith('main.py'):
                    self.callback()

        handler = ChangeHandler(self._handle_file_change)
        observer = Observer()
        observer.schedule(handler, path='.', recursive=False)
        observer.start()
        
        try:
            while not self.shutdown_flag.is_set():
                time.sleep(1)
        finally:
            observer.stop()
            observer.join()

    def _handle_file_change(self):
        """Handle main.py modifications"""
        print("Detected changes in main.py - reloading...")
        self.message_queue.put('RELOAD')

    def run(self):
        """Main execution loop"""
        try:
            # Initialize browser
            self.driver = self._setup_chrome()
            
            # Start Flask app
            self.flask_process = self._start_flask_app()
            
            # Initial PDF generation
            self._generate_pdf()
            
            # Start file watcher in separate thread
            watcher_thread = threading.Thread(
                target=self._monitor_files,
                daemon=True
            )
            watcher_thread.start()
            
            # Main processing loop
            while not self.shutdown_flag.is_set():
                try:
                    msg = self.message_queue.get_nowait()
                    if msg == 'RELOAD':
                        self._kill_process_tree(self.flask_process.pid)
                        self.flask_process = self._start_flask_app()
                        self._generate_pdf()
                except queue.Empty:
                    pass
                
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("Shutdown requested...")
        finally:
            print("Cleaning up resources...")
            if self.driver:
                self.driver.quit()
            if self.flask_process:
                self._kill_process_tree(self.flask_process.pid)
            self.shutdown_flag.set()

if __name__ == "__main__":
    generator = PDFGenerator()
    generator.run()