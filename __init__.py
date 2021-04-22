from mycroft import MycroftSkill, intent_file_handler
from datetime import datetime, timedelta
import copy
import os


class Announcer(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.custom_data_folder_name = "AnnouncerSkill"
        self.announcements_filepath = "~/MycroftSkillsUserData/" + self.custom_data_folder_name \
                                      + "/announcements.txt"
        self.announcements_filepath = os.path.expanduser(self.announcements_filepath)

        # List of event name hashes for all scheduled announcement events
        self.announcement_events = []

    def initialize(self):
        # Set up data folder
        self.custom_data_setup()
        # Announcements is a list of tuple pairs {datetime:string}
        announcements = self.parse_file(self.announcements_filepath)
        self.schedule_announcements(announcements)

    def cancel_announcement(self, annc_name):
        self.cancel_scheduled_event(annc_name)
        self.announcement_events.clear(annc_name)

    def cancel_all_annc(self):
        self.log.info("Before %s" % self.announcement_events)
        for annc_name in self.announcement_events:
            self.cancel_scheduled_event(annc_name)
            self.log.info("Cancelling event: %s" % annc_name)
        self.announcement_events.clear()
        self.log.info("After %s" % self.announcement_events)

    @intent_file_handler('announcer.intent')
    def handle_announcer(self, message):
        self.speak_dialog('announcer')

    @intent_file_handler('reload_announcements.intent')
    def handle_reload_announcements(self, message):

        self.cancel_all_annc()
        announcements = self.parse_file(self.announcements_filepath)
        self.schedule_announcements(announcements)
        self.speak_dialog('Announcements file reloaded.')
        self.log.info("Current %s" % self.announcement_events)

    def parse_file(self, filename):
        lines = open(filename, "r")

        # TODO: Allocate Input Validation responsibility
        # TODO: Input validation

        announcements_list = []
        for line in lines:
            try:
                annc_tuple = self.parse_line(line)
                announcements_list.append(annc_tuple)
            except Exception as e:
                self.log.error("Failed to parse line: %s" % (line))
                self.log.error(e)
        return announcements_list

    def parse_line(self, line):
        str_split = line.split("|")
        dt = self.parse_datetime(str_split[0])
        annc = str_split[1]
        freq = int(str_split[2])
        annc_tuple = (dt, annc, freq)
        return annc_tuple

    def parse_datetime(self, dt_str):
        now = datetime.now()
        today = now.date()

        t = datetime.strptime(dt_str, "%H:%M:%S").time()
        if t > (now + timedelta(seconds=1)).time():
            dt = datetime.combine(today, t)
        else:
            tmr = today + timedelta(days=1)
            dt = datetime.combine(tmr, t)

        return dt

    def schedule_announcements(self, announcements):
        for announcement in announcements:

            dt = announcement[0]
            phrase = announcement[1]
            freq = announcement[2]

            event_name_hash = str(hash(announcement))

            dt_str = str(dt)
            self.log.info("Scheduling: %s @ %s" % (phrase, dt_str))
            self.schedule_repeating_event(self.announce, dt,
                                          freq, {"phrase": phrase}, event_name_hash)
            self.announcement_events.append(event_name_hash)

    def announce(self, msg):
        phrase = msg.data["phrase"]
        self.log.info("Announcement: %s" % (phrase))
        self.speak(phrase, expect_response=False)

    '''
    Methods for Custom Data Folder Setup
    '''
    def custom_data_setup(self):
        folder_path = "MycroftSkillsUserData/" + self.custom_data_folder_name
        self.custom_data_folder_setup(folder_path)
        if self.custom_file_setup(folder_path):
            self.speak_dialog("Please edit announcements.txt in {0} for announcer skill.".format(folder_path))

    def print_files(self):
        folder_path = "~/MycroftSkillsUserData/" + self.custom_data_folder_name
        folder_path = os.path.expanduser(folder_path)
        files = os.listdir(folder_path)
        self.log.info(files)

    '''
    Returns True if announcements.txt created
    Returns False if announcements.txt not created, either because it exists or exception raised during creation
    '''
    def custom_file_setup(self, folder_path):
        # Get home path
        home_path = os.path.expanduser('~')
        file_name = "announcements.txt"

        # Append custom file to homepath (Name:MycroftSkillsUserData/AnnouncerSkill/announcements.txt)
        # Create path for file
        user_file_path = os.path.join(home_path, folder_path, file_name)
        # Check if announcements.txt exists in MycroftSkillsUserData/AnnouncerSkill .
        if not os.path.exists(user_file_path):
            # Try Create if doesn't
            try:
                f = open(user_file_path, "w")
                f.close()
                # Fail Gracefully if exception
            except Exception as e:
                print("Unexpected error: {0}".format(e))
                return False
        else:
            return False
        self.log.info("Please check the announcements.txt exists.")
        return True

    '''
    Returns True if folder created
    Returns False if folder not created, either because it exists or exception raised during creation
    '''
    def custom_data_folder_setup(self, folder_path):
        # Get home path
        home_path = os.path.expanduser('~')
        # Append custom foldername to homepath (Name:MycroftSkillsUserData/SleepyTimeSkill)
        # Create path for folder
        user_data_path = os.path.join(home_path, folder_path)

        # Check if MycroftSkillsUserData/SleepyTimeSkill folder does not exist,
        if not os.path.exists(user_data_path):
            # Try Create if doesn't
            try:
                os.makedirs(user_data_path, exist_ok=False)
                # Fail Gracefully if exception
            except Exception as e:
                print("Unexpected error: {0}".format(e))
                return False
        else:
            return False
        return True
    '''
    END: Methods for Custom Data Folder Setup
    '''

    '''
    Custom Data Folder Methods
    '''

    '''
    :return:  True if files present in custom data folder, false otherwise.
    '''
    def custom_data_has_files(self):

        home_path = os.path.expanduser('~')
        folder_path = "MycroftSkillsUserData/" + self.custom_data_folder_name
        user_data_path = os.path.join(home_path, folder_path)

        dir_list = os.listdir(user_data_path)
        return len(dir_list) != 0

    '''
    END: Custom Data Folder Methods
    '''


def create_skill():
    return Announcer()
