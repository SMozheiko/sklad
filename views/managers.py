from database.models import Manager
from schema.http import Request
from views.base import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView
from views.mixins import LoginRequiredMixin
from utils import render, get_hashed_password, get_code, send_code, generate_password, \
    send_password


class ManagersListView(LoginRequiredMixin, BaseListView):

    template_path = 'managers'
    template = 'list.html'
    model = Manager


class ManagerCreateView(LoginRequiredMixin, BaseCreateView):

    model = Manager
    template = "create.html"
    template_path = 'managers'

    def post(self, request: Request):
        try:
            password = generate_password()
            request.data['password'] = password
            send_password(password, request.data.get('email'))
            super().post(request)
        except Exception as e:
            return render(self.template_path, self.template, {'errors': [str(e)]})
    
    def get(self, request: Request):
        return render(self.template_path, self.template, {})


class ManagerUpdateView(LoginRequiredMixin, BaseUpdateView):
    model = Manager
    template = "update.html"
    template_path = 'managers'

    def post(self, request: Request):
        try:
            super().post(request)
        except Exception as e:
            context = self.get_context(request)
            context.update({'errors': [str(e)]})
            return render(self.template_path, self.template, context)


class ManagerPasswordResetView(BaseUpdateView):
    model = Manager
    template = 'password_reset.html'
    template_path = 'managers'

    _user_state = None

    def get_queryset(self, request: Request):
        queryset = self.model.get_many(username=request.data.get('username'))
        return queryset[0] if queryset else None
    
    def post(self, request: Request):
        stage = request.data.get('stage')
        if stage == 'send_uname':
            context = self.get_context(request)
            user = context.get('object')
            if user:
                code = get_code()
                self._user_state = {'user': user, 'code': code}
                code_sent = send_code(code, address=user.email)
                if code_sent:
                    return render(self.template_path, 'password_reset_2.html', context)
                context['errors'] = ['Ошибка отправки кода подтверждения. Пожалуйста попробуйте позднее']
            else:
                context['errors'] = ['Указанный пользователь не существует']
            return render(self.template_path, self.template, context=context)

        if stage == 'send_code':
            if request.data.get('code') == self._user_state.get('code'):
                return render(self.template_path, 'password_reset_3.html', {})
            errors = ['Не правильный код подтверждения']
            return render(self.template_path, 'password_reset_2.html', {'errors': errors})

        if request.data.get('password') != request.data.get('password2'):
            context = self.get_context(request)
            context.update({'errors': ['Пароль и подтверждение не совпадают']})
            return render(self.template_path, self.template, context)

        password = get_hashed_password(request.data.get('password'))
        self.model.update({'username': self._user_state.get('user').username}, password=password, one_time_pass=False)
        self._user_state = None


class ManagerDeleteView(LoginRequiredMixin, BaseDeleteView):
    model = Manager
    template = 'delete.html'
    template_path = 'managers'
