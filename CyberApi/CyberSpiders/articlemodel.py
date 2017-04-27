import pymodm

class Article(pymodm.MongoModel):
    id = pymodm.fields.CharField(primary_key=True)
    uri = pymodm.fields.CharField(blank=False)
    date = pymodm.fields.DateTimeField()
    author = pymodm.fields.CharField()
    title = pymodm.fields.CharField()
    body = pymodm.fields.CharField(blank=False)
    polarity = pymodm.fields.FloatField(blank=False)
    subjectivity = pymodm.fields.FloatField(blank=False)

    class Meta:
        connection_alias = 'articledb'
        collection_name = 'articleinfo'