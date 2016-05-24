from wtforms.validators import Email, DataRequired
from wtforms.fields import PasswordField, StringField
from wtforms_tornado import Form
from sqlalchemy.orm.exc import NoResultFound
from tables import session, UserProfile


class AuthForm(Form):
    """ Authentication user form """

    login_user = None

    email = StringField(validators=[Email(), DataRequired()])
    password = PasswordField(validators=[DataRequired()])

    def validate(self):
        success = super(AuthForm, self).validate()
        try:
            user = session.query(UserProfile).filter(UserProfile.email == self.email.data).one()
        except NoResultFound:
            errors = self.errors.get("email", [])
            errors.append("No such user.")
            self.errors.update({
                'email': errors
            })
            return False
        if not user.check_password(self.password.data):
            errors = self.errors.get("password", [])
            errors.append("Incorrect password.")
            self.errors.update({
                'password': errors
            })
            return False
        self.login_user = user
        return success

    @property
    def data(self):
        """
        override default property `data`.

        :return: UserProfile object
        """
        return self.login_user
