import platform
import subprocess
from datetime import datetime
import traceback
import tobii_research as tr

gaze_file = None


def call_calibrator(eyetracker):
    try:
        # found_eyetrackers = tr.find_all_eyetrackers()
        # eyetracker = found_eyetrackers[0]
        os_type = platform.system()
        ETM_PATH = ''
        #DEVICE_ADDRESS = eyetracker.address
        if os_type == "Windows":
            ETM_PATH = r'C:\Users\user\AppData\Local\Programs\TobiiProEyeTrackerManager\TobiiProEyeTrackerManager.exe'
            #ETM_PATH = glob.glob(os.environ["LocalAppData"] + "/TobiiProEyeTrackerManager/app-*/TobiiProEyeTrackerManager.exe")[0]
            DEVICE_ADDRESS = "tobii-ttp://IS404-100107417574"
        else:
            print("Unsupported...")
            exit(1)
        #eyetracker = tr.EyeTracker(DEVICE_ADDRESS)
        mode = "usercalibration"
        etm_p = subprocess.Popen([ETM_PATH,
                                  "--device-address=" + eyetracker.address,
                                  "--mode=" + mode],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 shell=False)
        stdout, stderr = etm_p.communicate()  # Returns a tuple with (stdout, stderr)
        if etm_p.returncode == 0:
            print("Eye Tracker Manager was called successfully!")
        else:
            print("Eye Tracker Manager call returned the error code: " + str(etm_p.returncode))
            errlog = None
            if os_type == "Windows":
                errlog = stdout  # On Windows ETM error messages are logged to stdout
            else:
                errlog = stderr
            for line in errlog.splitlines():
                if line.startswith("ETM Error:"):
                    print(line)
    except Exception as e:
        traceback.print_exc()


def gaze_data_callback(gaze_data):
    global gaze_file

    system_time_stamp = tr.get_system_time_stamp()
    now = datetime.now()
    gaze_left_eye = gaze_data['left_gaze_point_on_display_area']
    gaze_right_eye = gaze_data['right_gaze_point_on_display_area']

    entry = f"{{\"timestamp\":\"{now}\", \"left_eye\": \"{gaze_left_eye}\", \"right_eye\":\"{gaze_right_eye}\"}}\n"

    gaze_file.write(entry)