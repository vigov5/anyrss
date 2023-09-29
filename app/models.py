from app import db, ModelView

class Source(db.Model):
    __tablename__ = 'sources'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False, unique=True)
    url = db.Column(db.String(255), nullable=False)
    config = db.Column(db.Text, nullable=False)

    def __init__(self, name, slug, url, config):
        self.name = name
        self.slug = slug
        self.url = url
        self.config = config


class SourceView(ModelView):

    def __init__(self, session, **kwargs):
        super(SourceView, self).__init__(Source, session, **kwargs)