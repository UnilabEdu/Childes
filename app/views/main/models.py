from app.extensions import db


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(80), unique=True, nullable=False)
    embed_yt_link = db.Column(db.String(80), unique=True, nullable=True)
    yt_link_id = db.Column(db.String(80), unique=True, nullable=True)

    def create(self, commit=True, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        if commit:
            db.session.add(self)
            db.session.commit()

    def strip(self, child_name):
        return self.file_name.strip(child_name).strip('.cha')

    def only_child_name(self, child_name):
        ten_number = [i for i in range(0, 10)]
        for num in ten_number:
            child_name = child_name.replace(str(num), '')
        ony_child = child_name.replace('.cha', '')

        return ony_child
    # create method already_exists with file_name
    @classmethod
    def already_exists(cls, file_name):
        return cls.query.filter_by(file_name=file_name).first() is not None

    @classmethod
    def already_exists_yt(cls, embed_yt_link):
        return cls.query.filter_by(embed_yt_link=embed_yt_link).first() is not None

    @staticmethod
    def get_by_name(name):
        return File.query.filter_by(file_name=name).first()

    @classmethod
    def update(cls, id, **kwargs):
        file = cls.get_by_id(id)
        for key, value in kwargs.items():
            setattr(file, key, value)
        db.session.commit()
        return file

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def __repr__(self):
        return self.file_name


class AboutPage(db.Model):
    __tablename__ = 'about_page'

    id = db.Column(db.Integer, primary_key=True)
    goals = db.Column(db.Text, nullable=False)
    instruction = db.Column(db.Text, nullable=False)
    who_worked = db.Column(db.Text, nullable=False)

    def create(self, commit=True, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        if commit:
            db.session.add(self)
            db.session.commit()

    @staticmethod
    def get_by_id(id):
        return AboutPage.query.get(id)

    @classmethod
    def update(cls, id, **kwargs):
        about_page = cls.get_by_id(id)
        for key, value in kwargs.items():
            setattr(about_page, key, value)
        db.session.commit()
        return about_page

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def __repr__(self):
        return self.title
