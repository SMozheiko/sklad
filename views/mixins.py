class LoginRequiredMixin:

    def __init__(self, *args, **kwargs):
        self.login_required = True
        super().__init__(*args, **kwargs)
