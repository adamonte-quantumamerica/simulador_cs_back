from djoser import email


class ActivationEmail(email.ActivationEmail):
    template_name = 'email/activation.html'
    
    def get_context_data(self):
        context = super().get_context_data()
        context['subject'] = 'Activa tu cuenta en WeSolar'
        return context


class ConfirmationEmail(email.ConfirmationEmail):
    template_name = 'email/confirmation.html'
    
    def get_context_data(self):
        context = super().get_context_data()
        context['subject'] = 'Tu cuenta ha sido activada'
        return context


class PasswordResetEmail(email.PasswordResetEmail):
    template_name = 'email/password_reset.html'
    
    def get_context_data(self):
        context = super().get_context_data()
        context['subject'] = 'Restablece tu contraseña'
        return context
