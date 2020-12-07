import os


class UiModel:

    def __init__(self, parent):

        self.parent = parent

        self.current_input_directory = ""
        self.current_edf_filename = ""
        self.current_edf_path = ""
        self.current_txt_filename = ""
        self.current_txt_path = ""

        self.current_output_directory = ""
        self.current_output_filename = ""
        self.current_output_path = ""

        self.input_directories_path_file = ""
        self.input_directories = []
        self.current_input_index = 0

        self.root_output_directory = ""
        self.output_directories = []
        self.current_output_index = 0

        self.report_path = ""

        self.interpreter_name = ""

    def set_current_names_and_directories(self):
        """
        :param eeg_path:
        :return:
        """
        self.current_input_directory = self.input_directories[self.current_input_index]
        self.current_output_directory = self.output_directories[self.current_output_index]
        print(f"Current input directory {self.current_input_directory}")
        print(f"Current output directory {self.current_output_directory}")

        files = next(os.walk(self.current_input_directory))[2]
        if len(files) == 2:
            for f in files:
                if '.edf' in f:
                    self.current_edf_filename = f
                    self.current_edf_path = os.path.join(self.current_input_directory, self.current_edf_filename)
                    self.current_output_filename = self.current_edf_filename.strip('.edf')
                if '.txt' in f:
                    self.current_txt_filename = f
                    self.current_txt_path = os.path.join(self.current_input_directory, self.current_txt_filename)

        self.current_output_path = os.path.join(self.current_output_directory, self.current_output_filename)
        self.report_path = f"{os.path.join(self.current_output_directory, self.current_output_filename)}.json"

    def setup_output_directories(self):
        for p in self.input_directories:
            mirror = p.split('v2.0.0')[1]
            mirror = os.path.normpath(mirror)
            root = self.root_output_directory
            root = os.path.normpath(root)
            rootmirror = rf"{root}{mirror}"
            dirs = rootmirror.split('\\')
            current_dir = f"{dirs[0]}\\"
            for i in range(len(dirs)):
                if os.path.exists(current_dir):
                    pass
                else:
                    os.mkdir(current_dir)
                current_dir = os.path.join(current_dir, dirs[i])
            if os.path.exists(current_dir):
                pass
            else:
                os.mkdir(current_dir)
            self.output_directories.append(current_dir)
            print(current_dir)

    def clear_session(self):
        self.interpreter_name = ""
        self.input_directories_path_file = ""  # The path to a txt file describing a list of specified input directories
        self.root_output_directory = ""  # A directory path to save the mirror directories
        self.input_directories = []
        self.current_input_index = 0
        self.current_input_directory = ""
        self.current_edf_filename = ""
        self.current_edf_path = ""
        self.current_txt_filename = ""
        self.current_txt_path = ""
        self.report_path = ""


