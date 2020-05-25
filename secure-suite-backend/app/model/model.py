

class User(db.Model):
    __tablename__ = 'user'
    user_key = db.Column(db.String(36), primary_key=True, nullable=False)
    user_name = db.Column(db.String(50), nullable=False)
    user_email = db.Column(db.String(50), nullable=False)
    user_password = db.Column(db.String(50), nullable=False)
    user_salt = db.Column(db.String(50), nullable=False)

    def __init__(self, user_key, user_name, user_email, user_password, user_salt):
        self.user_key = user_key
        self.user_name = user_name
        self.user_email = user_email
        self.user_password = user_password
        self.user_salt = user_salt


class Url(db.Model):
    __tablename__ = 'url'
    url_key = db.Column(db.String(36), primary_key=True, nullable=False)
    ref_user_key = db.Column(db.String(36), db.ForeignKey('user.user_key'))
    url_tokens = db.Column(db.Text, nullable=False)
    url_sequence = db.Column(db.Text, nullable=False)
    url_good = db.Column(db.Boolean, nullables=False)

    def __init__(self, url_key, ref_user_key, url_tokens, url_sequence, url_good):
        self.url_key = url_key
        self.ref_user_key = ref_user_key
        self.url_tokens = url_tokens
        self.url_sequence = url_sequence
        self.url_good = url_good


class Password(db.Model):
    __tablename__ = 'password'
    password_key = db.Column(db.String(36), primary_key=True, nullable=False)
    ref_user_key = db.Column(db.String(36), db.ForeignKey(
        'user.user_key'), nullable=False)
    ref_category_key = db.Column(
        db.String(36), db.ForeignKey('category.category_key'), nullable=False)
    password_content = db.Column(db.String(50), nullable=False)
    password_username = db.Column(db.Text, nullable=False)
    password_url = db.Column(db.Text, nullable=False)

    def __init__(self, password_key, ref_user_key, ref_category_key, password_content, password_username, password_url, password_salt):
        self.password_key = password_key
        self.ref_user_key = ref_user_key
        self.ref_category_key = ref_category_key
        self.password_content = password_content
        self.password_username = password_username
        self.password_url = password_url
        self.password_salt = password_salt
