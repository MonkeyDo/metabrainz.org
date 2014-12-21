from metabrainz.model import db
from metabrainz.model.admin_view import AdminView
from sqlalchemy.sql.expression import func
from markdown import markdown


class Organization(db.Model):
    __tablename__ = 'organization'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Unicode, nullable=False)
    logo_url = db.Column(db.Unicode)
    website_url = db.Column(db.Unicode)
    api_url = db.Column(db.Unicode)
    description = db.Column(db.Unicode)  # How organization uses MetaBrainz projects (Markdown)
    good_standing = db.Column(db.Boolean, nullable=False, default=True)
    featured = db.Column(db.Boolean, nullable=False, default=False)

    contact_name = db.Column(db.Unicode, nullable=False)
    email = db.Column(db.Unicode, nullable=False)

    # Address
    address_street = db.Column(db.Unicode)
    address_city = db.Column(db.Unicode)
    address_state = db.Column(db.Unicode)
    address_postcode = db.Column(db.Unicode)
    address_country = db.Column(db.Unicode)

    tier_id = db.Column(db.Integer, db.ForeignKey('tier.id'))

    def __unicode__(self):
        return self.name

    @classmethod
    def get_all(cls):
        """Returns list of all organizations."""
        return cls.query.all()

    @classmethod
    def get_featured(cls, limit=4):
        return cls.query.filter(cls.featured).order_by(func.random()).limit(limit).all()

    def get_description_html(self):
        """Converts description text (Markdown) into HTML and returns it."""
        if self.description is not None:
            return markdown(self.description, safe_mode="escape")
        else:
            return None


class OrganizationAdminView(AdminView):
    column_labels = dict(
        id='ID',
        logo_url='Logo URL',
        website_url='Homepage URL',
        api_url='API page URL',
        contact_name='Contact name',
        email='Email',
        address_street='Street',
        address_city='City',
        address_state='State',
        address_postcode='Postal code',
        address_country='Country',
    )
    column_descriptions = dict(
        description='How organization uses MetaBrainz projects (Markdown supported)',
    )
    column_list = ('name', 'tier', 'featured', 'good_standing',)
    form_columns = (
        'name', 'tier', 'good_standing', 'featured', 'logo_url', 'website_url',
        'description', 'api_url', 'contact_name', 'email', 'address_street',
        'address_city', 'address_state', 'address_postcode', 'address_country',
    )

    def __init__(self, session, **kwargs):
        super(OrganizationAdminView, self).__init__(Organization, session, name='Organizations', **kwargs)