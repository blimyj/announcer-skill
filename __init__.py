from mycroft import MycroftSkill, intent_file_handler


class Announcer(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('announcer.intent')
    def handle_announcer(self, message):
        self.speak_dialog('announcer')


def create_skill():
    return Announcer()

