class CaptchaException(Exception):
    pass


class StepFailed(Exception):
    pass


class TimeoutException(StepFailed):
    pass


class FailedToRegNewUser(Exception):
    pass


class LoadPageFailed(Exception):
    pass


class MeetSpammedAccount(Exception):
    pass
