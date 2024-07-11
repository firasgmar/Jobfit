from .TR_parser import TR_parser

class personCV:
    def __init__(self, trparser: TR_parser, text, cvpath):
        self.cv_path = cvpath
        self.parser=trparser
        self.name = self.parser.get_name(text) if text else ""
        self.phonenumber = self.parser.get_phone_number(text) if text else ""
        self.mail = self.parser.get_mail(text) if text else ""
        self.summary = self.parser.get_about(text) if text else ""
        self.hobbies = self.parser.get_hobbies(text) if text else ""
        self.education = self.parser.get_education(text) if text else ""
        self.experience = self.parser.get_experience(text) if text else ""
        self.languages = self.parser.get_languages(text) if text else ""

    def get_name(self):
        return self.name

    def get_phone_number(self):
        return self.phonenumber

    def get_mail(self):
        return self.mail

    def get_summary(self):
        return self.summary

    def get_hobbies(self):
        return self.hobbies

    def get_education(self):
        return self.education

    def get_experience(self):
        return self.experience

    def get_languages(self):
        return self.languages
