from src.views.tobii_toolbar import TobiiToolBar


class TobiiToolBarController:

    def __init__(self):
        self.view = TobiiToolBar()
        self.view.btn_eye_tracker_manager.triggered.connect(self.hdl_etm)

    def hdl_etm(self):
        pass

    def hdl_start_recording(self):
        pass

    def hdl_stop_recording(self):
        pass