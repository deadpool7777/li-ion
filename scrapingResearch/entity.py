from fields import StringField


class Entity:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_soup(cls, soup):
        """Factory method to create an instance from BeautifulSoup object."""
        fields = {}
        for field_name, field_obj in cls.__dict__.items():
            if isinstance(field_obj, StringField):
                fields[field_name] = field_obj.extract_value(soup)
        return cls(**fields)
