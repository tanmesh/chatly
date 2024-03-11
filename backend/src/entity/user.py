class User:
    def __init__(
        self, email, password, calendly_personal_access_token, calendy_user_url
    ):
        self.email = email
        self.password = password
        self.calendly_personal_access_token = calendly_personal_access_token
        self.calendy_user_url = calendy_user_url

    def get_calendly_personal_access_token(self):
        return self.calendly_personal_access_token

    def get_calendy_user_url(self):
        return self.calendy_user_url

    def get_email(self):
        return self.email
    
    def get_password(self):
        return self.password
