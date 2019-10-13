from datetime import datetime
from config import db, ma, SHORTCODE_LENGHT


class URLShortenModel(db.Model):
    __tablename__ = 'url_shorten'

    shortcode = db.Column(db.String(SHORTCODE_LENGHT), primary_key=True)
    url = db.Column(db.String, index=True)
    created_at = db.Column(db.DateTime, default=datetime.now,
                           nullable=False)
    last_redirect = db.Column(db.DateTime)
    redirect_count = db.Column(db.Integer, nullable=False, default=0)


class URLShortenSchema(ma.ModelSchema):
    class Meta:
        model = URLShortenModel
        sqla_session = db.session
